"""mkdocs-alias-plugin tests

Various unit tests for the non-mkdocs functions in plugin.py.
"""
from alias.plugin import get_alias_names, get_page_title

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
