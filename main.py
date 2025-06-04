import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Treeview
import os
import threading
from file_utils import find_duplicates_and_similars
from preview import show_preview
import shutil
import json
from datetime import datetime

# Konfiguration laden
with open("config/ui_config.json") as f:
    config = json.load(f)

PRIMARY_COLOR = config.get("primary_color", "#D6EAF8")  # hellblau

class DuplikatcopyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplikatcopy – KI-gestützter Duplikatvergleich")
        self.root.geometry("900x600")
        self.root.configure(bg=PRIMARY_COLOR)

        self.source_path = tk.StringVar()
        self.target_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Quellordner:", bg=PRIMARY_COLOR).pack()
        tk.Entry(self.root, textvariable=self.source_path, width=80).pack()
        tk.Button(self.root, text="Ordner wählen", command=self.browse_source).pack(pady=5)

        tk.Label(self.root, text="Zielordner (Masterstruktur):", bg=PRIMARY_COLOR).pack()
        tk.Entry(self.root, textvariable=self.target_path, width=80).pack()
        tk.Button(self.root, text="Ordner wählen", command=self.browse_target).pack(pady=5)

        tk.Button(self.root, text="Duplikate prüfen & kopieren", command=self.start_processing).pack(pady=10)

        self.progress = Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        tk.Button(self.root, text="Vorschau anzeigen", command=show_preview).pack(pady=5)

        self.tree = Treeview(self.root, columns=("Datei", "Status"), show="headings")
        self.tree.heading("Datei", text="Dateiname")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill="both", expand=True, pady=10)

    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_path.set(folder)

    def browse_target(self):
        folder = filedialog.askdirectory()
        if folder:
            self.target_path.set(folder)

    def start_processing(self):
        source = self.source_path.get()
        target = self.target_path.get()
        if not source or not target:
            messagebox.showwarning("Fehlende Angabe", "Bitte Quell- und Zielordner angeben.")
            return
        threading.Thread(target=self.run, args=(source, target), daemon=True).start()

    def run(self, source, target):
        self.progress["value"] = 0
        duplicates = find_duplicates_and_similars(source)
        total = len(duplicates)
        for i, file_info in enumerate(duplicates):
            rel_path = file_info["rel_path"]
            src_file = file_info["path"]
            status = file_info["status"]

            try:
                mod_date = datetime.fromtimestamp(os.path.getmtime(src_file)).strftime("%Y-%m")
                file_ext = os.path.splitext(src_file)[-1].lower().strip(".")
                if not file_ext:
                    file_ext = "unknown"

                subfolder = os.path.join(target, mod_date, file_ext)
                os.makedirs(subfolder, exist_ok=True)
                dest_file = os.path.join(subfolder, os.path.basename(src_file))
                shutil.copy2(src_file, dest_file)

                self.tree.insert("", "end", values=(rel_path, status))
            except Exception as e:
                self.tree.insert("", "end", values=(rel_path, f"Fehler: {str(e)}"))

            self.progress["value"] = int((i + 1) / total * 100)
        messagebox.showinfo("Fertig", f"{total} Dateien verarbeitet.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DuplikatcopyApp(root)
    root.mainloop()

