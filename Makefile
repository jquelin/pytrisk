PYFILES = $(shell find . -type f -name *.py)
POTDIR  = pytrisk/locale
POFILE  = ${POTDIR}/messages.pot
FRDIR   = ${POTDIR}/fr/LC_MESSAGES/

upload: build
	twine upload dist/*

build: clean
	python -m build

pot: ${PYFILES}
	@mkdir -p ${POTDIR}
	pygettext.py -p ${POTDIR} ${PYFILES}

mo: ${FRDIR}/pytrisk.po
	msgfmt ${FRDIR}/pytrisk.po -o ${FRDIR}/pytrisk.mo

clean:
	rm -rf dist pytrisk.egg-info
