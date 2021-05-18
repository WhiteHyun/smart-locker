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
        super().__init__(parent)
        self.controller = controller

        self.canvas = tk.Canvas(self, width=controller.width,
                                height=controller.height, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(controller.width >> 1, controller.height/7,
                                text="화면을 눌러주세요", font=controller.title_font, fill="#ffffff")

        settings_img = ImageTk.PhotoImage(Image.open(
            "../img/INU_logo.png" if __name__ == "__main__" or __name__ == "screensaver_page" else "src/img/INU_logo.png"
        ).resize((int(controller.width/5/1.618), int(controller.height/3/1.8))))

        self.canvas.create_image(
            controller.width >> 1, controller.height >> 1, image=settings_img)

        self.canvas.bind("<Button-1>", lambda e: self.destroy)
