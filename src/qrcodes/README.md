# QR코드 생성 모듈

## 메소드

### QR생성 메소드

- 해당 메소드 실행 시 url값에 따른 QR코드가 생성되어지며 어떠한 오류 없이 생성되었을 경우 True를 리턴합니다.

  ```python
  def generateQR(self, url: str)


  >>> qr = QRCodes()
  >>> qr.generateQR("SAMPLE URL")

  True
  ```

  단, 어떠한 이유로 인한 오류 발생 시 에러를 일으킵니다.

  ```python
  # 빈 문자열을 넣는 경우
  >>> qr = QRCodes()
  >>> qr.generateQR("")

  ValueError
  ```

  ```python
  # 그 외 코드 실행중 오류가 발생한 경우
  >>> qr = QRCodes()
  >>> qr.generateQR("test code")

  QRCode 생성 중 오류가 발생하였습니다. QRCodeError
  ```

### QR인식 메소드

- 해당 메소드를 실행하게 되면 라즈베리파이에 부착되어있는 카메라 모듈이 QR코드를 인식하는 기능으로 사용되게 됩니다.
  이 때 카메라에 QR코드를 나타낼 경우 해당 QR코드에 대한 정보를 반환합니다.

  ```python

  def detectQR(self)


  >>> qr = QRCodes()
  >>> qr.detectQR()

  [("Hello World!", "QRCODE"), ("https://github.com/WhiteHyun", "QRCODE")]

  ```

### 앞으로 시도해볼 것 (선택)

- QRCode 내에 사진 붙여보기 😎

### 참고 사이트

[Generate QR code image with Python, Pillow, qrcode | note.nkmk.me](https://note.nkmk.me/en/python-pillow-qrcode/)
