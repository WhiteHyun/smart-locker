import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.util import *


class StartPage(tk.Frame):
    """
    첫 페이지를 보여주는 프레임입니다.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="택배보관함",
                 font=controller.large_font
                 ).pack(side="top", fill="x", pady=50)

        SMLButton(master=self,
                  text_font=controller.large_font,
                  text="맡기기",
                  width=240,
                  height=90,
                  hover=True,
                  command=lambda: controller.show_frame(
                      "DeliveryPage", self
                  )
                  ).place(relx=0.33, rely=0.2, anchor=tk.CENTER)
        SMLButton(master=self,
                  text_font=controller.large_font,
                  text="찾기",
                  width=240,
                  height=90,
                  hover=True,
                  command=lambda: controller.show_frame(
                      "FindPage", self
                  )
                  ).place(relx=0.66, rely=0.2, anchor=tk.CENTER)
        SMLButton(master=self,
                  fg_color="#922B21",
                  border_color="white",
                  hover_color="#CD6155",
                  text_font=None,
                  text="tkinter 종료",
                  border_width=2,
                  width=150,
                  height=45,
                  hover=True,
                  command=lambda: controller.destroy()
                  ).place(relx=0.50, rely=0.3, anchor=tk.CENTER)

        self.sync_to_json()

    def sync_to_json(self):
        """
        함의 정보를 동기화하여 json파일을 수정합니다.
        초기 파일을 실행할 때, 또는 관리자 페이지에서 사물함을 동기화할 때 사용됩니다.
        """
        try:
            import json
            from utils.sql import SQL
            locker_manage_key = None
            sql = SQL("root", "", "10.80.76.63", "SML")

            # 사물함 관리 번호를 알지 못하는 경우 입력받게 함
            with open("data/information.json") as f:
                file_read = f.readlines()
                if len(file_read) == 0:
                    manage_key_list = list(map(lambda dic: dic["LCKMngKey"], sql.processDB(
                        "SELECT LCKMngKey FROM LCKInfo;"
                    )))

                    while locker_manage_key is None or locker_manage_key not in manage_key_list:
                        locker_manage_key = askstring(
                            "사물함 관리번호", "사물함 관리번호가 무엇인지 정확하게 기입하여주세요!"
                        )
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
            showerror("에러!", "잘못된 정보입니다. 새롭게 json세팅을 시도해주세요.")
            raise e
        except FileNotFoundError as e:
            with open("data/information.json", "w") as f:
                f.write("")
                self.sync_to_json()
        except Exception as e:
            raise e