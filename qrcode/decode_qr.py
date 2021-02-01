import sys
import cv2
import pyzbar.pyzbar as pyzbar

ESC_KEY = 27
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    i = 0  # 캡처 저장용 변수

    # 비디오 캡처가 준비되었는지
    if not cap.isOpened():
        print("camera open failed")
        sys.exit()

    while True:
        ret, img = cap.read()  # 프레임 받아오기 -> ret: 성공하면 True, 아니면 False, img: 현재 프레임(numpy.ndarray)

        if not ret:  # 카메라 캡처에 실패할 경우
            print("camera read failed")
            break

        # RGB 3채널로 되어있는 이미지 파일을 GRAY 1채널로 변경하여 저장
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        decoded = pyzbar.decode(gray)  # 바코드 또는 QR코드를 찾고 해석
        for d in decoded:
            x, y, w, h = d.rect
            barcode_data = d.data.decode("utf-8")  # 디코드된 값 또는 파일
            barcode_type = d.type   # QR타입인지 바코드타입인지 확인

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

            text = f"{barcode_data} ({barcode_type})"
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('img', img)

        key = cv2.waitKey(1)
        if key == ord('q') or key == ESC_KEY:
            break
        elif key == ord('s'):
            i += 1
            cv2.imwrite(f'capture_{i:03d}.jpg', img)

    cap.release()
    cv2.destroyAllWindows()
