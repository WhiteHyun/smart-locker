import os
import sys
if __name__:
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    from utils.util import *


class AdminPage(tk.Frame):
    """
    첫 페이지를 보여주는 프레임입니다.
    """

    def __init__(self, parent, controller, bg, *args, **kwargs):
        super().__init__(parent)
        self.controller = controller

        canvas = tk.Canvas(self, width=controller.width,
                           height=controller.height, bg=bg)
        canvas.pack(fill="both", expand=True)

        canvas.create_text(controller.width/2, controller.height/7,
                           text="택배 보관함 (관리자)", font=controller.title_font, fill="#385ab7")

        settings_img = ImageTk.PhotoImage(Image.open(
            "../img/settings.png" if __name__ == "__main__" or __name__ == "start_page" else "src/img/settings.png"
        ).resize((int(controller.width/5/1.618), int(controller.height/3/1.8))))

        fix_img = ImageTk.PhotoImage(Image.open(
            "../img/support.png" if __name__ == "__main__" or __name__ == "start_page" else "src/img/support.png"
        ).resize((int(controller.width/5/1.618), int(controller.height/3/1.8))))

        unlock_img = ImageTk.PhotoImage(Image.open(
            "../img/unlock.png" if __name__ == "__main__" or __name__ == "start_page" else "src/img/unlock.png"
        ).resize((int(controller.width/5/1.618), int(controller.height/3/1.8))))
        previous_arrow_img = ImageTk.PhotoImage(Image.open(
            "../img/previous.png" if __name__ == "__main__" or __name__ == "information_page" else "src/img/previous.png"
        ).resize((int(100/1.618), int(100/1.618))))

        SMLButton(master=self,
                  text_font=controller.large_font,
                  text="사물함번호설정",
                  fg_color=None if not self.__check_json_file() else "#7C7877",
                  image=settings_img,
                  width=controller.width/4,
                  height=controller.height/2.6,
                  command=lambda: self.controller.show_frame(
                      "InformationPage", self, page="AdminPage")
                  ).place(relx=0.22, rely=0.5, anchor=tk.CENTER)
        SMLButton(master=self,
                  text_font=controller.large_font,
                  text="고장유무설정",
                  fg_color="#7C7877" if not self.__check_json_file() else None,
                  image=fix_img,
                  width=controller.width/4,
                  height=controller.height/2.6,
                  command=None
                  ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        SMLButton(master=self,
                  text_font=controller.large_font,
                  text="문강제개방",
                  fg_color="#7C7877" if not self.__check_json_file() else None,
                  image=unlock_img,
                  width=controller.width/4,
                  height=controller.height/2.6,
                  command=None
                  ).place(relx=0.78, rely=0.5, anchor=tk.CENTER)
        SMLButton(master=self,
                  text="이전으로",
                  border_width=1,
                  width=100,
                  height=100,
                  image=previous_arrow_img,
                  command=self.__move_to_start_page
                  ).place(x=20, y=controller.height-120)

    def __check_json_file(self) -> bool:
        """json파일이 만들어졌는지 체크합니다.
        """
        try:
            with open("data/information.json") as f:
                file_read = f.readlines()
                if len(file_read) == 0:
                    raise FileNotFoundError
        except FileNotFoundError as e:
            return False
        else:
            return True

    def __move_to_start_page(self):
        """시작페이지로 이동하는 함수입니다.
        """
        if self.__check_json_file():
            self.controller.show_frame("StartPage", frame=self)
        else:
            MessageFrame(self.controller, "사물함번호입력을 먼저 해주세요")
