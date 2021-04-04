import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from tkinter import messagebox

if __name__ == "__main__" or __name__ == "ui":
    from custom.button import SMLButton
    from event import *
    from sms import SMS

else:
    from .custom.button import SMLButton
    from .event import *
    from .sms import SMS


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
            f"{super().winfo_screenwidth()}x{super().winfo_screenheight()}+0+0"
        )
        super().attributes('-type', 'splash')

        # 화면에 보여질 컨테이너 생성
        self.container = tk.Frame()
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # 모든 프레임들을 가지는 변수
        self.pages = {}
        for F in (StartPage, DeliveryPage, FindPage, LockerFrame, InformationPage):
            page_name = F.__name__
            self.pages[page_name] = F
        self.show_frame("StartPage")

    def show_frame(self, new_frame, frame=None, parent=None, CRRMngKey=None, page=None):
        """
        프레임(창)을 띄워줍니다.

        Args:
            new_frame_cls (str): 새롭게 보여줄 프레임 객체의 이름
            frame (tk.Frame): 기존에 보여지고 있는 프레임
            parent (tk.Frame): 새롭게 보여질 프레임의 부모프레임
        """
        try:
            if CRRMngKey is None or page is None:
                temp_frame = self.pages[new_frame](
                    parent=parent if parent is not None else self.container, controller=self
                )
            else:
                temp_frame = self.pages[new_frame](
                    parent=parent if parent is not None else self.container, controller=self, CRRMngKey=CRRMngKey, page=page
                )

            temp_frame.grid(row=0, column=0, sticky="nsew")
            temp_frame.tkraise()

            # 기존 프레임 종료
            if frame is not None:
                frame.destroy()
        except Exception as e:
            raise e


class StartPage(tk.Frame):
    """
    첫 페이지를 보여주는 프레임입니다.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="택배보관함",
                 font=controller.large_font
                 ).pack(side="top", fill="x", pady=50)

        SMLButton(master=self,
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
                  command=lambda: controller.show_frame(
                      "DeliveryPage", self
                  )
                  ).place(relx=0.33, rely=0.2, anchor=tk.CENTER)
        SMLButton(master=self,
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
                  command=lambda: controller.show_frame(
                      "FindPage", self
                  )
                  ).place(relx=0.66, rely=0.2, anchor=tk.CENTER)
        SMLButton(master=self,
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
                  ).place(relx=0.50, rely=0.3, anchor=tk.CENTER)

        self.sync_to_json()

    def sync_to_json(self):
        """
        함의 정보를 동기화하여 json파일을 수정합니다.
        초기 파일을 실행할 때, 또는 관리자 페이지에서 사물함을 동기화할 때 사용됩니다.
        """
        try:
            locker_manage_key = None
            sql = SQL("root", "", "10.80.76.63", "SML")

            # 사물함 관리 번호를 알지 못하는 경우 입력받게 함
            import json
            with open("data/information.json") as f:
                file_read = f.readlines()
                if len(file_read) == 0:
                    manage_key_list = list(map(lambda dic: dic["LCKMngKey"], sql.processDB(
                        "SELECT LCKMngKey FROM LCKInfo;"
                    )))

                    while locker_manage_key is None or locker_manage_key not in manage_key_list:
                        locker_manage_key = UIEvent.get_value_from_user_to_dialog(
                            "사물함 관리번호", "사물함 관리번호가 무엇인지 정확하게 기입하여주세요!"
                        )
                else:
                    json_object = json.loads("".join(file_read))
                    locker_manage_key = json_object["LCKMngKey"]

            # 본격적인 파싱 시작
            locker_size = sql.processDB(
                f"SELECT LCKSizeX, LCKSizeY FROM LCKInfo WHERE LCKMngKey='{locker_manage_key}'"
            )[0]

            result = sql.processDB(
                f"SELECT c.CRRMngKey, CRRNo, PosX, PosY, Width, Height, UseStat FROM CRRInfo c INNER JOIN LCKStat l ON LCKMngKey='{locker_manage_key}' AND c.CRRMngKey=l.CRRMngKey;"
            )
            result = list(map(lambda dic: f"""
        {{
            "CRRMngKey": "{dic["CRRMngKey"]}",
            "CRRNo": "{dic["CRRNo"]}",
            "location": {{
                "start": {{
                    "row": {dic["PosY"]},
                    "col": {dic["PosX"]}
                }},
                "width": {dic["Width"]},
                "height": {dic["Height"]}
            }},
            "useState": "{dic["UseStat"]}"
        }}""", result))

            json_string = f"""{{
    "LCKMngKey": "{locker_manage_key}",
    "LCKSize": {{
        "width": {locker_size["LCKSizeX"]},
        "height": {locker_size["LCKSizeY"]}
    }},
    "CRRInfo": [
        {",".join(result)}
    ]
}}"""
            with open("data/information.json", "w") as f:
                json.dump(json.loads(json_string), f, indent=2)

        except json.decoder.JSONDecodeError as e:
            UIEvent.show_error("에러!", "잘못된 정보입니다. 새롭게 json세팅을 시도해주세요.")
            raise e
        except FileNotFoundError as e:
            with open("data/information.json", "w") as f:
                f.write("")
                self.sync_to_json()
        except Exception as e:
            raise e


class DeliveryPage(tk.Frame):
    """
    맡기기 버튼을 눌렀을 때 보여지는 프레임입니다.
    사물함의 위치 및 상태가 gui로 보여집니다.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="택배를 넣을 함을 선택해주세요.",
                 font=controller.title_font
                 ).pack(side="top", fill="x", pady=10)

        SMLButton(master=self,
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
                  command=lambda: controller.show_frame(
                      "StartPage", self
                  )
                  ).pack(side="bottom", anchor="w", padx=20, pady=20)

        LockerFrame(
            parent=self, controller=controller, relief="solid").pack(pady=20)


class FindPage(tk.Frame):
    """
    찾기 페이지입니다.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        SMLButton(master=self,
                  bg_color=None,
                  fg_color="#2874A6",
                  hover_color="#5499C7",
                  text_font=controller.large_font,
                  text="QR코드로 찾기",
                  text_color="white",
                  corner_radius=10,
                  width=240,
                  height=90,
                  hover=True,
                  command=lambda: print()
                  ).pack()
        SMLButton(master=self,
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
                  command=lambda: controller.show_frame(
                      "StartPage", self
                  )
                  ).pack(side="bottom", anchor="w", padx=20, pady=20)
        LockerFrame(
            parent=self, controller=controller, page="FindPage", relief="solid").pack(pady=20)


class LockerFrame(tk.Frame):

    STATE_WAIT = "W"
    STATE_USED = "U"
    STATE_BROKEN = "B"

    def __init__(self, parent, controller, page="DeliveryPage", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.controller = controller
        self.page = page
        self.color_dict = {
            f"{LockerFrame.STATE_WAIT}": ("#1E8449", "#2ECC71") if page == "DeliveryPage" else ("#A93226", "#CD6155"),
            f"{LockerFrame.STATE_USED}": ("#A93226", "#CD6155") if page == "DeliveryPage" else ("#1E8449", "#2ECC71"),
            f"{LockerFrame.STATE_BROKEN}": ("#7C7877", "#7C7877")
        }
        self.__show_locker()

    def __show_locker(self):
        """
        json을 참조하여 사물함을 보여줍니다.
        grid 형태로 나타내어지기 때문에 frame에 pack으로 표시되어있는 상태에서는 사용될 수 없습니다.
        """
        try:
            with open("data/information.json") as f:
                import json
                json_object = json.load(f)
                locker_list = sorted(
                    json_object["CRRInfo"], key=lambda dic: dic["location"]["start"]["row"]
                )
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
            "src/img/lockers.png"
        ).resize((60, 60)))
        location = json_data["location"]
        width = location["width"]
        height = location["height"]
        state = json_data["useState"]

        def decide_function():
            """
            함이 어디 페이지에 위치해있으며 상태값이 어떤지에 따라 그에 걸맞게 함수를 지정해줍니다
            """
            # useState == 'U' when FindPage, useState == 'W' when DeliveryPage
            if state == LockerFrame.STATE_USED and self.page == "FindPage" or state == LockerFrame.STATE_WAIT and self.page == "DeliveryPage":
                return lambda CRRMngKey=json_data["CRRMngKey"]: self.controller.show_frame("InformationPage", self.parent, CRRMngKey=CRRMngKey, page=self.page)

            # useState == 'B' or 'U' when deliveryPage, 'W' when FindPage
            else:
                return lambda: UIEvent.show_error("오류!", "해당 함을 사용할 수 없습니다.")
        SMLButton(master=self,
                  bg_color=None,
                  fg_color=self.color_dict[json_data["useState"]][0],
                  border_color=None,
                  hover_color=self.color_dict[json_data["useState"]][1],
                  image=play_image,
                  corner_radius=10,
                  border_width=1,
                  width=100 if width == 1 else 100*width,
                  height=100 if height == 1 else 100*height,
                  hover=True,
                  command=decide_function()
                  ).grid(row=location["start"]["row"],
                         column=location["start"]["col"], rowspan=height, columnspan=width)


class InformationPage(tk.Frame):
    """
    함을 클릭했을 때 사용자 정보를 입력할 프레임입니다.
    """

    def __init__(self, parent, controller, CRRMngKey, page, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.CRRMngKey = CRRMngKey
        self.index = 0
        intro_label = tk.Label(
            self, text="휴대폰 번호를 입력해주세요.", font=controller.large_font
        )
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
                                  command=lambda: controller.show_frame(
                                      page, self
                                  )
                                  )
        row = 0
        col = 0
        button_name_list = ["1", "2", "3", "4", "5",
                            "6", "7", "8", "9", "«", "0", "확인"]

        # 밑에 함수는 Entry에 입력갱신을 위해 만들어진 함수입니다.
        def insert_text(button_num, entry):
            entry.insert(self.index, button_num)
            self.index += 1

        def delete_text(entry):
            entry.delete(self.index-1)
            self.index = self.index-1 if self.index > 0 else 0

        def verify_phone_number(phone_number):
            """
            휴대폰 번호를 확인하고, 맞다면 process함수로 넘어갑니다.
            """
            if len(phone_number) != 11 or phone_number[:3] != "010":
                return
            phone_format_number = f"{phone_number[:3]}-{phone_number[3:7]}-{phone_number[7:]}"
            user_check = UIEvent.show_question(
                "번호 확인", f"{phone_format_number}가 맞습니까?"
            )
            if user_check == "yes":
                if page == "DeliveryPage":
                    self.__process_delivery(phone_number)
                elif page == "FindPage":
                    self.__find_delivery()

        for i in button_name_list:
            SMLButton(master=number_frame,
                      bg_color=None,
                      fg_color="#2874A6",
                      border_color=None,
                      hover_color="#5499C7",
                      text_font=controller.large_font,
                      text=i,
                      text_color="white",
                      corner_radius=10,
                      border_width=1,
                      width=100,
                      height=100,
                      hover=True,
                      command=lambda button_num=i, entry=entry: insert_text(
                          button_num, entry) if button_num.isnumeric() else delete_text(entry) if button_num == "«" else verify_phone_number(entry.get())
                      ).grid(row=row, column=col)
            row = row+1 if col == 2 else row
            col = 0 if col == 2 else col+1

        intro_label.pack()
        entry.pack(pady=10)
        number_frame.pack()
        before_button.pack(side="bottom", anchor="w", padx=20, pady=20)

    def __process_delivery(self, phone_number):
        """
        함 정보와 유저정보, 현재 시간을 통해 해시 암호화 하여 qr코드를 생성후 유저에게 보냅니다.
        그리고 데이터베이스에 해당 내용을 저장합니다.
        """
        from datetime import datetime
        from encrypt import encrypt
        from qrcodes import generateQR
        DATE_FORMAT = "%Y-%m-%d %H:%M:%S"   # datetime 포맷값
        hash_value = self.CRRMngKey+phone_number+datetime.now().strftime(DATE_FORMAT)
        hash_qr = encrypt(hash_value)
        generateQR(hash_qr)

        # TODO: #17 택배함이 열리고 물건넣고 닫은 후의 과정을 넣어야 함

        # 여기서부터 데이터베이스 저장 시작
        sql = SQL("root", "", "10.80.76.63", "SML")

        result = sql.processDB(
            f"SELECT * FROM LCKStat WHERE HashKey='{hash_qr}';"
        )

        # FIXME: 경로 수정해야함
        nSMS = SMS(to=phone_number, text="임시", imagePath=f"data/{hash_qr}.png")
        if not nSMS.sendMessage():
            UIEvent.show_error(message="문자전송에 실패 하였습니다.")
        # TODO: #16 CoolSMS를 통해 sms를 보냄
        # 전화번호 문자내용 qr경로

    def __find_delivery(self):
        """
        택배함을 열어 유저가 택배를 가져갈 수 있게 처리해줍니다.
        """


if __name__ == "__main__":
    app = App()
    app.mainloop()
