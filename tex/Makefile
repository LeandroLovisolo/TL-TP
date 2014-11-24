.PHONY: all clean PLP-TP3.st.txt

all: informe.pdf

PLP-TP3.st.txt:
	cat ../PLP-TP3.st | tr '\r' '\n' | tr -d '\0\f' | sed '1s/^.//' > PLP-TP3.st.txt

informe.pdf: informe.tex PLP-TP3.st.txt
	pdflatex -interaction=nonstopmode -halt-on-error informe.tex && \
	pdflatex -interaction=nonstopmode -halt-on-error informe.tex

clean:
	rm -f informe.pdf PLP-TP3.st.txt *.aux *.log *.toc *.out *.pdf
