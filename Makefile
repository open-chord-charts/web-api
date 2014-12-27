all: check

check: flake8 jshint

clean: clean-pyc

clean-pyc:
	find -name "*.pyc" -exec rm \{\} \;

compile-i18n-python:
	python setup.py compile_catalog

ctags:
	ctags --recurse=yes .

flake8: clean-pyc
	flake8

poedit: update-i18n-python
	poedit openchordcharts_api/i18n/fr/LC_MESSAGES/openchordcharts-api.po
	make compile-i18n-python

# test:
# 	nosetests openchordcharts_api/tests

update-i18n: update-i18n-js update-i18n-python

update-i18n-python:
	python setup.py extract_messages update_catalog

update-i18n-js:
	./openchordcharts_api/scripts/extract_i18n_json_messages.py --all --no-delete-regex='.+:.+'
