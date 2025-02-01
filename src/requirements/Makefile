 ifeq (, $(shell which pip-compile))
 $(error "No pip-compile in PATH, consider doing pip install pip-tools")
 endif

.PHONY: all clean install install-dev

all: requirements.txt requirements-dev.txt

requirements.txt: pyproject.toml
	pip-compile --output-file=$@ --strip-extras

requirements-dev.txt: pyproject.toml
	pip-compile --extra=dev --output-file=$@ --strip-extras

install: requirements.txt
	pip install -r $^

install-dev: requirements-dev.txt
	pip install -r $^

clean:
	rm -f requirements.txt requirements-dev.txt