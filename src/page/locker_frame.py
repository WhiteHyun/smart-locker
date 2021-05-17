import os
import sys
if __name__:
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    from utils.util import *


class LockerFrame(tk.Frame):

    STATE_WAIT = "W"
    STATE_USED = "U"
    STATE_BROKEN = "B"
    DEFAULT_MODE = 0
    FIX_MODE = 1
    UNLOCK_MODE = 2

    def __init__(self, parent, controller, page, mode=0, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.controller = controller
        self.page = page
        self.mode = mode
        self.size = None
        self.color_dict = {
            f"{self.STATE_WAIT}": ("#A93226", "#CD6155") if self.page == "FindPage" else ("#385ab7", "#496bc9") if self.mode == self.UNLOCK_MODE else ("#1E8449", "#2ECC71"),
            f"{self.STATE_USED}": ("#1E8449", "#2ECC71") if self.page == "FindPage" else ("#385ab7", "#496bc9") if self.mode == self.UNLOCK_MODE else ("#A93226", "#CD6155"),
            f"{self.STATE_BROKEN}": ("#7C7877", "#7C7877")
        }
        self.button_dict = {}
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
                self.size = (json_object["LCKSize"]["width"],
                             json_object["LCKSize"]["height"])
                for json_data in locker_list:
                    self.__make_locker_button(json_data)
        except Exception as e:
            raise e

    def __make_locker_button(self, json_data):
        """
        json 데이터를 가지고 버튼을 생성하여 나타냅니다.
        버튼은 세 가지 버튼으로 만들어집니다.

        사물(택배)함이 고장났을 경우
            회색의 사물(택배)함 버튼이 만들어지며 누를 경우 사용할 수 없다는 경고창이 발생합니다.

        사물(택배)함이 고장나지 않은 경우
        - 페이지에 따라 다르게 보여집니다.
            빨간색의 사물(택배)함 버튼이 만들어지며 누를 경우 사용할 수 없다는 경고창이 발생합니다.
            초록색의 사물(택배)함 버튼이 만들어지며 누를 경우 사용관련 창으로 넘어갑니다.
        """
        locker_width, locker_height = self.size
        img_size = 170 - 50*(max(locker_height, locker_width)-1)
        button_size = 250 - 50*(max(locker_width, locker_height)-1)
        text_font = tkfont.Font(
            family="a시월구일1",
            size=20-2*(max(locker_width, locker_height)-1),
            weight="bold")
        locker_image = ImageTk.PhotoImage(Image.open(
            "../img/lockers.png" if __name__ == "__main__" or __name__ == "locker_frame" else "src/img/lockers.png"
        ).resize((img_size, img_size)))
        location = json_data["location"]
        width = location["width"]
        height = location["height"]
        state = json_data["useState"]
        locker_number = json_data["CRRNo"]
        CRRMngKey = json_data["CRRMngKey"]

        def decide_function():
            """
            함이 어디 페이지에 위치해있으며 상태값이 어떤지에 따라 그에 걸맞게 함수를 지정해줍니다
            """
            # useState == 'U' when FindPage, useState == 'W' when DeliveryPage
            if state == self.STATE_USED and self.page == "FindPage" or state == self.STATE_WAIT and self.page == "DeliveryPage":
                return lambda CRRMngKey=CRRMngKey: self.controller.show_frame("InformationPage", frame=self.parent, CRRMngKey=CRRMngKey, mode=0, page=self.page)
            elif self.page == "SettingPage":
                if self.mode == self.FIX_MODE:
                    return lambda CRRMngKey=CRRMngKey: self.parent.set_locker(CRRMngKey, state, locker_number)
                elif self.mode == self.UNLOCK_MODE:
                    return lambda CRRMngKey=CRRMngKey: self.parent.force_open_door(CRRMngKey)
            # useState == 'B' or 'U' when deliveryPage, 'W' when FindPage
            else:
                return lambda: MessageFrame(self.controller, "해당 함을 사용할 수 없습니다.")

        button = SMLButton(master=self,
                           fg_color=self.color_dict[json_data["useState"]][0],
                           hover_color=self.color_dict[json_data["useState"]][1],
                           image=locker_image,
                           border_width=1,
                           corner_radius=10,
                           text=locker_number,
                           text_font=text_font,
                           width=button_size*width,
                           height=button_size*height,
                           command=decide_function()
                           )
        button.grid(row=location["start"]["row"], column=location["start"]
                    ["col"], rowspan=height, columnspan=width)
        self.button_dict[locker_number] = button
