#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Append the argument passed in the terminal to SCRIPT_DIR
if [ -n "$1" ]; then
  SCRIPT_DIR="$SCRIPT_DIR/$1"
fi

# Change to the tex directory relative to the script's location
cd "$SCRIPT_DIR/tex" || exit

pdflatex -shell-escape -interaction=nonstopmode main.tex
biber main
pdflatex -shell-escape -interaction=nonstopmode main.tex
pdflatex -shell-escape -interaction=nonstopmode main.tex

# Create the build folder if it doesn't exist
mkdir -p "$SCRIPT_DIR/build"

# cleanup
for f in $(find ./ -name '*.pdf' -or -name '*.doc' -or -name '*.aux' -or -name 'build' -or -name '*.aux' -or -name '*.bbl' -or -name \
'*.bcf' -or -name '*.blg' -or -name '*.log' -or -name '*.out' -or -name '*.run.xml' -or -name '*.toc' -or -name \
'*.synctex.gz' -or -name '*.lof' -or -name '*.lot' -or -name '*.lol' -or -name '*.gz' -or -name '*.fls' -or -name \
'*.fdb_latexmk' -or -name '*.xdv' -or -name '*.bak' -or -name '*.dvi' -or -name '*.thm' -or -name '*.snm' -or -name \
'*.nav' -or -name '*.vrb' -or -name '*.snm' -or -name '*.nav' -or -name '*.vrb' -or -name '*.synctex(busy)' -or -name \
'*.synctex'); do
  mv "$f" "$SCRIPT_DIR/build"
done
