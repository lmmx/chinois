"""Test Soup Sieve API."""

import copy
import pickle
import random

import pytest

import chinois as ch

from . import util


class TestSoupSieve(util.TestCase):
    """Test Soup Sieve."""

    def test_select(self):
        """Test select."""

        markup = """
        <!-- before header -->
        <html>
        <head>
        </head>
        <body>
        <!-- comment -->
        <p id="1"><code id="2"></code><img id="3" src="./image.png"/></p>
        <pre id="4"></pre>
        <p><span id="5" class="some-class"></span><span id="some-id"></span></p>
        <pre id="6" class='ignore'>
            <!-- don't ignore -->
        </pre>
        </body>
        </html>
        """

        soup = self.soup(markup, "html.parser")
        ids = []
        for el in ch.select("span[id]", soup):
            ids.append(el.attrs["id"])

        self.assertEqual(sorted(["5", "some-id"]), sorted(ids))

    def test_select_order(self):
        """Test select order."""

        markup = """
        <!-- before header -->
        <html>
        <head>
        </head>
        <body>
        <!-- comment -->
        <p id="1"><code id="2"></code><img id="3" src="./image.png"/></p>
        <pre id="4"></pre>
        <p><span id="5" class="some-class"></span><span id="some-id"></span></p>
        <pre id="6" class='ignore'>
            <!-- don't ignore -->
        </pre>
        </body>
        </html>
        """

        soup = self.soup(markup, "html.parser")
        ids = []
        for el in ch.select("[id]", soup.body):
            ids.append(el.attrs["id"])

        self.assertEqual(["1", "2", "3", "4", "5", "some-id", "6"], ids)

    def test_select_limit(self):
        """Test select limit."""

        markup = """
        <!-- before header -->
        <html>
        <head>
        </head>
        <body>
        <!-- comment -->
        <p id="1"><code id="2"></code><img id="3" src="./image.png"/></p>
        <pre id="4"></pre>
        <p><span id="5" class="some-class"></span><span id="some-id"></span></p>
        <pre id="6" class='ignore'>
            <!-- don't ignore -->
        </pre>
        </body>
        </html>
        """

        soup = self.soup(markup, "html.parser")

        ids = []
        for el in ch.select("span[id]", soup, limit=1):
            ids.append(el.attrs["id"])

        self.assertEqual(sorted(["5"]), sorted(ids))

    def test_select_one(self):
        """Test select one."""

        markup = """
        <!-- before header -->
        <html>
        <head>
        </head>
        <body>
        <!-- comment -->
        <p id="1"><code id="2"></code><img id="3" src="./image.png"/></p>
        <pre id="4"></pre>
        <p><span id="5" class="some-class"></span><span id="some-id"></span></p>
        <pre id="6" class='ignore'>
            <!-- don't ignore -->
        </pre>
        </body>
        </html>
        """

        soup = self.soup(markup, "html.parser")
        self.assertEqual(
            ch.select("span[id]", soup, limit=1)[0].attrs["id"],
            ch.select_one("span[id]", soup).attrs["id"],
        )

    def test_select_one_none(self):
        """Test select one returns none for no match."""

        markup = """
        <!-- before header -->
        <html>
        <head>
        </head>
        <body>
        <!-- comment -->
        <p id="1"><code id="2"></code><img id="3" src="./image.png"/></p>
        <pre id="4"></pre>
        <p><span id="5" class="some-class"></span><span id="some-id"></span></p>
        <pre id="6" class='ignore'>
            <!-- don't ignore -->
        </pre>
        </body>
        </html>
        """

        soup = self.soup(markup, "html.parser")
        self.assertEqual(None, ch.select_one("h1", soup))

    def test_iselect(self):
        """Test select iterator."""

        markup = """
        <!-- before header -->
        <html>
        <head>
        </head>
        <body>
        <!-- comment -->
        <p id="1"><code id="2"></code><img id="3" src="./image.png"/></p>
        <pre id="4"></pre>
        <p><span id="5" class="some-class"></span><span id="some-id"></span></p>
        <pre id="6" class='ignore'>
            <!-- don't ignore -->
        </pre>
        </body>
        </html>
        """

        soup = self.soup(markup, "html.parser")

        ids = []
        for el in ch.iselect("span[id]", soup):
            ids.append(el.attrs["id"])

        self.assertEqual(sorted(["5", "some-id"]), sorted(ids))

    def test_iselect_order(self):
        """Test select iterator order."""

        markup = """
        <!-- before header -->
        <html>
        <head>
        </head>
        <body>
        <!-- comment -->
        <p id="1"><code id="2"></code><img id="3" src="./image.png"/></p>
        <pre id="4"></pre>
        <p><span id="5" class="some-class"></span><span id="some-id"></span></p>
        <pre id="6" class='ignore'>
            <!-- don't ignore -->
        </pre>
        </body>
        </html>
        """

        soup = self.soup(markup, "html.parser")
        ids = []
        for el in ch.iselect("[id]", soup):
            ids.append(el.attrs["id"])

        self.assertEqual(["1", "2", "3", "4", "5", "some-id", "6"], ids)

    def test_match(self):
        """Test matching."""

        markup = """
        <!-- before header -->
        <html>
        <head>
        </head>
        <body>
        <!-- comment -->
        <p id="1"><code id="2"></code><img id="3" src="./image.png"/></p>
        <pre id="4"></pre>
        <p><span id="5" class="some-class"></span><span id="some-id"></span></p>
        <pre id="6" class='ignore'>
            <!-- don't ignore -->
        </pre>
        </body>
        </html>
        """

        soup = self.soup(markup, "html.parser")
        nodes = ch.select("span[id]", soup)
        self.assertTrue(ch.match("span#\\35", nodes[0]))
        self.assertFalse(ch.match("span#\\35", nodes[1]))

    def test_filter_tag(self):
        """Test filter tag."""

        markup = """
        <!-- before header -->
        <html>
        <head>
        </head>
        <body>
        <!-- comment -->
        <p id="1"><code id="2"></code><img id="3" src="./image.png"/></p>
        <pre id="4"></pre>
        <p><span id="5" class="some-class"></span><span id="some-id"></span></p>
        <pre id="6" class='ignore'>
            <!-- don't ignore -->
        </pre>
        </body>
        </html>
        """

        soup = self.soup(markup, "html.parser")
        nodes = ch.filter("pre#\\36", soup.html.body)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].attrs["id"], "6")

    def test_filter_tag_order(self):
        """Test filter tag order."""

        markup = """
        <!-- before header -->
        <html>
        <head>
        </head>
        <body>
        <!-- comment -->
        <p id="1"><code id="2"></code><img id="3" src="./image.png"/></p>
        <pre id="4"></pre>
        <p><span id="5" class="some-class"></span><span id="some-id"></span></p>
        <pre id="6" class='ignore'>
            <!-- don't ignore -->
        </pre>
        </body>
        </html>
        """

        soup = self.soup(markup, "html.parser")
        ids = [tag["id"] for tag in ch.filter("[id]", soup.html.body.p)]
        self.assertEqual(["2", "3"], ids)

    def test_filter_list(self):
        """
        Test filter list.

        Even if a list is created from the content of a tag, as long as the
        content is document nodes, filter will still handle it.  It doesn't have
        to be just tags.
        """

        markup = """
        <!-- before header -->
        <html>
        <head>
        </head>
        <body>
        <!-- comment -->
        <p id="1"><code id="2"></code><img id="3" src="./image.png"/></p>
        <pre id="4"></pre>
        <p><span id="5" class="some-class"></span><span id="some-id"></span></p>
        <pre id="6" class='ignore'>
            <!-- don't ignore -->
        </pre>
        </body>
        </html>
        """

        soup = self.soup(markup, "html.parser")
        nodes = ch.filter("pre#\\36", [el for el in soup.html.body.children])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].attrs["id"], "6")

    def test_closest_match_parent(self):
        """Test match parent closest."""

        markup = """
        <article id="article">
          <div id="div-01">Here is div-01
            <div id="div-02">Here is div-02
              <div id="div-04">Here is div-04</div>
              <div id="div-03">Here is div-03</div>
            </div>
            <div id="div-05">Here is div-05</div>
          </div>
        </article>
        """

        soup = self.soup(markup, "html.parser")
        el = ch.select_one("#div-03", soup)
        self.assertTrue(ch.closest("#div-02", el).attrs["id"] == "div-02")

    def test_closest_match_complex_parent(self):
        """Test closest match complex parent."""

        markup = """
        <article id="article">
          <div id="div-01">Here is div-01
            <div id="div-02">Here is div-02
              <div id="div-04">Here is div-04</div>
              <div id="div-03">Here is div-03</div>
            </div>
            <div id="div-05">Here is div-05</div>
          </div>
        </article>
        """

        soup = self.soup(markup, "html.parser")
        el = ch.select_one("#div-03", soup)
        self.assertTrue(ch.closest("article > div", el).attrs["id"] == "div-01")
        self.assertTrue(ch.closest(":not(div)", el).attrs["id"] == "article")

    def test_closest_match_self(self):
        """Test closest match self."""

        markup = """
        <article id="article">
          <div id="div-01">Here is div-01
            <div id="div-02">Here is div-02
              <div id="div-04">Here is div-04</div>
              <div id="div-03">Here is div-03</div>
            </div>
            <div id="div-05">Here is div-05</div>
          </div>
        </article>
        """

        soup = self.soup(markup, "html.parser")
        el = ch.select_one("#div-03", soup)
        self.assertTrue(ch.closest("div div", el).attrs["id"] == "div-03")

    def test_closest_must_be_parent(self):
        """Test that closest only matches parents or self."""

        markup = """
        <article id="article">
          <div id="div-01">Here is div-01
            <div id="div-02">Here is div-02
              <div id="div-04">Here is div-04</div>
              <div id="div-03">Here is div-03</div>
            </div>
            <div id="div-05">Here is div-05</div>
          </div>
        </article>
        """

        soup = self.soup(markup, "html.parser")
        el = ch.select_one("#div-03", soup)
        self.assertTrue(ch.closest("div #div-05", el) is None)
        self.assertTrue(ch.closest("a", el) is None)

    def test_escape_hyphen(self):
        """Test escape hyphen cases."""

        self.assertEqual(r"\-", ch.escape("-"))
        self.assertEqual(r"--", ch.escape("--"))

    def test_escape_numbers(self):
        """Test escape hyphen cases."""

        self.assertEqual(r"\33 ", ch.escape("3"))
        self.assertEqual(r"-\33 ", ch.escape("-3"))
        self.assertEqual(r"--3", ch.escape("--3"))

    def test_escape_null(self):
        """Test escape null character."""

        self.assertEqual("\ufffdtest", ch.escape("\x00test"))

    def test_escape_ctrl(self):
        """Test escape control character."""

        self.assertEqual(r"\1 test", ch.escape("\x01test"))

    def test_escape_special(self):
        """Test escape special character."""

        self.assertEqual(r"\{\}\[\]\ \(\)", ch.escape("{}[] ()"))

    def test_escape_wide_unicode(self):
        """Test handling of wide Unicode."""

        self.assertEqual("Emoji\\ \U0001F60D", ch.escape("Emoji \U0001F60D"))

    def test_copy_pickle(self):
        """Test copy and pickle."""

        # Test that we can pickle and unpickle
        # We force a pattern that contains all custom types:
        # `Selector`, `NullSelector`, `SelectorTag`, `SelectorAttribute`,
        # `SelectorNth`, `SelectorLang`, `SelectorList`, `Namespaces`,
        # `SelectorContains`, and `CustomSelectors`.
        p1 = ch.compile(
            'p.class#id[id]:nth-child(2):lang(en):focus:-soup-contains("text", "other text")',
            {"html": "http://www.w3.org/TR/html4/"},
            custom={":--header": "h1, h2, h3, h4, h5, h6"},
        )
        sp1 = pickle.dumps(p1)
        pp1 = pickle.loads(sp1)
        self.assertTrue(pp1 == p1)

        # Test that we pull the same one from cache
        p2 = ch.compile(
            'p.class#id[id]:nth-child(2):lang(en):focus:-soup-contains("text", "other text")',
            {"html": "http://www.w3.org/TR/html4/"},
            custom={":--header": "h1, h2, h3, h4, h5, h6"},
        )
        self.assertTrue(p1 is p2)

        # Test that we compile a new one when providing a different flags
        p3 = ch.compile(
            'p.class#id[id]:nth-child(2):lang(en):focus:-soup-contains("text", "other text")',
            {"html": "http://www.w3.org/TR/html4/"},
            custom={":--header": "h1, h2, h3, h4, h5, h6"},
            flags=0x10,
        )
        self.assertTrue(p1 is not p3)
        self.assertTrue(p1 != p3)

        # Test that the copy is equivalent, but not same.
        p4 = copy.copy(p1)
        self.assertTrue(p4 is not p1)
        self.assertTrue(p4 == p1)

        p5 = copy.copy(p3)
        self.assertTrue(p5 is not p3)
        self.assertTrue(p5 == p3)
        self.assertTrue(p5 is not p4)

    def test_cache(self):
        """Test cache."""

        ch.purge()
        self.assertEqual(ch.cp._cached_css_compile.cache_info().currsize, 0)
        for x in range(1000):
            value = f'[value="{str(random.randint(1, 10000))}"]'
            p = ch.compile(value)
            self.assertTrue(p.pattern == value)
            self.assertTrue(ch.cp._cached_css_compile.cache_info().currsize > 0)
        self.assertTrue(ch.cp._cached_css_compile.cache_info().currsize == 500)
        ch.purge()
        self.assertEqual(ch.cp._cached_css_compile.cache_info().currsize, 0)

    def test_recompile(self):
        """If you feed through the same object, it should pass through unless you change parameters."""

        p1 = ch.compile("p[id]")
        p2 = ch.compile(p1)
        self.assertTrue(p1 is p2)

        with pytest.raises(ValueError):
            ch.compile(p1, flags=ch.DEBUG)

        with pytest.raises(ValueError):
            ch.compile(p1, namespaces={"": ""})

        with pytest.raises(ValueError):
            ch.compile(p1, custom={":--header": "h1, h2, h3, h4, h5, h6"})

    def test_immutable_dict_size(self):
        """Test immutable dictionary."""

        idict = ch.ct.ImmutableDict({"a": "b", "c": "d"})
        self.assertEqual(2, len(idict))


class TestInvalid(util.TestCase):
    """Test invalid."""

    def test_immutable_object(self):
        """Test immutable object."""

        obj = ch.ct.Immutable()

        with self.assertRaises(AttributeError):
            obj.member = 3

    def test_immutable_dict_read_only(self):
        """Test immutable dictionary is read only."""

        idict = ch.ct.ImmutableDict({"a": "b", "c": "d"})
        with self.assertRaises(TypeError):
            idict["a"] = "f"

    def test_immutable_dict_hashable_value(self):
        """Test immutable dictionary has a hashable value."""

        with self.assertRaises(TypeError):
            ch.ct.ImmutableDict([[3, {}]])

    def test_immutable_dict_hashable_key(self):
        """Test immutable dictionary has a hashable key."""

        with self.assertRaises(TypeError):
            ch.ct.ImmutableDict([[{}, 3]])

    def test_immutable_dict_hashable_value_dict(self):
        """Test immutable dictionary has a hashable value."""

        with self.assertRaises(TypeError):
            ch.ct.ImmutableDict({3: {}})

    def test_invalid_namespace_type(self):
        """Test invalid namespace type."""

        with self.assertRaises(TypeError):
            ch.ct.Namespaces(((3, 3),))

    def test_invalid_namespace_hashable_value(self):
        """Test namespace has hashable value."""

        with self.assertRaises(TypeError):
            ch.ct.Namespaces({"a": {}})

    def test_invalid_namespace_hashable_key(self):
        """Test namespace key is hashable."""

        with self.assertRaises(TypeError):
            ch.ct.Namespaces({{}: "string"})

    def test_invalid_custom_type(self):
        """Test invalid custom selector type."""

        with self.assertRaises(TypeError):
            ch.ct.CustomSelectors(((3, 3),))

    def test_invalid_custom_hashable_value(self):
        """Test custom selector has hashable value."""

        with self.assertRaises(TypeError):
            ch.ct.CustomSelectors({"a": {}})

    def test_invalid_custom_hashable_key(self):
        """Test custom selector key is hashable."""

        with self.assertRaises(TypeError):
            ch.ct.CustomSelectors({{}: "string"})

    def test_invalid_type_input_match(self):
        """Test bad input into the match API."""

        flags = ch.DEBUG

        with self.assertRaises(TypeError):
            ch.match("div", "not a tag", flags=flags)

    def test_invalid_type_input_select(self):
        """Test bad input into the select API."""

        flags = ch.DEBUG

        with self.assertRaises(TypeError):
            ch.select("div", "not a tag", flags=flags)

    def test_invalid_type_input_filter(self):
        """Test bad input into the filter API."""

        flags = ch.DEBUG

        with self.assertRaises(TypeError):
            ch.filter("div", "not a tag", flags=flags)


class TestSyntaxErrorReporting(util.TestCase):
    """Test reporting of syntax errors."""

    def test_syntax_error_has_text_and_position(self):
        """Test that selector syntax errors contain the position."""

        with self.assertRaises(ch.SelectorSyntaxError) as cm:
            ch.compile("input.field[type=42]")
        e = cm.exception
        self.assertEqual(e.context, "input.field[type=42]\n           ^")
        self.assertEqual(e.line, 1)
        self.assertEqual(e.col, 12)

    def test_syntax_error_with_multiple_lines(self):
        """Test that multiline selector errors have the right position."""

        with self.assertRaises(ch.SelectorSyntaxError) as cm:
            ch.compile("input\n" ".field[type=42]")
        e = cm.exception
        self.assertEqual(e.context, "    input\n--> .field[type=42]\n          ^")
        self.assertEqual(e.line, 2)
        self.assertEqual(e.col, 7)

    def test_syntax_error_on_third_line(self):
        """Test that multiline selector errors have the right position."""

        with self.assertRaises(ch.SelectorSyntaxError) as cm:
            ch.compile("input:is(\n" "  [name=foo]\n" "  [type=42]\n" ")\n")
        e = cm.exception
        self.assertEqual(e.line, 3)
        self.assertEqual(e.col, 3)

    def test_simple_syntax_error(self):
        """Test a simple syntax error (no context)."""

        with self.assertRaises(ch.SelectorSyntaxError) as cm:
            raise ch.SelectorSyntaxError("Syntax Message")

        e = cm.exception
        self.assertEqual(e.context, None)
        self.assertEqual(e.line, None)
        self.assertEqual(e.col, None)
        self.assertEqual(str(e), "Syntax Message")
