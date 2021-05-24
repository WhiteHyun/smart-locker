import serial
if __name__ == "__main__" or __name__ == "ratchController":
    from util import connect_arduino
    from sound import Sound
    from sql import SQL
else:
    from .util import connect_arduino
    from .sound import Sound
    from .sql import SQL


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

    def __init__(self) -> None:
        """사물함 정보값을 받아와 각 함의 연결되어있는 Ratch들을 연동하여 리스트로 저장합니다.
        """
        try:
            with open("data/information.json") as f:
                import json
                json_object = json.load(f)
                locker_key = json_object["LCKMngKey"]
            sql = SQL("root", "", "10.80.76.63", "SML")
            result = sql.processDB(
                f"SELECT Port FROM ARDInfo WHERE LCKMngKey='{locker_key}' AND ARDKind='R' ORDER BY ARDNum;")
            assert result and result[0]["Port"] is not None

            self.seri = list()
            for port_dict in result:
                self.seri.append(connect_arduino(f"/dev/{port_dict['Port']}"))

        except Exception as e:
            raise e

    def execute(self, sync_number, order):
        """
        Parameter
        ---------
        sync_number: str
            아두이노 번호와 Ratch 번호의 조합 번호

        order: str
            Ratch를 Open할지 Close 할지 판단하기 위한 명령 문자열
        Example
        --------

        >>> self.execute("01", "O")
        # 이는 0번째 아두이노의 1번 Ratch를 'O'pen 하겠다 라는 의미임.
        """
        # sync_number: "00", "01", "10", "11", "12"....
        index = int(sync_number[0])
        self.seri[index].write(
            bytes(f'{sync_number[1]}:{order}', encoding='ascii'))
        if order == "O":
            path = "../../data/opened.wav" if __name__ == "__main__" or __name__ == "ratchController" else "data/opened.wav"
            Sound(path=path).play()
        else:
            path = "../../data/closed.wav" if __name__ == "__main__" or __name__ == "ratchController" else "data/closed.wav"
            Sound(path=path).play()


if __name__ == "__main__":
    pass
