all: compile

compile:
	rm -rf js
	mkdir js
	coffee -c -o js coffee

uglify:
	for f in `find js -name "*.js" -not -name "*.min.js"`; do \
		uglifyjs -o `dirname $$f`/`basename $$f .js`.min.js $$f; \
	done

watch:
	make || notify-send "coffee compile error"
	while inotifywait -e modify -r coffee; do \
		make || notify-send "coffee compile error"; \
	done
