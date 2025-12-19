import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("An image", TextType.IMAGE, "http://image.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertIsNone(html_node.value)
        self.assertEqual(
            html_node.props, {"src": "http://image.com/img.png", "alt": "An image"}
        )

    def test_link(self):
        node = TextNode("A link", TextType.LINK, "http://link.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "A link")
        self.assertEqual(html_node.props, {"href": "http://link.com"})


if __name__ == "__main__":
    unittest.main()
