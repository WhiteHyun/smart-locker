import os
import sys
import tkinter as tk
from tkinter import font as tkfont
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from custom.button import SMLButton


def show_message(root_view, text, width=290, height=150):
    """메시지를 표시해줍니다."""

    sw = root_view.winfo_screenwidth()
    sh = root_view.winfo_screenheight()
    x = (sw - width) // 2
    y = (sh - height) // 2
    top = tk.Toplevel(width=width, height=height)
    top.attributes("-type", "splash")
    top.geometry(f"{width}x{height}+{x}+{y}")
    SMLButton(master=top,
              border_width=1,
              corner_radius=10,
              text=text,
              text_font=root_view.title_font,
              width=100*width,
              height=100*height,
              command=top.destroy
              ).pack()
    top.after(4000, top.destroy)
