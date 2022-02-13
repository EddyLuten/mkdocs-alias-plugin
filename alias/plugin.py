import logging
import re
from tokenize import group
from mkdocs.plugins import BasePlugin
from mkdocs.utils import meta
from mkdocs.config import config_options

log = logging.getLogger(f'mkdocs.plugins.{__name__}')
tags_regex = r"\[\[([^|^\]]+)\|?([^\]]+)?\]\]"

class AliasPlugin(BasePlugin):
    config_scheme = (
        ('verbose', config_options.Type(bool, default=False)),
    )
    aliases = dict()

    def on_post_build(self, **_):
        self.__verbose_info(f"Defined {len(self.aliases)} alias(es).")
        self.aliases.clear()

    def on_page_markdown(self, markdown, **_):
        return re.sub(
            tags_regex,
            lambda m: self.__replace_tag(m),
            markdown
        )

    def __verbose_info(self, message):
        if self.config['verbose']:
            log.info(message)

    def __replace_tag(self, match, **_):
        alias = self.aliases.get(match.group(1))
        if alias is None:
            log.warn(f"Alias '{match.group(1)}' not found")
            return match.group(0) # return the input string

        text = alias['text'] if match.group(2) is None else match.group(2)
        if text is None:
            text = alias['url']
        self.__verbose_info(
            f"replaced alias '{alias['alias']}' with '{text}' to '{alias['url']}'"
        )
        return f"[{text}]({alias['url']})"

    def on_files(self, files, **_):
        for file in filter(lambda f: f.is_documentation_page(), files):
            with open(file.abs_src_path, encoding='utf-8-sig', errors='strict') as f:
                source = f.read()
                _, meta_data = meta.get_data(source)
                if len(meta_data) > 0:
                    existing = self.aliases.get(meta_data['alias']['name'])
                    if existing != None:
                        log.warn(
                            f"{file.url}: alias {meta_data['alias']['name']} already defined in {existing['url']}, skipping."
                        )
                        continue

                    new_alias = {
                        'alias': meta_data['alias']['name'],
                        'url': f"/{file.url}",
                        'text': meta_data['alias']['text']
                    }
                    self.__verbose_info(
                        f"Alias {new_alias['alias']} to {new_alias['url']}"
                    )
                    self.aliases[new_alias['alias']] = new_alias
