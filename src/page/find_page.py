import os
import sys
import cv2
if __name__:
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    from utils.util import *

if __name__ == "__main__" or __name__ == "find_page":
    from locker_frame import LockerFrame
else:
    from .locker_frame import LockerFrame

RESIDENTIAL_MODE = 1
COMMERCIAL_MODE = 2


class FindPage(tk.Frame):
    """
    찾기 페이지입니다.
    """

    def __init__(self, parent, controller, bg, *args, **kwargs):
        super().__init__(parent)
        controller.sync_to_json()
        self.controller = controller
        self.camera = cv2.VideoCapture(0)
        # after 함수를 종료시키기 위한 탈출 id
        self.escape = ""

        previous_arrow_img = ImageTk.PhotoImage(Image.open(
            "../img/previous.png" if __name__ == "__main__" or __name__ == "find_page" else "src/img/previous.png"
        ).resize((int(100/1.618), int(100/1.618))))

        self.canvas = tk.Canvas(self, width=controller.width,
                                height=controller.height, bg=bg)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(controller.width/2, controller.height*0.36,
                                text="QR코드를 이용하실 분은 QR코드를 화면에 보여지게 해주세요.", font=controller.large_font)
        # 캠을 보여줄 label 객체
        self.label = tk.Label(width=300, height=250)
        self.label.place(x=controller.width/2-150, y=10)

        LockerFrame(parent=self, controller=controller, page="FindPage", relief="solid").place(
            x=controller.width/2, y=controller.height*0.66, anchor=tk.CENTER)

        SMLButton(master=self,
                  text="이전으로",
                  border_width=1,
                  width=100,
                  height=100,
                  image=previous_arrow_img,
                  command=lambda: controller.show_frame(
                      "StartPage", frame=self
                  )
                  ).place(x=20, y=controller.height-120)

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
            hash_data = detectQR(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
            img = cv2.resize(img, (300, 250))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.flip(img, 1)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            self.label.configure(image=img)
            self.label.image = img

            # 받아오지 못한 경우 단순 리턴
            if hash_data is None:
                self.escape = self.label.after(1, self.__open_door_by_qrcode)
                return

            sql = SQL("root", "", "10.80.76.63", "SML")
            result = sql.processDB(
                f"SELECT * FROM LCKStat WHERE HashKey='{hash_data}';"
            )
            if not result:
                raise ValueError
            result = result[0]
            if self.controller.mode == COMMERCIAL_MODE:
                self.controller.show_frame(new_frame="ProcessPage",
                                           CRRMngKey=result["CRRMngKey"],
                                           page="FindPage",
                                           USRMngKey=result["USRMngKey"])
                self.controller.show_frame(new_frame="StartPage",
                                           frame=self)
            else:
                self.controller.show_frame(new_frame="ProcessPage",
                                           frame=self,
                                           CRRMngKey=result["CRRMngKey"],
                                           page="FindPage",
                                           USRMngKey=result["USRMngKey"])

        except ValueError as e:
            MessageFrame(self.controller, "존재하지 않는 QR코드입니다.")
        except Exception as e:
            raise e

    def destroy(self) -> None:
        self.label.after_cancel(self.escape)    # 카메라 실행 중지
        self.camera.release()   # 카메라 모듈 사용 해제
        self.label.destroy()    # 캠을 가지고있는 레이블 삭제
        super().destroy()
