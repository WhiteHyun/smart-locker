import os
import sys
if __name__:
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    from utils.util import *


class StartPage(tk.Frame):
    """
    첫 페이지를 보여주는 프레임입니다.
    """

    def __init__(self, parent, controller, bg, *args, **kwargs):
        super().__init__(parent)
        self.controller = controller
        self.count = 0
        canvas = tk.Canvas(self, width=controller.width,
                           height=controller.height, bg=bg)
        canvas.pack(fill="both", expand=True)

        canvas.create_text(controller.width/2, controller.height/7,
                           text="택배 보관함", font=controller.title_font, fill="#385ab7", tags="admin")
        canvas.tag_bind("admin", '<ButtonPress-1>', self.__go_to_admin_page)
        man_img = ImageTk.PhotoImage(Image.open(
            "../img/delivery-man.png" if __name__ == "__main__" or __name__ == "start_page" else "src/img/delivery-man.png"
        ).resize((int(controller.width/5/1.618), int(controller.height/3/1.8))))

        box_img = ImageTk.PhotoImage(Image.open(
            "../img/delivery-box.png" if __name__ == "__main__" or __name__ == "start_page" else "src/img/delivery-box.png"
        ).resize((int(controller.width/5/1.618), int(controller.height/3/1.8))))

        SMLButton(master=self,
                  text_font=controller.xlarge_font,
                  text="맡기기",
                  image=man_img,
                  width=controller.width/4,
                  height=controller.height/2.6,
                  command=lambda: controller.show_frame(
                      "DeliveryPage", frame=self
                  )
                  ).place(relx=0.32, rely=0.5, anchor=tk.CENTER)
        SMLButton(master=self,
                  text_font=controller.xlarge_font,
                  text="찾기",
                  image=box_img,
                  width=controller.width/4,
                  height=controller.height/2.6,
                  command=lambda: controller.show_frame(
                      "FindPage", frame=self
                  )
                  ).place(relx=0.67, rely=0.5, anchor=tk.CENTER)

    def __go_to_admin_page(self, event):
        """관리자페이지로 이동하는 일종의 트릭함수입니다.
        """
        self.count += 1
        if self.count == 5:
            self.controller.show_frame("InformationPage",
                                       frame=self,
                                       mode=3,
                                       page=None)
