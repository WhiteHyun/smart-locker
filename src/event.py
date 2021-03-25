import tkinter as tk
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
    def show_warning(cls, _title=None, _message=None):
        """
        새 창으로 경고 이벤트를 발생시킵니다.
        """
        title = _title if _title is not None else "버튼"
        message = _message if _message is not None else "버튼 이벤트 발생"
        return messagebox.showwarning(title=title, message=message)

    @classmethod
    def show_error(cls, _title=None, _message=None):
        """
        새 창으로 에러 이벤트를 발생시킵니다.
        """
        title = _title if _title is not None else "버튼"
        message = _message if _message is not None else "버튼 이벤트 발생"
        return messagebox.showerror(title=title, message=message)

    @classmethod
    def show(cls, frame):
        """
        프레임(창)을 최상단으로 띄워줍니다.
        """
        frame.tkraise()

    @classmethod
    def __delivery_process(cls, _self):
        """
        택배 보관 처리 함수입니다. 택배보관 가능한 사물함을 누를 시 발생하는 함수입니다.

        Args:
            _self (tk.frame): DeliveryPage 클래스

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
    def delivery(cls, _self):
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
        if len(_self.lockers) != len(result):
            cls.__make_button(_self, result)
        cls.show(_self)

    @classmethod
    def __make_button(cls, _self, result):
        """
        쿼리로 가져온 결과값을 가지고 버튼을 생성하여 나타냅니다.
        버튼은 두 가지 버튼으로 만들어집니다.

        사물(택배)함이 사용중일 경우
            빨간색의 사물(택배)함 버튼이 만들어지며 누를 경우 사용할 수 없다는 경고창이 뜹니다.

        사물(택배)함이 미사용중일 경우

        """
        from PIL import Image, ImageTk

        # TODO: 무조건 경로 수정해야함!!!
        play_image = ImageTk.PhotoImage(Image.open(
            "src/img/lockers.png").resize((60, 60)))
        for data in result:
            # 새로운 사물(택배)함이 들어왔을 때
            if data["LCKMngKey"] not in _self.lockers.keys():
                if data["UseYn"] == 0:
                    button = TkinterCustomButton(master=_self,
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
                                                 command=lambda: cls.__delivery_process(_self))
                else:
                    button = TkinterCustomButton(master=_self,
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
                _self.lockers[data["LCKMngKey"]] = button
                button.place(relx=cls.relx, rely=cls.rely, anchor=tk.CENTER)
                cls.rely = cls.rely + 0.1 if cls.relx == 0.99 else cls.rely
                cls.relx = cls.relx + 0.11 if cls.relx != 0.99 else 0.22

    @classmethod
    def __makeQR(cls):
        """

        """

    @classmethod
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
