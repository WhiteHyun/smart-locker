import os
import sys
import tkinter as tk
from tkinter import font as tkfont
from tkinter.messagebox import showerror, askquestion
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from custom.button import SMLButton
