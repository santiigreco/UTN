Add-Type -AssemblyName 'System.IO.Compression.FileSystem'

$docFile = Get-ChildItem 'd:\Descargas\UTN\Repo-UTN\2026\Manejo_de_materiales\TP1_localizacion\*.docx' | Select-Object -First 1

$zip = [System.IO.Compression.ZipFile]::OpenRead($docFile.FullName)
$entry = $zip.GetEntry('word/document.xml')
$stream = $entry.Open()
$reader = New-Object System.IO.StreamReader($stream)
$content = $reader.ReadToEnd()
$reader.Close()
$stream.Close()
$zip.Dispose()

$xml = [xml]$content
$nsmgr = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
$nsmgr.AddNamespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')

# Save full text to file
$outPath = 'd:\Descargas\UTN\Repo-UTN\2026\Manejo_de_materiales\TP1_localizacion\document_text.txt'
$paragraphs = $xml.SelectNodes('//w:p', $nsmgr)
$allLines = @()
foreach ($p in $paragraphs) {
    $texts = $p.SelectNodes('.//w:t', $nsmgr)
    $line = ""
    foreach ($t in $texts) {
        $line += $t.InnerText
    }
    $allLines += $line
}
$allLines | Out-File -FilePath $outPath -Encoding UTF8
Write-Output "Saved to $outPath"
