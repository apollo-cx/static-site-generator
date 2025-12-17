import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            props={"href": "http://hello.com", "target": "_blank"}
        ).props_to_html()
        expected_result = ' href="http://hello.com" target="_blank"'
        self.assertEqual(node, expected_result)

    def test_props_to_html_fail(self):
        node = HTMLNode().props_to_html()
        expected_result = ""
        self.assertEqual(node, expected_result)

    def test_repr(self):
        node = HTMLNode("a", "hello world")
        expected_result = "HTMLNode(a, hello world, None, None)"
        self.assertEqual(repr(node), expected_result)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!", props={"class": "title"})
        self.assertEqual(node.to_html(), '<h1 class="title">Hello, world!</h1>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()
