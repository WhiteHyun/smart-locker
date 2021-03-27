import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
if __name__ == "__main__" or __name__ == "event":
    from sql import SQL
    from custom.tkinter_custom_button import TkinterCustomButton
else:
    from .sql import SQL
    from .custom.tkinter_custom_button import TkinterCustomButton


class ButtonEvent():

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"   # datetime 포맷값
    relx = 0.22  # 함 이미지 위치 지정값 중 x
    rely = 0.2  # 함 이미지 위치 지정값 중 y

    @classmethod
    def show_warning(cls, title="버튼", message="버튼 이벤트 발생"):
        """
        새 창으로 경고 이벤트를 발생시킵니다.
        """
        return messagebox.showwarning(title=title, message=message)

    @classmethod
    def show_error(cls, title="버튼", message="버튼 이벤트 발생"):
        """
        새 창으로 에러 이벤트를 발생시킵니다.
        """
        return messagebox.showerror(title=title, message=message)

    @classmethod
    def show_frame(cls, frame):
        """
        프레임(창)을 최상단으로 띄워줍니다.
        """
        frame.tkraise()

    @classmethod
    def get_value_from_user_to_dialog(cls, title="dialog", message="dialog test"):
        return simpledialog.askstring(title=title, prompt=message)

    @classmethod
    def __delivery_process(cls, frame):
        """
        택배 보관 처리 함수입니다. 택배보관 가능한 사물함을 누를 시 발생하는 함수입니다.

        Args:
            frame (tk.frame): DeliveryPage 클래스

        flow:
            1. 사용자의 전화번호를 입력받게 함
            2. 사용자의 전화번호를 통해 유저정보를 가져옴
            3. 사용자와 사물함정보 그리고 보관한 시각을 더해 해시를 생성합니다.
            4. 해시를 가지고 QR코드를 생성합니다.
            6. DB에 관련 내용을 Insert 합니다.
            5. SMS를 통해 QR코드를 전달합니다.
            7. 사물함의 표시색깔을 변경하여 뿌려줍니다.
        """
        # TODO: 전화번호 입력을 받게 하기 위해 프레임 하나 더 생성?

    @classmethod
    def delivery(cls, frame):
        """
        맡기기 버튼을 눌렀을 때 발생할 이벤트 함수입니다.

        flow:
            1. 현재 사물함의 상태를 긁어옴({빨간색, 초록색}
            2. 해당 정보에 대해 사물함 버튼 생성 및 이벤트 구현
            3. 화면에 전달
        """

        """
        FIXME: json이나 xml을 통해 사물함의 키값과 크기, 함의 위치값과 크기를 로컬로 저장하여(이는 관리자 화면에서 동기화를 통해 갱신)
               함의 정보를 화면에 띄울 때 값을 가져오고 사용유무에 대한 db값을 가져와 보여주기!
        """
        stats_sql = SQL("root", "", "10.80.76.63", "SML")
        result = stats_sql.processDB(
            "SELECT LCKMngKey, UseYn FROM LCKStat ORDER BY LCKMngKey ASC;")

        # 추가된 게 없는 경우 버튼 생성 X
        if len(frame.lockers) != len(result):
            cls.__make_button(frame, result)
        cls.show_frame(frame)

    @classmethod
    def __make_button(cls, frame, result):
        """
        쿼리로 가져온 결과값을 가지고 버튼을 생성하여 나타냅니다.
        버튼은 두 가지 버튼으로 만들어집니다.

        사물(택배)함이 사용중일 경우
            빨간색의 사물(택배)함 버튼이 만들어지며 누를 경우 사용할 수 없다는 경고창이 뜹니다.

        사물(택배)함이 미사용중일 경우

        """
        from PIL import Image, ImageTk

        # FIXME: 무조건 경로 수정해야함!!!
        play_image = ImageTk.PhotoImage(Image.open(
            "src/img/lockers.png").resize((60, 60)))
        for data in result:
            # 새로운 사물(택배)함이 들어왔을 때
            if data["LCKMngKey"] not in frame.lockers.keys():
                if data["UseYn"] == 0:
                    button = TkinterCustomButton(master=frame,
                                                 bg_color=None,
                                                 fg_color="#1E8449",
                                                 border_color=None,
                                                 hover_color="#2ECC71",
                                                 image=play_image,
                                                 corner_radius=10,
                                                 border_width=0,
                                                 width=100,
                                                 height=100,
                                                 hover=True,
                                                 command=lambda: cls.__delivery_process(frame))
                else:
                    button = TkinterCustomButton(master=frame,
                                                 bg_color=None,
                                                 fg_color="#A93226",
                                                 border_color=None,
                                                 hover_color="#CD6155",
                                                 image=play_image,
                                                 corner_radius=10,
                                                 border_width=0,
                                                 width=100,
                                                 height=100,
                                                 hover=True,
                                                 command=lambda: cls.show_error(_title="오류!", _message="사용할 수 없습니다."))
                frame.lockers[data["LCKMngKey"]] = button
                button.place(relx=cls.relx, rely=cls.rely, anchor=tk.CENTER)
                cls.rely = cls.rely + 0.1 if cls.relx == 0.99 else cls.rely
                cls.relx = cls.relx + 0.11 if cls.relx != 0.99 else 0.22

    @ classmethod
    def sync_to_json(cls):
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
                        "SELECT LCKMngKey FROM LCKInfo;")))

                    while locker_manage_key is None or locker_manage_key not in manage_key_list:
                        locker_manage_key = cls.get_value_from_user_to_dialog(
                            "사물함 관리번호", "사물함 관리번호가 무엇인지 정확하게 기입하여주세요!")
                else:
                    json_object = json.loads("".join(file_read))
                    locker_manage_key = json_object["LCKMngKey"]

            # 본격적인 파싱 시작
            locker_size = sql.processDB(
                f"SELECT LCKSizeX, LCKSizeY FROM LCKInfo WHERE LCKMngKey='{locker_manage_key}'")[0]

            result = sql.processDB(
                f"SELECT c.CRRMngKey, CRRNo, PosX, PosY, Width, Height, UseStat FROM CRRInfo c INNER JOIN LCKStat l ON LCKMngKey='{locker_manage_key}' AND c.CRRMngKey=l.CRRMngKey;")
            result = list(map(lambda dic: f"""
        {{
            "CRRMngKey": "{dic["CRRMngKey"]}",
            "CRRNo": "{dic["CRRNo"]}",
            "location": {{
                "start": {{
                    "x": {dic["PosX"]},
                    "y": {dic["PosY"]}
                }},
                "width": {dic["Width"]},
                "height": {dic["Height"]}
            }},
            "useState": "{dic["UseStat"]}"
        }}""", result))

            with open("data/information.json", "w") as f:
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

                print(json_string)
                print(json.dump(json.loads(json_string), f, indent=2))

        except json.decoder.JSONDecodeError as e:
            cls.show_error("에러!", "잘못된 정보입니다. 새롭게 json세팅을 시도해주세요.")
            raise e

        except Exception as e:
            raise e

    @ classmethod
    def find_delivery(cls):
        """
        택배를 찾으려고 할 때 발생하는 이벤트
        """
        if __name__ == "__main__" or __name__ == "event":
            from qrcodes import detectQR
            from sql import SQL
            from encrypt import encrypt
        else:
            from .qrcodes import detectQR
            from .sql import SQL
            from .encrypt import encrypt

        hash_qr = detectQR()[0]
        info_sql = SQL("root", "", "10.80.76.63", "SML")
        result = info_sql.processDB(
            f"SELECT * FROM LCKStat WHERE HashKey='{hash_qr}';")

        print(result)


if __name__ == "__main__":
    ButtonEvent.sync_to_json()
