import tkinter as tk
from tkinter import TclError, simpledialog
from tkinter import messagebox
if __name__ == "__main__" or __name__ == "event":
    from sql import SQL
    from custom.tkinter_custom_button import SMLButton
else:
    from .sql import SQL
    from .custom.tkinter_custom_button import SMLButton


class UIEvent():

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"   # datetime 포맷값
    relx = 0.22  # 함 이미지 위치 지정값 중 x
    rely = 0.2  # 함 이미지 위치 지정값 중 y

    @classmethod
    def show_warning(cls, title="버튼", message="버튼 이벤트 발생"):
        """
        새 창으로 경고 이벤트를 발생시킵니다.
        """
        return messagebox.showwarning(title=title, message=message)

    @classmethod
    def show_error(cls, title="버튼", message="버튼 이벤트 발생"):
        """
        새 창으로 에러 이벤트를 발생시킵니다.
        """
        return messagebox.showerror(title=title, message=message)

    @classmethod
    def get_value_from_user_to_dialog(cls, title="dialog", message="dialog test"):
        return simpledialog.askstring(title=title, prompt=message)

    @classmethod
    def __delivery_process(cls, frame):
        """
        택배 보관 처리 함수입니다. 택배보관 가능한 사물함을 누를 시 발생하는 함수입니다.

        Args:
            frame (tk.frame): DeliveryPage 클래스

        flow:
            1. 사용자의 전화번호를 입력받게 함
            2. 사용자의 전화번호를 통해 유저정보를 가져옴
            3. 사용자와 사물함정보 그리고 보관한 시각을 더해 해시를 생성합니다.
            4. 해시를 가지고 QR코드를 생성합니다.
            6. DB에 관련 내용을 Insert 합니다.
            5. SMS를 통해 QR코드를 전달합니다.
            7. 사물함의 표시색깔을 변경하여 뿌려줍니다.
        """
        # TODO: 전화번호 입력을 받게 하기 위해 프레임 하나 더 생성?

    @classmethod
    def delivery(cls):
        """
        맡기기 버튼을 눌렀을 때 발생할 이벤트 함수입니다.

        flow:
            1. 현재 사물함의 상태를 긁어옴({빨간색, 초록색}
            2. 해당 정보에 대해 사물함 버튼 생성 및 이벤트 구현
            3. 화면에 전달
        """

        """
        FIXME: json이나 xml을 통해 사물함의 키값과 크기, 함의 위치값과 크기를 로컬로 저장하여(이는 관리자 화면에서 동기화를 통해 갱신)
               함의 정보를 화면에 띄울 때 값을 가져오고 사용유무에 대한 db값을 가져와 보여주기!
        """

        # 추가된 게 없는 경우 버튼 생성 X
        # if len(frame.lockers) != len(result):
        #     cls.__make_button(frame, result)

    @ classmethod
    def sync_to_json(cls):
        """
        함의 정보를 동기화하여 json파일을 수정합니다.
        초기 파일을 실행할 때, 또는 관리자 페이지에서 사물함을 동기화할 때 사용됩니다.
        """
        try:
            locker_manage_key = None
            sql = SQL("root", "", "10.80.76.63", "SML")

            # 사물함 관리 번호를 알지 못하는 경우 입력받게 함
            import json
            with open("data/information.json") as f:
                file_read = f.readlines()
                if len(file_read) == 0:
                    manage_key_list = list(map(lambda dic: dic["LCKMngKey"], sql.processDB(
                        "SELECT LCKMngKey FROM LCKInfo;")))

                    while locker_manage_key is None or locker_manage_key not in manage_key_list:
                        locker_manage_key = cls.get_value_from_user_to_dialog(
                            "사물함 관리번호", "사물함 관리번호가 무엇인지 정확하게 기입하여주세요!")
                else:
                    json_object = json.loads("".join(file_read))
                    locker_manage_key = json_object["LCKMngKey"]

            # 본격적인 파싱 시작
            locker_size = sql.processDB(
                f"SELECT LCKSizeX, LCKSizeY FROM LCKInfo WHERE LCKMngKey='{locker_manage_key}'")[0]

            result = sql.processDB(
                f"SELECT c.CRRMngKey, CRRNo, PosX, PosY, Width, Height, UseStat FROM CRRInfo c INNER JOIN LCKStat l ON LCKMngKey='{locker_manage_key}' AND c.CRRMngKey=l.CRRMngKey;")
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

            with open("data/information.json", "w") as f:
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
                print(json_string)
                json.dump(json.loads(json_string), f, indent=2)

        except json.decoder.JSONDecodeError as e:
            cls.show_error("에러!", "잘못된 정보입니다. 새롭게 json세팅을 시도해주세요.")
            raise e

        except Exception as e:
            raise e

    @ classmethod
    def find_delivery(cls):
        """
        택배를 찾으려고 할 때 발생하는 이벤트
        """
        if __name__ == "__main__" or __name__ == "event":
            from qrcodes import detectQR
            from sql import SQL
            from encrypt import encrypt
        else:
            from .qrcodes import detectQR
            from .sql import SQL
            from .encrypt import encrypt

        hash_qr = detectQR()[0]
        info_sql = SQL("root", "", "10.80.76.63", "SML")
        result = info_sql.processDB(
            f"SELECT * FROM LCKStat WHERE HashKey='{hash_qr}';")

        print(result)


if __name__ == "__main__":
    UIEvent.sync_to_json()
