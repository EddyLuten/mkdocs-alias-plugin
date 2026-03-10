"""mkdocs-alias-plugin tests

Various unit tests for the non-mkdocs functions in plugin.py.
"""

import logging
import re

from mkdocs.structure.files import File

from alias.plugin import (
    ALIAS_TAG_REGEX,
    REFERENCE_REGEX,
    get_alias_names,
    get_page_title,
    replace_reference,
    replace_tag,
    ReplaceTagContext,
    split_anchor,
    find_anchor_by_id,
)

PAGE_FILE = File("/folder1/folder4/folder5/test.md", "/src/", "/dest/", False)


def test_split_anchor():
    """Test splitting an alias tag into the alias and anchor parts"""
    assert split_anchor("my-alias#anchor") == ("my-alias", "anchor")
    assert split_anchor("my-alias#anchor#another") == ("my-alias", "anchor")
    assert split_anchor("my-alias") == ("my-alias", None)
    assert split_anchor("#anchor") == (None, "anchor")
    assert split_anchor("#anchor#another") == (None, "anchor")
    assert split_anchor("") == ('', None)


def test_find_anchor_by_id():
    """Test finding an anchor by its ID in a list of anchors"""
    anchors = [
        {"id": "anchor1", "name": "Anchor 1"},
        {"id": "anchor2", "name": "Anchor 2"},
        {"id": "anchor3", "name": "Anchor 3"},
        {"id": "anchor4", "name": "Anchor 4", "children": [
            {"id": "nested1", "name": "Nested Anchor 1"},
            {"id": "nested2", "name": "Nested Anchor 2"},
        ]},
    ]
    assert find_anchor_by_id(anchors, "anchor1") == anchors[0]
    assert find_anchor_by_id(anchors, "anchor2") == anchors[1]
    assert find_anchor_by_id(anchors, "anchor3") == anchors[2]
    assert find_anchor_by_id(anchors, "nested1") == anchors[3]["children"][0]
    assert find_anchor_by_id(anchors, "nested2") == anchors[3]["children"][1]
    assert find_anchor_by_id(anchors, "not-an-anchor") is None


def test_get_page_title_1():
    """Test title from H1 tag extraction"""
    source = "# The actual title\n\nSome body text"
    meta = {}
    assert get_page_title(source, meta) == "The actual title"


def test_get_page_title_2():
    """Test title from meta block extraction"""
    source = "# NOT The actual title\n\nSome body text"
    meta = {"title": "The actual title"}
    assert get_page_title(source, meta) == "The actual title"


def test_get_page_title_3():
    """Test page without a title"""
    source = "Some body text"
    meta = {}
    assert get_page_title(source, meta) is None


def test_get_page_title_4():
    """Test page with both meta and H1 titles"""
    source = "# Not the title\n\nsome text\n"
    meta = {"title": "The actual title"}
    assert get_page_title(source, meta) == "The actual title"


def test_get_page_title_5():
    """Test page with both meta title and icon enabled"""
    source = "# Not the title\n\nsome text\n"
    meta = {"title": "The actual title", "icon": "path/to/my-icon"}
    assert (
        get_page_title(source, meta, include_icon=True)
        == ":path-to-my-icon: The actual title"
    )


def test_get_page_title_6():
    """Test page with both meta title and icon but disabled"""
    source = "# Not the title\n\nsome text\n"
    meta = {"title": "The actual title", "icon": "path/to/my-icon"}
    assert get_page_title(source, meta, include_icon=False) == "The actual title"


def test_get_alias_name_1():
    """Test alias from meta extraction"""
    meta = {"alias": "my-alias"}
    assert get_alias_names(meta) == ["my-alias"]


def test_get_alias_name_2():
    """Test alias from empty meta extraction"""
    meta = {}
    assert get_alias_names(meta) is None


def test_get_alias_name_3():
    """Test alias from name/title pair"""
    meta = {"alias": {"name": "my-alias", "title": "My Title"}}
    assert get_alias_names(meta) == ["my-alias"]


def test_get_alias_name_4():
    """Test aliases from array"""
    meta = {"alias": ["my-alias", "my-other-alias", "foobar"]}
    assert get_alias_names(meta) == ["my-alias", "my-other-alias", "foobar"]


def test_get_alias_name_5():
    """Test aliases from array with non-string entries"""
    meta = {"alias": ["my-alias", 1, False, None, 4.821]}
    assert get_alias_names(meta) == ["my-alias"]


def test_get_multiple_aliases():
    """Allow for the use of multiple aliases"""
    meta = {"alias": ["my-alias", "ma", "myalias"]}
    assert get_alias_names(meta) == ["my-alias", "ma", "myalias"]


def test_replace_tag_1():
    """Should match a simple alias tag"""
    context = ReplaceTagContext(
        aliases={
            "my-alias": {"text": "link text", "alias": "my-alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[my-alias]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [link text](../../../my-alias.md)"


def test_replace_tag_2():
    """Should replace an alias with a specified title"""
    context = ReplaceTagContext(
        aliases = {
            "my-alias": {"text": "link text", "alias": "my-alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[my-alias|Alternate Text]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [Alternate Text](../../../my-alias.md)"


def test_replace_tag_3():
    """Should not replace an escaped alias"""
    context = ReplaceTagContext(
        aliases={
            "my-alias": {"text": "link text", "alias": "my-alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: \\[[my-alias|Alternate Text]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [[my-alias|Alternate Text]]"


def test_replace_tag_4():
    """Should not parse an escaped alias"""
    context = ReplaceTagContext(
        aliases={
            "my-alias": {"text": "link text", "alias": "my-alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "\\[[ ! -d $HOME/myfolder ]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "[[ ! -d $HOME/myfolder ]]"


def test_replace_tag_5():
    """Should return the original string if the alias wasn't found"""
    context = ReplaceTagContext(
        aliases={
            "my-alias": {"text": "link text", "alias": "my-alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[unknown]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == markdown


def test_replace_tag_6():
    """Should use the URL as text if the text wasn't set"""
    context = ReplaceTagContext(
        log=logging.getLogger(),
        aliases={"my-alias": {"text": None, "alias": "my-alias", "url": "my-alias.md"}},
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[my-alias]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [my-alias.md](../../../my-alias.md)"


def test_replace_tag_7():
    """Should handle aliases with spaces"""
    context = ReplaceTagContext(
        aliases={
            " my spacey alias ": {
                "text": "The Text",
                "alias": " my spacey alias ",
                "url": "my-alias.md",
            }
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[ my spacey alias ]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [The Text](../../../my-alias.md)"


def test_replace_tag_with_anchor():
    """Should handle aliases with URL anchors"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {"text": "The Text", "alias": "my alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[my alias#anchor]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [The Text](../../../my-alias.md#anchor)"


def test_replace_tag_with_anchor2():
    """Should handle aliases with multiple URL anchors"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {"text": "The Text", "alias": "my alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[my alias#anchor#another ignored anchor]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [The Text](../../../my-alias.md#anchor)"


def test_replace_tag_with_anchor3():
    """Should handle aliases with an anchor and a title"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {"text": "The Text", "alias": "my alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[my alias#my anchor|The Title]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [The Title](../../../my-alias.md#my anchor)"


def test_replace_tag_shouldnt_break_alias_not_found():
    """An alias that doesn't exist shouldn't break the plugin"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {"text": "The Text", "alias": "my alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[unknown]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == markdown


def test_replace_tag_shouldnt_break_alias_not_found_with_anchor():
    """An alias that doesn't exist shouldn't break the plugin"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {"text": "The Text", "alias": "my alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[unknown#anchor]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == markdown


def test_replace_tag_shouldnt_break_alias_not_found_with_text():
    """An alias that doesn't exist shouldn't break the plugin"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {"text": "The Text", "alias": "my alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[unknown|Some bad reference]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == markdown


def test_replace_tag_shouldnt_break_alias_not_found_with_text_and_anchor():
    """An alias that doesn't exist shouldn't break the plugin"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {"text": "The Text", "alias": "my alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[unknown#anchor|Some bad reference]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == markdown


def test_plugin_shouldnt_break_with_text():
    """An alias with the word 'text' in it shouldn't break the plugin"""
    context = ReplaceTagContext(
        aliases={"text": {"text": "The Text", "alias": "text", "url": "my-alias.md"}},
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[text]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [The Text](../../../my-alias.md)"


def test_plugin_should_replace_anchors_with_titles():
    """An alias with an anchor should be replaced with the title if the
    config option is set"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {
                "text": "The Text",
                "alias": "my alias",
                "url": "my-alias.md",
                "anchors": [{"id": "anchor", "name": "The Anchor"}],
            }
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
        use_anchor_titles=True,
    )
    markdown = "Test: [[my alias#anchor]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [The Anchor](../../../my-alias.md#anchor)"


def test_plugin_should_note_replace_anchors_with_titles():
    """An alias with an anchor should be NOT replaced with the title if the
    config option is not set"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {
                "text": "The Text",
                "alias": "my alias",
                "url": "my-alias.md",
                "anchors": [{"id": "anchor", "name": "The Anchor"}],
            }
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
        use_anchor_titles=False,
    )
    markdown = "Test: [[my alias#anchor]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [The Text](../../../my-alias.md#anchor)"


def test_plugin_should_replace_anchors_with_nesting():
    """An alias with an anchor should be replaced with the title if the
    config option is set with the appropriate nested child anchor"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {
                "text": "The Text",
                "alias": "my alias",
                "url": "my-alias.md",
                "anchors": [
                    {
                        "id": "anchor",
                        "name": "The Anchor",
                        "children": [{"id": "nested", "name": "The Nested Anchor"}],
                    }
                ],
            }
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
        use_anchor_titles=True,
    )
    markdown = "Test: [[my alias#nested]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [The Nested Anchor](../../../my-alias.md#nested)"


def test_plugin_should_function_as_usual_without_anchors():
    """An alias with an anchor, with the config option set to true, but no
    anchors should still function as usual"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {
                "text": "The Text",
                "alias": "my alias",
                "url": "my-alias.md",
                "anchors": [],
            }
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
        use_anchor_titles=True,
    )
    markdown = "Test: [[my alias#anchor]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [The Text](../../../my-alias.md#anchor)"


def test_plugin_should_use_custom_title_with_anchor_titles():
    """An alias with an anchor, with the config option set to true, with
    anchors, but with a custom title should use the custom title"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {
                "text": "The Text",
                "alias": "my alias",
                "url": "my-alias.md",
                "anchors": [
                    {
                        "id": "anchor",
                        "name": "The Anchor",
                        "children": [{"id": "nested", "name": "The Nested Anchor"}],
                    }
                ],
            }
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
        use_anchor_titles=True,
    )
    markdown = "Test: [[my alias#nested|Custom Title]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [Custom Title](../../../my-alias.md#nested)"


def test_plugin_should_link_to_anchor_on_current_page():
    """An alias with an anchor on the current page should link to it
    without the page path"""
    page_file = File(
        "foo/bar.md",
        src_dir=None,
        dest_dir="/path/to/site",
        use_directory_urls=False,
    )
    page_file.content_string = "Test: [[#anchor]]\n\n## Anchor\n\nSome text"
    context = ReplaceTagContext(
        aliases={},
        log=logging.getLogger(),
        page_file=page_file,
    )
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        page_file.content_string,
    )
    assert result == "Test: [Anchor](#anchor)\n\n## Anchor\n\nSome text"


def test_plugin_should_not_break_on_anchor_not_found_on_current_page():
    """An alias that doesn't exist shouldn't break the plugin"""
    page_file = File(
        "foo/bar.md",
        src_dir=None,
        dest_dir="/path/to/site",
        use_directory_urls=False,
    )
    page_file.content_string = "Test: [[#anchor]]\n\n## Anchor\n\nSome text"
    context = ReplaceTagContext(
        aliases={
            "my alias": {"text": "The Text", "alias": "my alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=page_file,
    )
    markdown = "Test: [[#not-anchor]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == markdown


def test_get_alias_names_1():
    """Test alias from meta extraction"""
    meta = {"alias": "my-alias"}
    assert get_alias_names(meta) == ["my-alias"]


def test_get_alias_names_2():
    """Test alias from empty meta extraction"""
    meta = {}
    assert get_alias_names(meta) is None


def test_get_alias_names_3():
    """Test alias from meta extraction using a custom key"""
    meta = {"custom-key": "my-alias"}
    assert get_alias_names(meta, "custom-key") == ["my-alias"]


def test_get_alias_names_4():
    """Test alias from name/title pair"""
    meta = {"alias": {"name": "my-alias", "title": "My Title"}}
    assert get_alias_names(meta, "alias") == ["my-alias"]


def test_replace_reference():
    """reference syntax: basic alias"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {"text": "The Text", "alias": "my alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "[alias]: [[my alias]]"
    result = re.sub(
        REFERENCE_REGEX,
        lambda match: replace_reference(match, context),
        markdown,
    )
    assert result == "[alias]: ../../../my-alias.md"


def test_replace_reference_anchor():
    """reference syntax: alias with anchor"""
    context = ReplaceTagContext(
        aliases={
            "my alias": {"text": "The Text", "alias": "my alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "[alias]: [[my alias#anchor]]"
    result = re.sub(
        REFERENCE_REGEX,
        lambda match: replace_reference(match, context),
        markdown,
    )
    assert result == "[alias]: ../../../my-alias.md#anchor"


def test_accept_escaped_brackets_1():
    """allow escaping square brackets within the alias"""
    context = ReplaceTagContext(
        aliases={
            "my-alias": {"text": "link text", "alias": "my-alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[my-alias|Alternate \\[alt\\] Text]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [Alternate \\[alt\\] Text](../../../my-alias.md)"


def test_dont_accept_unescaped_brackets():
    """don't allow unescaped square brackets within the alias"""
    context = ReplaceTagContext(
        aliases={
            "my-alias": {"text": "link text", "alias": "my-alias", "url": "my-alias.md"}
        },
        log=logging.getLogger(),
        page_file=PAGE_FILE,
    )
    markdown = "Test: [[my-alias|Alternate [alt] Text]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [[my-alias|Alternate [alt] Text]]"


def test_interwiki_alias_basic():
    """Test interwiki alias replacement without a title"""
    context = ReplaceTagContext(
        aliases={},
        log=logging.getLogger(),
        page_file=PAGE_FILE,
        interwiki={"wp": "https://en.wikipedia.org/wiki/{{alias}}"},
    )
    markdown = "Test: [[wp:Python (programming language)]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == (
        "Test: [Python (programming language)]"
        "(https://en.wikipedia.org/wiki/Python%20%28programming%20language%29)"
    )


def test_interwiki_alias_basic_with_anchor():
    """Test interwiki alias replacement without a title with an anchor"""
    context = ReplaceTagContext(
        aliases={},
        log=logging.getLogger(),
        page_file=PAGE_FILE,
        interwiki={"wp": "https://en.wikipedia.org/wiki/{{alias}}"},
    )
    markdown = "Test: [[wp:Python (programming language)#History]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == (
        "Test: [Python (programming language)#History]"
        "(https://en.wikipedia.org/wiki/Python%20%28programming%20language%29%23History)"
    )


def test_interwiki_alias_with_title():
    """Test interwiki alias replacement with a title"""
    context = ReplaceTagContext(
        aliases={},
        log=logging.getLogger(),
        page_file=PAGE_FILE,
        interwiki={"wp": "https://en.wikipedia.org/wiki/{{alias}}"},
    )
    markdown = "Test: [[wp:Python (programming language)|Wikipedia Article]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == (
        "Test: [Wikipedia Article]"
        "(https://en.wikipedia.org/wiki/Python%20%28programming%20language%29)"
    )


def test_interwiki_prefix_not_in_interwiki():
    """Test that an interwiki alias with a prefix not in the interwiki config is not replaced"""
    context = ReplaceTagContext(
        aliases={},
        log=logging.getLogger(),
        page_file=PAGE_FILE,
        interwiki={"wp": "https://en.wikipedia.org/wiki/{{alias}}"},
    )
    markdown = "Test: [[unknown:Python (programming language)]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == "Test: [[unknown:Python (programming language)]]"


def test_interwiki_alias_with_anchor_and_title():
    """Test interwiki alias replacement with an anchor and a title"""
    context = ReplaceTagContext(
        aliases={},
        log=logging.getLogger(),
        page_file=PAGE_FILE,
        interwiki={"wp": "https://en.wikipedia.org/wiki/{{alias}}"},
    )
    markdown = "Test: [[wp:Python (programming language)#History|History]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == (
        "Test: [History]"
        "(https://en.wikipedia.org/wiki/Python%20%28programming%20language%29%23History)"
    )

def test_interwiki_alias_with_multiple_anchors():
    """Test interwiki alias replacement with multiple anchors, only the first
    anchor should be used"""
    context = ReplaceTagContext(
        aliases={},
        log=logging.getLogger(),
        page_file=PAGE_FILE,
        interwiki={"wp": "https://en.wikipedia.org/wiki/{{alias}}"},
    )
    markdown = "Test: [[wp:Python (programming language)#History#Another Anchor|History]]"
    result = re.sub(
        ALIAS_TAG_REGEX,
        lambda match: replace_tag(match, context),
        markdown,
    )
    assert result == (
        "Test: [History]"
        "(https://en.wikipedia.org/wiki/Python%20%28programming%20language%29%23History)"
    )
