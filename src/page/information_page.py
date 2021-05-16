import os
import sys
if __name__:
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    from utils.util import *
    from utils.sql import SQL

NUMBER_ERROR = 0
NO_SIGN_ERROR = 1
FAILED_ERROR = 2


class InformationPage(tk.Frame):
    """
    정보를 입력받는 프레임입니다.
    """

    def __init__(self, parent, controller, bg, *args, **kwargs):
        super().__init__(parent)

        page = kwargs["page"]
        previous_arrow_img = ImageTk.PhotoImage(Image.open(
            "../img/previous.png" if __name__ == "__main__" or __name__ == "information_page" else "src/img/previous.png"
        ).resize((int(100/1.618), int(100/1.618))))

        canvas = tk.Canvas(self, width=controller.width,
                           height=controller.height, bg=bg)
        canvas.pack(fill="both", expand=True)

        canvas.create_text(controller.width/2, controller.height/10,
                           text="사물함관리번호를 입력하세요" if page == "AdminPage" else "휴대폰 번호를 입력해주세요.", font=controller.title_font, fill="#385ab7")

        self.controller = controller
        self.index = 0
        entry = tk.Entry(self, font=controller.large_font)

        if page == "AdminPage":
            entry.insert(0, "H")
            self.index += 1
        else:
            self.CRRMngKey = kwargs["CRRMngKey"]
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
            if page == "AdminPage" and self.index == 1:
                return
            entry.delete(self.index-1)
            self.index = self.index-1 if self.index > 0 else 0

        for i in button_name_list:
            SMLButton(master=number_frame,
                      text_font=controller.large_font,
                      text=i,
                      border_width=1,
                      width=100,
                      height=100,
                      command=lambda button_num=i, entry=entry: insert_text(
                          button_num, entry) if button_num.isnumeric() else delete_text(entry) if button_num == "<<" else self.__check_and_show_page(entry.get(), page)
                      ).grid(row=row, column=col)
            row = row+1 if col == 2 else row
            col = 0 if col == 2 else col+1

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

    def __verify_number(self, number, page):
        """
        입력받은 번호를 확인하고, 검증합니다.
        """
        user_check = [""]
        if page != "AdminPage":
            if len(number) != 11 or number[:3] != "010":
                # 올바르지 않는 전화번호
                return False, NUMBER_ERROR
            format_number = f"{number[:3]}-{number[3:7]}-{number[7:]}"
        else:
            format_number = number

        # 번호가 맞는지 물어봄
        message_frame = MessageFrame(
            self.controller, f"{format_number}가 맞습니까?", user_check=user_check, flag=ASK)
        self.wait_window(message_frame)

        # No!
        if user_check[0] != "yes":
            return False, NO_SIGN_ERROR

        # ok verify time!
        sql = SQL("root", "", "10.80.76.63", "SML")
        if page != "AdminPage":
            user_key = self.__get_user_key(number)
            # 찾기 페이지일 때 동일한 번호인지 처리
            if page == "FindPage":
                result = sql.processDB(
                    f"SELECT * FROM LCKStat WHERE CRRMngKey='{self.CRRMngKey}';")

                # 다른 번호일 경우
                if not result or result[0]["USRMngKey"] != user_key:
                    return False, FAILED_ERROR
            return True, user_key
        else:
            manage_key_list = list(map(lambda dic: dic["LCKMngKey"], sql.processDB(
                "SELECT LCKMngKey FROM LCKInfo;"
            )))
            # 입력받은 관리번호가 존재하지 않는 경우
            if number not in manage_key_list:
                return False, FAILED_ERROR
            # 아두이노 연결이 되어있는가
            result = sql.processDB(
                f"SELECT Port FROM ARDInfo WHERE LCKMngKey='{number}' AND ARDKind='R' ORDER BY ARDNum;")
            if result and result[0]["Port"] is not None:
                return False, NUMBER_ERROR
            return True, None

    def __set_locker_key(self, locker_manage_key: str) -> None:
        """입력받은 LCKMngKey를 가지고 sync_to_json합니다.
        """

        self.controller.sync_to_json(locker_manage_key)
        from utils.ratchController import RatchController
        RatchController.instance()

    def __check_and_show_page(self, number, page):
        result, code = self.__verify_number(number, page)
        if result:
            if page == "AdminPage":
                self.__set_locker_key(number)
                MessageFrame(self.controller, "사물함번호가 설정되었습니다")
                self.controller.show_frame("AdminPage", self)

            else:
                self.controller.show_frame(
                    "ProcessPage", frame=self, CRRMngKey=self.CRRMngKey, page=page, USRMngKey=code, phone_number=number)
        # 실패메시지 표시
        else:
            if code == NUMBER_ERROR:
                MessageFrame(self.controller, "실패! 번호를 다시 입력해주세요")
            elif code == FAILED_ERROR:
                MessageFrame(self.controller, "실패! 올바르지 않는 값입니다")
