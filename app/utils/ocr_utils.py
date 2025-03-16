# OCR processing utilities
import pytesseract
from PIL import Image

def extract_text_from_image(image_path: str, tesseract_path: str = "") -> str:
    """Extract text from an image using Tesseract OCR."""
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    try:
        img = Image.open(image_path)
        return pytesseract.image_to_string(img)
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""