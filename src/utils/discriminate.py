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

    def check_door(self):
        while True:
            try:
                with open("data/information.json") as f:
                    import json
                    json_object = json.load(f)
                    # json을 읽어 CRRMngKey 값을 리스트 형태로 저장
                    locker_list = list(
                        map(lambda x: x["CRRMngKey"], json_object["CRRInfo"]))
                    for locker_key in locker_list:
                        data = self.sql.processDB(
                            f"SELECT LIG, HAL FROM SensorValue WHERE CRRMngKey='{locker_key}' LIMIT 1;")
                        if data:
                            print(data)

            except Exception as e:
                print(e)
