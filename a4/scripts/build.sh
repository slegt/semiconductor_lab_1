cd ./tex|| exit

xelatex -shell-escape -interaction=nonstopmode main.tex
biber main
xelatex -shell-escape -interaction=nonstopmode main.tex
xelatex -shell-escape -interaction=nonstopmode main.tex

for f in $(find ./ -name '*.pdf' -or -name '*.doc' -or -name '*.aux' -or -name '*.aux' -or -name '*.bbl' -or -name \
'*.bcf' -or -name '*.blg' -or -name '*.log' -or -name '*.out' -or -name '*.run.xml' -or -name '*.toc' -or -name \
'*.synctex.gz' -or -name '*.lof' -or -name '*.lot' -or -name '*.lol' -or -name '*.gz' -or -name '*.fls' -or -name \
'*.fdb_latexmk' -or -name '*.xdv' -or -name '*.bak' -or -name '*.dvi' -or -name '*.thm' -or -name '*.snm' -or -name \
'*.nav' -or -name '*.vrb' -or -name '*.snm' -or -name '*.nav' -or -name '*.vrb' -or -name '*.synctex(busy)' -or -name \
'*.synctex'); do
  mv $f ../build; done

