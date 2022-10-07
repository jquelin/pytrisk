upload: build
	twine upload dist/*

build: clean
	python -m build

clean:
	rm -rf dist pytrisk.egg-info
