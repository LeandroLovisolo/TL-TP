BUNDLE       = TL-TP.tar.gz
BUNDLE_DIR   = TL-TP
BUNDLE_FILES = src tex Makefile README.md enunciado.pdf informe.pdf

PARSER_FILES = src/parser.out src/parsetab.py

.PHONY: all informe.pdf clean clean-tex bundle

all: informe.pdf

informe.pdf:
	make -C tex all
	mv tex/informe.pdf .

bundle: clean informe.pdf 
	make clean-tex
	mkdir $(BUNDLE_DIR)
	cp $(BUNDLE_FILES) $(BUNDLE_DIR) -r
	tar zcf $(BUNDLE) $(BUNDLE_DIR)
	rm -rf $(BUNDLE_DIR)

clean: clean-tex
	rm -rf informe.pdf $(PARSER_FILES) $(BUNDLE) $(BUNDLE_DIR)
	find . -type f -name *.swp -delete
	find . -type f -name *.pyc -delete

clean-tex:
	make -C tex clean
