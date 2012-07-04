all: compile

compile:
	stylus css
	coffee -c js
	eco templates

uglify:
	for f in `find js -name "*.js" -not -name "*.min.js"`; do \
		uglifyjs -o `dirname $$f`/`basename $$f .js`.min.js $$f; \
	done

watch:
	make || notify-send "coffee compile error"
	while inotifywait -e modify -r css js templates; do \
		make || notify-send "coffee compile error"; \
	done
