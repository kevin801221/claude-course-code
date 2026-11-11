# pomocat

終端番茄鐘 — TUI pomodoro timer with sound and stats.

## Install

```bash
uv tool install pomocat
```

## Usage

```bash
# Start a pomodoro session (default label)
pomocat

# Start with a task label
pomocat start "寫教材"

# View stats (default: today)
pomocat stats

# View monthly stats
pomocat stats -r month

# Open config editor
pomocat config
```

## Keyboard Shortcuts

| Key     | Action        |
|---------|---------------|
| `space` | Pause / Resume |
| `s`     | Skip current phase |
| `r`     | Reset timer   |
| `q`     | Quit          |
