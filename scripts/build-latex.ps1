param(
  [string]$Document = "*"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$documentsDir = Join-Path $repoRoot "latex\documents"
$buildDir = Join-Path $repoRoot "latex\build"
$pdfDir = Join-Path $repoRoot "docs\pdf"

$xelatex = Get-Command xelatex -ErrorAction SilentlyContinue
if (-not $xelatex) {
  throw "xelatex was not found. Install MiKTeX or TeX Live, then reopen the terminal so PATH is refreshed."
}

New-Item -ItemType Directory -Force -Path $buildDir, $pdfDir | Out-Null

if ($Document -eq "*") {
  $sources = Get-ChildItem -LiteralPath $documentsDir -Filter "*.tex"
} else {
  $sourcePath = Join-Path $documentsDir "$Document.tex"
  if (-not (Test-Path -LiteralPath $sourcePath)) {
    throw "Document not found: $sourcePath"
  }
  $sources = @(Get-Item -LiteralPath $sourcePath)
}

foreach ($source in $sources) {
  Write-Host "Building $($source.BaseName).pdf"

  & $xelatex.Source `
    -interaction=nonstopmode `
    -halt-on-error `
    -output-directory="$buildDir" `
    $source.FullName | Out-Host
  if ($LASTEXITCODE -ne 0) {
    throw "xelatex failed while building $($source.Name)"
  }

  & $xelatex.Source `
    -interaction=nonstopmode `
    -halt-on-error `
    -output-directory="$buildDir" `
    $source.FullName | Out-Host
  if ($LASTEXITCODE -ne 0) {
    throw "xelatex failed while finalizing $($source.Name)"
  }

  $pdfPath = Join-Path $buildDir "$($source.BaseName).pdf"
  if (-not (Test-Path -LiteralPath $pdfPath)) {
    throw "Expected PDF was not created: $pdfPath"
  }

  Copy-Item -LiteralPath $pdfPath -Destination (Join-Path $pdfDir "$($source.BaseName).pdf") -Force
}

Write-Host "LaTeX build complete. PDFs are in $pdfDir"
