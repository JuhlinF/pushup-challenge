 ifeq (, $(shell which pip-compile))
 $(error "No pip-compile in PATH, consider doing pip install pip-tools")
 endif

all: requirements.txt requirements-dev.txt

requirements.txt: pyproject.toml
	pip-compile --output-file=requirements.txt --strip-extras

requirements-dev.txt: pyproject.toml
	pip-compile --extra=dev --output-file=requirements-dev.txt --strip-extras

clean:
	rm -f requirements.txt requirements-dev.txt