if __name__ == "__main__" or __name__ == "discriminate":
    from sql import SQL
else:
    from .sql import SQL


class Discriminate:
    """
    센싱값을 판별해주는 클래스
    """

    def __init__(self) -> None:
        self.sql = SQL("root", "", "10.80.76.63", "SML")

        with open("data/information.json") as f:
            import json
            json_object = json.load(f)
            # json을 읽어 CRRMngKey 값을 리스트 형태로 저장
            locker_list = list(
                map(lambda x: x["CRRMngKey"], json_object["CRRInfo"]))
        self.locker_list = locker_list

    def is_door_open(self, CRRMngKey):
        """`CRRMngKey`의 함의 문 개폐 여부를 확인합니다.
        """
        try:
            data = self.sql.processDB(
                f"SELECT LIG, HAL FROM SensorValue WHERE CRRMngKey='{CRRMngKey}' ORDER BY SenKey DESC LIMIT 1;")
            if not data:
                return
            else:
                data = data[0]
                if data["HAL"] == 1:
                    return True
                else:
                    return False
        except Exception as e:
            print(e)
            return

    def has_item(self, CRRMngKey):
        """`CRRMngKey`의 함 내부에 물건이 존재하는지 판별하는 함수입니다.
        """
        try:
            data = self.sql.processDB(
                f"SELECT SSO, FSR FROM SensorValue WHERE CRRMngKey='{CRRMngKey}' ORDER BY SenKey DESC LIMIT 1;")
            if not data:
                return
            else:
                data = data[0]
                if data["SSO"] < 25 or data["FSR"] > 160:
                    return True
                else:
                    return False
        except Exception as e:
            print(e)
            return

    def check_door(self):
        from time import sleep
        while True:
            # locker_list = ["H001234001", "H001234002", ...]
            for locker_key in self.locker_list:
                result = self.is_door_open(locker_key)
                if result:
                    print(f"{locker_key}: {result}")
            sleep(1)
