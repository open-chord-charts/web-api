all: compile

compile:
	make -C openchordcharts/static all

watch:
	cd openchordcharts/static; make watch
