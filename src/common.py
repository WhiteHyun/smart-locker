def encrypt(url: str) -> str:
    """
    url 값을 받아와 sha256로 암호화하여 리턴합니다.


    Example:
        >>> encrypt("a")
        ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb
    """
    from hashlib import sha256
    return sha256(url.encode()).hexdigest()


def dict_to_dml(data: dict, command_type: int) -> str:
    """
    directory로 되어있는 str 값을
    데이터 조작어(DML)로 변경해주는 함수입니다.

    Example:
        >>> dict_to_dml()
    """
