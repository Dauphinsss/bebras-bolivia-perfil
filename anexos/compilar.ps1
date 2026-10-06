# Compila solo los anexos y deja "Anexos-Bebras.pdf" en esta carpeta.
# Uso:  .\compilar.ps1   (desde bebras-doc\anexos)
# Los archivos auxiliares quedan en anexos\build\

$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$nombre = 'Anexos-Bebras'

& latexmk -pdf -interaction=nonstopmode -outdir=build "-jobname=$nombre" anexos.tex

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nLa compilacion fallo. Revisa anexos\build\$nombre.log" -ForegroundColor Red
    exit $LASTEXITCODE
}

$pdf = Join-Path 'build' "$nombre.pdf"
if (Test-Path $pdf) {
    Copy-Item $pdf -Destination ".\$nombre.pdf" -Force
    Write-Host "`nListo: anexos\$nombre.pdf generado." -ForegroundColor Green
} else {
    Write-Host "`nNo se encontro el PDF en $pdf" -ForegroundColor Red
    exit 1
}
