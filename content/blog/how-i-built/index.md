# How I Built This Website

[< Back Home](../..)

This post documents how the static site generator works and how this site is built and deployed.

## Overview

- Content is written in Markdown under content/
- A simple Python generator converts Markdown to HTML using a template
- Static assets (CSS, images) are copied from static/ to the output
- The final site is emitted to docs/ for GitHub Pages

## Content structure

- Home page: content/index.md
- Contact page: content/contact/index.md
- Blog index: content/blog/index.md
- Individual posts: content/blog/<post-slug>/index.md

Each page starts with a title line using a single leading hash (#), for example:

```text
# My Page Title
Page content in Markdown.
```

## Generator flow

The generator runs from src/main.py and performs these steps:

1. Copy static assets from static/ to the output (docs/)
2. Walk the content/ directory recursively
3. For each .md file:
  - Read the file and extract the title from the first "# " heading
  - Convert Markdown to HTML using the Markdown parser
  - Load template.html and replace the placeholders for Title and Content
  - Rewrite absolute asset and link paths using a configurable basepath:

```text
href="/  →  href="{basepath}
src="/   →  src="{basepath}
```

  - Write the resulting HTML into the mirrored path under docs/

## Local development

- Default basepath is "/", suitable for local serving
- Build locally:

```bash
python3 src/main.py
python3 -m http.server 8888 -d docs
# Open http://localhost:8888/
```

## Production build (GitHub Pages)

- The build.sh script runs:

```bash
python3 src/main.py "/static-site-generator/"
```

- Push the generated docs/ to the main branch
- Configure GitHub Pages: Source = main, Folder = /docs
- Live URL: https://USERNAME.github.io/static-site-generator/

## Adding a new blog post

1. Create a new folder: content/blog/my-first-post/
2. Add index.md with a # title and Markdown content
3. Link it from content/blog/index.md
4. Rebuild and push

That’s it — a fast, minimal workflow focused on content.
