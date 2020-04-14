.PHONY: exe
exe:
	pyinstaller --onefile src/fuxenpruefung.py
	pyinstaller ./fuxenpruefung.spec

exe-snake:
	pyinstaller --onefile src/fuxensnake.py
	pyinstaller ./fuxensnake.spec

.PHONY: run
run:
	python src/fuxenpruefung.py

.PHONY: snake
snake:
	python src/snake.py
