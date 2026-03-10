# Contributing

Pull requests are disabled for the time being, but if you find a bug, or wish to request a feature, feel free to open a new issue.

## Local Development

Upgrade pip and install the dependencies:

```zsh
python -m pip install --upgrade pip
pip install mkdocs pytest pylint markdown setuptools
```

Installing a local copy of the plugin (potentially from your MkDoc's venv location):

```zsh
pip install -e /path/to/mkdocs-alias-plugin/
```

Running unit tests after installing pytest from the root directory:

```zsh
pytest -vv
```

Both unit test and linting:

```zsh
pylint $(git ls-files '*.py') && pytest -vv
```
