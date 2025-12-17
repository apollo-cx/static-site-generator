import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_text_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("Hello world", TextType.LINK, "http://hello.com")
        node2 = TextNode("Hello world", TextType.LINK, "http://hello.com")
        self.assertEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("Hello world", TextType.LINK, "http://hello.com")
        node2 = TextNode("Hello world", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_text_type_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_type_neq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
