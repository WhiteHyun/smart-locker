from pymysql import connect, cursors


def connect_sql(user: str, passwd: str, host: str, db: str, charset: str = "utf8"):
    """
    **서버 전용** 함수

    데이터베이스 연결을 시도하고, 연결 후 사용되는 객체들을 반환하는 함수

    Args:
        user: user name
        passwd: 설정한 패스워드
        host: DB가 존재하는 host
        db: 연결할 데이터베이스 이름
        charset: 인코딩 설정

    Return:
        cursor (Cursor): 연결한 DB와 상호작용하기 위해 사용되는 객체
        connection (Connection): Connection 객체
    """
    try:
        connection = connect(
            user=user,
            passwd=passwd,
            host=host,
            db=db,
            charset=charset
        )
        cursor = connection.cursor(cursors.DictCursor)
    except Exception as e:
        print(f"SQL Error, {e}")
        raise Exception
    else:
        return cursor, connection
