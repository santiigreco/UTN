$files = Get-ChildItem 'd:\Descargas\UTN\Repo-UTN\2026\Manejo_de_materiales\TP1_localizacion'
foreach ($f in $files) {
    Write-Output $f.FullName
}
