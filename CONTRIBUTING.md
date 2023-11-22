# How to contribute

## Dependencies

We use [poetry](https://github.com/python-poetry/poetry) to manage the dependencies.

To install them you would need to run `install` command:

```bash
poetry install
```

To activate your `virtualenv` run `poetry shell`.

## One magic command

Run `make test` to run everything we have!

## Tests

We use `pytest` and `ruff` for quality control.

To run all tests:

```bash
make unit
```

To run linting:

```bash
make format
```

These steps are mandatory during the CI.

## Type checks

We use `mypy` to run type checks on our code.
To use it:

```bash
make lint
```

This step is mandatory during the CI.
