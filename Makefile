MODULE := gml
BLUE = '\033[0;34m'
NC = '\033[0m'
.DEFAULT_GOAL := run

run:
	@python3 -m $(MODULE)

run_auto:
	@printf "2\n1\n3\n1\n" | python3 -m $(MODULE) --arg myArg.

install:
	wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
	tar -xzvf geckodriver-v0.26.0-linux64.tar.gz
	rm geckodriver-v0.26.0-linux64.tar.gz
	sudo mv geckodriver /usr/local/bin
	python3 --version
	python3 -m venv env
	source ./env/bin/activate
	python3 -m pip install -r requirements.txt

env:
	python3 -m venv env
	source ./env/bin/activate

clean:
	rm -rf data/*
	kill -9 `pidof geckodriver`
	kill -9 `pidof firefox`
	kill -9 `pidof python3`
