PACKAGE="pycran"
.DEFAULT_GOAL:=help

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: tests
tests:
	@pytest --cov-report html:htmlcov --cov=$(PACKAGE)

.PHONY: install
install: clean
	@pip install .

.PHONY: develop
develop: clean
	@pip install .[dev,test]

.PHONY: uninstall
uninstall: clean
	@pip uninstall $(PACKAGE)

.PHONY: clean
clean: clean-build clean-test

.PHONY: clean-build
clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr .eggs/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-test
clean-test:
	@rm -f .coverage
	@rm -fr htmlcov/
	@rm -fr .mypy_cache
	@rm -fr .pytest_cache

.PHONY: lint
lint:
	@echo "Running code-style check..."
	@isort --check-only -rc pycran tests
	@black --check pycran tests
	@echo "Running static-type checker..."
	@mypy pycran tests

.PHONY: format
format:
	@isort -ac -rc pycran tests
	@black pycran tests
	@mypy pycran tests
