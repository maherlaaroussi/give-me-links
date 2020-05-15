MODULE := gml
BLUE = '\033[0;34m'
NC = '\033[0m'
.DEFAULT_GOAL := run

run:
	@python3 -m $(MODULE)

run_auto:
	@printf "2\n1\n3\n1\n" | python3 -m $(MODULE) --arg myArg.

install:
	@chmod +x ./install.sh
	@chmod +x ./before_run.sh
	@chmod +x ./clean.sh
	@./install.sh

prepare:
	@./before_run.sh

clean:
	@./clean.sh
