# This module can be executed as module and script and by doctest.
if __name__ == "__main__" or __name__ == "qrcodes":
    from error import *
else:
    from .error import *


def generateQR(url: str) -> bool:
    """
    url 해시값을 통해 QRCode를 생성합니다.
    만약 url이 없을 경우 Error를 뿜습니다 *^^*

    Args:

    url (str): QRCode를 생성할 url 해시값입니다.

    Example:
        >>> extractQRCode(url) # If Success
        True

        >>> extractQRCode(url) # Fail
        Value Error
    """
    if not url:
        print("URL 값이 입력되지 않았습니다!")
        raise ValueError
    elif type(url) is not str:
        print("문자열값이 아닙니다!")
        raise TypeError

    try:
        import qrcode
        qr = qrcode.make(url)
        if __name__ == "__main__" or __name__ == "qrcodes":
            qr.save(f"../data/qrcode_{url}.png")
        else:  # 실행 위치와 환경에 따라 변동 가능성 존재
            qr.save(f"data/{url}.png")
    except QRCodeError as e:
        print(f"QRCode 생성 중 오류가 발생하였습니다. {e}")
        raise QRCodeError
    else:
        return True


def detectQR() -> list:
    """
    캠 모듈을 사용하여 QR코드를 탐지합니다.
    사용자의 QR코드를 읽어오려는 경우 해당 함수를 호출합니다.

    Returns:
        list (url: str, qrtype: str): QR코드에 대한 url과 타입을 튜플로 받아 배열로 반환합니다.

    Example:
        >>> detectQR()
        [("https://github.com/WhiteHyun", "QRCODE")]
    """
    import cv2
    import pyzbar.pyzbar as pyzbar
    cap = cv2.VideoCapture(0)
    # 비디오 캡처가 준비되었는지
    decoded_list = []
    if not cap.isOpened():
        print("camera open failed")
        raise VideoError
    while True:
        ret, img = cap.read()  # 프레임 받아오기 -> ret: 성공하면 True, 아니면 False, img: 현재 프레임(numpy.ndarray)

        if not ret:  # 카메라 캡처에 실패할 경우
            print("camera read failed")
            raise VideoError

        cv2.imshow('img', img)
        cv2.waitKey(1)

        # RGB 3채널로 되어있는 이미지 파일을 GRAY 1채널로 변경하여 저장
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        decoded = pyzbar.decode(gray)  # 바코드 또는 QR코드를 찾고 해석

        if len(decoded) > 1:
            print("QRCODE가 2개 이상입니다!!!!!!!!!!!!")
            continue
        for decode in decoded:
            qrcode_data = decode.data.decode("utf-8")  # 디코드된 값 또는 파일
            qrcode_type = decode.type   # QR타입인지 바코드타입인지 확인
            decoded_list.append((qrcode_data, qrcode_type))

        if decoded_list:
            break

    cap.release()
    cv2.destroyAllWindows()
    return decoded_list[0]
