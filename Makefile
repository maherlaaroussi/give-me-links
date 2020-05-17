MODULE := "gml/app.py"
BLUE = '\033[0;34m'
NC = '\033[0m'
.DEFAULT_GOAL := run

run:
	@python3 $(MODULE)

install:
	@python3 -m setup install --user
	@echo "GML is now installed!"

clean:
	@./clean.sh
