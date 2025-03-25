# PDF Bookmark Automator [![GitHub Clones](https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count&url=https://gist.githubusercontent.com/AhmedMoustafaa/420bd07b5cc1be6f609b6da9f116a3f3/raw/clone.json&logo=github)](https://github.com/MShawon/github-clone-count-badge)


![Demo](images/tutorial.gif)

Automate PDF bookmark creation using OCR and AI processing. This tool allows you to generate bookmarks for PDFs by processing table of contents (TOC) images or manually inputting JSON data. It supports both text-based and scanned PDFs with OCR functionality.

---

## Features

- **OCR Processing**: Extract text from TOC images using Tesseract OCR.
- **AI-Powered JSON Generation**: Use OpenAI's GPT to refine OCR output into structured JSON.
- **Manual JSON Input**: Load or paste JSON data for bookmark creation.
- **Scanned PDF Support**: Enable OCR for scanned PDFs to locate bookmark positions accurately.
- **Page Offset Adjustment**: Adjust page numbers to match the PDF's actual content.
- **Modern GUI**: Built with CustomTkinter for a sleek and user-friendly interface.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

---

## Installation

### Prerequisites

1. **Python 3.8+**: Ensure Python is installed on your system.
2. **Tesseract OCR**: Install Tesseract from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/AhmedMoustafaa/PDF-Bookmark-Automator.git
   cd PDF-Bookmark-Automator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure Tesseract (for OCRing the image-based table of contents):
   - Set the Tesseract path in the Settings tab of the application.
   - Alternatively, add Tesseract to your system PATH.

4. Set OpenAI API Key (only if you wish to use LLM to automatically refine OCR output):
   - Obtain an API key from [OpenAI](https://platform.openai.com/api-keys).
   - Enter the key in the Settings tab.

5. Run the application:
   ```bash
   python app/main.py
   ```

---

## Usage

### OCR Processing
1. Go to the **OCR Processing** tab.
2. Select images of your table of contents (PNG/JPG).
3. Click **Run OCR** to extract text.
4. Review the OCR output and click **Refine with LLM** to generate structured JSON.

### Manual JSON Input
1. Go to the **Manual JSON Input** tab.
2. Use the **Copy LLM Prompt Template** button to get a template for generating JSON.
3. Paste the JSON or load it from a file.
4. Click **Validate JSON** to ensure the structure is correct.

### PDF Operations
1. Go to the **PDF Operations** tab.
2. Select the target PDF file.
3. Set the page offset if needed (e.g., if TOC page numbers don't match the PDF)

   `offset = [pdf-viewer page number] - [page number]`.
4. Enable **OCR for Scanned Pages** if working with scanned PDFs.
5. Click **Apply Bookmarks** to generate the bookmarked PDF.

---

## Configuration

### Settings
- **Tesseract Path**: Set the path to the Tesseract executable.
- **OpenAI API Key**: Enter your OpenAI API key for AI processing.
- **Default Offset**: Set a default page offset for all operations.

### Config File
The application saves settings in `config.json`:
```json
{
    "tesseract_path": "/path/to/tesseract",
    "openai_api_key": "your-api-key",
    "default_offset": 0
}
```

---

## Troubleshooting

### Common Issues
1. **OCR Errors**:
   - Ensure Tesseract is installed and the path is correct.
   - Use high-quality images for better OCR accuracy.

2. **PDF Encryption**:
   - Decrypt PDFs before processing.

3. **Page Offset Issues**:
   - Calculate the offset as `PDF_page = JSON_page + offset`.

4. **OpenAI API Errors**:
   - Verify your API key and ensure you have sufficient credits.

---

## Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern GUI.
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF manipulation.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for text recognition.
- [OpenAI](https://openai.com/) for AI-powered JSON generation.
- [REPO: pdf-bookmark](https://github.com/ifnoelse/pdf-bookmark) inspired by the need and this old REPO written with JAVA


<!-- TRAFFIC_START -->
**📊 GitHub Traffic (Last 14 Days)**
- Clones: 64
- Views: 61
<!-- TRAFFIC_END -->
