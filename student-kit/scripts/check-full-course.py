#!/usr/bin/env python3
"""Verify expanded source provenance and actual lecture/project coverage offline."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
manifest = json.loads((ROOT / 'sources/full-manifest.json').read_text())
fixes = json.loads((ROOT / 'sources/classroom-fixes-manifest.json').read_text())
for item in manifest['files'] + manifest.get('supplemental_files', []) + fixes:
    target = (ROOT / item['destination']).resolve()
    if not target.is_relative_to(ROOT) or not target.is_file():
        errors.append('來源檔不存在或越界：' + item['destination'])
        continue
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual != item['destination_sha256']:
        errors.append('來源檔 hash 已改變：' + item['destination'])
    if item.get('kind') == 'copy' and actual != item['source_sha256']:
        errors.append('原樣複製與來源不符：' + item['destination'])
    if target.suffix == '.ipynb':
        notebook = json.loads(target.read_text())
        if any(c.get('cell_type') == 'code' and (c.get('outputs') or c.get('execution_count') is not None) for c in notebook.get('cells', [])):
            errors.append('Notebook仍含執行輸出：' + item['destination'])

required = [
    'course/Projects/01-weekly-haiku/.claude/commands/weekly-haiku.md',
    'course/Projects/02-recipe-genie/.claude/agents/recipe-genie.md',
    'course/Projects/03-youtube-notes/.claude/skills/youtube-notes/SKILL.md',
    'course/Projects/04-pomodoro/try/.claude/settings.json',
    'course/Projects/05-organize-downloads/.claude/settings.json',
    'course/Projects/06-discord-dm-bot/discord_dm_bot.py',
    'course/Projects/07-weekly-reports-skill/README.md',
    'course/Projects/08-agent-team-review/app/backend/server.py',
    'course/Projects/09-timetrace/WALKTHROUGH.md',
    'course/context-engineering-intro/INITIAL.md',
    'course/agent_group_projects/computer-vision-wafer-detection/scripts/train_yolo.py',
    'course/agent_teams/ios-app-flutter-dev/arxiv-1-完成版/pubspec.yaml',
    'course/agent_teams/ios-app-flutter-dev/arxiv-2-空白課堂版/pubspec.yaml',
    'course/important-plugins/superpowers/LICENSE',
    'references/zh-TW/reports/why-harness-is-important.md',
    'references/matt-flow-mods/docs/new-project.md',
    'docs/platform-guide.md',
    'classroom-fixes/weekly-reports/README.md',
    'classroom-fixes/mcp-sandbox/README.md',
    'classroom-fixes/plugin-marketplace/README.md',
]
for name in required:
    if not (ROOT / name).is_file():
        errors.append('課堂必要內容缺失：' + name)
for name in ['01-slash-commands', '02-memory', '03-skills', '04-subagents', '05-mcp', '06-hooks', '07-plugins', '08-checkpoints', '09-advanced-features', '10-cli']:
    if not (ROOT / 'course' / name / 'README.md').is_file():
        errors.append('十模組缺失：' + name)

coverage = json.loads((ROOT / 'sources/full-coverage.json').read_text())
if {x['part'] for x in coverage} != {f'{i:02}' for i in range(22)} | {'A', 'B'}:
    errors.append('覆蓋矩陣需列22個Part與附錄A/B')
for row in coverage:
    for target in row['destinations']:
        if not (ROOT / target).exists():
            errors.append('覆蓋矩陣指向缺件：' + target)
if {x['source_repo'] for x in manifest['files']} != {'claude-course-code', 'claude-code-best-practice', 'claude-code-zh-tw', 'claude-howto-zh-TW', 'matt-flow-mods'}:
    errors.append('需含五個指定來源')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f"完整課堂檢查通過：{len(manifest['files'])} 份來源檔、{len(fixes)} 項修正版映射、十模組、九核心專題、24 個章節/附錄定位。")
print(f"上游文件原有缺件/占位連結：{len(manifest['original_document_issues'])} 項，見來源問題清單。")
print('原碼已收錄不等於整合環境已驗證；藍圖、設定模板與外部缺件各有標示。')
