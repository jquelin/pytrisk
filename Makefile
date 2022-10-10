PYFILES = $(shell find . -type f -name *.py)
POTDIR  = pytrisk/locale
POFILE  = ${POTDIR}/messages.pot
FRDIR   = ${POTDIR}/fr/LC_MESSAGES/

COLOR = 3

LASTVER = $(shell git tag | tail -1 | tr -d v)
CURVER  = $(shell grep version pyproject.toml| sed -e 's/^.*=//' | tr -d ' "')



dist: build

upload: build
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	twine upload dist/*

build: clean
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	[ "${LASTVER}" == "${CURVER}" ] && echo "version has not changed" && exit 1
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
