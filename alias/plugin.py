"""mkdocs-alias-plugin

An MkDocs plugin allowing links to your pages using a custom alias.
"""
from __future__ import annotations

import logging
import re
from typing import Match, TypedDict

from markdown import Markdown
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page
from mkdocs.utils import get_markdown_title, get_relative_url, meta

# The Regular Expression used to find alias tags
# group 1: escape character
# group 2: alias name
# group 3: alias text
ALIAS_TAG_REGEX = r"([\\])?\[\[([^|\]]+)\|?([^\]]+)?\]\]"


class MarkdownAnchor(TypedDict):
    """A single entry in the table of contents. See the following link for more info:
    https://python-markdown.github.io/extensions/toc/#syntax"""
    level: int
    id: str
    name: str
    children: list['MarkdownAnchor']


def get_markdown_toc(markdown_source) -> list[MarkdownAnchor]:
    """Parse the markdown source and return the table of contents tokens."""
    md = Markdown(extensions=['toc'])
    md.convert(markdown_source)
    return getattr(md, 'toc_tokens', [])


def find_anchor_by_id(anchors: list[MarkdownAnchor], anchor_id: str) -> MarkdownAnchor | None:
    """Find an anchor by its ID in a list of anchors returned by get_markdown_toc."""
    for anchor in anchors:
        if anchor['id'] == anchor_id:
            return anchor
        if 'children' in anchor:
            child = find_anchor_by_id(anchor['children'], anchor_id)
            if child is not None:
                return child
    return None


def get_page_title(page_src: str, meta_data: dict):
    """Returns the title of the page. The title in the meta data section
    will take precedence over the H1 markdown title if both are provided."""
    return (
        meta_data['title']
        if 'title' in meta_data and isinstance(meta_data['title'], str)
        else get_markdown_title(page_src)
    )


def get_alias_names(meta_data: dict):
    """Returns the list of configured alias names."""
    if len(meta_data) <= 0 or 'alias' not in meta_data:
        return None
    aliases = meta_data['alias']
    if isinstance(aliases, list):
        # If the alias meta data is a list, ensure that they're strings
        return list(filter(lambda value: isinstance(value, str), aliases))
    if isinstance(aliases, dict) and 'name' in aliases:
        return [aliases['name']]
    if isinstance(aliases, str):
        return [aliases]
    return None


def replace_tag(
    match: Match,
    aliases: dict,
    log: logging.Logger,
    page_file: File,
    use_anchor_titles: bool = False
):
    """Callback used in the sub function within on_page_markdown."""
    if match.group(1) is not None:
        # if the alias match was escaped, return the unescaped version
        return match.group(0)[1:]
    # split the tag up in case there's an anchor in the link
    tag_bits = ['']
    if match.group(2) is not None:
        tag_bits = str(match.group(2)).split('#')
    alias = aliases.get(tag_bits[0])
    if alias is None:
        log.warning(
            "Alias '%s' not found in '%s'",
            match.group(2),
            page_file.src_path
        )
        return match.group(0)  # return the input string

    text = None
    anchor = tag_bits[1] if len(tag_bits) > 1 else None
    # if the use_anchor_titles config option is set, replace the text with the
    # anchor title, but only if the alias tag doesn't have a custom text
    if use_anchor_titles and anchor is not None and match.group(3) is None:
        anchor_tag = find_anchor_by_id(alias['anchors'], anchor)
        if anchor_tag is not None:
            text = anchor_tag['name']
    if text is None:
        # if the alias tag has a custom text, use that instead
        text = alias['text'] if match.group(3) is None else match.group(3)
    # if the alias tag has no text, use the alias URL
    if text is None:
        text = alias['url']

    url = get_relative_url(alias['url'], page_file.src_uri)
    if anchor is not None:
        url = f"{url}#{tag_bits[1]}"

    log.info(
        "replaced alias '%s' with '%s' to '%s'",
        alias['alias'],
        text,
        url
    )
    return f"[{text}]({url})"


class AliasPlugin(BasePlugin):
    """An extension of BasePlugin providing all of the aliasing logic.

    The plugin works by reading all of the markdown files before they are
    processed and parsing their meta sections.

    See on_files() for more info.

    For overridden BasePlugin methods, see the MkDocs source code.
    """
    config_scheme = (
        ('verbose', config_options.Type(bool, default=False)),
        ('use_anchor_titles', config_options.Type(bool, default=False)),
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

    def on_page_markdown(self, markdown: str, *, page: Page, **_):
        """Replaces any alias tags on the page with markdown links."""
        self.current_page = page
        return re.sub(
            ALIAS_TAG_REGEX,
            lambda match: replace_tag(
                match,
                self.aliases,
                self.log,
                self.current_page.file,
                self.config['use_anchor_titles']
            ),
            markdown
        )

    def on_files(self, files: Files, **_):
        """When MkDocs loads its files, extract aliases from any Markdown files
        that were found.
        """
        for file in filter(lambda f: f.is_documentation_page(), files):
            with open(file.abs_src_path, encoding='utf-8-sig', errors='strict') as handle:
                source, meta_data = meta.get_data(handle.read())
                alias_names = get_alias_names(meta_data)
                if alias_names is None or len(alias_names) < 1:
                    continue

                # If the use_anchor_titles config option is set, parse the markdown
                # and get the table of contents for the page
                anchors: list[MarkdownAnchor] = []
                if self.config['use_anchor_titles']:
                    anchors = get_markdown_toc(source)

                if len(alias_names) > 1:
                    self.log.info(
                        '%s defines %d aliases:', file.url, len(alias_names)
                    )
                for alias in alias_names:
                    existing = self.aliases.get(alias)
                    if existing is not None:
                        self.log.warning(
                            "%s: alias %s already defined in %s, skipping.",
                            file.src_uri,
                            alias,
                            existing['url']
                        )
                        continue

                    new_alias = {
                        'alias': alias,
                        'text': (
                            meta_data['alias']['text']
                            # if meta_data['alias'] is a dictionary and 'text' is a key
                            if isinstance(meta_data['alias'], dict) and 'text' in meta_data['alias']
                            else get_page_title(source, meta_data)
                        ),
                        'url': file.src_uri,
                        'anchors': anchors,
                    }
                    self.log.info(
                        "Alias %s to %s",
                        alias,
                        new_alias['url']
                    )
                    self.aliases[alias] = new_alias
