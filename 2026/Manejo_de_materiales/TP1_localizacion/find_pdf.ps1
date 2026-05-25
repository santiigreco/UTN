$files = Get-ChildItem 'd:\Descargas\UTN\Repo-UTN\2026\Manejo_de_materiales\TP1_localizacion\*.pdf'
foreach ($f in $files) {
    Write-Output "PDF: $($f.FullName)"
}
