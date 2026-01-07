# mkdocs-alias-plugin

[![PyPI version](https://badge.fury.io/py/mkdocs-alias-plugin.svg)](https://pypi.org/project/mkdocs-alias-plugin/)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Downloads](https://pepy.tech/badge/mkdocs-alias-plugin)](https://pepy.tech/project/mkdocs-alias-plugin) [![CI](https://github.com/eddyluten/mkdocs-alias-plugin/workflows/mkdocs-alias-plugin%20CI/badge.svg)](https://github.com/EddyLuten/mkdocs-alias-plugin/actions/workflows/ci.yml)

The `mkdocs-alias-plugin` MkDocs plugin allows links to your pages using a custom alias such as `[[my-alias]]` or `[[my-alias|My Title]]`.

The aliases are configured through the meta-sections of each page (see Usage below).

If you like this plugin, you'll probably also like [mkdocs-categories-plugin](https://github.com/EddyLuten/mkdocs-categories-plugin) and [mkdocs-live-edit-plugin](https://github.com/EddyLuten/mkdocs-live-edit-plugin).

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

A more advanced example would be to use the dictionary-style configuration instead of providing a different link title:

```yaml
---
alias:
    name: wuthering-heights
    text: Wuthering Heights, a novel by Emily Brontë
---
```

If you'd like to supply a custom link text instead on a link-by-link basis, you can do so using a pipe to separate the title from the alias:

```md
The song references [[wuthering-heights|Wuthering Heights]].
```

As of version 0.6.0, you can also use link anchors in your aliases:

```md
The song references [[wuthering-heights#references]].
```

Or, using a custom title:

```md
The song references [[wuthering-heights#references|Wuthering Heights]].
```

As of version 0.8.0, you can enable the plugin option `use_anchor_titles` to replace anchor links with the text of the page heading that defined it. This behavior is opt-in to preserve backward compatibility.

As of version 0.9.0, you may also use `aliases` in addition to (or in place of) the `alias` key in the meta section of your pages. This is to provide some similarity to other Markdown based software that supports aliases, such as Obsidian.

Please refer to the [MkDocs documentation](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data) for more information on how the meta-data block is used.

As of version 0.10.0, you may use a specialized version of the alias syntax for aliases in footnotes:

```markdown
The plugin [`mkdocs-alias-plugin`][alias-plugin] is awesome!

[alias-plugin]: https://github.com/EddyLuten/mkdocs-alias-plugin
```

### Multiple Aliases

As of version 0.3.0, assigning multiple aliases to a single page is possible. This feature does come with the limitation that these aliases cannot define a per-alias title and instead will use the page title. The syntax for this is:

```yaml
---
alias:
    - wuthering-heights
    - wuthering
    - wh
---
```

### Escaping Aliases (Escape Syntax)

As of version 0.4.0, it is possible to escape aliases to prevent them being parsed by the plugin. This is useful if you use a similar double-bracket markup for a different purpose (e.g. shell scripts in code blocks). The syntax for this feature is a leading backslash:

```md
\[[this text will remain untouched]]

[[this text will be parsed as an alias]]
```

## Options

You may customize the plugin by passing options into the plugin's configuration sections in `mkdocs.yml`:

```yaml
plugins:
    - alias:
        verbose: true
        use_anchor_titles: true
        use_page_icon: true
```

### `verbose`

You may use the optional `verbose` option to print more information about which aliases were used and defined during the build process. A tab-delimited file named `aliases.log` will also be defined at the project root, containing a list of every alias defined by the wiki.

The default value is `false` and should only be enabled when debugging issue with the plugin.

### `use_anchor_titles`

Setting this flag to true causes the plugin to replace an alias containing an anchor (`[[my-page#sub-heading]]`) with the text of the header that defined it. You can still override the title of the link as usual.

### `use_page_icon`

Setting this flag to true will include the [page's icon](https://squidfunk.github.io/mkdocs-material/reference/?h=page+icon#setting-the-page-icon) in the alias substitution if it's set for a given page.

## Troubleshooting

### The link text looks like a path or URL

Your alias doesn't have link text defined *and* your page doesn't have a title H1 tag or a `title` attribute in its meta data section. Once you add this, your link will render with the appropriate text.

### My alias is not replaced

`WARNING  -  Alias 'my-alias' not found`

The alias could not be found in the defined aliases, usually due to a typo. Enable verbose output in the plugin's configuration to display all of the found aliases.

However, it is also possible that the plugin is trying to interpret another double-bracketed syntax as an alias. In this case, use the escape syntax to prevent the plugin from parsing it.

### "Alias already defined"

You're getting a message resembling this in your output:

`WARNING  -  page-url: alias alias-name already defined in other-url, skipping.`

Aliases *must* be unique. Ensure that you're not redefining the same alias for a different page. Rename one of them and the warning should go away.

## Local Development

Upgrade pip and install the dependencies:

```zsh
python -m pip install --upgrade pip
pip install mkdocs pytest pylint markdown setuptools
```

Installing a local copy of the plugin:

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

## Changelog

## 0.10.0

2026-01-07

Adds the ability to use aliases in footnotes. Thank you @joapuiib for your [contribution](https://github.com/EddyLuten/mkdocs-alias-plugin/pull/22)!

## 0.9.0

2025-02-21

**Features and Bug Fixes:**

- Added the ability to use alias style links to anchors withing the current page, e.g.: `[[#my-anchor]]`.
- Added support for page icons in link aliases, thank you @joapuiib for your [contribution](https://github.com/EddyLuten/mkdocs-alias-plugin/pull/15)!
- Added support for using the key `alias` and/or `aliases` for defining page aliases in meta sections.
- Changed verbose mode to now also generates a tab-delimited log file containing each alias in the wiki.

## 0.8.1

2024-04-08

**Bug Fix:** fixes a bug where annotations would break older versions of Python 3. Bug report: [#9](https://github.com/EddyLuten/mkdocs-alias-plugin/issues/9).

## 0.8.0

2024-04-06

This release adds functionality to replace the titles of aliases containing anchors with the text of the heading that defines them. Enable this feature by setting the plugin option `use_anchor_titles` to true. Feature request: [#8](https://github.com/EddyLuten/mkdocs-alias-plugin/issues/8).

### 0.7.1

2024-04-07

**Bug Fix:** fixes a bug where any alias with the word "text" would break the plugin due to faulty logic. Bug report: [#7](https://github.com/EddyLuten/mkdocs-alias-plugin/issues/7).

### 0.7.0

2024-02-01

This release removes support for the `use_relative_link` option introduced in issue [#3](https://github.com/EddyLuten/mkdocs-alias-plugin/issues/3). As of version 1.5.0, MkDocs prefers relative links to absolute links, which was this package's default before. As of this version, all alias links generated are relative to the file from where they were linked.

### 0.6.0

2023-04-17

Adds support for page anchor links from within an alias. E.g.:

```md
[[my alias#my anchor]]
````

### 0.5.0

2023-02-08

Adds the ability to use the `use_relative_link` config flag, which causes the plugin to generate relative links to the aliased document rather than absolute ones. This flag is useful for those who host their wikis in subdirectories.

@SimonDelmas contributed this feature in PR #3. Thanks!

### 0.4.0

2022-07-10

Adds the ability to escape aliases so they won't be parsed by the plugin. Also adds more unit tests.

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
