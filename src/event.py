import tkinter as tk
from tkinter import messagebox


class ButtonEvent():

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def show_warning():
        """
        새 창으로 이벤트를 발생시킵니다.
        """
        return messagebox.showwarning(title="버튼", message="버튼 이벤트 발생")

    @staticmethod
    def find_delivery():
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
