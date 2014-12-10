.PHONY: clean flake8 jshint

all: clean flake8 jshint

clean:
	find -name "*.pyc" | xargs rm -f
	rm -rf cache/*

flake8:
	flake8 --ignore=E123,E128 --max-line-length=120 openchordcharts

jshint:
	jshint --show-non-errors openchordcharts/static
