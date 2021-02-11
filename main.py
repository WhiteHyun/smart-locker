import time
import serial


PORT = "/dev/ttyACM0"   # for test by arduino uno

arduino = serial.Serial(PORT, baudrate=9600, timeout=5)

time.sleep(5)

while True:
    try:
        do_rotate = "T" if len(input("문을 열고싶을 경우 아무거나 입력하세요.")) > 1 else "F"
        arduino.write(do_rotate.encode())
    except Exception:
        raise Exception
