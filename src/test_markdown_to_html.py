import unittest
from textnode import TextNode, TextType
from markdown_to_html import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_blocktype,
    BlockType,
)


class MarkdownParse(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_multiple_delimiters(self):
        node = TextNode("This is **bold** and this is **also bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and this is ", TextType.TEXT),
                TextNode("also bold", TextType.BOLD),
            ],
        )

    def test_split_nodes_delimiter_unmatched(self):
        node = TextNode("This is **bold and this is not closed", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertTrue("umatched delimiter" in str(context.exception))

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This is normal text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is normal text", TextType.TEXT)])

    def test_split_nodes_delimiter_multiple_textnodes(self):
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("Another **bold** word here", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
                TextNode("Another ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word here", TextType.TEXT),
            ],
        )


class MarkdownLinkExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [anchor](https://i.imgur.com)"
        )
        self.assertListEqual([("anchor", "https://i.imgur.com")], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [anchor1](https://i.imgur.com) and another [anchor2](https://example.com)"
        )
        self.assertListEqual(
            [("anchor1", "https://i.imgur.com"), ("anchor2", "https://example.com")],
            matches,
        )


class MarkdownSplitImageNodes(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )


class MarkdownSplitLinkNodes(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [anchor](https://i.imgur.com)", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("anchor", TextType.LINK, "https://i.imgur.com"),
            ],
        )


class TextToTextNode(unittest.TestCase):
    def test_text_to_textnodes_plain(self):
        text = "This is plain text without any markup."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [TextNode("This is plain text without any markup.", TextType.TEXT)],
        )

    def test_text_to_textnodes_with_image_and_link(self):
        text = "Here is an image ![alt text](http://image.url) and a link [click here](http://link.url)."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Here is an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "http://image.url"),
                TextNode(" and a link ", TextType.TEXT),
                TextNode("click here", TextType.LINK, "http://link.url"),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_with_delimiters(self):
        text = "This is **bold** text and this is _italic_ text."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text and this is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text.", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_combined(self):
        text = "Here is **bold** text, an image ![alt](http://img.url), and a link [here](http://link.url)."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text, an image ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "http://img.url"),
                TextNode(", and a link ", TextType.TEXT),
                TextNode("here", TextType.LINK, "http://link.url"),
                TextNode(".", TextType.TEXT),
            ],
        )


class MarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_paragraph(self):
        md = "This is a single paragraph without any line breaks."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, ["This is a single paragraph without any line breaks."]
        )

    def test_markdown_to_blocks_multiple_paragraphs(self):
        md = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, ["First paragraph.", "Second paragraph.", "Third paragraph."]
        )

    def test_markdown_to_blocks_with_list(self):
        md = "Here is a list:\n\n- Item 1\n- Item 2\n- Item 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Here is a list:", "- Item 1\n- Item 2\n- Item 3"])


class BlockToBlocktype(unittest.TestCase):
    def test_block_to_blocktype_paragraph(self):
        block = "This is a simple paragraph."
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_blocktype_heading(self):
        block = "# This is a heading"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_code(self):
        block = "```\nprint('Hello, world!')\n```"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_blocktype_quote(self):
        block = "> This is a blockquote."
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_blocktype_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()
