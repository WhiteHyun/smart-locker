if __name__ == "__main__":
    import cv2
    import sys
    from qrcodes import QRCode

    ESC_KEY = 27

    cap = cv2.VideoCapture(0)
    qr = QRCode()

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

        result = qr.decodeQR(gray)
        if result:
            break
        key = cv2.waitKey(1)

    cv2.destroyAllWindows()
