$ErrorActionPreference = 'Stop'
Push-Location -LiteralPath $PSScriptRoot
try {
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        throw 'Install uv first (https://docs.astral.sh/uv/getting-started/installation/), reopen PowerShell, then rerun setup.'
    }
    & uv sync --locked --python 3.12
    if ($LASTEXITCODE -ne 0) { throw 'uv sync failed.' }
    & uv run --locked python live_visio.py --preflight
    if ($LASTEXITCODE -ne 0) { throw 'Desktop Visio COM check failed.' }
    & uv run --locked python smoke.py --list-only
    if ($LASTEXITCODE -ne 0) { throw 'MCP tool discovery failed.' }
    & uv run --locked python live_visio.py --prompts
    if ($LASTEXITCODE -ne 0) { throw 'Prompt generation failed.' }
    Write-Host 'Now launch claude in this lab folder. Run /mcp and allow visio-live.'
} finally {
    Pop-Location
}
