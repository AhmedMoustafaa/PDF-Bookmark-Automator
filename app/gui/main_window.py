import os
import json
import fitz
import pytesseract
import tempfile
import pyperclip
import traceback
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
import openai
import tkinter as tk
# Configure appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class PDFBookmarkerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PDF Bookmark Automator")
        self.geometry("1200x800")

        # Initialize variables
        self.api_key = ""
        self.tesseract_path = ""
        self.image_paths = []
        self.json_data = None
        self.pdf_file = ""
        self.ocr_cache = {}
        self.full_text = ''
        self.create_widgets()
        self.configure_menu()

    def create_widgets(self):
        """Create main application widgets"""
        self.tabview = ctk.CTkTabview(self, width=1150, height=750)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # Create tabs
        tabs = ["OCR Processing", "Manual JSON Input", "PDF Operations", "Settings"]
        for tab in tabs:
            self.tabview.add(tab)

        self.create_ocr_tab()
        self.create_json_tab()
        self.create_pdf_operations_tab()
        self.create_settings_tab()

    def create_ocr_tab(self):
        """OCR Processing tab components"""
        tab = self.tabview.tab("OCR Processing")
        container = ctk.CTkFrame(tab)
        container.pack(pady=20, padx=20, fill="both", expand=True)

        # Instructions
        instructions = """
        1. Select images of your Table of Contents pages (PNG/JPG)
        2. Click 'Run OCR' to extract text
        3. Review OCR results and click 'Refine with LLM' to generate structured JSON
        """
        ctk.CTkLabel(container, text=instructions, wraplength=1000).pack(pady=10)

        # Image selection
        ctk.CTkButton(container, text="Select TOC Images", command=self.load_images,
                      width=200, height=40).pack(pady=10)
        self.image_list = ctk.CTkTextbox(container, width=800, height=100)
        self.image_list.pack(pady=10)

        # OCR output
        self.ocr_output = scrolledtext.ScrolledText(container, width=100, height=20,
                                                    font=("Consolas", 12))
        self.ocr_output.pack(pady=10)

        # Processing buttons
        btn_frame = ctk.CTkFrame(container)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Run OCR", command=self.run_ocr,
                      width=150, height=40).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Refine with LLM", command=self.refine_with_llm,
                      width=150, height=40).pack(side="left", padx=10)

    def create_json_tab(self):
        """Manual JSON Input tab components"""
        tab = self.tabview.tab("Manual JSON Input")
        container = ctk.CTkFrame(tab)
        container.pack(pady=20, padx=20, fill="both", expand=True)

        # Instructions and template
        instructions = """
        1. Use template button to get LLM prompt
        2. Paste generated JSON or load from file
        3. Validate JSON before proceeding
        """
        ctk.CTkLabel(container, text=instructions, wraplength=1000).pack(pady=10)
        ctk.CTkButton(container, text="📋 Copy LLM Prompt Template",
                      command=self.copy_template, width=250, height=40).pack(pady=10)

        # JSON input
        self.json_input = scrolledtext.ScrolledText(container, width=100, height=25,
                                                    font=("Consolas", 12))
        self.json_input.pack(pady=10)

        # JSON controls
        btn_frame = ctk.CTkFrame(container)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Load JSON File", command=self.load_json_file,
                      width=150, height=40).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Validate JSON", command=self.validate_json,
                      width=150, height=40).pack(side="left", padx=10)

    def create_pdf_operations_tab(self):
        """PDF Operations tab components"""
        tab = self.tabview.tab("PDF Operations")
        container = ctk.CTkFrame(tab)
        container.pack(pady=20, padx=20, fill="both", expand=True)

        # Instructions
        instructions = """
        1. Select target PDF file
        2. Set page offset if needed
        3. Enable OCR for scanned documents
        4. Apply bookmarks
        """
        ctk.CTkLabel(container, text=instructions, wraplength=1000).pack(pady=10)

        # PDF controls
        ctk.CTkButton(container, text="Select PDF File", command=self.select_pdf,
                      width=200, height=40).pack(pady=10)
        self.pdf_path = ctk.CTkLabel(container, text="No PDF selected")
        self.pdf_path.pack(pady=5)

        # OCR toggle
        self.ocr_var = ctk.CTkCheckBox(container, text="Enable OCR for scanned pages")
        self.ocr_var.pack(pady=5)

        # Page offset
        offset_frame = ctk.CTkFrame(container)
        offset_frame.pack(pady=10)
        ctk.CTkLabel(offset_frame, text="Page Offset:").pack(side="left", padx=5)
        self.offset_entry = ctk.CTkEntry(offset_frame, width=100)
        self.offset_entry.pack(side="left", padx=5)

        # Apply button
        ctk.CTkButton(container, text="Apply Bookmarks", command=self.apply_bookmarks,
                      width=200, height=40).pack(pady=20)

    def create_settings_tab(self):
        """Settings tab components"""
        tab = self.tabview.tab("Settings")
        container = ctk.CTkFrame(tab)
        container.pack(pady=20, padx=20, fill="both", expand=True)

        # Tesseract settings
        ctk.CTkLabel(container, text="Tesseract Path:").pack(pady=5)
        tesseract_frame = ctk.CTkFrame(container)
        tesseract_frame.pack(pady=5)
        self.tesseract_entry = ctk.CTkEntry(tesseract_frame, width=400)
        self.tesseract_entry.pack(side="left", padx=5)
        ctk.CTkButton(tesseract_frame, text="Browse", command=self.set_tesseract_path,
                      width=100).pack(side="left", padx=5)

        # OpenAI settings
        ctk.CTkLabel(container, text="\nOpenAI API Key:").pack(pady=5)
        self.api_entry = ctk.CTkEntry(container, width=400)
        self.api_entry.pack(pady=5)
        ctk.CTkButton(container, text="Save API Key", command=self.save_api_key,
                      width=150).pack(pady=10)

    # Core functionality methods
    def load_images(self):
        self.image_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        self.image_list.delete("1.0", "end")
        self.image_list.insert("end", "\n".join(self.image_paths))

    def run_ocr(self):
        if not self.image_paths:
            messagebox.showerror("Error", "Please select images first")
            return

        full_text = ""
        for img_path in self.image_paths:
            try:
                img = Image.open(img_path)
                text = pytesseract.image_to_string(img)
                full_text += text + "\n"
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process {os.path.basename(img_path)}:\n{str(e)}")
        self.full_text = full_text
        self.ocr_output.delete("1.0", "end")
        self.ocr_output.insert("end", full_text)

    def refine_with_llm(self):
        if not self.api_key:
            messagebox.showerror("Error", "Please set OpenAI API key in Settings")
            return

        prompt = """Please convert this table of contents into a JSON structure following this exact format:
{
    "toc": [
        {
            "title": "Main Chapter Title",
            "page": 1,
            "children": [
                {"title": "Subsection Title", "page": 2},
                {"title": "Another Subsection", "page": 3}
            ]
        },
        {
            "title": "Appendix",
            "page": 4
        }
    ]
}
respect Hierarchy. So include Chapters, Sections, and Subsections as Children to one another, you may need to OCR if it's scanned and doesn't have text
""" + self.full_text

        try:
            openai.api_key = self.api_key
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            json_str = response.choices[0].message.content
            self.json_data = json.loads(json_str)
            self.json_input.delete("1.0", "end")
            self.json_input.insert("end", json.dumps(self.json_data, indent=2))
            messagebox.showinfo("Success", "JSON generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"LLM processing failed: {str(e)}")

    def generate_toc_structure(self, entries, offset, doc):
        toc = []
        self.ocr_cache = {}

        def clean_text(text):
            return (text.lower()
                    .replace('\n', ' ')
                    .replace('\r', '')
                    .strip(' :.-'))

        def ocr_page(page_num):
            if page_num in self.ocr_cache:
                return self.ocr_cache[page_num]

            page = doc[page_num]
            mat = fitz.Matrix(3, 3)
            pix = page.get_pixmap(matrix=mat)

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                pix.save(tmp.name)
                img = Image.open(tmp.name)
                os.unlink(tmp.name)

            if self.tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

            self.ocr_cache[page_num] = []
            for i in range(len(data['text'])):
                if data['text'][i].strip():
                    self.ocr_cache[page_num].append({
                        'text': data['text'][i],
                        'x': data['left'][i] / 3,
                        'y': data['top'][i] / 3
                    })
            return self.ocr_cache[page_num]

        def find_title_position(page, title):
            clean_title = clean_text(title)

            # Try native text search first
            rects = page.search_for(title)
            if rects:
                return fitz.Point(rects[0].x0, rects[0].y0)

            # Use OCR if enabled and needed
            if self.ocr_var.get() and len(page.get_text()) < 50:
                ocr_data = ocr_page(page.number)
                for item in ocr_data:
                    if clean_text(item['text']) == clean_title:
                        return fitz.Point(item['x'], item['y'])

                for word in clean_title.split():
                    for item in ocr_data:
                        if clean_text(item['text']) == clean_text(word):
                            return fitz.Point(item['x'], item['y'])

            # Fallback position
            return fitz.Point(50, 50)

        def process_entries(entries, level):
            for entry in entries:
                try:
                    page_number = entry['page'] + offset
                    adjusted_page = max(0, page_number-1)

                    if adjusted_page >= len(doc):
                        messagebox.showerror("Error", f"Page {page_number} exceeds PDF length")
                        continue

                    page = doc[adjusted_page]
                    point = find_title_position(page, entry['title'])

                    toc.append([
                        level,
                        entry['title'],
                        page_number,
                        {
                            'kind': fitz.LINK_GOTO,
                            'pageno': adjusted_page,
                            'to': point
                        }
                    ])

                    if 'children' in entry:
                        process_entries(entry['children'], level + 1)

                except KeyError as e:
                    messagebox.showerror("Error", f"Missing key in JSON: {str(e)}")

        process_entries(entries, 1)
        return toc

    def apply_bookmarks(self):
        if not self.pdf_file:
            messagebox.showerror("Error", "Please select a PDF file")
            return

        try:
            print("\n--- Starting Bookmark Process ---")
            doc = fitz.open(self.pdf_file)

            if doc.is_encrypted:
                messagebox.showerror("Error", "Encrypted PDF - please decrypt first")
                return

            if not self.json_data or 'toc' not in self.json_data:
                messagebox.showerror("Error", "Invalid or missing JSON data")
                return

            try:
                offset = int(self.offset_entry.get()) if self.offset_entry.get().strip() else 0
            except ValueError:
                messagebox.showerror("Error", "Page offset must be an integer")
                return

            print("[Generating TOC structure...]")
            toc = self.generate_toc_structure(self.json_data['toc'], offset, doc)

            print("[Applying bookmarks...]")
            doc.set_toc(toc)

            output_file = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"bookmarked_{os.path.basename(self.pdf_file)}"
            )

            if output_file:
                doc.save(output_file)
                messagebox.showinfo("Success", f"Saved bookmarked PDF:\n{output_file}")

        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"PDF processing failed: {str(e)}")
        finally:
            if 'doc' in locals():
                doc.close()

    # Helper methods
    def copy_template(self):
        prompt = """Please convert this table of contents into a JSON structure following this exact format:
        {
            "toc": [
                {
                    "title": "Main Chapter Title",
                    "page": 1,
                    "children": [
                        {"title": "Subsection Title", "page": 2},
                        {"title": "Another Subsection", "page": 3}
                    ]
                },
                {
                    "title": "Appendix",
                    "page": 4
                }
            ]
        }
        respect Hierarchy. So include Chapters, Sections, and Subsections as Children to one another, you may need to OCR if it's scanned and doesn't have text"""
        pyperclip.copy(prompt)
        messagebox.showinfo("Template Copied", "LLM prompt template copied to clipboard!")

    def load_json_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                content = f.read()
                self.json_input.delete("1.0", "end")
                self.json_input.insert("end", content)
                self.json_data = json.loads(content)

    def validate_json(self):
        try:
            self.json_data = json.loads(self.json_input.get("1.0", "end"))
            if "toc" not in self.json_data:
                raise ValueError("Missing 'toc' key")
            messagebox.showinfo("Success", "Valid JSON structure!")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid JSON: {str(e)}")

    def set_tesseract_path(self):
        path = filedialog.askopenfilename(title="Select Tesseract Executable")
        if path:
            self.tesseract_entry.delete(0, "end")
            self.tesseract_entry.insert(0, path)
            self.tesseract_path = path

    def save_api_key(self):
        self.api_key = self.api_entry.get()
        messagebox.showinfo("Success", "API key saved")

    def select_pdf(self):
        self.pdf_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        self.pdf_path.configure(text=os.path.basename(self.pdf_file))

    def configure_menu(self):
        """Configure system menu using standard Tkinter"""
        self.menu_bar = tk.Menu(self, tearoff=0)
        self.config(menu=self.menu_bar)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.destroy)

        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Style the menu to match CustomTkinter
        self.configure(menu=self.menu_bar)
        self.option_add('*Menu*background', '#2b2b2b')
        self.option_add('*Menu*foreground', 'white')
        self.option_add('*Menu*activeBackground', '#3b3b3b')
        self.option_add('*Menu*activeForeground', 'white')

    def show_about(self):
        messagebox.showinfo("About", "PDF Bookmark Automator\nVersion 1.0")



if __name__ == "__main__":
    app = PDFBookmarkerApp()
    app.mainloop()