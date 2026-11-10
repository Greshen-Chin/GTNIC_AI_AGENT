param([string]$FilePath)

$word = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = "wdAlertsNone"
    $doc = $word.Documents.Open($FilePath, $false, $true)
    $pages = $doc.ComputeStatistics(2)
    $doc.Close([ref]$false)
    Write-Host "PAGES:$pages"
} catch {
    Write-Host "ERROR: $_"
} finally {
    if ($word) {
        $word.Quit()
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    }
}

