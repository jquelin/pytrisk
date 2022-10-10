TOML_FILE = pyproject.toml
PYFILES = $(shell find . -type f -name *.py)
POTDIR  = pytrisk/locale
POFILE  = ${POTDIR}/messages.pot
FRDIR   = ${POTDIR}/fr/LC_MESSAGES/

COLOR = 3

LASTVER = $(shell git tag | tail -1 | tr -d v)
CURVER  = $(shell grep version ${TOML_FILE}| sed -e 's/^.*=//' | tr -d ' "')
LASTVER_MAJOR = $(shell echo ${LASTVER} | cut -d. -f1)
LASTVER_MINOR = $(shell echo ${LASTVER} | cut -d. -f2)
LASTVER_PATCH = $(shell echo ${LASTVER} | cut -d. -f3)



dist: build

clean:
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	rm -rf dist pytrisk.egg-info

upload: build
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	[ "${LASTVER}" == "${CURVER}" ] && echo "version has not changed" && exit 1 || exit 0
	twine upload dist/*

build: clean
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	python -m build

# l10n

pot: ${PYFILES}
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	@mkdir -p ${POTDIR}
	pygettext.py -p ${POTDIR} ${PYFILES}

mo: ${FRDIR}/pytrisk.po
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	msgfmt ${FRDIR}/pytrisk.po -o ${FRDIR}/pytrisk.mo

# version handling

patch:
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	$(eval NEWVER_PATCH=$(shell echo ${LASTVER_PATCH}+1|bc))
	$(eval NEWVER="${LASTVER_MAJOR}.${LASTVER_MINOR}.${NEWVER_PATCH}")
	@echo "previous version: ${LASTVER}"
	@echo "new version:      ${NEWVER}"
	toml set --toml-path ${TOML_FILE} project.version ${NEWVER}

minor:
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	$(eval NEWVER_MINOR=$(shell echo ${LASTVER_MINOR}+1|bc))
	$(eval NEWVER="${LASTVER_MINOR}.${NEWVER_MINOR}.0")
	@echo "previous version: ${LASTVER}"
	@echo "new version:      ${NEWVER}"
	toml set --toml-path ${TOML_FILE} project.version ${NEWVER}

major:
	@tput setaf ${COLOR} && echo $@ && tput sgr 0
	$(eval NEWVER_MAJOR=$(shell echo ${LASTVER_MAJOR}+1|bc))
	$(eval NEWVER="${NEWVER_MAJOR}.0.0")
	@echo "previous version: ${LASTVER}"
	@echo "new version:      ${NEWVER}"
	toml set --toml-path ${TOML_FILE} project.version ${NEWVER}

