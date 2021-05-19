import os
import sys
if __name__:
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    from utils.util import *
    from utils.sql import SQL

if __name__ == "__main__" or __name__ == "fix_page":
    from locker_frame import LockerFrame
else:
    from .locker_frame import LockerFrame


class SettingPage(tk.Frame):
    """
    맡기기 버튼을 눌렀을 때 보여지는 프레임입니다.
    사물함의 위치 및 상태가 gui로 보여집니다.
    """

    def __init__(self, parent, controller, bg, *args, **kwargs):
        super().__init__(parent)
        controller.sync_to_json()
        self.controller = controller

        previous_arrow_img = ImageTk.PhotoImage(Image.open(
            "../img/previous.png" if __name__ == "__main__" or __name__ == "setting_page" else "src/img/previous.png"
        ).resize((int(100/1.618), int(100/1.618))))
        fix_img = ImageTk.PhotoImage(Image.open(
            "../img/support.png" if __name__ == "__main__" or __name__ == "setting_page" else "src/img/support.png"
        ).resize((int(100/1.618), int(100/1.618))))

        unlock_img = ImageTk.PhotoImage(Image.open(
            "../img/unlock.png" if __name__ == "__main__" or __name__ == "setting_page" else "src/img/unlock.png"
        ).resize((int(100/1.618), int(100/1.618))))
        open_img = ImageTk.PhotoImage(Image.open(
            "../img/open.png" if __name__ == "__main__" or __name__ == "setting_page" else "src/img/open.png"
        ).resize((int(100/1.618), int(100/1.618))))
        closed_img = ImageTk.PhotoImage(Image.open(
            "../img/closed.png" if __name__ == "__main__" or __name__ == "setting_page" else "src/img/closed.png"
        ).resize((int(100/1.618), int(100/1.618))))

        self.canvas = tk.Canvas(self, width=controller.width,
                                height=controller.height, bg=bg)
        self.canvas.pack(fill="both", expand=True)
        self.mode = kwargs["mode"]
        self.door_state = "O"
        self.canvas.create_text(controller.width/2, controller.height/7,
                                text="설정 페이지 (관리자)", font=controller.title_font, fill="#385ab7")
        self.button_group = tk.Frame(master=self)
        self.open_button = SMLButton(master=self.button_group,
                                     border_width=1,
                                     width=160,
                                     height=100,
                                     image=open_img,
                                     text="열기 모드",
                                     command=lambda: self.set_door_state("O"))
        self.closed_button = SMLButton(master=self.button_group,
                                       border_width=1,
                                       fg_color="#7C7877",
                                       hover_color="#7C7877",
                                       width=160,
                                       height=100,
                                       image=closed_img,
                                       text="닫기 모드",
                                       command=lambda: self.set_door_state("C"))

        self.open_button.pack(side="top", fill="both", expand=True)
        self.closed_button.pack(side="bottom", fill="both", expand=True)
        self.locker_frame = self.__load_locker(self.mode)

        SMLButton(master=self,
                  text="관리페이지로",
                  border_width=1,
                  width=100,
                  height=100,
                  image=previous_arrow_img,
                  command=lambda: controller.show_frame(
                      "AdminPage", self
                  )
                  ).place(x=20, y=controller.height-120)

        SMLButton(master=self,
                  text="고장 유무 설정",
                  border_width=1,
                  width=160,
                  height=100,
                  image=fix_img,
                  command=lambda: self.__change_locker(LockerFrame.FIX_MODE)
                  ).place(x=controller.width-180, y=20)

        SMLButton(master=self,
                  text="문 강제 개폐",
                  border_width=1,
                  width=160,
                  height=100,
                  image=unlock_img,
                  command=lambda: self.__change_locker(LockerFrame.UNLOCK_MODE)
                  ).place(x=controller.width-180, y=140)
        self.__show_door_mode_button(self.mode)

    def set_door_state(self, state):
        """문 개폐 모드를 설정합니다.

        모드 종류:
            `Open mode`
            `Closed mode`
        """
        # 기존과 같은 경우에는 단순리턴
        if self.door_state == state:
            return
        # 오픈상태로 바꿀예정인가?
        if state == "O":
            self.open_button.configure_color(fg_color="#385ab7",
                                             hover_color="#496bc9")
            self.closed_button.configure_color(fg_color="#7C7877",
                                               hover_color="#7C7877")
        elif state == "C":
            self.closed_button.configure_color(fg_color="#385ab7",
                                               hover_color="#496bc9")
            self.open_button.configure_color(fg_color="#7C7877",
                                             hover_color="#7C7877")
        else:   # dangerous!
            print("!DANGEROUS! PLESASE FIX ME!!")
            return
        self.door_state = state

    def set_locker(self, CRRMngKey, current_state, locker_number):
        """함의 고장유무를 설정합니다.
        """
        sql = SQL("root", "", "10.80.76.63", "SML")
        sql.processDB(
            f"UPDATE LCKStat SET UseStat='{LockerFrame.STATE_WAIT if current_state == LockerFrame.STATE_BROKEN else LockerFrame.STATE_BROKEN}' WHERE CRRMngKey='{CRRMngKey}';"
        )
        self.locker_frame.button_dict[locker_number].configure_color(
            fg_color="#1E8449" if current_state == LockerFrame.STATE_BROKEN else"#7C7877",
            hover_color="#2ECC71" if current_state == LockerFrame.STATE_BROKEN else"#7C7877")
        state = LockerFrame.STATE_WAIT if current_state == LockerFrame.STATE_BROKEN else LockerFrame.STATE_BROKEN
        self.locker_frame.button_dict[locker_number].function = lambda: self.set_locker(
            CRRMngKey, state, locker_number)
        self.controller.sync_to_json()  # json sync

    def force_open_door(self, CRRMngKey):
        """함의 문을 강제개방합니다.
        """
        from utils.ratchController import RatchController
        sql = SQL("root", "", "10.80.76.63", "SML")
        result = sql.processDB(
            f"SELECT SyncSensor FROM CRRInfo WHERE CRRMngKey='{CRRMngKey}';")
        assert result is not None
        result = result[0]["SyncSensor"]
        ratch = RatchController.instance()
        ratch.execute(result, self.door_state)

    def __load_locker(self, mode):
        """LockerFrame을 로드합니다.
        """

        locker_frame = LockerFrame(
            parent=self, controller=self.controller, page="SettingPage", mode=mode, relief="solid")
        locker_frame.place(x=self.controller.width/2,
                           y=self.controller.height/2, anchor=tk.CENTER)
        return locker_frame

    def __show_door_mode_button(self, mode):
        """모드에 따라 문 개폐버튼을 보여줄지 말지 결정합니다
        """
        # 강제개폐 설정모드일 경우 문 여닫기버튼 띄워줌
        if mode == LockerFrame.UNLOCK_MODE:
            self.button_group.place(
                x=self.controller.width-180, y=260)
        # 고장상태 설정모드일 경우 여닫기 버튼 지워줌
        elif mode == LockerFrame.FIX_MODE:
            self.button_group.place_forget()

    def __change_locker(self, mode):
        """locker의 모드를 바꿉니다
        """
        # 기존 모드와 동일한 경우
        if self.mode == mode:
            return
        self.__show_door_mode_button(mode)
        self.mode = mode
        self.locker_frame.destroy()
        self.locker_frame = self.__load_locker(mode)
