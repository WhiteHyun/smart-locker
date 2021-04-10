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

        background_image = ImageTk.PhotoImage(Image.open(
            "../img/background6.png" if __name__ == "__main__" or __name__ == "find_page" else "src/img/background6.png"
        ).resize((controller.width, controller.height)))

        canvas = tk.Canvas(self, width=controller.width,
                           height=controller.height)
        canvas.pack(fill="both", expand=True)

        canvas.create_image(0, 0, image=background_image, anchor="nw")
        canvas.image = background_image
        canvas.create_text(controller.width/2, controller.height *
                           1/10, text="택배를 넣을 함을 선택해주세요.", font=controller.medium_font)

        LockerFrame(
            parent=self, controller=controller, relief="solid").place(x=controller.width/2, y=controller.height/2, relwidth=1, relheight=1)

        SMLButton(master=self,
                  text="이전으로",
                  border_width=1,
                  width=100,
                  height=100,
                  command=lambda: controller.show_frame(
                      "StartPage", self
                  )
                  ).place(x=20, y=controller.height-170)
