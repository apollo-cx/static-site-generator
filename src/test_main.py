from unittest import TestCase
from main import extract_title

class TestExtractTitle(TestCase):
    def test_extract_title_with_title(self):
        markdown = "# My Title\n\nSome content here."
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")

    def test_extract_title_without_title(self):
        markdown = "No title here.\nJust some content."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found in markdown")

class TestGeneratePage(TestCase):
    def test_generate_page_creates_file(self):
        from tempfile import NamedTemporaryFile
        import os

        markdown_content = "# Test Page\n\nThis is a test."
        template_content = "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"

        with NamedTemporaryFile(delete=False, mode='w', suffix='.md') as md_file:
            md_file.write(markdown_content)
            md_path = md_file.name

        with NamedTemporaryFile(delete=False, mode='w', suffix='.html') as tmp_file:
            tmp_file.write(template_content)
            tmp_path = tmp_file.name

        dest_path = md_path + "_output.html"

        try:
            from main import generate_page
            generate_page(md_path, tmp_path, dest_path)

            self.assertTrue(os.path.exists(dest_path))

            with open(dest_path, 'r') as output_file:
                output_content = output_file.read()
                self.assertIn("<title>Test Page</title>", output_content)
                self.assertIn("<p>This is a test.</p>", output_content)
        finally:
            os.remove(md_path)
            os.remove(tmp_path)
            if os.path.exists(dest_path):
                os.remove(dest_path)
