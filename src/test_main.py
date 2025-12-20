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
