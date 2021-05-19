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

        self.canvas = tk.Canvas(self, width=controller.width,
                                height=controller.height, bg=bg)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(controller.width/2, controller.height/7,
                                text="택배 보관함 (관리자)", font=controller.title_font, fill="#385ab7")

        settings_img = ImageTk.PhotoImage(Image.open(
            "../img/settings.png" if __name__ == "__main__" or __name__ == "admin_page" else "src/img/settings.png"
        ).resize((int(controller.width/5/1.618), int(controller.height/3/1.8))))

        fix_img = ImageTk.PhotoImage(Image.open(
            "../img/support.png" if __name__ == "__main__" or __name__ == "admin_page" else "src/img/support.png"
        ).resize((int(controller.width/5/1.618), int(controller.height/3/1.8))))

        unlock_img = ImageTk.PhotoImage(Image.open(
            "../img/unlock.png" if __name__ == "__main__" or __name__ == "admin_page" else "src/img/unlock.png"
        ).resize((int(controller.width/5/1.618), int(controller.height/3/1.8))))
        previous_arrow_img = ImageTk.PhotoImage(Image.open(
            "../img/previous.png" if __name__ == "__main__" or __name__ == "admin_page" else "src/img/previous.png"
        ).resize((int(100/1.618), int(100/1.618))))

        has_json_file = self.controller.check_json_file()

        SMLButton(master=self,
                  text_font=controller.large_font,
                  text="사물함번호설정",
                  fg_color="#385ab7" if not has_json_file else "#7C7877",
                  hover_color="#496bc9" if not has_json_file else "#7C7877",
                  image=settings_img,
                  width=controller.width/4,
                  height=controller.height/2.6,
                  command=lambda: self.controller.show_frame(
                      "InformationPage", self, mode=2, page="AdminPage") if not has_json_file else MessageFrame(self.controller, "사물함 번호를 한 번 설정 후 다시 할 수 없습니다")
                  ).place(relx=0.22, rely=0.5, anchor=tk.CENTER)
        SMLButton(master=self,
                  text_font=controller.large_font,
                  text="고장유무설정",
                  fg_color="#7C7877" if not has_json_file else "#385ab7",
                  hover_color="#7C7877" if not has_json_file else "#496bc9",
                  image=fix_img,
                  width=controller.width/4,
                  height=controller.height/2.6,
                  command=lambda: MessageFrame(self.controller, "사물함번호를 설정한 후 다시 시도해주세요") if not has_json_file else self.controller.show_frame(
                      "SettingPage", self, mode=1)
                  ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        SMLButton(master=self,
                  text_font=controller.large_font,
                  text="문강제개방",
                  fg_color="#7C7877" if not has_json_file else "#385ab7",
                  hover_color="#7C7877" if not has_json_file else "#496bc9",
                  image=unlock_img,
                  width=controller.width/4,
                  height=controller.height/2.6,
                  command=lambda: MessageFrame(self.controller, "사물함번호를 설정한 후 다시 시도해주세요") if not has_json_file else self.controller.show_frame(
                      "SettingPage", self, mode=2)
                  ).place(relx=0.78, rely=0.5, anchor=tk.CENTER)
        SMLButton(master=self,
                  text="시작페이지로",
                  fg_color="#7C7877" if not has_json_file else "#385ab7",
                  hover_color="#7C7877" if not has_json_file else "#496bc9",
                  border_width=1,
                  width=100,
                  height=100,
                  image=previous_arrow_img,
                  command=lambda: MessageFrame(self.controller, "사물함번호를 설정한 후 다시 시도해주세요") if not has_json_file else self.controller.show_frame(
                      "StartPage", frame=self
                  )
                  ).place(x=20, y=controller.height-120)
