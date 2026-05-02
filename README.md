# GPN Einkauf Tools

Contains tools used by the GPN Einkauf Team to manage their workload.

## KAUF command line tool

Located at `/src/kauf` is a command line utility with some neat commands to make shopping simpler.

**Create a shopping list from JIRA issues by tag**

```bash
kauf jira list --jira-url jira.example.com --tag "Buy Now" --hedgedoc-url "pad.example.com"
```

**Create a shopping list from JIRA issues by keys**

```bash
kauf jira list --jira-url jira.example.com --hedgedoc-url "pad.example.com" -k PROJ-111 -k PROJ-112 -k PROJ-113
```

**Transition all JIRA issues from a shopping list where all items from that issue are ticked**

```bash
kauf jira update --hedgedoc-url "pad.example.com/XXXXX" --jira-url jira.example.com --transition "Mark arrived"
```

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

#### Secrets

In case your JIRA needs authentication:

```bash
kauf secrets set jira_token xxx
```

Or the HedgeDoc requires to be logged in (use SID cookie from your browser):

```bash
kauf secrets set hedgedoc_sid xxx
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

**Verbose mode**

Use the `--verbose` flag for verbose output.

```bash
kauf --verbose ...
```

**Linting**

Run `ruff format .` and `ruff check . --fix` for local linting.