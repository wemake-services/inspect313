SHELL:=/usr/bin/env bash

.PHONY: format
format:
	poetry run ruff --exit-non-zero-on-fix .
	poetry run ruff format --check .

.PHONY: lint
lint:
	poetry run mypy .

.PHONY: unit
unit:
	poetry run pytest

.PHONY: doctest
doctest:
	poetry run python -m doctest README.md

.PHONY: package
package:
	poetry check
	poetry run pip check

.PHONY: test
test: format lint package unit doctest
