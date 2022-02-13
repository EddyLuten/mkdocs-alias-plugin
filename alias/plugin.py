"""mkdocs-alias-plugin

An MkDocs plugin allowing links to your pages using a custom alias.
"""

import logging
import re
from mkdocs.plugins import BasePlugin
from mkdocs.utils import meta
from mkdocs.config import config_options

TAGS_REGEX = r"\[\[([^|^\]]+)\|?([^\]]+)?\]\]"

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

    def on_page_markdown(self, markdown, **_):
        """Replaces any alias tags on the page with markdown links."""
        return re.sub(
            TAGS_REGEX,
            self.__replace_tag,
            markdown
        )

    def __replace_tag(self, match, **_):
        """Callback used in the sub function within on_page_markdown."""
        alias = self.aliases.get(match.group(1))
        if alias is None:
            self.log.warning("Alias '%s' not found", match.group(1))
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
                source = handle.read()
                _, meta_data = meta.get_data(source)
                if len(meta_data) > 0:
                    existing = self.aliases.get(meta_data['alias']['name'])
                    if existing is not None:
                        self.log.warning(
                            "%s: alias %s already defined in %s, skipping.",
                            file.url,
                            meta_data['alias']['name'],
                            existing['url']
                        )
                        continue

                    new_alias = {
                        'alias': meta_data['alias']['name'],
                        'url': f"/{file.url}",
                        'text': meta_data['alias']['text']
                    }
                    self.log.info(
                        "Alias %s to %s",
                        new_alias['alias'],
                        new_alias['url']
                    )
                    self.aliases[new_alias['alias']] = new_alias
