import serial
from serial.serialutil import SerialException


class SingletonInstane:
    __instance = None

    @classmethod
    def instance(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = cls(*args, **kwargs)
        elif args or kwargs:
            print("이미 객체가 생성되어진 상태입니다")
        return cls.__instance


class ratchController(SingletonInstane):

    def __init__(self, port) -> None:
        self.port = port

        self.seri = self.connect_arduino()

    def excute(self, arduinoNum, order):
        self.seri.write(bytes(f'{arduinoNum}:{order}', encoding='ascii'))

    def connect_arduino(self):
        import time
        try:
            seri = serial.Serial(self.port, baudrate=9600, timeout=None)

        except Exception as e:
            time.sleep(2)
            return self.connect_arduino()
        return seri

    def test(self):
        print(self.port)


if __name__ == "__main__":
    a = ratchController.instance(2)
    b = ratchController.instance(3)
    a.test()
    b.test()
