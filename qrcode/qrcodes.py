class QRCode:
    """
    QR코드 생성과 추출에 관여하는 클래스입니다.

    url 값을 가져와 QR코드를 생성할 수 있고, 이미지 값을 가져와 url로 추출할 수 있습니다.
    """


    def extractQRCode(self, url: str):
        """
        url 값을 통해 QRCode를 추출(생성)합니다.
        만약 url이 없을 경우 Error를 뿜습니다 *^^*

        Args:

        url (str): QRCode를 생성할 url값입니다.

        Example:
            >>> extractQRCode(url) # If Success
            <class 'qrcode.image.pil.PilImage'>

            >>> extractQRCode(url) # Fail
            Value Error
        """
        if url is None:
            print("URL 값이 입력되지 않았습니다!")
            raise ValueError

        import qrcode
        from lib.error import QRCodeError
        try:
            qr = qrcode.make(url)
            return qr
        except QRCodeError as e:
            print(f"QRCode 생성 중 오류가 발생하였습니다. {e}")
            raise QRCodeError
            

    def decodeQR(self, img) -> list:
        """
        받아온 흑백의 1차원 이미지(image)를 가지고 내부에 QR코드가 있는지에 대해 값을 리턴해주는 메서드입니다.

        Args:
            
            img (numpy.ndarray): 카메라를 통해 가져온 이미지 파일
        
        Returns:
            
            list (url: str, qrtype: str): QR코드에 대한 url과 타입을 튜플로 받아 배열로 반환합니다.

        Example:
            >>> decodeQR(img)
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