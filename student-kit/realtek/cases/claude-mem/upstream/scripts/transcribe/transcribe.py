"""Transcribe meeting recordings with WhisperX (speaker diarization included).

Usage:
    python transcribe.py --recordings ../../recordings --out ../../meetings
    python transcribe.py --recordings recordings --out meetings --date 2026-11-16

For every audio file in --recordings that has no matching
<out>/<stem>.transcript.md yet, this writes a Markdown transcript grouped by
speaker, with timestamps. File names should look like
"2026-11-16_週會.m4a" so the date and meeting name can be read from them.

On success it prints the path of each NEW transcript, one per line, so the
scheduling scripts can hand them to Claude to turn into meeting minutes.

Environment variables:
    WHISPER_MODEL     default large-v3
    WHISPER_LANGUAGE  default zh (set empty to auto-detect)
    HF_TOKEN          Hugging Face token; needed for speaker diarization.
                      Without it, the transcript is written without speakers.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

AUDIO_EXTS = {".m4a", ".mp3", ".wav", ".flac", ".ogg", ".aac", ".mp4", ".webm"}


def log(msg: str) -> None:
    # Progress goes to stderr; stdout is reserved for new transcript paths.
    print(msg, file=sys.stderr, flush=True)


def fmt_ts(seconds: float) -> str:
    seconds = int(seconds or 0)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def load_speaker_map(config_path: Path, stem: str) -> dict[str, str]:
    """Return SPEAKER_xx -> real name for this recording, if configured."""
    if not config_path.exists():
        return {}
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        log(f"[warn] cannot read {config_path}: {exc}")
        return {}
    mapping = dict(data.get("default", {}))
    for key, value in data.items():
        if key.startswith("_") or key == "default" or not isinstance(value, dict):
            continue
        if stem.startswith(key):
            mapping.update(value)
    return mapping


def pick_device() -> tuple[str, str]:
    try:
        import torch

        if torch.cuda.is_available():
            return "cuda", "float16"
    except ImportError:
        pass
    # Apple Silicon: ctranslate2 has no MPS backend, so CPU with int8 is the
    # reliable choice on Mac.
    return "cpu", "int8"


def get_diarization_pipeline(hf_token: str, device: str):
    import whisperx

    # The class moved between WhisperX releases; try both locations.
    try:
        from whisperx.diarize import DiarizationPipeline
    except ImportError:
        DiarizationPipeline = getattr(whisperx, "DiarizationPipeline")
    return DiarizationPipeline(use_auth_token=hf_token, device=device)


def transcribe_file(audio_path: Path, model, device: str, language: str | None,
                    diarizer, speaker_map: dict[str, str]) -> list[dict]:
    import whisperx

    audio = whisperx.load_audio(str(audio_path))
    result = model.transcribe(audio, batch_size=16, language=language)
    lang = result.get("language") or language or "zh"

    try:
        align_model, metadata = whisperx.load_align_model(language_code=lang, device=device)
        result = whisperx.align(result["segments"], align_model, metadata, audio, device,
                                return_char_alignments=False)
    except Exception as exc:  # alignment model may not exist for every language
        log(f"[warn] alignment skipped for {audio_path.name}: {exc}")

    if diarizer is not None:
        diarize_segments = diarizer(audio)
        result = whisperx.assign_word_speakers(diarize_segments, result)

    segments = []
    for seg in result.get("segments", []):
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        code = seg.get("speaker", "UNKNOWN")
        segments.append({
            "start": seg.get("start", 0.0),
            "speaker": speaker_map.get(code, code),
            "text": text,
        })
    return segments


def to_markdown(stem: str, segments: list[dict], diarized: bool) -> str:
    lines = [f"# 逐字稿：{stem}", ""]
    if not diarized:
        lines += ["> 未分辨說話者（沒有設定 HF_TOKEN）。", ""]
    current = None
    for seg in segments:
        if seg["speaker"] != current:
            current = seg["speaker"]
            lines += ["", f"**{current}**", ""]
        lines.append(f"[{fmt_ts(seg['start'])}] {seg['text']}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--recordings", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--date", help="only process files whose name starts with this date")
    parser.add_argument("--speakers", type=Path,
                        default=Path(__file__).resolve().parents[2] / "config" / "speakers.json")
    args = parser.parse_args()

    if not args.recordings.is_dir():
        log(f"[info] no recordings folder at {args.recordings}")
        return 0
    args.out.mkdir(parents=True, exist_ok=True)

    pending = []
    for path in sorted(args.recordings.iterdir()):
        if path.suffix.lower() not in AUDIO_EXTS:
            continue
        if args.date and not path.stem.startswith(args.date):
            continue
        if (args.out / f"{path.stem}.transcript.md").exists():
            continue
        pending.append(path)

    if not pending:
        log("[info] nothing new to transcribe")
        return 0

    try:
        import whisperx
    except ImportError:
        log("[error] whisperx is not installed. See scripts/transcribe/requirements.txt")
        return 1

    device, compute_type = pick_device()
    model_name = os.environ.get("WHISPER_MODEL", "large-v3")
    language = os.environ.get("WHISPER_LANGUAGE", "zh") or None
    log(f"[info] loading {model_name} on {device} ({compute_type})")
    model = whisperx.load_model(model_name, device, compute_type=compute_type, language=language)

    hf_token = os.environ.get("HF_TOKEN", "").strip()
    diarizer = None
    if hf_token:
        try:
            diarizer = get_diarization_pipeline(hf_token, device)
        except Exception as exc:
            log(f"[warn] diarization unavailable, continuing without speakers: {exc}")
    else:
        log("[warn] HF_TOKEN not set; transcripts will not separate speakers")

    failures = 0
    for path in pending:
        log(f"[info] transcribing {path.name}")
        try:
            segments = transcribe_file(path, model, device, language, diarizer,
                                       load_speaker_map(args.speakers, path.stem))
        except Exception as exc:
            failures += 1
            log(f"[error] failed on {path.name}: {exc}")
            continue
        out_path = args.out / f"{path.stem}.transcript.md"
        out_path.write_text(to_markdown(path.stem, segments, diarizer is not None),
                            encoding="utf-8")
        print(out_path.resolve(), flush=True)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
