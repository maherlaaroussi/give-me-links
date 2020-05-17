MODULE := "gml/app.py"
BLUE = '\033[0;34m'
NC = '\033[0m'
.DEFAULT_GOAL := run
.SILENT: install

run:
	@python3 $(MODULE)

install:
	@echo "Installation start ..."
	@wget -q https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
	@tar -xzf geckodriver-v0.26.0-linux64.tar.gz
	@rm geckodriver-v0.26.0-linux64.tar.gz
	@sudo -E mv geckodriver /usr/local/bin
	@python3 -m venv env
	@python3 -m setup -q install --user
	@echo "GML is now installed!"

clean:
	@./clean.sh
