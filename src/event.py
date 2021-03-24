import tkinter as tk
from tkinter import messagebox


def show_warning():
    """
    새 창으로 이벤트를 발생시킵니다.
    """
    return messagebox.showwarning(title="버튼", message="버튼 이벤트 발생")


def detect_QR():
    """
    QR코드 인식하는 이벤트
    """
    if __name__ == "__main__" or __name__ == "event":
        from qrcodes import detectQR
    else:
        from .qrcodes import detectQR

    qr_info = detectQR()
    print(qr_info)
