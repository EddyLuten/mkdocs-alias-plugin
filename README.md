# mkdocs-alias-plugin

[![PyPI version](https://badge.fury.io/py/mkdocs-alias-plugin.svg)](https://pypi.org/project/mkdocs-alias-plugin/)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![example workflow](https://github.com/eddyluten/mkdocs-alias-plugin/actions/workflows/pylint.yml/badge.svg) [![Downloads](https://pepy.tech/badge/mkdocs-alias-plugin)](https://pepy.tech/project/mkdocs-alias-plugin) ![](https://github.com/eddyluten/mkdocs-alias-plugin/workflows/mkdocs-alias-plugin%20Tests/badge.svg)

An MkDocs plugin allowing links to your pages using a custom alias such as `[[my-alias]]` or `[[my-alias|My Title]]`.

The aliases are configured through the meta-sections of each page (see Usage below).

If you like this plugin, you'll probably also like [mkdocs-categories-plugin](https://github.com/EddyLuten/mkdocs-categories-plugin).

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
alias: wuthering-heights
---
```

Then, using the alias in the markdown content of your pages:

```md
The song references [[wuthering-heights]].
```

Which, after the page builds, renders as a regular link to your page.

Or, a more advanced example by using the dictionary-style configuration instead to provide a different link title.

```yaml
---
alias:
    name: wuthering-heights
    text: Wuthering Heights, a novel by Emily Brontë
---
```

If you'd like to supply your own link text instead on a link-by-link basis, you can do so using a pipe to separate the title from the alias:

```md
The song references [[wuthering-heights|Wuthering Heights]].
```

Please refer to the [MkDocs documentation](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data) for more information on how the meta-data block is used.

### Multiple Aliases

As of version 0.3.0, it is possible to assign multiple aliases to a single page. This does come with the limitation that these aliases cannot define a per-alias title. The syntax for this is:

```yaml
---
alias:
    - wuthering-heights
    - wuthering
    - wh
---
```

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

### The link text looks like a path or URL

Your alias doesn't have link text defined *and* your page doesn't have a title H1 tag or a `title` attribute in its meta data section. Once you add this, your link will render with the appropriate text.

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

## Changelog

### 0.3.0

2022-04-27

Adds the ability to create multiple aliases for a single page (see the documentation for "Multiple Aliases" above). Improves the "alias not found" warning by listing the file attempting to use the alias.

### 0.2.0

2022-02-23

Allow strings as aliases instead of dictionaries, which allows for the use of page titles in the link text of the alias.

This version also makes the `text` key optional in the alias dictionary configuration, using the same page title link text instead if it's not provided.

### 0.1.1

2022-02-12

Fixes a bunch of linter issues, but no new logic.

### 0.1.0

2022-02-12

Initial release with all of the base logic in place.
