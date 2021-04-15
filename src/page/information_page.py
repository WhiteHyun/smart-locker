import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.util import *
from utils.sql import SQL

if __name__ == "__main__" or __name__ == "information_page":
    from locker_frame import LockerFrame
else:
    from .locker_frame import LockerFrame


class InformationPage(tk.Frame):
    """
    함을 클릭했을 때 사용자 정보를 입력할 프레임입니다.
    """

    def __init__(self, parent, controller, CRRMngKey, page, bg):
        super().__init__(parent)

        previous_arrow_img = ImageTk.PhotoImage(Image.open(
            "../img/previous.png" if __name__ == "__main__" or __name__ == "information_page" else "src/img/previous.png"
        ).resize((int(100/1.618), int(100/1.618))))

        canvas = tk.Canvas(self, width=controller.width,
                           height=controller.height, bg=bg)
        canvas.pack(fill="both", expand=True)

        canvas.create_text(controller.width/2, controller.height/10,
                           text="휴대폰 번호를 입력해주세요.", font=controller.title_font, fill="#385ab7")

        self.controller = controller
        self.CRRMngKey = CRRMngKey
        self.index = 0
        entry = tk.Entry(self, font=controller.large_font)
        number_frame = tk.Frame(self)
        SMLButton(master=self,
                  text="이전으로",
                  border_width=1,
                  width=100,
                  height=100,
                  image=previous_arrow_img,
                  command=lambda: controller.show_frame(
                      page, self
                  )
                  ).place(x=20, y=controller.height-120)

        row = 0
        col = 0
        button_name_list = ["1", "2", "3", "4", "5",
                            "6", "7", "8", "9", "<<", "0", "확인"]

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
            user_check = askquestion(
                "번호 확인", f"{phone_format_number}가 맞습니까?"
            )
            if user_check == "yes":
                user_key = self.make_user_key(phone_number)
                if page == "DeliveryPage":
                    self.__process_delivery(user_key, phone_number)
                elif page == "FindPage":
                    self.__find_delivery(user_key)

        for i in button_name_list:
            SMLButton(master=number_frame,
                      text_font=controller.large_font,
                      text=i,
                      border_width=1,
                      width=100,
                      height=100,
                      command=lambda button_num=i, entry=entry: insert_text(
                          button_num, entry) if button_num.isnumeric() else delete_text(entry) if button_num == "<<" else verify_phone_number(entry.get())
                      ).grid(row=row, column=col)
            row = row+1 if col == 2 else row
            col = 0 if col == 2 else col+1

        entry.place(x=controller.width/2,
                    y=controller.height*2/10, anchor=tk.CENTER)
        number_frame.place(x=controller.width/2,
                           y=controller.height/2, anchor=tk.CENTER)

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

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # datetime 포맷값
        value = self.CRRMngKey+user_key+time
        hash_value = encrypt(value)
        # QR코드 생성 실패시 다시 시도
        if not generateQR(hash_value):
            showerror("에러!", "qr코드 생성에 실패하였습니다.")
            sleep(2)
            self.__process_delivery(user_key, phone_number)

        # TODO: #17 택배함이 열리고 물건넣고 닫은 후의 과정을 넣어야 함

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
            showerror(message="문자전송에 실패 하였습니다.")

        # 완료 메시지 표시
        top = tk.Toplevel()
        tk.Message(top, text="완료되었습니다.", padx=20, pady=20).pack()
        top.after(7000, top.destroy)

        # 일반화면으로 이동
        self.controller.show_frame("StartPage", self)

    def __find_delivery(self, user_key):
        """
        택배함을 열어 유저가 택배를 가져갈 수 있게 처리해줍니다.
        """
        # TODO: #17 택배함이 열리고 택배함에 물건을 가져가고 문을 닫는 등의 확인절차 필요

        sql = SQL("root", "", "10.80.76.63", "SML")

        # TODO: USRMngKey값이 phone_number로 현재는 대체중이며 나중에 바꿔야함!
        if sql.processDB(f"SELECT * FROM LCKStat WHERE CRRMngKey='{self.CRRMngKey}';"):
            sql.processDB(
                f"UPDATE LCKStat SET UseStat='{LockerFrame.STATE_WAIT}' WHERE USRMngKey='{user_key}';"
            )

        # 완료메시지 표시
        success_message(self.controller)

        # 일반화면으로 이동
        self.controller.show_frame("StartPage", self)

    def make_user_key(self, phone_number: str):
        """
        휴대폰 번호를 받아 유저를 생성하여 데이터베이스에 저장한 후 관리번호를 리턴합니다.
        만약 이미 존재하는 경우 존재하는 관리번호를 리턴합니다.
        """
        sql = SQL("root", "", "10.80.76.63", "SML")
        result = sql.processDB(
            f"SELECT USRMngKey FROM USRInfo WHERE USRTellNo='{phone_number}';")

        # 해당 유저가 등록되지 않은 경우
        if not result:
            recent_user_key = sql.processDB(
                "SELECT USRMngKey FROM USRInfo ORDER BY USRMngKey DESC LIMIT 1;")[0]["USRMngKey"]
            user_key = recent_user_key[:-1] + str(int(recent_user_key[-1])+1)
            # FIXME: USRDis를 강제적으로 A로 만듦. 후에 수정 필요!
            sql.processDB(
                f"INSERT INTO USRInfo(USRMngKey, USRTellNo, USRDis) values('{user_key}', '{phone_number}', 'A');")
            return user_key
        else:
            return result[0]["USRMngKey"]
