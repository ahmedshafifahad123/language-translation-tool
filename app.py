import threading
import tkinter.messagebox as messagebox

import customtkinter as ctk
import pyperclip
from deep_translator import GoogleTranslator
from flask import Flask, render_template, request


app = Flask(__name__)

WEB_LANGUAGES = [
    ("auto", "Detect Language"), ("en", "English"), ("ur", "Urdu"),
    ("ar", "Arabic"), ("ps", "Pashto"), ("es", "Spanish"), ("fr", "French"),
    ("de", "German"), ("it", "Italian"), ("pt", "Portuguese"),
    ("hi", "Hindi"), ("zh-CN", "Chinese"), ("ja", "Japanese"),
    ("ko", "Korean"), ("ru", "Russian"),
]


@app.route("/", methods=["GET", "POST"])
def index():
    text, translated, error = "", "", None
    source, target = "auto", "ur"

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        source = request.form.get("source", "auto")
        target = request.form.get("target", "ur")
        valid_codes = dict(WEB_LANGUAGES)

        if not text:
            error = "Please enter text to translate."
        elif source not in valid_codes or target not in valid_codes or target == "auto":
            error = "Please select valid languages."
        else:
            try:
                translated = GoogleTranslator(source=source, target=target).translate(text)
            except Exception:
                error = "Translation failed. Please check your internet connection and try again."

    return render_template(
        "index.html", languages=WEB_LANGUAGES, text=text, translated=translated,
        source=source, target=target, error=error, provider="Google",
    )


LANGUAGES = {
    "English": "en", "Urdu": "ur", "Spanish": "es", "French": "fr",
    "German": "de", "Italian": "it", "Portuguese": "pt", "Arabic": "ar",
    "Hindi": "hi", "Chinese": "zh-CN", "Japanese": "ja", "Korean": "ko",
    "Russian": "ru",
}

# These languages are written from right to left.
RTL_LANGUAGES = {"Urdu", "Arabic"}


class TranslationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Lingua - Language Translation Tool")
        self.geometry("900x620")
        self.minsize(720, 520)
        self.configure(fg_color="#f5f3ff")
        ctk.set_appearance_mode("light")
        self.create_widgets()

    def create_widgets(self):
        header = ctk.CTkFrame(self, fg_color="#5b4bdf", corner_radius=0, height=115)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="lingua", text_color="white", font=ctk.CTkFont(size=32, weight="bold")).pack(anchor="w", padx=38, pady=(20, 0))
        ctk.CTkLabel(header, text="Translate your words in seconds", text_color="#e9e6ff", font=ctk.CTkFont(size=15)).pack(anchor="w", padx=40, pady=(0, 18))

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=34, pady=28)
        language_bar = ctk.CTkFrame(content, fg_color="white", corner_radius=14)
        language_bar.pack(fill="x", pady=(0, 18))

        menu_style = {"width": 225, "fg_color": "#eeeaff", "button_color": "#d8d2ff", "button_hover_color": "#c7bfff", "text_color": "#28243e", "font": ctk.CTkFont(size=14, weight="bold")}
        self.source_menu = ctk.CTkOptionMenu(language_bar, values=list(LANGUAGES), **menu_style)
        self.source_menu.set("English")
        self.source_menu.pack(side="left", padx=(22, 8), pady=16)
        ctk.CTkButton(language_bar, text="⇄", width=42, height=34, corner_radius=10, fg_color="#eeeaff", hover_color="#ddd7ff", text_color="#5b4bdf", font=ctk.CTkFont(size=20, weight="bold"), command=self.swap_languages).pack(side="left", padx=8, pady=16)
        self.target_menu = ctk.CTkOptionMenu(language_bar, values=list(LANGUAGES), **menu_style)
        self.target_menu.set("Urdu")
        self.target_menu.pack(side="left", padx=8, pady=16)
        ctk.CTkButton(language_bar, text="Clear", width=78, height=34, corner_radius=10, fg_color="transparent", border_width=1, border_color="#d8d4e5", text_color="#69657a", hover_color="#f1eff7", command=self.clear_text).pack(side="right", padx=22, pady=16)

        text_area = ctk.CTkFrame(content, fg_color="transparent")
        text_area.pack(fill="both", expand=True)
        text_area.grid_columnconfigure((0, 1), weight=1)
        text_area.grid_rowconfigure(0, weight=1)
        self.input_box = self.make_text_card(text_area, "Text to translate", 0)
        self.output_box = self.make_text_card(text_area, "Translation", 1)
        self.output_box.configure(state="disabled")

        buttons = ctk.CTkFrame(content, fg_color="transparent")
        buttons.pack(fill="x", pady=(20, 0))
        self.translate_button = ctk.CTkButton(buttons, text="Translate  →", height=44, width=170, corner_radius=10, fg_color="#5b4bdf", hover_color="#493aca", font=ctk.CTkFont(size=15, weight="bold"), command=self.start_translation)
        self.translate_button.pack(side="left")
        ctk.CTkButton(buttons, text="Copy", height=42, width=90, corner_radius=10, fg_color="#ffffff", hover_color="#f0edfa", border_width=1, border_color="#d8d4e5", text_color="#504b62", command=self.copy_translation).pack(side="right", padx=(10, 0))

    def make_text_card(self, parent, title, column):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=14)
        card.grid(row=0, column=column, sticky="nsew", padx=(0, 9) if column == 0 else (9, 0))
        ctk.CTkLabel(card, text=title, text_color="#373248", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=20, pady=(17, 8))
        textbox = ctk.CTkTextbox(card, corner_radius=8, border_width=1, border_color="#e6e2ef", fg_color="#fcfbff", text_color="#29253b", font=ctk.CTkFont(size=15), wrap="word")
        textbox.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        return textbox

    def swap_languages(self):
        source = self.source_menu.get()
        self.source_menu.set(self.target_menu.get())
        self.target_menu.set(source)

    def clear_text(self):
        self.input_box.delete("1.0", "end")
        self.set_output("")

    def set_output(self, text, right_to_left=False):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        if right_to_left:
            self.output_box.insert("1.0", "\u200f" + text, "rtl")
            self.output_box._textbox.tag_configure("rtl", justify="right")
        else:
            self.output_box.insert("1.0", text, "ltr")
            self.output_box._textbox.tag_configure("ltr", justify="left")
        self.output_box.configure(state="disabled")

    def start_translation(self):
        text = self.input_box.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("No text", "Please enter text to translate.")
            return
        self.translate_button.configure(text="Translating...", state="disabled")
        source_code = LANGUAGES[self.source_menu.get()]
        target_language = self.target_menu.get()
        target_code = LANGUAGES[target_language]
        threading.Thread(
            target=self.translate,
            args=(text, source_code, target_code, target_language in RTL_LANGUAGES),
            daemon=True,
        ).start()

    def translate(self, text, source_code, target_code, right_to_left):
        try:
            result = GoogleTranslator(source=source_code, target=target_code).translate(text)
            self.after(0, lambda: self.set_output(result, right_to_left))
        except Exception:
            self.after(0, lambda: messagebox.showerror("Translation failed", "Please check your internet connection and try again."))
        finally:
            self.after(0, lambda: self.translate_button.configure(text="Translate  →", state="normal"))

    def copy_translation(self):
        translated = self.output_box.get("1.0", "end").strip().lstrip("\u200f")
        if not translated:
            messagebox.showinfo("Nothing to copy", "Translate some text first.")
            return
        pyperclip.copy(translated)
        messagebox.showinfo("Copied", "Translation copied to clipboard.")

if __name__ == "__main__":
    app.run(debug=True)
