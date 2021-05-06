import serial
if __name__ == "__main__" or __name__ == "ratchController":
    from util import connect_arduino
else:
    from .util import connect_arduino


class SingletonInstane:
    __instance = None

    @classmethod
    def instance(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = cls(*args, **kwargs)
        elif args or kwargs:
            print("이미 객체가 생성되어진 상태입니다")
        return cls.__instance


class RatchController(SingletonInstane):

    def __init__(self, port) -> None:

        self.seri = connect_arduino(port)

    def excute(self, arduinoNum, order):
        self.seri.write(bytes(f'{arduinoNum}:{order}', encoding='ascii'))


if __name__ == "__main__":
    pass
