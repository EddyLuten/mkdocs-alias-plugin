"""mkdocs-alias-plugin tests

Various unit tests for the non-mkdocs functions in plugin.py.
"""
import logging
import re

from mkdocs.structure.files import File
from alias.plugin import get_alias_names, get_page_title, replace_tag, ALIAS_TAG_REGEX

PAGE_FILE = File("/folder1/folder4/folder5/test.md", "/src/", "/dest/", False)


def test_get_page_title_1():
    """Test title from H1 tag extraction"""
    source = "# The actual title\n\nSome body text"
    meta = {}
    assert get_page_title(source, meta) == 'The actual title'


def test_get_page_title_2():
    """Test title from meta block extraction"""
    source = "# NOT The actual title\n\nSome body text"
    meta = {'title': 'The actual title'}
    assert get_page_title(source, meta) == 'The actual title'


def test_get_page_title_3():
    """Test page without a title"""
    source = "Some body text"
    meta = {}
    assert get_page_title(source, meta) is None


def test_get_page_title_4():
    """Test page with both meta and H1 titles"""
    source = "# Not the title\n\nsome text\n"
    meta = {'title': 'The actual title'}
    assert get_page_title(source, meta) == 'The actual title'


def test_get_page_title_5():
    """Test page with both meta title and icon enabled"""
    source = "# Not the title\n\nsome text\n"
    meta = {'title': 'The actual title', 'icon': 'path/to/my-icon'}
    assert get_page_title(source, meta, include_icon=True) == ':path-to-my-icon: The actual title'


def test_get_page_title_6():
    """Test page with both meta title and icon but disabled"""
    source = "# Not the title\n\nsome text\n"
    meta = {'title': 'The actual title', 'icon': 'path/to/my-icon'}
    assert get_page_title(source, meta, include_icon=False) == 'The actual title'


def test_get_alias_name_1():
    """Test alias from meta extraction"""
    meta = {'alias': 'my-alias'}
    assert get_alias_names(meta) == ['my-alias']


def test_get_alias_name_2():
    """Test alias from empty meta extraction"""
    meta = {}
    assert get_alias_names(meta) is None


def test_get_alias_name_3():
    """Test alias from name/title pair"""
    meta = {'alias': {'name': 'my-alias', 'title': 'My Title'}}
    assert get_alias_names(meta) == ['my-alias']


def test_get_alias_name_4():
    """Test aliases from array"""
    meta = {'alias': ['my-alias', 'my-other-alias', 'foobar']}
    assert get_alias_names(meta) == ['my-alias', 'my-other-alias', 'foobar']


def test_get_alias_name_5():
    """Test aliases from array with non-string entries"""
    meta = {'alias': ['my-alias', 1, False, None, 4.821]}
    assert get_alias_names(meta) == ['my-alias']


def test_get_multiple_aliases():
    """Allow for the use of multiple aliases"""
    meta = {'alias': ['my-alias', 'ma', 'myalias']}
    assert get_alias_names(meta) == ['my-alias', 'ma', 'myalias']


def test_replace_tag_1():
    """Should match a simple alias tag"""
    logger = logging.getLogger()
    aliases = {'my-alias': {
        'text': 'link text',
        'alias': 'my-alias',
        'url': 'my-alias.md'
    }}
    markdown = 'Test: [[my-alias]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE),
        markdown
    )
    assert result == 'Test: [link text](../../../my-alias.md)'


def test_replace_tag_2():
    """Should replace an alias with a specified title"""
    logger = logging.getLogger()
    aliases = {'my-alias': {
        'text': 'link text',
        'alias': 'my-alias',
        'url': 'my-alias.md'
    }}
    markdown = 'Test: [[my-alias|Alternate Text]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE),
        markdown
    )
    assert result == 'Test: [Alternate Text](../../../my-alias.md)'


def test_replace_tag_3():
    """Should not replace an escaped alias"""
    logger = logging.getLogger()
    aliases = {'my-alias': {
        'text': 'link text',
        'alias': 'my-alias',
        'url': 'my-alias.md'
    }}
    markdown = 'Test: \\[[my-alias|Alternate Text]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE),
        markdown
    )
    assert result == 'Test: [[my-alias|Alternate Text]]'


def test_replace_tag_4():
    """Should not parse an escaped alias"""
    logger = logging.getLogger()
    aliases = {'my-alias': {
        'text': 'link text',
        'alias': 'my-alias',
        'url': 'my-alias.md'
    }}
    markdown = '\\[[ ! -d $HOME/myfolder ]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE),
        markdown
    )
    assert result == '[[ ! -d $HOME/myfolder ]]'


def test_replace_tag_5():
    """Should return the original string if the alias wasn't found"""
    logger = logging.getLogger()
    aliases = {'my-alias': {
        'text': 'link text',
        'alias': 'my-alias',
        'url': 'my-alias.md'
    }}
    markdown = 'Test: [[unknown]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE),
        markdown
    )
    assert result == markdown


def test_replace_tag_6():
    """Should use the URL as text if the text wasn't set"""
    logger = logging.getLogger()
    aliases = {'my-alias': {
        'text': None,
        'alias': 'my-alias',
        'url': 'my-alias.md'
    }}
    markdown = 'Test: [[my-alias]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE),
        markdown
    )
    assert result == 'Test: [my-alias.md](../../../my-alias.md)'


def test_replace_tag_7():
    """Should handle aliases with spaces"""
    logger = logging.getLogger()
    aliases = {' my spacey alias ': {
        'text': 'The Text',
        'alias': ' my spacey alias ',
        'url': 'my-alias.md'
    }}
    markdown = 'Test: [[ my spacey alias ]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE),
        markdown
    )
    assert result == 'Test: [The Text](../../../my-alias.md)'


def test_replace_tag_with_anchor():
    """Should handle aliases with URL anchors"""
    logger = logging.getLogger()
    aliases = {'my alias': {
        'text': 'The Text',
        'alias': 'my alias',
        'url': 'my-alias.md'
    }}
    markdown = 'Test: [[my alias#anchor]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE),
        markdown
    )
    assert result == 'Test: [The Text](../../../my-alias.md#anchor)'


def test_replace_tag_with_anchor2():
    """Should handle aliases with multiple URL anchors"""
    logger = logging.getLogger()
    aliases = {'my alias': {
        'text': 'The Text',
        'alias': 'my alias',
        'url': 'my-alias.md'
    }}
    markdown = 'Test: [[my alias#anchor#another ignored anchor]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE),
        markdown
    )
    assert result == 'Test: [The Text](../../../my-alias.md#anchor)'


def test_replace_tag_with_anchor3():
    """Should handle aliases with an anchor and a title"""
    logger = logging.getLogger()
    aliases = {'my alias': {
        'text': 'The Text',
        'alias': 'my alias',
        'url': 'my-alias.md'
    }}
    markdown = 'Test: [[my alias#my anchor|The Title]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE),
        markdown
    )
    assert result == 'Test: [The Title](../../../my-alias.md#my anchor)'


def test_plugin_shouldnt_break_with_text():
    """An alias with the word 'text' in it shouldn't break the plugin"""
    logger = logging.getLogger()
    aliases = {'text': {
        'text': 'The Text',
        'alias': 'text',
        'url': 'my-alias.md'
    }}
    markdown = 'Test: [[text]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE),
        markdown
    )
    assert result == 'Test: [The Text](../../../my-alias.md)'


def test_plugin_should_replace_anchors_with_titles():
    """An alias with an anchor should be replaced with the title if the
    config option is set"""
    logger = logging.getLogger()
    aliases = {'my alias': {
        'text': 'The Text',
        'alias': 'my alias',
        'url': 'my-alias.md',
        'anchors': [{
            'id': 'anchor',
            'name': 'The Anchor'
        }]
    }}
    markdown = 'Test: [[my alias#anchor]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE, True),
        markdown
    )
    assert result == 'Test: [The Anchor](../../../my-alias.md#anchor)'


def test_plugin_should_note_replace_anchors_with_titles():
    """An alias with an anchor should be NOT replaced with the title if the
    config option is not set"""
    logger = logging.getLogger()
    aliases = {'my alias': {
        'text': 'The Text',
        'alias': 'my alias',
        'url': 'my-alias.md',
        'anchors': [{
            'id': 'anchor',
            'name': 'The Anchor'
        }]
    }}
    markdown = 'Test: [[my alias#anchor]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE, False),
        markdown
    )
    assert result == 'Test: [The Text](../../../my-alias.md#anchor)'


def test_plugin_should_replace_anchors_with_nesting():
    """An alias with an anchor should be replaced with the title if the
    config option is set with the appropriate nested child anchor"""
    logger = logging.getLogger()
    aliases = {'my alias': {
        'text': 'The Text',
        'alias': 'my alias',
        'url': 'my-alias.md',
        'anchors': [{
            'id': 'anchor',
            'name': 'The Anchor',
            'children': [{
                'id': 'nested',
                'name': 'The Nested Anchor'
            }]
        }]
    }}
    markdown = 'Test: [[my alias#nested]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE, True),
        markdown
    )
    assert result == 'Test: [The Nested Anchor](../../../my-alias.md#nested)'


def test_plugin_should_function_as_usual_without_anchors():
    """An alias with an anchor, with the config option set to true, but no
    anchors should still function as usual"""
    logger = logging.getLogger()
    aliases = {'my alias': {
        'text': 'The Text',
        'alias': 'my alias',
        'url': 'my-alias.md',
        'anchors': []
    }}
    markdown = 'Test: [[my alias#anchor]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE, True),
        markdown
    )
    assert result == 'Test: [The Text](../../../my-alias.md#anchor)'


def test_plugin_should_use_custom_title_with_anchor_titles():
    """An alias with an anchor, with the config option set to true, with
    anchors, but with a custom title should use the custom title"""
    logger = logging.getLogger()
    aliases = {'my alias': {
        'text': 'The Text',
        'alias': 'my alias',
        'url': 'my-alias.md',
        'anchors': [{
            'id': 'anchor',
            'name': 'The Anchor',
            'children': [{
                'id': 'nested',
                'name': 'The Nested Anchor'
            }]
        }]
    }}
    markdown = 'Test: [[my alias#nested|Custom Title]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, PAGE_FILE, True),
        markdown
    )
    assert result == 'Test: [Custom Title](../../../my-alias.md#nested)'


def test_plugin_should_link_to_anchor_on_current_page():
    """An alias with an anchor on the current page should link to it
    without the page path"""
    logger = logging.getLogger()
    page_file = File(
        'foo/bar.md',
        src_dir=None,
        dest_dir='/path/to/site',
        use_directory_urls=False,
    )
    page_file.content_string = 'Test: [[#anchor]]\n\n## Anchor\n\nSome text'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, {}, logger, page_file),
        page_file.content_string
    )
    assert result == 'Test: [Anchor](#anchor)\n\n## Anchor\n\nSome text'


def test_get_alias_names_1():
    """Test alias from meta extraction"""
    meta = {'alias': 'my-alias'}
    assert get_alias_names(meta) == ['my-alias']


def test_get_alias_names_2():
    """Test alias from empty meta extraction"""
    meta = {}
    assert get_alias_names(meta) is None


def test_get_alias_names_3():
    """Test alias from meta extraction using a custom key"""
    meta = {'custom-key': 'my-alias'}
    assert get_alias_names(meta, 'custom-key') == ['my-alias']


def test_get_alias_names_4():
    """Test alias from name/title pair"""
    meta = {'alias': {'name': 'my-alias', 'title': 'My Title'}}
    assert get_alias_names(meta, 'alias') == ['my-alias']
