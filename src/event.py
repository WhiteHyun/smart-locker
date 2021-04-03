import tkinter as tk
from tkinter import TclError, simpledialog
from tkinter import messagebox
if __name__ == "__main__" or __name__ == "event":
    from sql import SQL
    from custom.tkinter_custom_button import SMLButton
else:
    from .sql import SQL
    from .custom.tkinter_custom_button import SMLButton


class UIEvent():

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
    def get_value_from_user_to_dialog(cls, title="dialog", message="dialog test"):
        return simpledialog.askstring(title=title, prompt=message)

    @classmethod
    def show_question(cls, title="버튼", message="버튼 이벤트 발생"):
        """
        새 창으로 질문 이벤트 창을 발생시킵니다.
        """
        return messagebox.askquestion(title=title, message=message)

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
    UIEvent.sync_to_json()
