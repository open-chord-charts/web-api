.PHONY: clean flake8 jshint

all: clean flake8 jshint

clean:
	find -name "*.pyc" | xargs rm -f
	rm -rf cache/*

flake8:
	flake8

jshint:
	jshint openchordcharts/static
