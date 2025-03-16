# Custom widgets
import customtkinter as ctk

class CustomTextbox(ctk.CTkTextbox):
    """Custom textbox with additional features."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(state="normal")