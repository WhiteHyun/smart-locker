import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from tkinter import messagebox
if __name__ == "__main__" or __name__ == "ui":
    from custom.tkinter_custom_button import SMLButton
    from event import *

else:
    from .custom.tkinter_custom_button import SMLButton
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

        # 모든 프레임들을 가지는 변수
        self.pages = {}
        for F in (StartPage, DeliveryPage, FindPage, LockerFrame, InformationFrame):
            page_name = F.__name__
            is_static = True if page_name == "StartPage" else False
            self.pages[page_name] = {"isStatic": is_static, "class": F}
            if is_static:
                frame = F(parent=self.container, controller=self)
                self.pages[page_name]["frame"] = frame
        UIEvent.show_frame(self.pages["StartPage"])


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

        self.delivery_button = SMLButton(master=self,
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
                                         command=lambda: UIEvent.show_frame(
                                             controller.pages["DeliveryPage"], controller=controller)
                                         )
        self.find_delivery_button = SMLButton(master=self,
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
                                                  controller.frames["FindPage"], controller=controller)
                                              )
        self.exit_button = SMLButton(master=self,
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

        UIEvent.sync_to_json()


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
                           command=lambda: UIEvent.show_frame(controller.pages["StartPage"], self, controller))
        button.pack()

        button = tk.Button(self, text="destroy page",
                           command=self.destroy)
        button.pack()
        frame = LockerFrame(
            parent=self, controller=controller, relief="solid")
        frame.pack(pady=20)


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

    STATE_WAIT = "W"
    STATE_USED = "U"
    STATE_BROKEN = "B"

    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller
        self.show_locker()

    def show_locker(self):
        """
        json을 참조하여 사물함을 보여줍니다.
        grid 형태로 나타내어지기 때문에 frame에 pack으로 표시되어있는 상태에서는 사용될 수 없습니다.
        """
        try:
            with open("data/information.json") as f:
                import json
                json_object = json.load(f)
                locker_list = sorted(
                    json_object["CRRInfo"], key=lambda dic: dic["location"]["start"]["row"])
                for json_data in locker_list:
                    self.__make_locker_button(json_data)
        except Exception as e:
            print(e)
            raise e

    def __make_locker_button(self, json_data):
        """
        json 데이터를 가지고 버튼을 생성하여 나타냅니다.
        버튼은 세 가지 버튼으로 만들어집니다.

        사물(택배)함이 고장났을 경우
            회색의 사물(택배)함 버튼이 만들어지며 누를 경우 사용할 수 없다는 경고창이 발생합니다.

        사물(택배)함이 사용중일 경우
            빨간색의 사물(택배)함 버튼이 만들어지며 누를 경우 사용할 수 없다는 경고창이 발생합니다.

        사물(택배)함이 미사용중일 경우
            초록색의 사물(택배)함 버튼이 만들어지며 누를 경우 사용관련 창으로 넘어갑니다.
        """
        from PIL import Image, ImageTk

        # FIXME: 무조건 경로 수정해야함!!!
        play_image = ImageTk.PhotoImage(Image.open(
            "src/img/lockers.png").resize((60, 60)))

        location = json_data["location"]
        width = location["width"]
        height = location["height"]
        color_dict = {
            f"{LockerFrame.STATE_WAIT}": ("#1E8449", "#2ECC71"),
            f"{LockerFrame.STATE_USED}": ("#A93226", "#CD6155"),
            f"{LockerFrame.STATE_BROKEN}": ("#7C7877", "#7C7877")
        }
        command_dict = {
            f"{LockerFrame.STATE_WAIT}": lambda: UIEvent.show_frame(self.controller.pages["InformationFrame"], self.parent, self.controller),
            f"{LockerFrame.STATE_USED}": lambda: UIEvent.show_error("오류!", "해당 함을 사용할 수 없습니다."),
            f"{LockerFrame.STATE_BROKEN}": lambda: UIEvent.show_error("오류!", "해당 함을 사용할 수 없습니다.")
        }

        button = SMLButton(master=self,
                           bg_color=None,
                           fg_color=color_dict[json_data["useState"]][0],
                           border_color=None,
                           hover_color=color_dict[json_data["useState"]][1],
                           image=play_image,
                           corner_radius=10,
                           border_width=1,
                           width=100 if width == 1 else 100*width,
                           height=100 if height == 1 else 100*height,
                           hover=True,
                           command=command_dict[json_data["useState"]])

        button.grid(row=location["start"]["row"],
                    column=location["start"]["col"], rowspan=height, columnspan=width)


class InformationFrame(tk.Frame):
    """
    사물함을 클릭했을 때 정보를 입력할 프레임입니다.
    """

    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        intro_label = tk.Label(
            self, text="휴대폰 번호를 입력해주세요.", font=controller.large_font)
        entry = tk.Entry(self)
        number_frame = tk.Frame(self)
        before_button = SMLButton(master=self,
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
                                  command=lambda: UIEvent.show_frame(
                                      controller.pages["DeliveryPage"], self, controller)
                                  )
        row = 0
        col = 0
        button_name_list = ["1", "2", "3", "4", "5",
                            "6", "7", "8", "9", "취소", "0", "확인"]

        for i in button_name_list:
            text = f"{i} 버튼 이벤트 발생"
            button = SMLButton(master=number_frame,
                               bg_color=None,
                               fg_color="#2874A6",
                               border_color=None,
                               hover_color="#5499C7",
                               text_font=None,
                               text=i,
                               text_color="white",
                               corner_radius=10,
                               border_width=1,
                               width=100,
                               height=100,
                               hover=True,
                               command=lambda i=i: UIEvent.show_error(
                                   message=f"{i} 버튼 이벤트 발생")
                               )
            button.grid(row=row, column=col)
            row = row+1 if col == 2 else row
            col = 0 if col == 2 else col+1

        intro_label.pack()
        entry.pack(pady=10)
        number_frame.pack()
        before_button.pack(side="bottom", anchor="w")


if __name__ == "__main__":
    app = App()
    app.mainloop()
