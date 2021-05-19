import os
import sys
if __name__:
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    from utils.util import *
    from utils.sql import SQL


if __name__ == "__main__" or __name__ == "information_page":
    from input_frame import InputFrame
else:
    from .input_frame import InputFrame

NUMBER_ERROR = 0
NO_SIGN_ERROR = 1
FAILED_ERROR = 2
DEFAULT_MODE = 0
VERIFY_MODE = 1
ADMIN_MODE = 2
GO_TO_SETTING_MODE = 3
COMMERCIAL_MODE = 2


class InformationPage(tk.Frame):
    """
    정보를 입력받는 프레임입니다.
    """

    def __init__(self, parent, controller, bg, mode, verified_number=None, *args, **kwargs):
        super().__init__(parent)

        previous_arrow_img = ImageTk.PhotoImage(Image.open(
            "../img/previous.png" if __name__ == "__main__" or __name__ == "information_page" else "src/img/previous.png"
        ).resize((int(100/1.618), int(100/1.618))))

        self.canvas = tk.Canvas(self, width=controller.width,
                                height=controller.height, bg=bg)
        self.canvas.pack(fill="both", expand=True)
        self.controller = controller
        self.mode = mode
        self.page = kwargs["page"]
        text_id = self.canvas.create_text(controller.width/2,
                                          controller.height/10,
                                          text="empty",
                                          font=controller.title_font if mode != VERIFY_MODE else controller.subtitle_font,
                                          fill="#385ab7")

        if self.mode == ADMIN_MODE:
            text = "사물함 관리번호를 입력해주세요"
        elif self.mode == GO_TO_SETTING_MODE:
            text = "관리자 비밀번호를 입력해주세요"
        else:
            self.CRRMngKey = kwargs["CRRMngKey"]
            if self.mode == DEFAULT_MODE:
                text = "휴대폰 번호를 입력해주세요"
            elif self.mode == VERIFY_MODE:
                self.tried = 0
                self.verified_number = verified_number
                self.user_key = kwargs["USRMngKey"]
                text = "인증번호를 전송했습니다. 인증번호를 입력해주세요"

        self.canvas.itemconfig(text_id, text=text)
        entry = tk.Entry(self, font=controller.large_font)

        number_frame = InputFrame(parent=self,
                                  controller=self.controller,
                                  entry=entry,
                                  mode=mode)
        SMLButton(master=self,
                  text="이전으로",
                  border_width=1,
                  width=100,
                  height=100,
                  image=previous_arrow_img,
                  command=lambda: controller.show_frame(
                      self.page, self
                  )
                  ).place(x=20, y=controller.height-120)
        entry.place(x=controller.width/2,
                    y=controller.height/5, anchor=tk.CENTER)
        number_frame.place(x=controller.width/2,
                           y=controller.height/2, anchor=tk.CENTER)

    def __get_user_key(self, phone_number: str) -> str:
        """
        휴대폰 번호를 받아 유저를 생성하여 데이터베이스에 저장한 후 유저관리번호를 리턴합니다.
        만약 이미 존재하는 경우 존재하는 유저관리번호를 리턴합니다.
        """
        sql = SQL("root", "", "10.80.76.63", "SML")
        result = sql.processDB(
            f"SELECT USRMngKey FROM USRInfo WHERE USRTellNo='{phone_number}';")

        # 해당 유저가 등록되지 않은 경우
        if not result:
            recent_user_key = sql.processDB(
                "SELECT USRMngKey FROM USRInfo ORDER BY USRInfoKey DESC LIMIT 1;")[0]["USRMngKey"]
            user_key = recent_user_key[:1] + str(int(recent_user_key[1:])+1)
            # FIXME: USRDis를 강제적으로 A로 만듦. 후에 수정 필요!
            sql.processDB(
                f"INSERT INTO USRInfo(USRMngKey, USRTellNo, USRDis) values('{user_key}', '{phone_number}', 'A');")
            return user_key
        else:
            return result[0]["USRMngKey"]

    def __verify_number(self, number):
        """
        입력받은 번호를 확인하고, 검증합니다.
        """
        user_check = [""]

        if self.mode == DEFAULT_MODE:
            # 올바르지 않는 전화번호
            if len(number) != 11 or number[:3] != "010":
                return False, NUMBER_ERROR
            format_number = f"{number[:3]}-{number[3:7]}-{number[7:]}"
        else:
            format_number = number

        # 번호가 맞는지 물어봄
        message_frame = MessageFrame(
            self.controller, f"입력하신 {format_number}가 맞습니까?", user_check=user_check, flag=ASK)
        self.wait_window(message_frame)

        # No!
        if user_check[0] != "yes":
            return False, NO_SIGN_ERROR

        # ok verify time!
        sql = SQL("root", "", "10.80.76.63", "SML")
        if self.mode == DEFAULT_MODE:
            user_key = self.__get_user_key(number)
            # 찾기 페이지일 때 동일한 번호인지 처리
            if self.page == "FindPage":
                result = sql.processDB(
                    f"SELECT * FROM LCKStat WHERE CRRMngKey='{self.CRRMngKey}';")

                # 다른 번호일 경우
                if not result or result[0]["USRMngKey"] != user_key:
                    return False, FAILED_ERROR
            return True, user_key
        elif self.mode == VERIFY_MODE:
            if self.verified_number == number:
                return True, self.user_key
            else:
                return False, NUMBER_ERROR
        elif self.mode == ADMIN_MODE:
            manage_key_list = list(map(lambda dic: dic["LCKMngKey"], sql.processDB(
                "SELECT LCKMngKey FROM LCKInfo;"
            )))
            # 입력받은 관리번호가 존재하지 않는 경우
            if number not in manage_key_list:
                return False, FAILED_ERROR
            # 아두이노 연결이 되어있는가
            result = sql.processDB(
                f"SELECT Port FROM ARDInfo WHERE LCKMngKey='{number}' AND ARDKind='R' ORDER BY ARDNum;")
            if not result or result[0]["Port"] is None:
                return False, NUMBER_ERROR
            return True, None

        elif self.mode == GO_TO_SETTING_MODE:
            if number == "1234":
                return True, None
            else:
                return False, FAILED_ERROR

    def __set_locker_key(self, locker_manage_key: str) -> None:
        """입력받은 LCKMngKey를 가지고 sync_to_json합니다.
        """

        self.controller.sync_to_json(locker_manage_key)
        from utils.ratchController import RatchController
        RatchController.instance()

    def __send_random_number_message(self, phone_number, text):
        """사용자에게 메시지를 보냅니다."""
        from utils.sms import Messenger
        messenger = Messenger.SMS(
            to=phone_number,
            text=f"[인증번호:{text}] INU 통합보관함 인증번호입니다")
        if not messenger.send_message():
            MessageFrame(self.controller, "문자전송에 실패 하였습니다. 다시 시도해주세요")
            return

    def check_and_show_page(self, number):
        from random import randint
        result, code = self.__verify_number(number)
        if result:
            if self.mode == ADMIN_MODE:
                self.__set_locker_key(number)
                MessageFrame(self.controller, "사물함번호가 설정되었습니다")
                self.controller.show_frame(
                    new_frame="AdminPage",
                    frame=self)

            elif self.mode == GO_TO_SETTING_MODE:
                self.controller.show_frame(new_frame="AdminPage",
                                           frame=self)

            elif self.page == "FindPage" and self.mode == DEFAULT_MODE:
                verified_number = f"{randint(0, 999999):06d}"
                self.__send_random_number_message(number, verified_number)
                self.controller.show_frame(
                    new_frame="InformationPage",
                    frame=self,
                    CRRMngKey=self.CRRMngKey,
                    page=self.page,
                    USRMngKey=code,
                    mode=VERIFY_MODE,
                    phone_number=number,
                    verified_number=verified_number)
            else:
                # 해당 함의 쓰레드가 동작하고 있는 경우 Kill
                if self.page == "DeliveryPage" and self.controller.mode == COMMERCIAL_MODE:
                    for page in self.controller.container.winfo_children():
                        if page.__class__.__name__ == "ProcessPage" and page.CRRMngKey == self.CRRMngKey:
                            page.destroy()

                self.controller.show_frame(
                    new_frame="ProcessPage",
                    frame=self,
                    CRRMngKey=self.CRRMngKey,
                    page=self.page,
                    USRMngKey=code,
                    phone_number=number)
        # 실패메시지 표시
        else:
            if self.mode == VERIFY_MODE:
                self.tried += 1
                if self.tried < 3:
                    MessageFrame(self.controller,
                                 text=f"틀린 인증번호입니다. (3회 제한 중 {self.tried}회 시도함)")
                else:
                    MessageFrame(self.controller, "3회 실패로 처음화면으로 돌아갑니다")
                    self.controller.show_frame(
                        new_frame="StartPage",
                        frame=self
                    )
            elif code == NUMBER_ERROR:
                MessageFrame(self.controller, "실패! 번호를 다시 입력해주세요")
            elif code == FAILED_ERROR:
                MessageFrame(self.controller, "실패! 올바르지 않는 값입니다")
