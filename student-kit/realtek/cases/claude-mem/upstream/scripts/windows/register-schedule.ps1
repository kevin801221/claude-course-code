# Register (or remove) Windows Task Scheduler jobs that run the reports.
#
# Usage (PowerShell, normal user is fine):
#   .\scripts\windows\register-schedule.ps1             # personal: daily, weekly, monthly
#   .\scripts\windows\register-schedule.ps1 -Team       # also manager: team-daily, team-weekly
#   .\scripts\windows\register-schedule.ps1 -Uninstall
#
# Times (local time, change below if needed):
#   daily        Mon-Fri 19:00
#   weekly       Fri     19:30
#   monthly      every day 20:00, but the script only acts on the last day of the month
#   team-daily   Mon-Fri 20:00
#   team-weekly  Fri     21:00
#
# Jobs run only while you are logged on. "StartWhenAvailable" runs a missed job
# as soon as the PC is on again.
# ASCII-only on purpose (PowerShell 5.1 compatibility).

param(
    [switch]$Team,
    [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'
$Runner = (Resolve-Path (Join-Path $PSScriptRoot 'run-report.ps1')).Path
$Folder = '\ClaudeMemDailyReport\'
$Weekdays = 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'

function Register-ReportTask([string]$type, $trigger) {
    $action = New-ScheduledTaskAction -Execute 'powershell.exe' `
        -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$Runner`" -Type $type"
    $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2)
    Register-ScheduledTask -TaskPath $Folder -TaskName $type -Action $action -Trigger $trigger `
        -Settings $settings -Description "claude-mem daily report: $type" -Force | Out-Null
    Write-Host "registered $Folder$type"
}

if ($Uninstall) {
    Get-ScheduledTask -TaskPath $Folder -ErrorAction SilentlyContinue |
        Unregister-ScheduledTask -Confirm:$false
    Write-Host 'removed all report tasks'
    return
}

Register-ReportTask 'daily'   (New-ScheduledTaskTrigger -Weekly -DaysOfWeek $Weekdays -At '19:00')
Register-ReportTask 'weekly'  (New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At '19:30')
Register-ReportTask 'monthly' (New-ScheduledTaskTrigger -Daily -At '20:00')

if ($Team) {
    Register-ReportTask 'team-daily'  (New-ScheduledTaskTrigger -Weekly -DaysOfWeek $Weekdays -At '20:00')
    Register-ReportTask 'team-weekly' (New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At '21:00')
}

Write-Host ''
Write-Host 'Check in Task Scheduler under the ClaudeMemDailyReport folder.'
Write-Host "Test now: powershell -ExecutionPolicy Bypass -File `"$Runner`" -Type daily"
