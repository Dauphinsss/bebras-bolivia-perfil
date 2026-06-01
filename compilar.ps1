# Compila el documento y deja SOLO el PDF "Perfil-Bebras.pdf" en la raiz.
# Uso:  .\compilar.ps1
# Los archivos auxiliares (.aux, .bbl, .log, etc.) quedan en la carpeta build\

$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$nombre = 'Perfil-Bebras'

$latexmkArgs = @(
    '-pdf'
    '-interaction=nonstopmode'
    '-synctex=1'
    '-outdir=build'
    "-jobname=$nombre"
    'main.tex'
)

& latexmk @latexmkArgs

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nLa compilacion fallo. Revisa build\$nombre.log" -ForegroundColor Red
    exit $LASTEXITCODE
}

$pdf = Join-Path 'build' "$nombre.pdf"
if (Test-Path $pdf) {
    Copy-Item $pdf -Destination ".\$nombre.pdf" -Force
    Write-Host "`nListo: $nombre.pdf generado en la raiz." -ForegroundColor Green
} else {
    Write-Host "`nNo se encontro el PDF en $pdf" -ForegroundColor Red
    exit 1
}
