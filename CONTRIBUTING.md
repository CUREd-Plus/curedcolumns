# Development environment

Use an IDE such as PyCharm or Visual Studio Code

Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment

```bash
source .venv/bin/activate
```

## Install package during development

### Local machine

Install the package in editable mode

```bash
pip install --editable .[test]
```

### Remote machine

Install from GitHub using [pip install](https://pip.pypa.io/en/stable/cli/pip_install/):

```bash
pip install --force git+https://github.com/CUREd-Plus/curedcolumns.git
```

## Testing

Tests are located in the `tests/` directory.

```bash
pytest
```
