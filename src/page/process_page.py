import os
import sys
from time import sleep

if __name__:
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    from utils.util import *
    from utils.sql import SQL
if __name__ == "__main__" or __name__ == "process_page":
    from locker_frame import LockerFrame
else:
    from .locker_frame import LockerFrame

RESIDENTIAL_MODE = 1
COMMERCIAL_MODE = 2


class ProcessPage(tk.Frame):
    """
    함을 클릭했을 때 사용자 정보를 입력할 프레임입니다.
    """

    def __init__(self, parent, controller, bg, *args, **kwargs):
        super().__init__(parent)
        from utils.locker_state import LockerState
        from utils.ratchController import RatchController
        self.canvas = tk.Canvas(self, width=controller.width,
                                height=controller.height, bg=bg)
        self.canvas.pack(fill="both", expand=True)
        self.controller = controller
        self.CRRMngKey = kwargs["CRRMngKey"]
        self.text_id = self.canvas.create_text(controller.width/2, controller.height/2,
                                               text="문을 여는 중입니다.", font=controller.title_font, fill="#385ab7")
        self.escape_open_door = ""
        self.escape_has_item = ""
        self.is_door_open = tk.BooleanVar(self, value=True)
        self.has_item = tk.BooleanVar(self, value=False)
        self.locker_state = LockerState()
        self.ratch = RatchController.instance()

        user_key = kwargs["USRMngKey"]
        page = kwargs["page"]
        sql = SQL("root", "", "10.80.76.63", "SML")
        result = sql.processDB(
            f"SELECT SyncSensor FROM CRRInfo WHERE CRRMngKey='{self.CRRMngKey}';")
        assert result is not None   # 값이 무조건 존재해야함
        self.sync_sensor = result[0]["SyncSensor"]

        if page == "DeliveryPage":
            self.after(1, lambda: self.__process_delivery(
                user_key, kwargs["phone_number"]))
        elif page == "FindPage":
            self.after(1, lambda: self.__find_delivery(
                user_key, self.controller.mode))

    def __process_delivery(self, user_key, phone_number):
        """
        함 정보와 유저정보, 현재 시간을 통해 해시 암호화 하여 qr코드를 생성후 유저에게 보냅니다.
        그리고 데이터베이스에 해당 내용을 저장합니다.
        """
        from datetime import datetime
        from utils.sms import Messenger
        from utils.encrypt import encrypt
        from utils.qrcodes import generateQR

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # datetime 포맷값
        value = self.CRRMngKey+user_key+time
        hash_value = encrypt(value)
        # QR코드 생성 실패시 다시 시도
        if not generateQR(hash_value):
            MessageFrame(self.controller, "qr코드 생성에 실패하였습니다.")
            return

        sql = SQL("root", "", "10.80.76.63", "SML")

        if not self.locker_state.is_door_open(self.CRRMngKey):

            self.ratch.execute(self.sync_sensor, "O")
            sleep(2)

        sqlDict = {'CRRMngKey': self.CRRMngKey,
                   'USRMngKey': user_key, 'HashKey': hash_value, 'UseStat': 'U'}
        sql.processDB(dict2Query('LCKLog', sqlDict))

        self.canvas.itemconfig(self.text_id, text="문이 열렸습니다. 물건을 넣어주세요")

        self.canvas.after(100, self.__listen_item)

        # 이미 물건이 들어있는 상태라면 바로 넘어감
        if not self.has_item.get():
            self.canvas.wait_variable(self.has_item)

        self.canvas.itemconfig(self.text_id, text="물건을 인지했습니다. 문을 닫아주세요.")
        sleep(2)

        self.canvas.after(100, self.__listen_door)
        self.canvas.wait_variable(self.is_door_open)
        self.canvas.itemconfig(self.text_id, text="문을 닫고있습니다.")

        self.ratch.execute(self.sync_sensor, "C")
        sleep(2)


#         # 저장하려는 함의 정보가 존재할 때
        if sql.processDB(f"SELECT * FROM LCKStat WHERE CRRMngKey='{self.CRRMngKey}';"):
            sql.processDB(
                f"UPDATE LCKStat SET USRMngKey='{user_key}', AddDt='{time}', HashKey='{hash_value}', UseStat='{LockerFrame.STATE_USED}' WHERE CRRMngKey='{self.CRRMngKey}';"
            )
        else:
            sql.processDB(
                f"INSERT INTO LCKStat(CRRMngkey, USRMngKey, AddDt, HashKey, UseStat) values('{self.CRRMngKey}', '{user_key}', '{time}', '{hash_value}', '{LockerFrame.STATE_USED}');"
            )

        messenger = Messenger.MMS(
            to=phone_number,
            text="""
QR코드가 발급되었습니다!!
택배를 찾을 때 표시에 따라 '찾기->QR코드로 찾기'를 누른 후
QR코드를 카메라에 보여주게 되면 간편하게 열립니다.
항상 저희 택배(사물)함을 이용해주셔서 감사합니다. 🙏
                """,
            image_path=f"../data/{hash_value}.png" if __name__ == "__main__" or __name__ == "ui" else f"data/{hash_value}.png")
        if not messenger.send_message():
            MessageFrame(self.controller, "문자전송에 실패 하였습니다.")
            return

        # 완료 메시지 표시
        MessageFrame(self.controller, "완료되었습니다")

        # 일반화면으로 이동
        self.controller.show_frame("StartPage", self)

    def __find_delivery(self, user_key, mode):
        """
        택배함을 열어 유저가 택배를 가져갈 수 있게 처리해줍니다.
        """

        sql = SQL("root", "", "10.80.76.63", "SML")

        if not self.locker_state.is_door_open(self.CRRMngKey):
            self.ratch.execute(self.sync_sensor, "O")
            sleep(2)

        self.canvas.itemconfig(self.text_id, text="문이 열렸습니다. 물건을 가져가세요")

        self.canvas.after(100, lambda: self.__listen_item(False))

        # 물건이 존재하지 않으면 바로 넘어감
        if self.has_item.get():
            self.canvas.wait_variable(self.has_item)

        self.canvas.itemconfig(self.text_id, text="사용이 완료되었습니다. 문을 닫아주세요.")
        sleep(2)

        # 물건을 가져갔으면 그 즉시 WAIT로 변경
        sql.processDB(
            f"UPDATE LCKStat SET UseStat='{LockerFrame.STATE_WAIT}' WHERE USRMngKey='{user_key}';"
        )
        sqlDict = {'CRRMngKey': self.CRRMngKey,
                   'USRMngKey': user_key, 'UseStat': 'W'}
        sql.processDB(dict2Query('LCKLog', sqlDict))

        self.canvas.after(100, self.__listen_door)
        self.canvas.wait_variable(self.is_door_open)
        self.canvas.itemconfig(self.text_id, text="문을 닫고있습니다.")

        self.ratch.execute(self.sync_sensor, "C")
        sleep(2)

        if mode == RESIDENTIAL_MODE:
            # 완료메시지 표시
            MessageFrame(self.controller, "완료되었습니다.")

            # 일반화면으로 이동
            self.controller.show_frame("StartPage", self)

        # 쓰레드화 되어있는 상태면 자신 삭제
        elif mode == COMMERCIAL_MODE:
            self.destroy()

    def __listen_item(self, flag=True):
        if (flag and not self.locker_state.has_item(self.CRRMngKey)) or (not flag and self.locker_state.has_item(self.CRRMngKey)):
            self.escape_has_item = self.canvas.after(1, self.__listen_item)
        else:
            self.has_item.set(flag)
            if self.escape_has_item:
                self.canvas.after_cancel(self.escape_has_item)  # after 중지

    def __listen_door(self):
        if self.locker_state.is_door_open(self.CRRMngKey):
            self.escape_open_door = self.canvas.after(1, self.__listen_door)
        else:
            self.is_door_open.set(False)
            if self.escape_open_door:
                self.canvas.after_cancel(self.escape_open_door)  # after 중지
