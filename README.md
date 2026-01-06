# GPN Einkauf Tools

Contains tools used by the GPN Einkauf Team to manage their workload.

## KAUF command line tool

Located at `/src/kauf` is a command line utility with some neat commands to make shopping simpler.

### Installation

Create a new virtual environment, e.g. with `virtualenv .venv` and activate it `source .venv/bin/activate`.

`kauf` can be installed via `pipx` with the following command:

```bash
pipx install .
```

Then call it

```bash
kauf --help
```

### Development

Create a new virtual environment, e.g. with `virtualenv .venv` and activate it `source .venv/bin/activate`.

**Dependencies**

To install the dependencies locally run

```bash
pip install .
```

**Running locally**

To avoid having to install the command line tool to test it locally you can run it as well with

```bash
python src/kauf
```

**Linting**

Run `ruff format .` and `ruff check . --fix` for local linting.