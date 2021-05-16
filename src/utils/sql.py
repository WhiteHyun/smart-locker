from pymysql import connect, cursors


class SQL:
    """
    데이터베이스 관리 클래스

    Member:
        cursor (Cursor): 연결한 DB와 상호작용하기 위해 사용되는 객체
        conn (Connection): Connection 객체
    """

    def __init__(self, user: str, passwd: str, host: str, db: str, charset: str = "utf8") -> None:
        """
        **서버 전용** 함수

        데이터베이스 연결을 시도하고, 연결 후 사용되는 객체들을 반환하는 함수

        Args:
            user: user name
            passwd: 설정한 패스워드
            host: DB가 존재하는 host ip
            db: 연결할 데이터베이스 이름
            charset: 인코딩 설정
        """
        try:
            self.__conn = connect(
                user=user,
                passwd=passwd,
                host=host,
                db=db,
                charset=charset
            )
            self.__cursor = self.__conn.cursor(cursors.DictCursor)
        except Exception as e:
            print(f"SQL Error, {e}")
            raise e

    def processDB(self, sql: str, type_csv=False):
        """
        sql문을 가지고 DB작업을 처리합니다.

        Args:
            sql (str): DML(데이터 조작어)문
            type_csv (bool): select의 경우 데이터 형식을 csv로 받아올지에 대한 부울값

        Example:
            >>> processDB("SELECT * FROM testTable")
            [{'name': 'sung-kyu'}, {'name': 'seung-hyeon'}]

            >>> processDB("SELECT * FROM testTable", type_csv=True)
            "name","age"
            "sung-kyu",24
            "seung-hyeon",23
        """
        try:
            if sql[:6].upper() == "SELECT":
                self.__cursor.execute(sql)
                result = self.__cursor.fetchall()
                if type_csv:
                    result = self.__convert_to_csv(result)
                return result
            else:
                self.__cursor.execute(sql)
                self.__conn.commit()
        except Exception as e:
            return
        finally:
            self.__conn.begin()

    def __del__(self):
        try:
            self.__conn.close()

        except Exception as e:
            print(f"sql Error!!! {e}")
            raise e
