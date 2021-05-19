import serial
import threading
if __name__ == "__main__" or __name__ == "sensor_listener":
    from util import dict2Query, connect_arduino
    from sql import SQL
else:
    from .util import dict2Query, connect_arduino
    from .sql import SQL


class SensorListener:
    """아두이노(여러 함)로 부터 센싱값을 듣는(Listening) 클래스.

    Attributes
    ----------
    sql: SQL Class
        DB에 저장하기 위한 `connection` 객체

    arduino_number: str
        연결되어있는 아두이노의 번호

    sync_sensor: str
        아두이노 번호(arduino_number)와 센서묶음셋 번호를 합친 문자열
    """

    def __init__(self, LCKMngKey):
        """
        Parameters
        ----------
        LCKMngKey : str
            사물함 관리번호

        Examples
        ---------
        >>> SensorListener(arduino_num=0, port="/dev/ttyACM0", LCKMngKey="H001234")
        """
        self.sql = SQL("root", "", "10.80.76.63", "SML")
        self.LCKMngKey = LCKMngKey
        self.seri, self.arduino_number = self.__get_serial_connection()
        self.sync_sensor = self.__set_sensor_number()

    def __get_serial_connection(self):
        try:

            sql = SQL("root", "", "10.80.76.63", "SML")
            result = sql.processDB(
                f"SELECT Port, ARDNum FROM ARDInfo WHERE LCKMngKey='{self.LCKMngKey}' AND ARDKind='S' ORDER BY ARDNum;")

            seri = []
            ardNum = []
            for portDict in result:
                seri.append(connect_arduino(f"/dev/{portDict['Port']}"))
                ardNum.append(portDict['ARDNum'])

            return seri, ardNum
        except Exception as e:
            print(e)

    def __set_sensor_number(self):
        """
        DB에 저장되어있는 함과 센서의 정보를 가지고 {"syncsensor": "CRRMngKey"} 형태의 딕셔너리로 생성합니다.
        """
        sync_sensor = dict()
        sql_data = self.sql.processDB(
            f"SELECT CRRMngKey, SyncSensor FROM CRRInfo WHERE State = 'N' AND LCKMngKey = '{self.LCKMngKey}'")
        for dataset in sql_data:
            if dataset["SyncSensor"] is not None:
                sync_sensor[dataset["SyncSensor"]] = dataset["CRRMngKey"]
        return sync_sensor

    def __listen_sensor(self, seri, ardNum):
        """각 함들의 센서들의 듣는(Listening) 값을 DB에 저장합니다.
        """
        dataset = {"CRRMngKey": None, "FSR": -1,
                   "LIG": -1, "SSO": -1, "HAL": -1, "VIB": -1}
        while True:
            if seri.readable():
                try:
                    res = seri.readline().decode()
                    res = res[:-2]
                    if not res:
                        continue

                    if res[:-1] == "dataset":
                        if dataset["CRRMngKey"] is not None:
                            sql_query = dict2Query("SensorValue", dataset)
                            self.sql.processDB(sql_query)

                        dataset = {"CRRMngKey": None, "FSR": -1,
                                   "LIG": -1, "SSO": -1, "HAL": -1, "VIB": -1}

                        dataset["CRRMngKey"] = self.sync_sensor.get(
                            ardNum + res[-1:])
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

    def listen(self):
        for i in range(len(self.seri)):
            t = threading.Thread(target=self.__listen_sensor, args=(
                self.seri[i], self.arduino_number[i]))
            t.start()

# test = sensorListener(0,"COM6","H001234")

# print (test.SyncSensor)
# test.listen()
