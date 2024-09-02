"""Test quirky behaviors."""

from campbells import CampbellsSoup as CS

from . import util


class TestQuirks(util.TestCase):
    """Test quirky behaviors."""

    def test_quirky_user_attrs(self):
        """Test cases where a user creates weird attributes: nested sequences."""

        html = """
        <div id="test">test</div>
        """

        soup = CS(html, "html.parser")
        soup.div.attrs["user"] = [["a"]]
        print(soup.div.attrs)
        self.assertTrue(soup.select_one("div[user=\"['a']\"]") is not None)
