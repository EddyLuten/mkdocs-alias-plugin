# mkdocs-alias-plugin

[![PyPI version](https://badge.fury.io/py/mkdocs-alias-plugin.svg)](https://pypi.org/project/mkdocs-alias-plugin/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/mkdocs-alias-plugin)](https://pepy.tech/project/mkdocs-alias-plugin)
[![CI Status](https://codeberg.org/luten/mkdocs-alias-plugin/badges/workflows/ci.yml/badge.svg)](https://codeberg.org/luten/mkdocs-alias-plugin/actions?workflow=ci.yml)

> [!IMPORTANT]
> This repository has moved to [Codeberg](https://codeberg.org/luten/mkdocs-alias-plugin).
>
> This GitHub **mirror** is synced automatically, but please file issues and pull requests on Codeberg. See the [CONTRIBUTING](CONTRIBUTING.md) file for details. All existing issues and pull requests have also migrated there.

The mkdocs-alias-plugin MkDocs plugin allows links to your pages using custom aliases:

```md
This is a link to [[my-page]].
This is a link to [[my-page|the same]] alias.
```

[Read the documentation](https://alias.luten.dev/) for more advanced use cases.

Using aliases allows you to decouple the file structure of your MkDocs wiki from its taxonomy. For example, if you have a wiki about animals which accidentally classifies pigs as reptiles, after moving the file into the mammals directory, you won’t have to update all of the links to the pig page. Depending on the size of your wiki, this can save quite a bit of time.

This plugin uses a wikilinks-like syntax, but is different in that the aliases are configured through the frontmatter (meta-sections) of each page, rather than defined by the page’s titles. For example, adding the following item to your page’s frontmatter allows you to use the above alias:

```yaml
alias: my-page
```

If you like this plugin, you'll probably also like [mkdocs-categories-plugin](https://pypi.org/project/mkdocs-categories-plugin) and [mkdocs-live-edit-plugin](https://pypi.org/project/mkdocs-live-edit-plugin).

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

## Basic Usage

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

This is the most common use case. If you have more advanced needs, you can find more complex examples in [the project's documentation](https://alias.luten.dev/).

## Changelog

### 0.11.1

2026-04-05

Non-code release. Updates the PyPI metadata to point to the new Codeberg repository.

### 0.11.0

2026-03-09

**Feature**: Adds the ability to use interwiki-style links, e.g.: `[[wp:Hypertext|An article on Hypertext]]`.

### 0.10.2

2026-02-09

**Bug Fix**: Fixes a bug where escaped square brackets in an alias would not be included in the generated link.

### 0.10.1

2026-01-08

**Bug Fix**: Fixes a bug where adding an anchor to a bad reference would cause a fatal crash.

Thank you @mdbenito for you [contribution](https://codeberg.org/luten/mkdocs-alias-plugin/issues/17) and @joapuiib for your [unit test coverage](https://codeberg.org/luten/mkdocs-alias-plugin/pulls/19)!

### 0.10.0

2026-01-07

**Feature**: Adds the ability to use aliases in footnotes. Thank you @joapuiib for your [contribution](https://codeberg.org/luten/mkdocs-alias-plugin/pulls/22)!

### 0.9.0

2025-02-21

**Features and Bug Fixes:**

- Added the ability to use alias style links to anchors withing the current page, e.g.: `[[#my-anchor]]`.
- Added support for page icons in link aliases
- Added support for using the key `alias` and/or `aliases` for defining page aliases in meta sections.
- Changed verbose mode to now also generates a tab-delimited log file containing each alias in the wiki.

Thank you, @joapuiib, for your [contribution](https://codeberg.org/luten/mkdocs-alias-plugin/pulls/15)!

### 0.8.1

2024-04-08

**Bug Fix:** fixes a bug where annotations would break older versions of Python 3. Bug report: [#9](https://codeberg.org/luten/mkdocs-alias-plugin/issues/9).

### 0.8.0

2024-04-06

This release adds functionality to replace the titles of aliases containing anchors with the text of the heading that defines them. Enable this feature by setting the plugin option `use_anchor_titles` to true. Feature request: [#8](https://codeberg.org/luten/mkdocs-alias-plugin/issues/8).

### 0.7.1

2024-04-07

**Bug Fix:** fixes a bug where any alias with the word "text" would break the plugin due to faulty logic. Bug report: [#7](https://codeberg.org/luten/mkdocs-alias-plugin/issues/7).

### 0.7.0

2024-02-01

This release removes support for the `use_relative_link` option introduced in issue [#3](https://codeberg.org/luten/mkdocs-alias-plugin/issues/3). As of version 1.5.0, MkDocs prefers relative links to absolute links, which was this package's default before. As of this version, all alias links generated are relative to the file from where they were linked.

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
