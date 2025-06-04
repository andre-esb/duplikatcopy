import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import cv2
import threading
import filetype

def show_preview():
    path = filedialog.askopenfilename(title="Datei zur Vorschau wählen")
    if not path or not os.path.exists(path):
        return

    kind = filetype.guess(path)
    if kind is None:
        show_text_preview(path)
        return

    if kind.mime.startswith("image"):
        show_image_preview(path)
    elif kind.mime.startswith("video"):
        show_video_preview(path)
    elif path.lower().endswith(('.txt', '.md', '.csv')):
        show_text_preview(path)
    else:
        show_unknown_file()

def show_image_preview(path):
    win = tk.Toplevel()
    win.title("Bildvorschau")

    img = Image.open(path)
    img.thumbnail((800, 600))
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(win, image=photo)
    label.image = photo
    label.pack()

def show_text_preview(path):
    win = tk.Toplevel()
    win.title("Textvorschau")

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    txt = tk.Text(win, wrap="word")
    txt.insert("1.0", text)
    txt.pack(expand=True, fill="both")

def show_video_preview(path):
    def run():
        cap = cv2.VideoCapture(path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Videovorschau (Q = schließen)", frame)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()

    threading.Thread(target=run, daemon=True).start()

def show_unknown_file():
    win = tk.Toplevel()
    win.title("Dateityp nicht unterstützt")
    tk.Label(win, text="Dieser Dateityp kann nicht angezeigt werden.").pack(padx=20, pady=20)

