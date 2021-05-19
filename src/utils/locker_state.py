if __name__ == "__main__" or __name__ == "locker_state":
    from sql import SQL
else:
    from .sql import SQL
import numpy as np


class LockerState:
    """
    각 함의 상태(물건의 유무, 문 개폐 여부)를 확인합니다.
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

    def calc_threshold(self, CRRMngKey, sensorNmLis):
        '''각 상태 판별을 위한 문턱값을 계산하여 반환합니다.

        Args:
            CRRMngKey (str): 문턱값을 구할 함 키.
            sensorNmLis (list): 문턱값을 구하고자 하는 센서 이름. 'LIG','FSR',...

        Return:
            dict: 구하고자 하는 센서의 문턱값을 딕셔너리 형태로 반환 {센서명:문턱값}
        '''
        selectQuery = ''
        resDict = {}

        try:
            firstUsedDate = self.sql.processDB(
                f"SELECT AddDt FROM LCKLog WHERE CRRMngKey='{CRRMngKey}' AND UseStat = 'U' ORDER BY LCKLogKey DESC LIMIT 1;")
            if not firstUsedDate:
                # 사용 데이터가 없으면 초기 데이터라 판단 -> 그냥 최근 데이터 긁어와서 판단

                selectQuery = f"SELECT {', '.join(sensorNmLis)} FROM SensorValue WHERE CRRMngKey = '{CRRMngKey}' ORDER BY SenKey DESC LIMIT 20"
            else:
                aaa = self.sql.processDB(
                    f"SELECT AddDt FROM LCKLog WHERE CRRMngKey='{CRRMngKey}' AND UseStat <> 'B' AND UseStat <> 'U' AND AddDt < '{firstUsedDate[0]['AddDt']}' ORDER BY LCKLogKey DESC LIMIT 1;")
                if not aaa:
                    # 여기 진입했다는 뜻은 최근 첫 사용 데이터라 판단-> 첫 사용 데이터 이전의 값을 가져와 사용
                    selectQuery = f"SELECT {', '.join(sensorNmLis)} FROM SensorValue WHERE CRRMngKey = '{CRRMngKey}' AND AddDt < '{firstUsedDate[0]['AddDt']}' ORDER BY SenKey DESC LIMIT 20"

                else:
                    selectQuery = f"SELECT {', '.join(sensorNmLis)} FROM SensorValue WHERE CRRMngKey = '{CRRMngKey}' AND AddDt > '{aaa[0]['AddDt']}' AND AddDt < '{firstUsedDate[0]['AddDt']}' ORDER BY SenKey DESC LIMIT 20"

            if not selectQuery:
                # 이론상 못들어오는곳
                pass

            sensorData = self.sql.processDB(selectQuery)

            if not sensorData:
                # 해당하는 센서값이 하나도 없는경우 -> 있을려나...? 나오면 뭔가 잘못된경우
                pass
            else:
                for senNm in sensorNmLis:
                    tmpLis = [d[senNm] for d in sensorData]
                    resDict[senNm] = np.mean(tmpLis)

        except Exception as e:
            print(e)
            return

        return resDict

    def is_door_open(self, CRRMngKey):
        """`CRRMngKey`의 함의 문 개폐 여부를 확인합니다.
        """
        try:
            threshold = self.clac_threshold(CRRMngKey, ['LIG'])

            if not threshold:
                # 뭔가 문제가 있어 문턱값 못구함
                return

            data = self.sql.processDB(
                f"SELECT HAL, LIG FROM SensorValue WHERE CRRMngKey='{CRRMngKey}' ORDER BY SenKey DESC LIMIT 1;")
            if not data:
                return

            if (data[0]['HAL'] == 0) or (np.abs(data[0]['LIG']-threshold['LIG']) < 20):
                # 닫혀 있는 케이스
                # 홀센서가 인식되어있으면 무조건 닫혀있는거
                # 홀센서가 인식 안되어있더라도 광량이 변화가 없다고 판단되면 닫혀있다고 판단?
                return False
            else:
                # 닫혀있지 않으면 열려있는걸로
                return True
        except Exception as e:
            print(e)
            return

    def has_item(self, CRRMngKey):
        """`CRRMngKey`의 함 내부에 물건이 존재하는지 판별하는 함수입니다.
        """
        try:

            threshold = self.clac_threshold(CRRMngKey, ['SSO', 'FSR'])

            if not threshold:
                # 뭔가 문제가 있어 문턱값 못구함
                return

            data = self.sql.processDB(
                f"SELECT SSO, FSR FROM SensorValue WHERE CRRMngKey='{CRRMngKey}' ORDER BY SenKey DESC LIMIT 1;")
            if not data:
                return

            if (threshold['SSO']-data[0]["SSO"]) > 5 or (data[0]["FSR"]-threshold['FSR']) > 10:
                # 물건이 있을려면 압력이 증가하거나 초음파가 감소하는경우
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
