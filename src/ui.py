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
        super().__init__(*args, **kwargs)

        # 폰트 지정
        self.title_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold")

        self.large_font = tkfont.Font(
            family="MS Sans Serif", size=24, weight="bold")

        # 화면 설정
        self.geometry(
            f"{super().winfo_screenwidth()}x{super().winfo_screenheight()}+0+0")
        super().attributes('-type', 'splash')

        # 화면에 보여질 컨테이너 생성
        self.container = tk.Frame()
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # 필요한 정적 UI 생성
        self.static_frames = {}

        for F in (StartPage, DeliveryPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.static_frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        UIEvent.show_frame(self.static_frames["StartPage"])


class StartPage(tk.Frame):
    """
    첫 페이지를 보여주는 프레임입니다.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="택배보관함",
                         font=controller.large_font)
        label.pack(side="top", fill="x", pady=50)

        self.delivery_button = TkinterCustomButton(master=self,
                                                   bg_color=None,
                                                   fg_color="#2874A6",
                                                   hover_color="#5499C7",
                                                   text_font=controller.large_font,
                                                   text="맡기기",
                                                   text_color="white",
                                                   corner_radius=10,
                                                   width=240,
                                                   height=90,
                                                   hover=True,
                                                   command=lambda: UIEvent.delivery(
                                                       self.controller)
                                                   )
        self.find_delivery_button = TkinterCustomButton(master=self,
                                                        bg_color=None,
                                                        fg_color="#2874A6",
                                                        hover_color="#5499C7",
                                                        text_font=controller.large_font,
                                                        text="찾기",
                                                        text_color="white",
                                                        corner_radius=10,
                                                        width=240,
                                                        height=90,
                                                        hover=True,
                                                        command=lambda: UIEvent.show_frame(
                                                            controller.frames["FindPage"])
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
        super().__init__(parent)
        self.controller = controller
        self.lockers = {}

        label = tk.Label(self, text="택배를 넣을 함을 선택해주세요.",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: UIEvent.show_frame(controller.static_frames["StartPage"]))
        button.pack()

        button = tk.Button(self, text="destroy page",
                           command=self.destroy)
        button.pack()
        frame1 = LockerFrame(
            parent=self, controller=controller, relief="solid", bd=2)
        frame1.pack(fill="both", expand=True)


class FindPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: UIEvent.show_frame(controller.static_frames["StartPage"]))
        button.pack()


class LockerFrame(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        UIEvent.show_locker()


if __name__ == "__main__":
    app = App()
    app.mainloop()
