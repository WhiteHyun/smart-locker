class QRCodeError(Exception):
    pass


class VideoError(Exception):
    pass


def generateQR(url: str) -> bool:
    """
    url 해시값을 통해 QRCode를 생성합니다.

    Args:
        url (str): QRCode를 생성할 url 해시값입니다.

    Return:
        bool: 성공하면 True, 실패할 시 False를 리턴합니다.

    Example:
        >>> generateQR(url) # If Success
        True

        >>> generateQR(url) # Fail
        False
    """

    result = False

    if not url:
        raise ValueError
    elif type(url) is not str:
        raise TypeError

    try:
        import qrcode
        qr = qrcode.make(url)
        if __name__ == "__main__" or __name__ == "qrcodes":
            qr.save(f"../data/qrcode_{url}.png")
        else:
            qr.save(f"data/{url}.png")
    except ValueError as e:
        print("URL 값이 입력되지 않았습니다!")
    except TypeError as e:
        print("문자열값이 아닙니다!")
    except QRCodeError as e:
        print(f"QRCode 생성 중 오류가 발생하였습니다. {e}")
    else:
        result = True
    finally:
        return result


def detectQR(gray_image) -> str:
    """
    이미지를 이용해 QR코드를 탐지합니다.
    사용자의 QR코드를 읽어오려는 경우 해당 함수를 호출합니다.

    Args:
        img (nd.array): 비디오로 가져온 이미지 프레임 객체입니다.
    Returns:
        value (str): 인식한 QR코드를 decode한 결과값입니다.

    Example:
        >>> detectQR(img)
        "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"
    """

    import pyzbar.pyzbar as pyzbar
    decoded = pyzbar.decode(gray_image)  # 바코드 또는 QR코드를 찾고 해석

    # QR코드가 2개 이상이거나 QRCODE로 인식하지 않은 경우
    if len(decoded) > 1 or (decoded and "QRCODE" != decoded[0].type):
        return
    # QR코드 값이 하나 들어온 경우
    if decoded:
        return decoded[0].data.decode("utf-8")  # 디코드된 값 또는 파일
