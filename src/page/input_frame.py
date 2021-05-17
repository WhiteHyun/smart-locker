import os
import sys

if __name__:
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    from utils.util import *

from page.information_page import ADMIN_MODE


class InputFrame(tk.Frame):
    """사용자로부터 입력을 받을 수 있는 프레임입니다.
    """

    def __init__(self, parent, controller, entry, mode, *args, **kwargs) -> None:
        super.__init__(parent, *args, **kwargs)
        self.index = 0
        row = 0
        col = 0
        button_name_list = ["1", "2", "3", "4", "5",
                            "6", "7", "8", "9", "<<", "0", "확인"]

        if mode == ADMIN_MODE:
            entry.insert(0, "H")
            self.index += 1
        # 밑에 함수는 Entry에 입력갱신을 위해 만들어진 함수입니다.

        def insert_text(button_num, entry):
            entry.insert(self.index, button_num)
            self.index += 1

        def delete_text(entry):
            if mode == ADMIN_MODE and self.index == 1:
                return
            entry.delete(self.index-1)
            self.index = self.index-1 if self.index > 0 else 0

        for i in button_name_list:
            SMLButton(master=self,
                      text_font=controller.large_font,
                      text=i,
                      border_width=1,
                      width=100,
                      height=100,
                      command=lambda button_num=i, entry=entry: insert_text(
                          button_num, entry) if button_num.isnumeric() else delete_text(entry) if button_num == "<<" else parent.check_and_show_page(entry.get())
                      ).grid(row=row, column=col)
            row = row+1 if col == 2 else row
            col = 0 if col == 2 else col+1
