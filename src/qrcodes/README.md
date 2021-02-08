# QR코드 생성 모듈

## 메소드

### QR생성 메소드

```python
def generateQR(self, url: str)


>>> qr = QRCodes()
>>> qr.generateQR("SAMPLE URL")

<class 'qrcode.image.pil.PilImage'>
```

### QR인식 메소드

```python

def detectQR(self)


>>> qr = QRCodes()
>>> qr.detectQR()

[("Hello World!", "QRCODE"), ("https://github.com/WhiteHyun", "QRCODE")]

```

### 앞으로 시도해볼 것

- QRCode 내에 사진 붙여보기 😎

### 참고 사이트

[Generate QR code image with Python, Pillow, qrcode | note.nkmk.me](https://note.nkmk.me/en/python-pillow-qrcode/)
