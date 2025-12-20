import os
import sys
from tempfile import template
from htmlnode import HTMLNode, ParentNode, LeafNode
from markdown_to_html import markdown_to_html_node
from staticcontent import copy_static_to_public

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in markdown")

def generate_pages(content_path, template_path, dest_path, basepath):
    if os.path.isfile(content_path):
        if content_path.endswith(".md"):
            print(f"Generating page from {content_path} to {dest_path} using {template_path}...")
            
            with open(content_path) as md:
                contents = md.read()
                if not contents:
                    raise ValueError("file empty")
            
            with open(template_path) as tmp:
                template = tmp.read()
                if not template:
                    raise ValueError("file empty")
            
            title = extract_title(contents)
            contents = markdown_to_html_node(contents)

            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", contents.to_html())
            template = template.replace('href="/', f'href="{basepath}')
            template = template.replace('src="/', f'src="{basepath}')

            with open(dest_path, "x") as page:
                page.write(template)
            
            print("Finished generating")
    elif os.path.isdir(content_path):
        for item in os.listdir(content_path):
            item_path = os.path.join(content_path, item)
            
            if os.path.isfile(item_path) and item.endswith(".md"):
                dest_file = item.replace(".md", ".html")
                dest_file_path = os.path.join(dest_path, dest_file)
                generate_pages(item_path, template_path, dest_file_path, basepath)
            elif os.path.isdir(item_path):
                dest_subdir = os.path.join(dest_path, item)
                os.makedirs(dest_subdir, exist_ok=True)
                generate_pages(item_path, template_path, dest_subdir, basepath)
    
def main():
    source_directory = "static"
    destination_directory = "docs"
    content_directory = "content"
    template_path = "template.html"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    copy_static_to_public(source_directory, destination_directory)
    generate_pages(content_directory, template_path, destination_directory, basepath)

if __name__ == "__main__":
    main()