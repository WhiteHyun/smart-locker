import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.util import *


class LockerFrame(tk.Frame):

    STATE_WAIT = "W"
    STATE_USED = "U"
    STATE_BROKEN = "B"

    def __init__(self, parent, controller, page="DeliveryPage", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.controller = controller
        self.page = page
        self.color_dict = {
            f"{LockerFrame.STATE_WAIT}": ("#1E8449", "#2ECC71") if page == "DeliveryPage" else ("#A93226", "#CD6155"),
            f"{LockerFrame.STATE_USED}": ("#A93226", "#CD6155") if page == "DeliveryPage" else ("#1E8449", "#2ECC71"),
            f"{LockerFrame.STATE_BROKEN}": ("#7C7877", "#7C7877")
        }
        self.__show_locker()

    def __show_locker(self):
        """
        json을 참조하여 사물함을 보여줍니다.
        grid 형태로 나타내어지기 때문에 frame에 pack으로 표시되어있는 상태에서는 사용될 수 없습니다.
        """
        try:
            with open("data/information.json") as f:
                import json
                json_object = json.load(f)
                locker_list = sorted(
                    json_object["CRRInfo"], key=lambda dic: dic["location"]["start"]["row"]
                )
                for json_data in locker_list:
                    self.__make_locker_button(json_data)
        except Exception as e:
            print(e)
            raise e

    def __make_locker_button(self, json_data):
        """
        json 데이터를 가지고 버튼을 생성하여 나타냅니다.
        버튼은 세 가지 버튼으로 만들어집니다.

        사물(택배)함이 고장났을 경우
            회색의 사물(택배)함 버튼이 만들어지며 누를 경우 사용할 수 없다는 경고창이 발생합니다.

        사물(택배)함이 사용중일 경우
            빨간색의 사물(택배)함 버튼이 만들어지며 누를 경우 사용할 수 없다는 경고창이 발생합니다.

        사물(택배)함이 미사용중일 경우
            초록색의 사물(택배)함 버튼이 만들어지며 누를 경우 사용관련 창으로 넘어갑니다.
        """

        play_image = ImageTk.PhotoImage(Image.open(
            "../img/lockers.png" if __name__ == "__main__" or __name__ == "locker_frame" else "src/img/lockers.png"
        ).resize((60, 60)))
        location = json_data["location"]
        width = location["width"]
        height = location["height"]
        state = json_data["useState"]

        def decide_function():
            """
            함이 어디 페이지에 위치해있으며 상태값이 어떤지에 따라 그에 걸맞게 함수를 지정해줍니다
            """
            # useState == 'U' when FindPage, useState == 'W' when DeliveryPage
            if state == LockerFrame.STATE_USED and self.page == "FindPage" or state == LockerFrame.STATE_WAIT and self.page == "DeliveryPage":
                return lambda CRRMngKey=json_data["CRRMngKey"]: self.controller.show_frame("InformationPage", self.parent, CRRMngKey=CRRMngKey, page=self.page)

            # useState == 'B' or 'U' when deliveryPage, 'W' when FindPage
            else:
                return lambda: showerror("오류!", "해당 함을 사용할 수 없습니다.")
        SMLButton(master=self,
                  bg_color=None,
                  fg_color=self.color_dict[json_data["useState"]][0],
                  border_color=None,
                  hover_color=self.color_dict[json_data["useState"]][1],
                  image=play_image,
                  corner_radius=10,
                  border_width=1,
                  width=100 if width == 1 else 100*width,
                  height=100 if height == 1 else 100*height,
                  hover=True,
                  command=decide_function()
                  ).grid(row=location["start"]["row"],
                         column=location["start"]["col"], rowspan=height, columnspan=width)
