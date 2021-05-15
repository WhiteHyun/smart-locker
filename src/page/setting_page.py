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

        canvas = tk.Canvas(self, width=controller.width,
                           height=controller.height, bg=bg)
        canvas.pack(fill="both", expand=True)
        self.mode = kwargs["mode"]
        canvas.create_text(controller.width/2, controller.height/7,
                           text="설정 페이지 (관리자)", font=controller.title_font, fill="#385ab7")

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
                  ).place(x=controller.width-180, y=200)

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
        ratch.execute(result, "O")

    def __load_locker(self, mode):
        """LockerFrame을 로드합니다.
        """

        locker_frame = LockerFrame(
            parent=self, controller=self.controller, page="SettingPage", mode=mode, relief="solid")
        locker_frame.place(x=self.controller.width/2,
                           y=self.controller.height/2, anchor=tk.CENTER)
        return locker_frame

    def __change_locker(self, mode):
        """locker의 모드를 바꿉니다
        """
        # 기존 모드와 동일한 경우
        if self.mode == mode:
            return

        self.locker_frame.destroy()
        self.locker_frame = self.__load_locker(mode)
