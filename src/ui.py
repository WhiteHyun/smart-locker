if __name__ == "__main__" or __name__ == "ui":
    from utils.util import *
    from page.find_page import FindPage
    from page.delivery_page import DeliveryPage
    from page.information_page import InformationPage
    from page.locker_frame import LockerFrame
    from page.start_page import StartPage

else:
    from .utils.util import *
    from .page.find_page import FindPage
    from .page.delivery_page import DeliveryPage
    from .page.information_page import InformationPage
    from .page.locker_frame import LockerFrame
    from .page.start_page import StartPage


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
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

        # 폰트 지정
        self.title_font = tkfont.Font(
            family="Malgun Gothic", size=self.width*self.height//25000, weight="bold")
        self.medium_font = tkfont.Font(
            family='Malgun Gothic', size=self.width*self.height//98000, weight="bold")
        self.xlarge_font = tkfont.Font(
            family="Malgun Gothic", size=self.width*self.height//35280, weight="bold")
        self.large_font = tkfont.Font(
            family="Malgun Gothic", size=self.width*self.height//73500, weight="bold")

        # 모든 프레임들을 가지는 변수
        self.pages = {}
        for F in (StartPage, DeliveryPage, FindPage, LockerFrame, InformationPage):
            page_name = F.__name__
            self.pages[page_name] = F
        self.show_frame("StartPage")

    def show_frame(self, new_frame, frame=None, parent=None, CRRMngKey=None, page=None):
        """
        프레임(창)을 띄워줍니다.

        Args:
            new_frame_cls (str): 새롭게 보여줄 프레임 객체의 이름
            frame (tk.Frame): 기존에 보여지고 있는 프레임
            parent (tk.Frame): 새롭게 보여질 프레임의 부모프레임
            CRRMngKey (str): 주어질 함 관리번호
            page (str): information에서 보여지는 page에 따른 구분값
        """
        try:
            if CRRMngKey is None or page is None:
                temp_frame = self.pages[new_frame](
                    parent=parent if parent is not None else self.container, controller=self
                )
            else:
                temp_frame = self.pages[new_frame](
                    parent=parent if parent is not None else self.container, controller=self, CRRMngKey=CRRMngKey, page=page
                )

            temp_frame.grid(row=0, column=0, sticky="nsew")
            temp_frame.tkraise()

            # 기존 프레임 종료
            if frame is not None:
                frame.destroy()
        except Exception as e:
            raise e
