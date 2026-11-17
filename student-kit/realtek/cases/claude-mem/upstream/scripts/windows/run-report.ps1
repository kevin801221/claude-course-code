# Run one report with Claude Code in headless mode (Windows).
#
# Usage (PowerShell):
#   .\scripts\windows\run-report.ps1 -Type daily        # meetings + personal daily report
#   .\scripts\windows\run-report.ps1 -Type weekly
#   .\scripts\windows\run-report.ps1 -Type monthly      # only runs on the last day of the month
#   .\scripts\windows\run-report.ps1 -Type monthly -Force
#   .\scripts\windows\run-report.ps1 -Type team-daily   # manager side
#   .\scripts\windows\run-report.ps1 -Type team-weekly  # manager side
#
# Works on Windows PowerShell 5.1 and PowerShell 7.
# This file is kept ASCII-only on purpose: PowerShell 5.1 misreads UTF-8 scripts without a BOM.

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('daily', 'weekly', 'monthly', 'team-daily', 'team-weekly')]
    [string]$Type,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$RepoDir = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

# UTF-8 everywhere so Chinese prompts reach claude intact.
$utf8 = New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

# ---------- settings ----------
$envFile = Join-Path $RepoDir 'config\report.env'
if (Test-Path $envFile) {
    foreach ($line in Get-Content $envFile -Encoding UTF8) {
        if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$') {
            [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2].Trim(), 'Process')
        }
    }
}
$Author = if ($env:AUTHOR) { $env:AUTHOR } else { $env:USERNAME }
$AllowedTools = if ($env:ALLOWED_TOOLS) { $env:ALLOWED_TOOLS } else { 'Read,Write,Edit,Glob,Grep' }
$TeamReportsDir = if ($env:TEAM_REPORTS_DIR) { $env:TEAM_REPORTS_DIR } else { Join-Path $RepoDir 'team-reports' }

foreach ($d in 'logs', 'reports\daily', 'reports\weekly', 'reports\monthly', 'reports\team', 'meetings') {
    New-Item -ItemType Directory -Force -Path (Join-Path $RepoDir $d) | Out-Null
}
$logFile = Join-Path $RepoDir ("logs\{0}-{1}.log" -f (Get-Date -Format 'yyyy-MM-dd'), $Type)
Start-Transcript -Path $logFile -Append | Out-Null

try {
    if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
        throw "claude command not found. Install Claude Code and open a new terminal."
    }

    # ---------- dates ----------
    $today = (Get-Date).Date
    $offset = ([int]$today.DayOfWeek + 6) % 7          # Monday = 0
    $monday = $today.AddDays(-$offset)
    $thursday = $monday.AddDays(3)                     # ISO week belongs to the year of its Thursday
    $isoWeek = [math]::Floor(($thursday.DayOfYear - 1) / 7) + 1
    $vars = @{
        'DATE'             = $today.ToString('yyyy-MM-dd')
        'WEEK_START'       = $monday.ToString('yyyy-MM-dd')
        'WEEK_END'         = $monday.AddDays(6).ToString('yyyy-MM-dd')
        'WEEK_LABEL'       = '{0}-W{1:D2}' -f $thursday.Year, [int]$isoWeek
        'MONTH'            = $today.ToString('yyyy-MM')
        'REPO_DIR'         = $RepoDir
        'AUTHOR'           = $Author
        'TEAM_REPORTS_DIR' = $TeamReportsDir
        'REPORT_DESTINATION' = "$env:REPORT_DESTINATION"
        'NOTION_REPORT_DB' = "$env:NOTION_REPORT_DB"
        'JIRA_ISSUE'       = "$env:JIRA_ISSUE"
    }

    function Render-Prompt([string]$name, [hashtable]$extra = @{}) {
        $text = Get-Content (Join-Path $RepoDir "prompts\$name") -Raw -Encoding UTF8
        $all = $vars.Clone()
        foreach ($k in $extra.Keys) { $all[$k] = $extra[$k] }
        foreach ($k in $all.Keys) { $text = $text.Replace('{{' + $k + '}}', $all[$k]) }
        return $text
    }

    function Invoke-Claude([string]$prompt) {
        # The prompt goes in through stdin so long Chinese text is not mangled by argument quoting.
        Push-Location $RepoDir
        try {
            $prompt | & claude -p --allowedTools $AllowedTools --permission-mode acceptEdits
            if ($LASTEXITCODE -ne 0) { Write-Warning "claude exited with code $LASTEXITCODE" }
        }
        finally { Pop-Location }
    }

    function Get-WhisperPython {
        $venv = Join-Path $RepoDir '.venv-whisper\Scripts\python.exe'
        if (Test-Path $venv) { return $venv }
        foreach ($cmd in 'python', 'py') {
            if (Get-Command $cmd -ErrorAction SilentlyContinue) { return $cmd }
        }
        return $null
    }

    function Invoke-MeetingMinutes {
        $py = Get-WhisperPython
        if (-not $py) { Write-Host '[info] python not found; skipping meeting transcription'; return }
        # PowerShell 5.1 turns redirected native stderr into errors, so guard the probe.
        $hasWhisper = $false
        try { & $py -c 'import whisperx' 2>$null; $hasWhisper = ($LASTEXITCODE -eq 0) } catch { $hasWhisper = $false }
        if (-not $hasWhisper) { Write-Host '[info] whisperx not installed; skipping meeting transcription'; return }

        $script = Join-Path $RepoDir 'scripts\transcribe\transcribe.py'
        $env:PYTHONIOENCODING = 'utf-8'
        $new = & $py $script --recordings (Join-Path $RepoDir 'recordings') --out (Join-Path $RepoDir 'meetings')
        if ($LASTEXITCODE -ne 0) { Write-Warning 'transcription reported errors; continuing with what succeeded' }

        foreach ($t in @($new)) {
            if (-not $t) { continue }
            $out = $t -replace '\.transcript\.md$', '.md'
            Write-Host "[info] writing minutes for $(Split-Path $t -Leaf)"
            Invoke-Claude (Render-Prompt 'meeting-minutes.md' @{ 'TRANSCRIPT' = $t; 'OUTPUT' = $out })
        }
    }

    Write-Host ("=== {0} start {1} ===" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Type)
    switch ($Type) {
        'daily' {
            Invoke-MeetingMinutes
            Invoke-Claude (Render-Prompt 'daily-report.md')
        }
        'weekly' { Invoke-Claude (Render-Prompt 'weekly-report.md') }
        'monthly' {
            if (-not $Force -and $today.AddDays(1).Month -eq $today.Month) {
                Write-Host '[info] not the last day of the month; skipping'
            }
            else { Invoke-Claude (Render-Prompt 'monthly-report.md') }
        }
        'team-daily' { Invoke-Claude (Render-Prompt 'team-daily.md') }
        'team-weekly' { Invoke-Claude (Render-Prompt 'team-weekly.md') }
    }
    Write-Host ("=== {0} done {1} ===" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Type)
}
finally {
    Stop-Transcript | Out-Null
}
