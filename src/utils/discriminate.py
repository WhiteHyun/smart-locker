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

    def check_door(self):
        from time import sleep
        while True:
            try:
                # locker_list = ["H001234001", "H001234002", ...]
                for locker_key in self.locker_list:
                    data = self.sql.processDB(
                        f"SELECT LIG, HAL FROM SensorValue WHERE CRRMngKey='{locker_key}' ORDER BY SenKey DESC LIMIT 1;")
                    print(data)
                sleep(1)

            except Exception as e:
                print(e)
