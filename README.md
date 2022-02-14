# mkdocs-alias-plugin

[![PyPI version](https://badge.fury.io/py/mkdocs-alias-plugin.svg)](https://pypi.org/project/mkdocs-alias-plugin/)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![example workflow](https://github.com/eddyluten/mkdocs-alias-plugin/actions/workflows/pylint.yml/badge.svg) [![Downloads](https://pepy.tech/badge/mkdocs-alias-plugin)](https://pepy.tech/project/mkdocs-alias-plugin)

An MkDocs plugin allowing links to your pages using a custom alias such as `[[my-alias]]` or `[[my-alias|My Title]]`.

The aliases are configured through the meta-sections of each page (see Usage below).

## Rationale

I maintain a fairly large wiki and occasionally will restructure parts of it, resulting in many broken links. This plugin allows me to separate the wiki contents from the file system structure and resolves the paths during build time. Maybe this plugin will help you out as well.

## Installation

Install the package using pip:

```zsh
pip install mkdocs-alias-plugin
```

Then add the following entry to the plugins section of your `mkdocs.yml` file:

```yml
plugins:
  - alias
```

For further configuration, see the Options section below.

## Usage

Add an `alias` section to your page's meta block:

```yaml
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

Which, after the page builds, renders as a regular link to your page.

If you'd like to supply your own link text instead, you can do so using a pipe to separate the title from the alias:

```md
The song references [[wuthering-heights|Wuthering Heights]].
```

Please refer to the [MkDocs documentation](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data) for more information on how the meta-data block is used.

## Options

You may customize the plugin by passing options into the plugin's configuration sections in `mkdocs.yml`:

```yaml
plugins:
    - alias:
        verbose: true
```

### `verbose`

You may use the optional `verbose` option to print more information about which aliases were used and defined during build. The default value is `false`.

## Troubleshooting

### My alias is not being replaced

`WARNING  -  Alias 'my-alias' not found`

The alias could not be found in the defined aliases, usually due to a typo. Enable verbose output in the plugin's configuration to display all of the found aliases.

### "Alias already defined"

You're getting a message resembling this in your output:

`WARNING  -  page-url: alias alias-name already defined in other-url, skipping.`

Aliases *must* be unique. Ensure that you're not redefining the same alias for a different page. Rename one of them and the warning should go away.

## Local Development

```zsh
pip install -e /path/to/mkdocs-alias-plugin/
```
