# PDF manipulation tests
import unittest
from app.utils.pdf_utils import add_bookmarks_to_pdf

class TestPDF(unittest.TestCase):
    def test_add_bookmarks(self):
        result = add_bookmarks_to_pdf("test.pdf", [], "output.pdf")
        self.assertTrue(result)