# This module can be executed as module and script and by doctest.
if __name__ == "__main__" or __name__ == "qrcodes":
    from error.error import VideoError
    from error.error import QRCodeError
else:
    from .error.error import VideoError
    from .error.error import QRCodeError


class QRCodes:
    """
    QR코드 생성과 추출에 관여하는 클래스입니다.

    url 값을 가져와 QR코드를 생성할 수 있고, 이미지 값을 가져와 url로 추출할 수 있습니다.
    """

    def generateQR(self, url: str) -> bool:
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
            qr.save(f"data/qrcode_{url}.png")
        except QRCodeError as e:
            print(f"QRCode 생성 중 오류가 발생하였습니다. {e}")
            raise QRCodeError
        else:
            return True

    def __scanQR(self, img) -> list:
        """
        받아온 흑백의 1차원 이미지(image)를 가지고 내부에 QR코드가 있는지에 대해 값을 리턴해주는 메서드입니다.

        Args:

            img (numpy.ndarray): 카메라를 통해 가져온 흑백 이미지 파일

        Returns:

            list (url: str, qrtype: str): QR코드에 대한 url과 타입을 튜플로 받아 배열로 반환합니다.

        Example:
            >>> __scanQR(img)
            [("Hello World!", "QRCODE"), ("https://github.com/WhiteHyun", "QRCODE")]
        """
        import pyzbar.pyzbar as pyzbar
        decoded_list = []
        decoded = pyzbar.decode(img)  # 바코드 또는 QR코드를 찾고 해석
        for decode in decoded:
            qrcode_data = decode.data.decode("utf-8")  # 디코드된 값 또는 파일
            qrcode_type = decode.type   # QR타입인지 바코드타입인지 확인
            decoded_list.append((qrcode_data, qrcode_type))

        return decoded_list

    def detectQR(self) -> list:
        """
        QR코드를 탐지합니다.
        """
        import cv2
        cap = cv2.VideoCapture(0)
        # 비디오 캡처가 준비되었는지
        if not cap.isOpened():
            print("camera open failed")
            raise VideoError
        while True:
            ret, img = cap.read()  # 프레임 받아오기 -> ret: 성공하면 True, 아니면 False, img: 현재 프레임(numpy.ndarray)

            if not ret:  # 카메라 캡처에 실패할 경우
                print("camera read failed")
                raise VideoError

            # RGB 3채널로 되어있는 이미지 파일을 GRAY 1채널로 변경하여 저장
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            result = self.__scanQR(gray)
            if result:
                break
            cv2.imshow('img', img)
            cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()
        return result


def testFunc(url):
    qr = QRCodes()
    return qr.generateQR("Hello, World!")
