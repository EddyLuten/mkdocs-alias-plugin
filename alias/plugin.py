"""mkdocs-alias-plugin

An MkDocs plugin allowing links to your pages using a custom alias.
"""

import logging
import re
from mkdocs.plugins import BasePlugin
from mkdocs.utils import meta, get_markdown_title
from mkdocs.config import config_options

# The Regular Expression used to find alias tags
ALIAS_TAG_REGEX = r"\[\[([^|^\]]+)\|?([^\]]+)?\]\]"

def get_page_title(page_src, meta_data):
    """Returns the title of the page. The title in the meta data section
    will take precedence over the H1 markdown title if both are provided."""
    return (
        meta_data['title']
        if 'title' in meta_data and isinstance(meta_data['title'], str)
        else get_markdown_title(page_src)
    )

def get_alias_names(meta_data):
    """Returns the list of configured alias names."""
    if len(meta_data) <= 0 or 'alias' not in meta_data:
        return None
    aliases = meta_data['alias']
    if isinstance(aliases, list):
        # If the alias meta data is a list, ensure that they're strings
        return list(filter(lambda value: isinstance(value, str), aliases))
    if isinstance(aliases, dict) and 'name' in aliases:
        return [ aliases['name'] ]
    if isinstance(aliases, str):
        return [ aliases ]
    return None

class AliasPlugin(BasePlugin):
    """An extension of BasePlugin providing all of the aliasing logic.

    The plugin works by reading all of the markdown files before they are
    processed and parsing their meta sections.

    See on_files() for more info.

    For overridden BasePlugin methods, see the MkDocs source code.
    """
    config_scheme = (
        ('verbose', config_options.Type(bool, default=False)),
    )
    aliases = {}
    log = logging.getLogger(f'mkdocs.plugins.{__name__}')
    current_page = None

    def on_config(self, _):
        """Set the log level if the verbose config option is set"""
        self.log.setLevel(
            logging.INFO if self.config['verbose'] else logging.WARNING
        )

    def on_post_build(self, **_):
        """Executed after the build has completed. Clears the aliases from
        memory and displays stats if the verbose option is configured.
        """
        self.log.info("Defined %s alias(es).", len(self.aliases))
        self.aliases.clear()

    def on_page_markdown(self, markdown, page, **_):
        """Replaces any alias tags on the page with markdown links."""
        self.current_page = page
        return re.sub(
            ALIAS_TAG_REGEX,
            self.__replace_tag,
            markdown
        )

    def __replace_tag(self, match, **_):
        """Callback used in the sub function within on_page_markdown."""
        alias = self.aliases.get(match.group(1))
        if alias is None:
            self.log.warning(
                "Alias '%s' not found in '%s'",
                match.group(1),
                self.current_page.file.src_path
            )
            return match.group(0) # return the input string

        text = alias['text'] if match.group(2) is None else match.group(2)
        if text is None:
            text = alias['url']
        self.log.info(
            "replaced alias '%s' with '%s' to '%s'",
            alias['alias'],
            text,
            alias['url']
        )
        return f"[{text}]({alias['url']})"

    def on_files(self, files, **_):
        """When MkDocs loads its files, extract aliases from any Markdown files
        that were found.
        """
        for file in filter(lambda f: f.is_documentation_page(), files):
            with open(file.abs_src_path, encoding='utf-8-sig', errors='strict') as handle:
                source, meta_data = meta.get_data(handle.read())
                alias_names = get_alias_names(meta_data)
                if alias_names is None or len(alias_names) < 1:
                    continue

                if len(alias_names) > 1:
                    self.log.info(
                        '%s defines %d aliases:', file.url, len(alias_names)
                    )
                for alias in alias_names:
                    existing = self.aliases.get(alias)
                    if existing is not None:
                        self.log.warning(
                            "%s: alias %s already defined in %s, skipping.",
                            file.url,
                            alias,
                            existing['url']
                        )
                        continue

                    new_alias = {
                        'alias': alias,
                        'text': (
                            meta_data['alias']['text']
                            if 'text' in meta_data['alias']
                            else get_page_title(source, meta_data)
                        ),
                        'url': f"/{file.url}",
                    }
                    self.log.info(
                        "Alias %s to %s",
                        alias,
                        new_alias['url']
                    )
                    self.aliases[alias] = new_alias
