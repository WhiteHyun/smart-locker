import sys
import cv2
import pyzbar.pyzbar as pyzbar

if __name__ == "__main__":

    img = cv2.imread("WhiteHyun Github QR.png", cv2.IMREAD_GRAYSCALE)

    decoded = pyzbar.decode(img)  # 바코드 또는 QR코드를 찾고 해석한다.
    for d in decoded:
        x, y, w, h = d.rect
        barcode_data = d.data.decode("utf-8")  # 디코드된 값 또는 파일
        barcode_type = d.type   # QR타입인지 바코드타입인지 확인

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        text = f"{barcode_data} ({barcode_type})"
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('img', img)
    key = cv2.waitKey()
