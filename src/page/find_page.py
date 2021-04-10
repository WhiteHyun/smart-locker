import os
import sys
import cv2
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.util import *

if __name__ == "__main__" or __name__ == "find_page":
    from locker_frame import LockerFrame
else:
    from .locker_frame import LockerFrame


class FindPage(tk.Frame):
    """
    찾기 페이지입니다.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.camera = cv2.VideoCapture(0)
        # after 함수를 종료시키기 위한 탈출 id
        self.escape = ""
        # 캠을 보여줄 label 객체
        self.label = tk.Label(width=300, height=250)
        self.label.place(x=controller.width/2-150,
                         y=10)

        tk.Label(self, text="QR코드를 이용하실 분은 QR코드를 화면에 보여지게 해주세요.", font=controller.large_font).pack(
            pady=(controller.height/3, 0))

        locker_frame = LockerFrame(
            parent=self, controller=controller, page="FindPage", relief="solid")
        locker_frame.pack(pady=20)

        SMLButton(master=self,
                  text="이전으로",
                  border_width=1,
                  width=100,
                  height=100,
                  command=lambda: controller.show_frame(
                      "StartPage", self
                  )
                  ).place(x=20, y=controller.height-170)

        self.__open_door_by_qrcode()

    def __open_door_by_qrcode(self):
        """
        QR코드를 통해 문을 열게 해주는 함수입니다.
        """

        from utils.qrcodes import detectQR, VideoError
        from utils.sql import SQL
        try:

            # 프레임 받아오기 -> ret: 성공하면 True, 아니면 False, img: 현재 프레임(numpy.ndarray)
            ret, img = self.camera.read()
            if not ret:  # 카메라 캡처에 실패할 경우
                print("camera read failed")
                raise VideoError

            # 흑백이미지로 변환하여 qr 디코드
            result_data = detectQR(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
            # 받아오지 못한 경우 단순 리턴

            img = cv2.resize(img, (300, 250))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            self.label.configure(image=img)
            self.label.image = img
            if result_data is None:
                self.escape = self.label.after(1, self.__open_door_by_qrcode)
                return

            sql = SQL("root", "", "10.80.76.63", "SML")
            result = sql.processDB(
                f"SELECT * FROM LCKStat WHERE HashKey='{result_data}';"
            )
            if not result:
                raise ValueError
            # TODO: #19 result 값을 가지고 함의 문을 열어줌
            # TODO: 문이 닫히고 나서 센서값을 가져와 물건을 잘 찾아갔다고 판단되는 경우 데이터베이스 갱신 후 기존화면으로 이동

            # 데이터베이스 갱신
            sql.processDB(
                f"UPDATE LCKStat SET UseStat='{LockerFrame.STATE_WAIT}' WHERE HashKey='{result_data}';"
            )

            # 완료 메시지 표시
            top = tk.Toplevel()
            tk.Message(top, text="완료되었습니다.", padx=20, pady=20).pack()
            top.after(7000, top.destroy)
            # 카메라 모듈 사용 해제
            self.camera.release()
            # 기존 화면으로 이동
            self.controller.show_frame("StartPage", self)
        except ValueError as e:
            showerror("오류!", "존재하지 않는 QR코드입니다.")
        except Exception as e:
            raise e

    def destroy(self) -> None:
        super().destroy()
        self.label.after_cancel(self.escape)
        self.camera.release()
        self.label.destroy()
