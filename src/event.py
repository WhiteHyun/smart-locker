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

    @classmethod
    def show_warning(cls):
        """
        새 창으로 이벤트를 발생시킵니다.
        """
        return messagebox.showwarning(title="버튼", message="버튼 이벤트 발생")

    def __show(frame):
        """
        프레임(창)을 띄워줍니다.
        """
        frame.tkraise()

    @classmethod
    def delivery(cls, _self):
        """
        맡기기 버튼을 눌렀을 때 발생할 이벤트 함수입니다.

        flow:
            현재 사물함의 상태를 긁어옴({빨간색, 초록색} 또는 {회색, 파란색}으로 구별할 예정)
            해당 정보에 대해 사물함 버튼 생성 및 이벤트 구현
            화면에 전달
        """
        stats_sql = SQL("root", "", "10.80.76.63", "SML")
        result = stats_sql.processDB(
            "SELECT LCKMngKey, UseYn FROM LCKStat ORDER BY LCKMngKey ASC;")
        cls.__make_button(_self, result)
        cls.show_frame(_self)

    def __make_button(cls, _self, result):
        """
        쿼리로 가져온 결과값을 가지고 버튼을 생성하여 나타냅니다.
        """
        from PIL import Image, ImageTk

        # TODO: 무조건 경로 수정해야함!!!
        play_image = ImageTk.PhotoImage(Image.open(
            "src/img/lockers.png").resize((60, 60)))
        for data in result:
            if data["UseYn"] == 0:
                _self.buttons.append(TkinterCustomButton(master=_self,
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
                                                         command=cls.show_warning))
            else:
                _self.buttons.append(TkinterCustomButton(master=_self,
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
                                                         command=cls.show_warning))
        relx = 0.33
        rely = 0.2
        for button in _self.buttons:
            button.place(relx=relx, rely=rely, anchor=tk.CENTER)
            relx = 0.66 if relx == 0.33 else 0.33
            rely = rely + 0.2 if relx == 0.66 else rely

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
