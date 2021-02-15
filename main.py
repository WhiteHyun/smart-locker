if __name__ == "__main__" or __name__ == "main":
    import time
    import serial
    from src.qrcodes import detectQR

PORT = "/dev/ttyACM0"   # for test by arduino uno

arduino = serial.Serial(PORT, baudrate=9600, timeout=5)

time.sleep(5)
while True:
    try:
        qr_lists = detectQR()
        for qr_url, _ in qr_lists:
            arduino.write(f"{qr_url}\n".encode())
    except Exception:
        raise Exception
