param(
  [string]$SubPath
)

# Verzeichnis des Skripts ermitteln
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($SubPath) {
  $ScriptDir = Join-Path $ScriptDir $SubPath
}

# In tex-Ordner wechseln
$texDir = Join-Path $ScriptDir "tex"
if (!(Test-Path $texDir)) {
  Write-Error "Ordner nicht gefunden: $texDir"
  exit 1
}
Set-Location $texDir

# LaTeX/Biber bauen
xelatex -shell-escape -interaction=nonstopmode main.tex
biber main
xelatex -shell-escape -interaction=nonstopmode main.tex
xelatex -shell-escape -interaction=nonstopmode main.tex

# build-Ordner anlegen
$buildDir = Join-Path $ScriptDir "build"
if (!(Test-Path $buildDir)) {
  New-Item -ItemType Directory -Path $buildDir | Out-Null
}

# Aufräumen: Artefakte in build verschieben
$patterns = @(
  "*.pdf","*.doc","*.aux","*.bbl","*.bcf","*.blg","*.log","*.out","*.run.xml",
  "*.toc","*.synctex.gz","*.lof","*.lot","*.lol","*.gz","*.fls","*.fdb_latexmk",
  "*.xdv","*.bak","*.dvi","*.thm","*.snm","*.nav","*.vrb","*.synctex","*.synctex(busy)"
)

$files = Get-ChildItem -Recurse -Path $texDir -File -Include $patterns -ErrorAction SilentlyContinue
foreach ($f in $files) {
  Move-Item -LiteralPath $f.FullName -Destination $buildDir -Force -ErrorAction SilentlyContinue
}

# Optional: falls es unter tex bereits einen build-Ordner gibt, mit verschieben
$localBuild = Join-Path $texDir "build"
if (Test-Path $localBuild) {
  Try {
    Move-Item -Path $localBuild -Destination $buildDir -Force -ErrorAction Stop
  } Catch {
    # Ignorieren, falls bereits vorhanden/konflikt
  }
}
cd ../..