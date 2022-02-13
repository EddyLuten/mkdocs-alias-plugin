# mkdocs-alias-plugin

An MkDocs plugin allowing links to your pages using a custom alias.

## Rationale

I maintain a fairly large wiki and occasionally will restructure parts of it, resulting in many broken links. This plugin allows me to separate the wiki contents from the file system structure and resolves the paths during build time. Maybe this plugin will help you out as well.

## Usage

In the meta section atop your page add:

```md
---
title: Wuthering Heights
alias:
    name: wuthering-heights
    text: Wuthering Heights, a novel by Emily Brontë
---
```

Then, using the alias:

```md
The song references [[wuthering-heights]].
```

If you'd like to supply your own link text instead:

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

## Local Development

```zsh
pip install -e /path/to/mkdocs-alias-plugin/
```
