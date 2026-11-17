$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$app = $null
$drawing = $null
try {
    $app = New-Object -ComObject Visio.InvisibleApp
    # OpenEx flags: read-only, don't list in Recents, disable macros.
    $drawing = $app.Documents.OpenEx($env:VISIO_LAB_DRAWING, (2 -bor 8 -bor 128))
    $pages = @(foreach ($page in $drawing.Pages) {
        $shapes = @(foreach ($shape in $page.Shapes) {
            [ordered]@{ id = [int]$shape.ID; text = [string]$shape.Text }
        })
        $connections = @(foreach ($link in $page.Connects) {
            [ordered]@{
                connector_id = [int]$link.FromSheet.ID
                endpoint = [string]$link.FromCell.NameU
                target_id = [int]$link.ToSheet.ID
            }
        })
        [ordered]@{ name = [string]$page.Name; shapes = $shapes; connections = $connections }
    })
    [ordered]@{ engine = 'Microsoft Visio'; version = [string]$app.Version; pages = $pages } |
        ConvertTo-Json -Depth 7 -Compress
}
finally {
    try {
        if ($null -ne $drawing) { $drawing.Close() }
    }
    finally {
        if ($null -ne $app) { $app.Quit() }
    }
}
