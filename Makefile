.PHONY: check coffeelint flake8

all: check

check: coffeelint flake8

clean:
	find -name *.pyc | xargs rm -f
	cd client; rm -rf node_modules
	cd openchordcharts; rm -f static/application.css static/application.js

coffeelint:
	coffeelint -f data/coffeelint.json -r client/app/

compile:
	cd client; npm install .; hem build

flake8:
	flake8 --ignore=E501 .

watch:
	cd client; npm install .; hem watch --debug
