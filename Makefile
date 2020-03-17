PACKAGE="pycran"

.DEFAULT_GOAL:=help
.PHONY: help tests install develop uninstall deps-check clean clean-build clean-test format lint

help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

tests:
	@pytest -n 4 --cov-report html:htmlcov --cov=$(PACKAGE)

install: clean
	@pip install .

develop: clean
	@pip install .[dev,test]

uninstall: clean
	@pip uninstall $(PACKAGE)

clean: clean-build clean-test

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr .eggs/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +

clean-test:
	@rm -f .coverage
	@rm -fr htmlcov/
	@rm -fr .mypy_cache
	@rm -fr .pytest_cache

lint:
	@echo "Running code-style check..."
	@isort --check-only -rc pycran tests
	@black --check pycran tests
	@echo "Running static-type checker..."
	@mypy pycran tests

reformat:
	@isort -ac -rc pycran tests
	@black pycran tests
	@mypy pycran tests
