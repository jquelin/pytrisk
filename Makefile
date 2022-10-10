PYFILES = $(shell find . -type f -name *.py)
POTDIR  = pytrisk/locale
POFILE  = ${POTDIR}/messages.pot
FRDIR   = ${POTDIR}/fr/LC_MESSAGES/

COLOR = 3

dist: build

upload: build
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	twine upload dist/*


build: clean
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	python -m build

pot: ${PYFILES}
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	@mkdir -p ${POTDIR}
	pygettext.py -p ${POTDIR} ${PYFILES}

mo: ${FRDIR}/pytrisk.po
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	msgfmt ${FRDIR}/pytrisk.po -o ${FRDIR}/pytrisk.mo

clean:
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	rm -rf dist pytrisk.egg-info
