import serial
if __name__ == "__main__" or __name__ == "sensorListener":
    from utils.util import dict2Query
    from utils.sql import SQL
else:
    from .utils.util import dict2Query
    from .utils.sql import SQL


class SensorBehavior:
    """아두이노(여러 함)를 동작시키는 클래스.

    Attributes
    ----------
    sql: SQL Class
        DB에 저장하기 위한 `connection` 객체

    port: str
        아두이노와 통신을 위한 포트

    arduino_number: str
        연결되어있는 아두이노의 번호

    SyncSensor: str
        아두이노 번호(arduino_number)와 센서묶음셋 번호를 합친 문자열
    """

    def __init__(self, arduino_num, port, LCKMngKey):
        """
        Parameters
        ----------
        arduino_num : int
            부착된 아두이노의 번호

        port : str
            연결된 포트

        LCKMngKey : str
            사물함 관리번호

        Examples
        ---------
        >>> SensorListener(arduino_num=0, port="/dev/ttyACM0", LCKMngKey="H001234")
        """
        self.sql = SQL("root", "", "10.80.76.63", "SML")
        self.port = port
        self.LCKMngKey = LCKMngKey
        self.seri = self.connect_arduino()
        self.arduino_number = str(arduino_num)
        self.sync_sensor = self.__set_sensor_number()

    def __set_sensor_number(self):
        """
        DB에 저장되어있는 함과 센서의 정보를 가지고 {"syncsensor": "CRRMngKey"} 형태의 딕셔너리로 생성합니다.
        """
        sync_sensor = dict()
        sql_data = self.sql.processDB(
            f"SELECT CRRMngKey, SyncSensor FROM CRRInfo WHERE LCKMngKey LIKE '{self.LCKMngKey}%'")
        for dataset in sql_data:
            if dataset["SyncSensor"] is not None:
                sync_sensor[dataset["SyncSensor"]] = dataset["CRRMngKey"]
        return sync_sensor

    def connect_arduino(self):
        """아두이노 연결을 시도합니다.
        연결에 성공하면 해당 `Serial`을 리턴합니다.
        """
        import time
        try:
            seri = serial.Serial(self.port, baudrate=9600, timeout=None)

        except Exception as e:
            time.sleep(2)
            return self.connect_arduino()
        return seri

    def listen(self):
        """각 함들의 센서들의 듣는(Listening) 값을 DB에 저장합니다.
        """
        dataset = {"CRRMngKey": None, "FSR": -1,
                   "LIG": -1, "SSO": -1, "HAL": -1, "VIB": -1}
        while True:
            if self.seri.readable():
                try:
                    res = self.seri.readline().decode()
                    res = res[:-2]
                    if not res:
                        continue

                    if res[:-1] == "dataset":
                        if dataset["CRRMngKey"] is not None:
                            sql_query = dict2Query("SensorValue", dataset)
                            self.sql.processDB(sql_query)

                        dataset = {"CRRMngKey": None, "FSR": -1,
                                   "LIG": -1, "SSO": -1, "HAL": -1, "VIB": -1}

                        dataset["CRRMngKey"] = self.sync_sensor[self.arduino_number + res[-1:]]
                    elif res[0] == "F":
                        dataset["FSR"] = res[2:]
                    elif res[0] == "S":
                        dataset["SSO"] = res[2:]
                    elif res[0] == "L":
                        dataset["LIG"] = res[2:]
                    elif res[0] == "H":
                        dataset["HAL"] = res[2:]
                    elif res[0] == "V":
                        dataset["VIB"] = res[2:]
                except Exception as e:
                    print(f'sensor exception : {e}')


# test = sensorListener(0,"COM6","H001234")

# print (test.SyncSensor)
# test.listen()
