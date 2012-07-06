.PHONY: check flake8 pep8

all: check

check: flake8

clean:
	find -name *.pyc | xargs rm -f
	cd client; rm -rf node_modules
	cd openchordcharts; rm -f static/application.css static/application.js

compile:
	cd client; npm install .; hem build

flake8:
	flake8 --ignore=E501 .

pep8:
	pep8 --max-line-length=120 .

watch:
	cd client; npm install .; hem watch --debug
