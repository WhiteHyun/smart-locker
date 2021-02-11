import time
import serial
from src.qrcodes.qrcodes import QRCodes

PORT = "/dev/ttyACM0"   # for test by arduino uno

arduino = serial.Serial(PORT, baudrate=9600, timeout=5)

time.sleep(5)
qr = QRCodes()
while True:
    try:
        qr_lists = qr.detectQR()
        for qr_url, _ in qr_lists:
            arduino.writelines(qr_url.encode())
    except Exception:
        raise Exception
