import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from tkinter import messagebox
if __name__ == "__main__" or __name__ == "ui":
    from custom.tkinter_custom_button import TkinterCustomButton
    from event import *

else:
    from .custom.tkinter_custom_button import TkinterCustomButton
    from .event import *


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold")

        # 컨테이너는 여러 개의 프레임을 서로 쌓아올리는 프레임객체
        # 우리가 원하는 프레임을 다른 컨테이너보다 위로 올려 보여주면 됨!
        container = tk.Frame(self)
        self.geometry(
            f"{container.winfo_screenwidth()}x{container.winfo_screenheight()}+0+0")
        super().attributes('-type', 'splash')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, DeliveryPage, FindPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def get_frame(self, page_name):
        """
        다른 창을 맨 앞으로 가져오게 하는 메서드

        Args:
            page_name (str): 불러올 page(frame)의 이름

        Example:
            >>> show_frame("StartPage")
            # tkinter frame에서 StartPage Frame이 화면에 보여짐

        """
        return self.frames[page_name]


class StartPage(tk.Frame):
    """
    첫 페이지를 보여주는 프레임입니다.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="택배보관함",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.delivery_button = TkinterCustomButton(master=self,
                                                   bg_color=None,
                                                   fg_color="#2874A6",
                                                   hover_color="#5499C7",
                                                   text_font=None,
                                                   text="맡기기",
                                                   text_color="white",
                                                   corner_radius=10,
                                                   width=120,
                                                   height=45,
                                                   hover=True,
                                                   command=lambda: ButtonEvent.delivery(
                                                       controller.get_frame("DeliveryPage"))
                                                   )
        self.find_delivery_button = TkinterCustomButton(master=self,
                                                        bg_color=None,
                                                        fg_color="#2874A6",
                                                        hover_color="#5499C7",
                                                        text_font=None,
                                                        text="찾기",
                                                        text_color="white",
                                                        corner_radius=10,
                                                        width=120,
                                                        height=45,
                                                        hover=True,
                                                        command=lambda: controller.show_frame(
                                                            "FindPage")
                                                        )
        self.exit_button = TkinterCustomButton(master=self,
                                               bg_color=None,
                                               fg_color="#922B21",
                                               border_color="white",
                                               hover_color="#CD6155",
                                               text_font=None,
                                               text="tkinter 종료",
                                               text_color="white",
                                               corner_radius=10,
                                               border_width=2,
                                               width=150,
                                               height=45,
                                               hover=True,
                                               command=lambda: controller.destroy()
                                               )
        self.delivery_button.place(relx=0.33, rely=0.2, anchor=tk.CENTER)
        self.find_delivery_button.place(relx=0.66, rely=0.2, anchor=tk.CENTER)
        self.exit_button.place(relx=0.50, rely=0.3, anchor=tk.CENTER)


class DeliveryPage(tk.Frame):
    """
    맡기기 버튼을 눌렀을 때 보여지는 프레임입니다.
    사물함의 위치 및 상태가 gui로 보여집니다.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="택배를 넣을 함을 선택해주세요.",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        from PIL import Image, ImageTk

        # TODO: 무조건 경로 수정해야함!!!
        play_image = ImageTk.PhotoImage(Image.open(
            "src/img/lockers.png").resize((60, 60)))

        # TODO: 사물(택배)함 버튼 구현
        self.buttons = []

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class FindPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
