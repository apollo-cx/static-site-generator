import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("b", "child1")
        child_node2 = LeafNode("b", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><b>child1</b><b>child2</b></div>")

    def test_to_html_with_children_and_grandchildren(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "div1.0", [LeafNode("b", "ggch1.1"), LeafNode("b", "ggch1.2")]
                ),
                LeafNode("i", "ch0.1"),
                ParentNode("div2.0", [LeafNode("b", "ggch2.1")]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><div1.0><b>ggch1.1</b><b>ggch1.2</b></div1.0><i>ch0.1</i><div2.0><b>ggch2.1</b></div2.0></div>",
        )


if __name__ == "__main__":
    unittest.main()
