import os
import sys
import tkinter as tk
from tkinter import font as tkfont
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from custom.button import SMLButton

CHECK = 0
ASK = 1


def show_message(root_view, text, width=400, height=200, flag=CHECK):
    """메시지를 표시해줍니다."""
    sw = root_view.winfo_screenwidth()
    sh = root_view.winfo_screenheight()
    x = (sw - width) // 2
    y = (sh - height) // 2
    top = tk.Toplevel(width=width, height=height)
    top.attributes("-type", "splash")
    top.attributes("-topmost", True)
    top.geometry(f"{width}x{height}+{x}+{y}")

    canvas = tk.Canvas(top, width=width,
                       height=height, bg="white")
    canvas.pack(fill="both", expand=True)

    canvas.create_text(width/2, height/7,
                       text=text, font=root_view.large_font)
    assert flag == CHECK or flag == ASK
    if flag == CHECK:
        SMLButton(master=top,
                  border_width=1,
                  corner_radius=10,
                  text="확인",
                  text_font=root_view.medium_font,
                  width=100,
                  height=100,
                  command=top.destroy
                  ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        top.after(4000, top.destroy)
    else:
        result = tk.StringVar()
        SMLButton(master=top,
                  border_width=1,
                  corner_radius=10,
                  text="예",
                  text_font=root_view.medium_font,
                  width=100,
                  height=100,
                  command=lambda: result.set("yes")
                  ).place(relx=0.32, rely=0.5, anchor=tk.CENTER)
        SMLButton(master=top,
                  border_width=1,
                  corner_radius=10,
                  text="아니오",
                  text_font=root_view.medium_font,
                  width=100,
                  height=100,
                  command=lambda: result.set("no")
                  ).place(relx=0.67, rely=0.5, anchor=tk.CENTER)
        while result.get() == "":
            pass
        return result.get()
