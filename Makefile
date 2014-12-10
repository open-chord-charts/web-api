.PHONY: clean flake8

all: clean flake8

clean:
	find -name "*.pyc" | xargs rm -f
	rm -rf cache/*

flake8:
	flake8 --ignore=E123 --max-line-length=120 openchordcharts scripts
