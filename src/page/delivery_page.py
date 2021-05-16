import os
import sys
if __name__:
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
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

    def __init__(self, parent, controller, bg, *args, **kwargs):
        super().__init__(parent)
        controller.sync_to_json()
        self.controller = controller

        previous_arrow_img = ImageTk.PhotoImage(Image.open(
            "../img/previous.png" if __name__ == "__main__" or __name__ == "delivery_page" else "src/img/previous.png"
        ).resize((int(100/1.618), int(100/1.618))))

        canvas = tk.Canvas(self, width=controller.width,
                           height=controller.height, bg=bg)
        canvas.pack(fill="both", expand=True)

        canvas.create_text(controller.width/2, controller.height/7,
                           text="택배 넣을 함을 선택해주세요.", font=controller.title_font, fill="#385ab7")

        LockerFrame(
            parent=self, controller=controller, page="DeliveryPage", relief="solid").place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        SMLButton(master=self,
                  text="이전으로",
                  border_width=1,
                  width=100,
                  height=100,
                  image=previous_arrow_img,
                  command=lambda: controller.show_frame(
                      "StartPage", self
                  )
                  ).place(x=20, y=controller.height-120)
