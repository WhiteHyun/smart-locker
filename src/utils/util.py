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


class MessageFrame(tk.Toplevel):
    """메시지를 표시해줍니다."""

    def __init__(self, root_view, text, width=400, height=200, user_check=None, flag=CHECK):
        super().__init__(width=width, height=height)
        sw = root_view.winfo_screenwidth()
        sh = root_view.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        self.attributes("-type", "splash")
        self.attributes("-topmost", True)
        self.geometry(f"{width}x{height}+{x}+{y}")
        if user_check:
            self.user_check = user_check

        canvas = tk.Canvas(self, width=width,
                           height=height, bg="white")
        canvas.pack(fill="both", expand=True)

        canvas.create_text(width/2, height/7,
                           text=text, font=root_view.large_font)
        assert flag == CHECK or flag == ASK
        if flag == CHECK:
            SMLButton(master=self,
                      border_width=1,
                      corner_radius=10,
                      text="확인",
                      text_font=root_view.medium_font,
                      width=100,
                      height=100,
                      command=self.destroy
                      ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.after(4000, self.destroy)
        else:
            SMLButton(master=self,
                      border_width=1,
                      corner_radius=10,
                      text="예",
                      text_font=root_view.medium_font,
                      width=100,
                      height=100,
                      command=lambda: self.__check_and_destroy("yes")
                      ).place(relx=0.32, rely=0.5, anchor=tk.CENTER)
            SMLButton(master=self,
                      border_width=1,
                      corner_radius=10,
                      text="아니오",
                      text_font=root_view.medium_font,
                      width=100,
                      height=100,
                      command=lambda: self.__check_and_destroy("no")
                      ).place(relx=0.67, rely=0.5, anchor=tk.CENTER)

    def __check_and_destroy(self, string):
        """user_check 값을 `string`으로 바꾸고 창을 닫습니다.
        """
        self.user_check[0] = string
        self.after(100, self.destroy)


def dict2Query(table_num, data_dict) -> str:
    """dictionary를 받아서 INSERT - QUERY 문을 만들어줍니다.
    """
    sql_query = f"INSERT INTO {table_num}({','.join(data_dict)}) VALUES("
    sql_query += ",".join(list(map(lambda x: str(x)
                                   if type(x) is int else f"'{x}'", data_dict.values())))
    sql_query += ");"
    return sql_query


def connect_arduino(port):
    """아두이노 연결을 시도합니다.
    연결에 성공하면 해당 `Serial`을 리턴합니다.

    Parameter
    ---------
    port : str
        연결할 아두이노의 포트
    """
    import time
    import serial

    try:
        return serial.Serial(port, baudrate=9600, timeout=None)
    except Exception as e:
        time.sleep(2)
        return connect_arduino(port)
