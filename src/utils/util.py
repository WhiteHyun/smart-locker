import os
import sys
import tkinter as tk
from tkinter import font as tkfont
from tkinter.messagebox import showerror, askquestion
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from custom.button import SMLButton


def success_message(root_view, width=290, height=150):
    """완료메시지를 가운데에 표시해줍니다."""

    sw = root_view.winfo_screenwidth()
    sh = root_view.winfo_screenheight()
    x = (sw - width)/2
    y = (sh - height)/2
    top = tk.Toplevel(width=width, height=height)
    top.geometry(f"{width}x{height}+{x}+{y}")
    tk.Message(top, text="완료되었습니다.", padx=20, pady=20).pack()
    top.after(4000, top.destroy)
