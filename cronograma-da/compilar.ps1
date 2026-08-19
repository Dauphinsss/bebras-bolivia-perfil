$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$nombre = 'Cronograma-Actividades'

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
    try {
        Copy-Item $pdf -Destination ".\$nombre.pdf" -Force
        Write-Host "`nListo: $nombre.pdf generado." -ForegroundColor Green
    } catch [System.IO.IOException] {
        $alternativo = "$nombre-Actualizado.pdf"
        Copy-Item $pdf -Destination ".\$alternativo" -Force
        Write-Host "`nEl PDF principal estaba abierto. Se genero: $alternativo" -ForegroundColor Yellow
    }
} else {
    Write-Host "`nNo se encontro el PDF en $pdf" -ForegroundColor Red
    exit 1
}
