.PHONY: check compile flake8 jshint pep8 pyflakes

all: check

check: flake8

clean:
	find -name *.pyc | xargs rm -f

flake8:
	flake8 --ignore=E501 .

pep8:
	pep8 --max-line-length=120 .

compile:
	make -C openchordcharts/static all

watch:
	cd openchordcharts/static; make watch
