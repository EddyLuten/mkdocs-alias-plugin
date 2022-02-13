# mkdocs-alias-plugin

[![PyPI version](https://badge.fury.io/py/mkdocs-alias-plugin.svg)](https://pypi.org/project/mkdocs-alias-plugin/)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![example workflow](https://github.com/eddyluten/mkdocs-alias-plugin/actions/workflows/pylint.yml/badge.svg)

An MkDocs plugin allowing links to your pages using a custom alias.

The use syntax of the alias is reminiscent of MediaWiki links.

## Rationale

I maintain a fairly large wiki and occasionally will restructure parts of it, resulting in many broken links. This plugin allows me to separate the wiki contents from the file system structure and resolves the paths during build time. Maybe this plugin will help you out as well.

## Usage

In the meta section atop your page add an `alias` section:

```md
---
alias:
    name: wuthering-heights
    text: Wuthering Heights, a novel by Emily Brontë
---
```

Then, using the alias in the markdown content of your pages:

```md
The song references [[wuthering-heights]].
```

If you'd like to supply your own link text instead, you can do so using a pipe to separate it from the alias:

```md
The song references [[wuthering-heights|Wuthering Heights]].
```

## Installation

Install the package with pip:

```bash
pip install mkdocs-alias-plugin
```

Then in your `mkdocs.yml` file add the following entry to the plugins section:

```yml
plugins:
  - alias
```

## Options

You may customize the plugin by passing options in mkdocs.yml:

```yaml
plugins:
    - alias:
        verbose: true
```

### `verbose`

You may use the optional `verbose` option to print more information about which aliases were used and defined during build. The default value is `false`.

## Troubleshooting

### My alias not being replaced

Or: `WARNING  -  Alias 'my-alias' not found`

The alias could not be found in the defined aliases, usually due to a typo. Enable verbose output in the plugin's configuration to display all of the found aliases.

### "Alias already defined"

You're getting a message resembling this in your output:

`WARNING  -  page-url: alias alias-name already defined in other-url, skipping.`

Aliases *must* be unique. Ensure that you're not redefining the same alias for a different page. Rename one of them and the warning should go away.

## Local Development

```zsh
pip install -e /path/to/mkdocs-alias-plugin/
```
