all: compile

check: pyflakes pep8

pyflakes:
	pyflakes .

pep8:
	pep8 .

compile:
	make -C openchordcharts/static all

watch:
	cd openchordcharts/static; make watch
