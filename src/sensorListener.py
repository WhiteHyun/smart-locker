if __name__ == "__main__" or __name__ == "sensorListener":
    import serial
    from serial.serialutil import SerialException
    from utils.makeQuery import makeQuery
    from utils.sql import SQL

else:
    import serial
    from serial.serialutil import SerialException
    from .utils.makeQuery import makeQuery
    from .utils.sql import SQL


class sensorListener:
    
    def __init__(self,ArduinoNum,Port,LCKMngKey):
        """
        아두이노로 부터 센싱값을 받기 위한 클래스.
        ArduinoNum : 부착된 여러 아두이노중 몇번째 아두이노인지 ex) 0 , 1 ...
        Port : 연결된 포트
        LCKMngKey : 사물함 관리번호
        """
        self.Sql= SQL("root", "", "10.80.76.63", "SML")
        self.port = Port
        self.brate = 9600
        self.LCKMngKey = LCKMngKey
        self.SyncSensor={}

        self.seri = self.connect_arduino()

        self.sArduinoNum = f"{ArduinoNum}"
        
        self.setSensorNo()

        self.dataset = {"CRRMngKey":None,"FSR":-1,"LIG":-1,"SSO":-1}

    def setSensorNo(self):
        tmpData = self.Sql.processDB(sql = f"SELECT CRRMngKey, SyncSensor FROM CRRInfo WHERE LCKMngKey LIKE '{self.LCKMngKey}%'")
        for dset in tmpData:
            print(dset)
            if(dset["SyncSensor"] != None):
                self.SyncSensor[dset["SyncSensor"]]=dset["CRRMngKey"]



    def connect_arduino(self):
        import time
        try:
            seri = serial.Serial(self.port,baudrate = self.brate, timeout = None)

        except Exception as e:
            print("Fail!")
            time.sleep(2)
            return self.connect_arduino()        
        return seri

    def startListen(self):
        print("listen start!!")
        while True:
            if self.seri.readable():
                res = self.seri.readline().decode()
                res = res[:-2]
                if len(res) == 0:
                    continue

                if res[:-1] == "dataset":
                    if self.dataset["CRRMngKey"] != None:
                        #dataset으로 insert 문 생성후 DB에 insert하는 로직 추가 필요
                        #print(makeQuery.dict2Query("testDB",self.dataset))
                        print("listen!")
                        self.Sql.processDB(makeQuery.dict2Query("SensorValue",self.dataset))
                        
                    
                    self.dataset = {"CRRMngKey":None,"FSR":-1,"LIG":-1,"SSO":-1}
                    #CRR에 아두이노에서 받아온 숫자를 넣음 -> 여러 함일경우 숫자 변환 과정이 필요함
                    self.dataset["CRRMngKey"]= self.SyncSensor[self.sArduinoNum + res[-1:]]
                elif res[0] == "F":
                    self.dataset["FSR"]= res[2:-1]
                    
                elif res[0] == "S":
                    self.dataset["SSO"]= res[2:-1]
                    
                elif res[0] == "L":
                    self.dataset["LIG"]= res[2:-1]


#test = sensorListener(0,"COM6","H001234")

#print (test.SyncSensor)
#test.startListen()

