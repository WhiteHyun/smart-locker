import cv2
if __name__ == "__main__" or __name__ == "ui":
    from utils.util import *
    from page.find_page import FindPage
    from page.delivery_page import DeliveryPage
    from page.information_page import InformationPage
    from page.start_page import StartPage
    from page.process_page import ProcessPage
    from page.admin_page import AdminPage
    from page.setting_page import SettingPage
    from page.screensaver_page import ScreenSaverPage

else:
    from .utils.util import *
    from .page.find_page import FindPage
    from .page.delivery_page import DeliveryPage
    from .page.information_page import InformationPage
    from .page.start_page import StartPage
    from .page.process_page import ProcessPage
    from .page.admin_page import AdminPage
    from .page.setting_page import SettingPage
    from .page.screensaver_page import ScreenSaverPage

RESIDENTIAL_MODE = 1
COMMERCIAL_MODE = 2


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        from utils.rasp_sensor import DetectMotion
        super().__init__(*args, **kwargs)

        # 화면 설정
        self.geometry(
            f"{super().winfo_screenwidth()}x{super().winfo_screenheight()}+0+0"
        )
        super().attributes('-type', 'splash')
        # 화면에 보여질 컨테이너 생성
        self.container = tk.Frame()
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.width = self.container.winfo_screenwidth()
        self.height = self.container.winfo_screenheight()
        self.timer = time()
        self.mode = COMMERCIAL_MODE
        self.human_sensor = DetectMotion()
        self.camera = cv2.VideoCapture(0)

        # 폰트 지정
        self.title_font = tkfont.Font(
            family="a시월구일1", size=self.width*self.height//22000, weight="bold")
        self.subtitle_font = tkfont.Font(
            family="a시월구일1", size=self.width*self.height//25000, weight="bold")
        self.medium_font = tkfont.Font(
            family='a시월구일1', size=self.width*self.height//98000, weight="bold")
        self.xlarge_font = tkfont.Font(
            family="a시월구일1", size=self.width*self.height//35280, weight="bold")
        self.large_font = tkfont.Font(
            family="a시월구일1", size=self.width*self.height//73500, weight="bold")

        # 모든 프레임들을 가지는 변수
        self.pages = {}
        for F in (StartPage, DeliveryPage, FindPage, InformationPage, ProcessPage, AdminPage, SettingPage, ScreenSaverPage):
            page_name = F.__name__
            self.pages[page_name] = F

        if self.check_json_file():
            from utils.ratchController import RatchController
            RatchController.instance()
            self.show_frame("StartPage")
        else:
            self.show_frame("AdminPage")
        self.after(1000, self.__screensaver)

    def get_qr_img(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def get_img(self, img):
        img = cv2.resize(img, (300, 250))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.flip(img, 1)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        return img

    def __screensaver(self):
        time_limit = 10  # 300초 = 5분
        if self.human_sensor.is_human_coming():
            self.timer = time()
            self.after(1000, self.__screensaver)
            return
        if time() - self.timer < time_limit:
            self.after(1000, self.__screensaver)
            return

        self.show_frame("ScreenSaverPage")
        page_list = self.container.winfo_children()
        page_list[0].wait_window(page_list[-1])
        self.timer = time()
        self.after(1000, self.__screensaver)

    def set_timer(self, event):
        self.timer = time()

    def show_frame(self, new_frame, frame=None, parent=None, *args, **kwargs):
        """
        프레임(창)을 띄워줍니다.

        Args:
            new_frame_cls (str): 새롭게 보여줄 프레임 객체의 이름
            frame (tk.Frame): 기존에 보여지고 있는 프레임, 삭제할 프레임
            parent (tk.Frame): 새롭게 보여질 프레임의 부모프레임
            CRRMngKey (str): 주어질 함 관리번호
            page (str): information에서 보여지는 page에 따른 구분값
        """
        try:
            temp_frame = self.pages[new_frame](
                parent=parent if parent is not None else self.container, controller=self, bg="white", *args, **kwargs
            )
            if new_frame != ScreenSaverPage.__name__:
                temp_frame.canvas.bind("<Button-1>", self.set_timer)

            temp_frame.grid(row=0, column=0, sticky="nsew")
            temp_frame.tkraise()

            # 기존 프레임 종료
            if frame is not None:
                frame.destroy()
            print(list(map(lambda page: page.__class__.__name__,
                           self.container.winfo_children())))
        except Exception as e:
            raise e

    def check_json_file(self) -> bool:
        """json파일이 만들어졌는지 체크합니다.
        """
        try:
            with open("data/information.json") as f:
                file_read = f.readlines()
                if len(file_read) == 0:
                    raise FileNotFoundError
        except FileNotFoundError as e:
            return False
        else:
            return True

    def sync_to_json(self, locker_manage_key=None):
        """
        함의 정보를 동기화하여 json파일을 수정합니다.
        유저가 함을 사용하고 난 다음, 또는 관리자 페이지에서 사물함을 동기화할 때 사용됩니다.
        """
        try:
            import json
            from utils.sql import SQL
            sql = SQL("root", "", "10.80.76.63", "SML")

            # 사물함 관리 번호를 알지 못하는 경우 오류 출력
            if locker_manage_key is None:
                with open("data/information.json") as f:
                    file_read = f.readlines()
                    if len(file_read) == 0:
                        MessageFrame(self, "json 파싱 오류!!! 얼른 고치시죠!")
                        return
                    else:
                        json_object = json.loads("".join(file_read))
                        locker_manage_key = json_object["LCKMngKey"]

            # 본격적인 파싱 시작
            locker_size = sql.processDB(
                f"SELECT LCKSizeX, LCKSizeY FROM LCKInfo WHERE LCKMngKey='{locker_manage_key}'"
            )[0]

            result = sql.processDB(
                f"SELECT c.CRRMngKey, CRRNo, PosX, PosY, Width, Height, UseStat FROM CRRInfo c INNER JOIN LCKStat l ON LCKMngKey='{locker_manage_key}' AND c.CRRMngKey=l.CRRMngKey;"
            )
            result = list(map(lambda dic: f"""
        {{
            "CRRMngKey": "{dic["CRRMngKey"]}",
            "CRRNo": "{dic["CRRNo"]}",
            "location": {{
                "start": {{
                    "row": {dic["PosY"]},
                    "col": {dic["PosX"]}
                }},
                "width": {dic["Width"]},
                "height": {dic["Height"]}
            }},
            "useState": "{dic["UseStat"]}"
        }}""", result))

            json_string = f"""{{
    "LCKMngKey": "{locker_manage_key}",
    "LCKSize": {{
        "width": {locker_size["LCKSizeX"]},
        "height": {locker_size["LCKSizeY"]}
    }},
    "CRRInfo": [
        {",".join(result)}
    ]
}}"""
            with open("data/information.json", "w") as f:
                json.dump(json.loads(json_string), f, indent=2)

        except json.decoder.JSONDecodeError as e:
            MessageFrame(self, "잘못된 정보입니다. 새롭게 json세팅을 시도해주세요.")

        except FileNotFoundError as e:
            with open("data/information.json", "w") as f:
                f.write("")
                self.sync_to_json(locker_manage_key)
