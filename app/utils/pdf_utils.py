# PDF manipulation utilities
import fitz

def add_bookmarks_to_pdf(pdf_path: str, toc: list, output_path: str) -> bool:
    """Add bookmarks to a PDF."""
    try:
        doc = fitz.open(pdf_path)
        doc.set_toc(toc)
        doc.save(output_path)
        return True
    except Exception as e:
        print(f"PDF Error: {e}")
        return False