"""mkdocs-alias-plugin tests

Various unit tests for the non-mkdocs functions in plugin.py.
"""
import logging
import re
from alias.plugin import get_alias_names, get_page_title, replace_tag, ALIAS_TAG_REGEX

def test_get_page_title_1():
    """Test title from H1 tag extraction"""
    source = "# The actual title\n\nSome body text"
    meta = {}
    assert get_page_title(source, meta) == 'The actual title'

def test_get_page_title_2():
    """Test title from meta block extraction"""
    source = "# NOT The actual title\n\nSome body text"
    meta = { 'title': 'The actual title' }
    assert get_page_title(source, meta) == 'The actual title'

def test_get_page_title_3():
    """Test page without a title"""
    source = "Some body text"
    meta = {}
    assert get_page_title(source, meta) is None

def test_get_page_title_4():
    """Test page with both meta and H1 titles"""
    source = "# Not the title\n\nsome text\n"
    meta = { 'title': 'The actual title' }
    assert get_page_title(source, meta) == 'The actual title'

def test_get_alias_name_1():
    """Test alias from meta extraction"""
    meta = { 'alias': 'my-alias' }
    assert get_alias_names(meta) == ['my-alias']

def test_get_alias_name_2():
    """Test alias from empty meta extraction"""
    meta = { }
    assert get_alias_names(meta) is None

def test_get_alias_name_3():
    """Test alias from name/title pair"""
    meta = { 'alias': { 'name': 'my-alias', 'title': 'My Title' } }
    assert get_alias_names(meta) == ['my-alias']

def test_get_alias_name_4():
    """Test aliases from array"""
    meta = { 'alias': [ 'my-alias', 'my-other-alias', 'foobar' ] }
    assert get_alias_names(meta) == [ 'my-alias', 'my-other-alias', 'foobar' ]

def test_get_alias_name_5():
    """Test aliases from array with non-string entries"""
    meta = { 'alias': [ 'my-alias', 1, False, None, 4.821 ] }
    assert get_alias_names(meta) == [ 'my-alias' ]

def test_get_multiple_aliases():
    """Allow for the use of multiple aliases"""
    meta = { 'alias': [ 'my-alias', 'ma', 'myalias' ] }
    assert get_alias_names(meta) == [ 'my-alias', 'ma', 'myalias' ]

def test_replace_tag_1():
    """Should match a simple alias tag"""
    logger = logging.getLogger()
    aliases = { 'my-alias': {
        'text': 'link text',
        'alias': 'my-alias',
        'url': 'my-alias.md',
        'link': 'my-alias.md',
    } }
    markdown = 'Test: [[my-alias]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, 'test.md'),
        markdown
    )
    assert result == 'Test: [link text](my-alias.md)'

def test_replace_tag_2():
    """Should replace an alias with a specified title"""
    logger = logging.getLogger()
    aliases = { 'my-alias': {
        'text': 'link text',
        'alias': 'my-alias',
        'url': 'my-alias.md',
        'link': 'my-alias.md',
    } }
    markdown = 'Test: [[my-alias|Alternate Text]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, 'test.md'),
        markdown
    )
    assert result == 'Test: [Alternate Text](my-alias.md)'

def test_replace_tag_3():
    """Should not replace an escaped alias"""
    logger = logging.getLogger()
    aliases = { 'my-alias': {
        'text': 'link text',
        'alias': 'my-alias',
        'url': 'my-alias.md',
        'link': 'my-alias.md',
    } }
    markdown = 'Test: \\[[my-alias|Alternate Text]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, 'test.md'),
        markdown
    )
    assert result == 'Test: [[my-alias|Alternate Text]]'

def test_replace_tag_4():
    """Should not parse an escaped alias"""
    logger = logging.getLogger()
    aliases = { 'my-alias': {
        'text': 'link text',
        'alias': 'my-alias',
        'url': 'my-alias.md',
        'link': 'my-alias.md',
    } }
    markdown = '\\[[ ! -d $HOME/myfolder ]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, 'test.md'),
        markdown
    )
    assert result == '[[ ! -d $HOME/myfolder ]]'

def test_replace_tag_5():
    """Should return the original string if the alias wasn't found"""
    logger = logging.getLogger()
    aliases = { 'my-alias': {
        'text': 'link text',
        'alias': 'my-alias',
        'url': 'my-alias.md',
        'link': 'my-alias.md',
    } }
    markdown = 'Test: [[unknown]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, 'test.md'),
        markdown
    )
    assert result == markdown

def test_replace_tag_6():
    """Should use the URL as text if the text wasn't set"""
    logger = logging.getLogger()
    aliases = { 'my-alias': {
        'text': None,
        'alias': 'my-alias',
        'url': 'my-alias.md',
        'link': 'my-alias.md',
    } }
    markdown = 'Test: [[my-alias]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, 'test.md'),
        markdown
    )
    assert result == 'Test: [my-alias.md](my-alias.md)'

def test_replace_tag_7():
    """Should handle aliases with spaces"""
    logger = logging.getLogger()
    aliases = { ' my spacey alias ': {
        'text': 'The Text',
        'alias': ' my spacey alias ',
        'url': 'my-alias.md',
        'link': 'my-alias.md',
    } }
    markdown = 'Test: [[ my spacey alias ]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, 'test.md'),
        markdown
    )
    assert result == 'Test: [The Text](my-alias.md)'

def test_replace_tag_with_relative_link():
    """Assert that alias 'link' key is used for link definition"""
    logger = logging.getLogger()
    aliases = { ' my spacey alias ': {
        'text': 'The Text',
        'alias': ' my spacey alias ',
        'url': 'my-alias.md',
        'link': 'my_custom_link',
    } }
    markdown = 'Test: [[ my spacey alias ]]'
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, aliases, logger, 'test.md'),
        markdown
    )
    assert result == 'Test: [The Text](my_custom_link)'
