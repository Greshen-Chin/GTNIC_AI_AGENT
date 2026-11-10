param(
    [string]$DocxPath,
    [string]$PdfPath
)

$word = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = "wdAlertsNone"
    $doc = $word.Documents.Open($DocxPath, $false, $true)
    $pages = $doc.ComputeStatistics(2)
    # wdExportFormatPDF = 17
    $doc.ExportAsFixedFormat($PdfPath, 17)
    $doc.Close([ref]$false)
    Write-Host "EXPORTED_PAGES:$pages"
} catch {
    Write-Host "ERROR: $_"
} finally {
    if ($word) {
        $word.Quit()
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    }
}

