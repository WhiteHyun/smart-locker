import os
import sys
if __name__:
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    from utils.util import *
    from utils.sql import SQL
if __name__ == "__main__" or __name__ == "process_page":
    from locker_frame import LockerFrame
else:
    from .locker_frame import LockerFrame


class ProcessPage(tk.Frame):
    """
    함을 클릭했을 때 사용자 정보를 입력할 프레임입니다.
    """

    def __init__(self, parent, controller, bg, *args, **kwargs):
        super().__init__(parent)
        from utils.discriminate import Discriminate

        self.canvas = tk.Canvas(self, width=controller.width,
                                height=controller.height, bg=bg)
        self.canvas.pack(fill="both", expand=True)
        self.controller = controller
        self.CRRMngKey = kwargs["CRRMngKey"]
        self.text_id = self.canvas.create_text(controller.width/2, controller.height/10,
                                               text="문을 여는 중입니다.", font=controller.title_font, fill="#385ab7")
        self.escape_open_door = ""
        self.escape_has_item = ""
        self.is_door_open = tk.BooleanVar(self, value=True)
        self.has_item = tk.BooleanVar(self, value=False)
        self.discriminate = Discriminate()

        user_key = kwargs["USRMngKey"]
        page = kwargs["page"]

        if page == "DeliveryPage":
            self.after(1, lambda: self.__process_delivery(
                user_key, kwargs["phone_number"]))
        elif page == "FindPage":
            self.after(1, lambda: self.__find_delivery(user_key))

    def __process_delivery(self, user_key, phone_number):
        """
        함 정보와 유저정보, 현재 시간을 통해 해시 암호화 하여 qr코드를 생성후 유저에게 보냅니다.
        그리고 데이터베이스에 해당 내용을 저장합니다.
        """
        from datetime import datetime
        from time import sleep
        from utils.sms import SMS
        from utils.encrypt import encrypt
        from utils.qrcodes import generateQR
        from utils.ratchController import RatchController

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # datetime 포맷값
        value = self.CRRMngKey+user_key+time
        hash_value = encrypt(value)
        # QR코드 생성 실패시 다시 시도
        if not generateQR(hash_value):
            MessageFrame(self.controller, "qr코드 생성에 실패하였습니다.")
            return

        # TODO: #17 택배함이 열리고 물건넣고 닫은 후의 과정을 넣어야 함
        ratch = RatchController.instance()
        if not self.discriminate.is_door_open(self.CRRMngKey):
            ratch.execute(0, "O")

        sleep(2)
        self.canvas.itemconfig(self.text_id, text="문이 열렸습니다. 물건을 넣어주세요")

        self.__listen_item()
        self.canvas.wait_variable(self.has_item)

        self.canvas.itemconfig(self.text_id, text="물건을 인지했습니다. 문을 닫아주세요.")

        self.__listen_door()
        self.canvas.wait_variable(self.is_door_open)
        self.canvas.itemconfig(self.text_id, text="문을 닫고있습니다.")

        ratch.execute(0, "C")
        sleep(3)

        # 완료 메시지 표시
        MessageFrame(self.controller, "완료되었습니다")

        # 일반화면으로 이동
        self.controller.show_frame("StartPage", self)
        return
        # 여기서부터 데이터베이스 저장 시작
        sql = SQL("root", "", "10.80.76.63", "SML")

        # 저장하려는 함의 정보가 존재할 때
        if sql.processDB(f"SELECT * FROM LCKStat WHERE CRRMngKey='{self.CRRMngKey}';"):
            sql.processDB(
                f"UPDATE LCKStat SET USRMngKey='{user_key}', AddDt='{time}', HashKey='{hash_value}', UseStat='{LockerFrame.STATE_USED}' WHERE CRRMngKey='{self.CRRMngKey}';"
            )
        else:
            sql.processDB(
                f"INSERT INTO LCKStat(CRRMngkey, USRMngKey, AddDt, HashKey, UseStat) values('{self.CRRMngKey}', '{user_key}', '{time}', '{hash_value}', '{LockerFrame.STATE_USED}');"
            )

        nSMS = SMS(
            to=phone_number,
            text="""
QR코드가 발급되었습니다!!
택배를 찾을 때 표시에 따라 '찾기->QR코드로 찾기'를 누른 후
QR코드를 카메라에 보여주게 되면 간편하게 열립니다.
항상 저희 택배(사물)함을 이용해주셔서 감사합니다. 🙏
                """,
            imagePath=f"../data/{hash_value}.png" if __name__ == "__main__" or __name__ == "ui" else f"data/{hash_value}.png")
        if not nSMS.sendMessage():
            MessageFrame(self.controller, "문자전송에 실패 하였습니다.")

        # 완료 메시지 표시
        MessageFrame(self.controller, "완료되었습니다")

        # 일반화면으로 이동
        self.controller.show_frame("StartPage", self)

    def __find_delivery(self, user_key):
        """
        택배함을 열어 유저가 택배를 가져갈 수 있게 처리해줍니다.
        """
        # TODO: #17 택배함이 열리고 택배함에 물건을 가져가고 문을 닫는 등의 확인절차 필요

        sql = SQL("root", "", "10.80.76.63", "SML")
        result = sql.processDB(
            f"SELECT * FROM LCKStat WHERE CRRMngKey='{self.CRRMngKey}';")
        if result and result[0]["USRMngKey"] == user_key:
            sql.processDB(
                f"UPDATE LCKStat SET UseStat='{LockerFrame.STATE_WAIT}' WHERE USRMngKey='{user_key}';"
            )
            # 완료메시지 표시
            MessageFrame(self.controller, "완료되었습니다.")

            # 일반화면으로 이동
            self.controller.show_frame("StartPage", self)
        else:
            # 실패메시지 표시
            MessageFrame(self.controller, "실패! 올바르지 않는 값입니다.")

    def __listen_item(self):
        if not self.discriminate.has_item(self.CRRMngKey):
            self.escape_has_item = self.canvas.after(1, self.__listen_item)
        else:
            self.has_item.set(True)
            self.canvas.after_cancel(self.escape_has_item)  # after 중지

    def __listen_door(self):
        if self.discriminate.is_door_open(self.CRRMngKey):
            self.escape_open_door = self.canvas.after(1, self.__listen_door)
        else:
            self.is_door_open.set(False)
            self.canvas.after_cancel(1, self.escape_open_door)  # after 중지
