import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils.util import *
if __name__ == "__main__" or __name__ == "delivery_page":
    from locker_frame import LockerFrame
else:
    from .locker_frame import LockerFrame

class DeliveryPage(tk.Frame):
    """
    맡기기 버튼을 눌렀을 때 보여지는 프레임입니다.
    사물함의 위치 및 상태가 gui로 보여집니다.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="택배를 넣을 함을 선택해주세요.",
                 font=controller.title_font
                 ).pack(side="top", fill="x", pady=10)

        SMLButton(master=self,
                  bg_color=None,
                  fg_color="#2874A6",
                  border_color=None,
                  hover_color="#5499C7",
                  text_font=None,
                  text="이전으로",
                  text_color="white",
                  corner_radius=10,
                  border_width=1,
                  width=100,
                  height=100,
                  hover=True,
                  command=lambda: controller.show_frame(
                      "StartPage", self
                  )
                  ).pack(side="bottom", anchor="w", padx=20, pady=20)

        LockerFrame(
            parent=self, controller=controller, relief="solid").pack(pady=20)
