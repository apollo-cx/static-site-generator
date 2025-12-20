from calendar import c
from enum import Enum
from pydoc import text
import re
from typing import Counter
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode


class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered List"
    ORDERED_LIST = "Ordered List"


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

        for i, part in enumerate(parts):
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

    for i, block in enumerate(blocks):
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

def block_to_children(block):
    blocktype = block_to_blocktype(block)

    match blocktype:
        case BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            text_nodes = text_to_textnodes(text)
            parent_node = ParentNode("p", [text_node_to_html_node(node) for node in text_nodes])
            return parent_node
        
        case BlockType.HEADING:
            level = len(re.match(r"^(#+) ", block).group(1))
            text = block[level + 1:]
            text_nodes = text_to_textnodes(text)
            parent_node = ParentNode(f"h{level}", [text_node_to_html_node(node) for node in text_nodes])
            return parent_node
               
        case BlockType.CODE:
            code_content = block[3:-3]
            if '\n' in code_content and not code_content.endswith('\n'):
                code_content += '\n'
            node = TextNode(code_content, TextType.CODE)
            leaf_node = text_node_to_html_node(node)
            parent_node = ParentNode("pre", [leaf_node])
            return parent_node
        
        case BlockType.QUOTE:
            lines = block.split("\n")
            child_nodes = []
            full_text = ""
            for line in lines:
                text = line[1:].strip()
                full_text += text + "\n"
            full_text = full_text.strip()
            text_nodes = text_to_textnodes(full_text)
            parent_node = ParentNode("blockquote", [text_node_to_html_node(node) for node in text_nodes])
            return parent_node
        
        case BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            child_nodes = []
            for line in lines:
                text = line[2:].strip()
                text_nodes = text_to_textnodes(text)
                list_item_node = ParentNode("li", [text_node_to_html_node(node) for node in text_nodes])
                child_nodes.append(list_item_node)
            parent_node = ParentNode("ul", child_nodes)
            return parent_node 
        
        case BlockType.ORDERED_LIST:
            lines = block.split("\n")
            child_nodes = []
            for line in lines:
                match = re.match(r"^\d+\. (.+)", line)
                if not match:
                    raise ValueError("invalid ordered list item")
                text = match.group(1).strip()
                text_nodes = text_to_textnodes(text)
                list_item_node = ParentNode("li", [text_node_to_html_node(node) for node in text_nodes])
                child_nodes.append(list_item_node)
            parent_node = ParentNode("ol", child_nodes)
            return parent_node
        
        case _:
            raise ValueError("unknown block type")
            

def markdown_to_html_node(markdown):
    html = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        child_nodes = block_to_children(block)
        html.append(child_nodes)
    
    parent_node = ParentNode("div", html)
    
    return parent_node
