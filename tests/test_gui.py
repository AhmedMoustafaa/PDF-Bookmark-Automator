# GUI component tests
import unittest
from app.gui.main_window import PDFBookmarkerApp

class TestGUI(unittest.TestCase):
    def test_window_creation(self):
        app = PDFBookmarkerApp()
        self.assertIsNotNone(app)