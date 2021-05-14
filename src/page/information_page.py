import os
import sys
if __name__:
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    from utils.util import *
    from utils.sql import SQL


class InformationPage(tk.Frame):
    """
    함을 클릭했을 때 사용자 정보를 입력할 프레임입니다.
    """

    def __init__(self, parent, controller, bg, *args, **kwargs):
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
        self.CRRMngKey = kwargs["CRRMngKey"]
        page = kwargs["page"]
        self.index = 0
        entry = tk.Entry(self, font=controller.large_font)
        if page == "AdminPage":
            entry.insert(0, "H")
            self.index += 1
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
            if page != "AdminPage":
                self.index = self.index-1 if self.index > 0 else 0
            else:
                self.index = self.index-1 if self.index > 1 else 1

        for i in button_name_list:
            SMLButton(master=number_frame,
                      text_font=controller.large_font,
                      text=i,
                      border_width=1,
                      width=100,
                      height=100,
                      command=lambda button_num=i, entry=entry: insert_text(
                          button_num, entry) if button_num.isnumeric() else delete_text(entry) if button_num == "<<" else self.__set_locker_key(entry.get()) if page == "AdminPage" else self.__verify_phone_number(entry.get(), page)
                      ).grid(row=row, column=col)
            row = row+1 if col == 2 else row
            col = 0 if col == 2 else col+1

        entry.place(x=controller.width/2,
                    y=controller.height/5, anchor=tk.CENTER)
        number_frame.place(x=controller.width/2,
                           y=controller.height/2, anchor=tk.CENTER)

    def __get_user_key(self, phone_number: str):
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

    def __verify_phone_number(self, phone_number, page):
        """
        휴대폰 번호를 확인하고, 맞다면 process함수로 넘어갑니다.
        """
        user_check = ["test"]
        if len(phone_number) != 11 or phone_number[:3] != "010":
            MessageFrame(self.controller, "오류! 정확한 번호를 입력해주세요")
            return
        phone_format_number = f"{phone_number[:3]}-{phone_number[3:7]}-{phone_number[7:]}"
        message_frame = MessageFrame(
            self.controller, f"{phone_format_number}가 맞습니까?", user_check=user_check, flag=ASK)
        self.wait_window(message_frame)
        if user_check[0] == "yes":
            user_key = self.__get_user_key(phone_number)
            self.controller.show_frame(
                "ProcessPage", frame=self, CRRMngKey=self.CRRMngKey, page=page, USRMngKey=user_key, phone_number=phone_number)

    def __set_locker_key(self, locker_manage_key: str):
        """입력받은 LCKMngKey를 가지고 sync_to_json합니다.
        """
        sql = SQL("root", "", "10.80.76.63", "SML")
        manage_key_list = list(map(lambda dic: dic["LCKMngKey"], sql.processDB(
            "SELECT LCKMngKey FROM LCKInfo;"
        )))
        if locker_manage_key not in manage_key_list:
            MessageFrame(self.controller, "실패! 존재하지 않는 키입니다")
            return

        self.controller.sync_to_json(locker_manage_key)
