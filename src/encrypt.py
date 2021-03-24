def encrypt(data: str) -> str:
    """
    data를 받아와 sha256로 암호화하여 리턴합니다.

    Example:
        >>> encrypt("a")
        ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb
    """
    from hashlib import sha256
    return sha256(data.encode()).hexdigest()
