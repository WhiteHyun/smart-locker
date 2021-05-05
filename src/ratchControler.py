if __name__ == "__main__" or __name__ == "sensorListener":
    import serial
    from serial.serialutil import SerialException

else:
    import serial
    from serial.serialutil import SerialException




class SingletonInstane:
  __instance = None

  @classmethod
  def __getInstance(cls):
    return cls.__instance

  @classmethod
  def instance(cls, *args, **kargs):
    cls.__instance = cls(*args, **kargs)
    cls.instance = cls.__getInstance
    return cls.__instance



class ratchControler(SingletonInstane):

    def __init__(self,Port) -> None:
        self.port = Port
        self.brate = 9600
        
        self.seri = self.connect_arduino()

    def excute(self,arduinoNum,order):
        self.seri.write(bytes(f'{arduinoNum}:{order}',encoding='ascii'))
        

    def connect_arduino(self):
        import time
        try:
            seri = serial.Serial(self.port,baudrate = self.brate, timeout = None)

        except Exception as e:
            #print("Fail!")
            time.sleep(2)
            return self.connect_arduino()        
        return seri


