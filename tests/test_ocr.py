# OCR functionality tests
import unittest
from app.utils.ocr_utils import extract_text_from_image

class TestOCR(unittest.TestCase):
    def test_extract_text(self):
        text = extract_text_from_image("test_image.png")
        self.assertIsInstance(text, str)