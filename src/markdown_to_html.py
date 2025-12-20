from enum import Enum
import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode


class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "UnorderedList"
    ORDERED_LIST = "OrderedList"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        res = []
        parts = node.text.split(f"{delimiter}")

        if len(parts) == 1:
            new_nodes.append(node)
            continue

        if len(parts) % 2 == 0:
            raise Exception("umatched delimiter")

        for i in range(len(parts)):
            part = parts[i]
            if part == "":
                continue
            if i % 2 == 0:
                res.append(TextNode(part, TextType.TEXT))
            else:
                res.append(TextNode(part, text_type))

        new_nodes.extend(res)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matched_images = extract_markdown_images(node.text)

        if not matched_images:
            new_nodes.append(node)
            continue

        res = []
        remaining_text = node.text

        for alt, url in matched_images:
            sections = remaining_text.split(f"![{alt}]({url})", maxsplit=1)
            if sections[0] != "":
                res.append(TextNode(sections[0], TextType.TEXT))
            res.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = sections[1]

        if remaining_text != "":
            res.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(res)
    return new_nodes


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matched_links = extract_markdown_links(node.text)

        if not matched_links:
            new_nodes.append(node)
            continue

        res = []
        remaining_text = node.text

        for anchor, url in matched_links:
            sections = remaining_text.split(f"[{anchor}]({url})", maxsplit=1)
            if sections[0] != "":
                res.append(TextNode(sections[0], TextType.TEXT))
            res.append(TextNode(anchor, TextType.LINK, url))
            remaining_text = sections[1]

        if remaining_text != "":
            res.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(res)
    return new_nodes


def text_to_textnodes(text):
    old_nodes = [TextNode(text, TextType.TEXT)]
    delimiters = {"**": TextType.BOLD, "_": TextType.ITALIC, "`": TextType.CODE}

    for delimiter, text_type in delimiters.items():
        old_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
    old_nodes = split_nodes_image(old_nodes)
    old_nodes = split_nodes_link(old_nodes)
    new_nodes = old_nodes

    return new_nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    for i in range(len(blocks)):
        block = blocks[i]
        block = block.strip()
        if block == "":
            blocks.pop(i)
            continue
        blocks[i] = block

    return blocks


def block_to_blocktype(block):
    lines = block.split("\n")

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    for i, line in enumerate(lines):
        expected_prefix = f"{i + 1}. "
        if not line.startswith(expected_prefix):
            is_ordered_list = False
            break

    if is_ordered_list and len(lines) > 0:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
