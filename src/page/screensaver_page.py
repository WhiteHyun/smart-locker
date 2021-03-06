import os
import sys
if __name__:
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    from utils.util import *


class ScreenSaverPage(tk.Frame):
    """
    첫 페이지를 보여주는 프레임입니다.
    """

    def __init__(self, parent, controller, bg, *args, **kwargs):
        from utils.rasp_sensor import DetectMotion
        self.human_sensor = DetectMotion()
        super().__init__(parent)
        self.controller = controller

        self.canvas = tk.Canvas(self, width=controller.width,
                                height=controller.height, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(controller.width >> 1, controller.height/7,
                                text="화면을 눌러주세요", font=controller.title_font, fill="#6D6E6C")

        self.logo_img = ImageTk.PhotoImage(Image.open(
            "../img/INU_logo.png" if __name__ == "__main__" or __name__ == "screensaver_page" else "src/img/INU_logo.png"
        ))

        self.canvas.create_image(
            controller.width >> 1, controller.height >> 1, image=self.logo_img)
        self.after(1, self.__check_human)
        self.canvas.bind("<Button-1>", lambda e: self.destroy())

    def __check_human(self):
        if self.human_sensor.is_human_coming():
            self.destroy()
        else:
            self.after(1, self.__check_human)
