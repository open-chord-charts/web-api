all: check

check: flake8 jshint

clean: clean-pyc

clean-pyc:
	find -name "*.pyc" -exec rm \{\} \;

ctags:
	ctags --recurse=yes .

flake8: clean-pyc
	flake8
