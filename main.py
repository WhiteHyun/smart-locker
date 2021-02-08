import time
import serial


PORT = "/dev/ttyACM0"   # for test by arduino uno

arduino = serial.Serial(PORT, baudrate=9600, timeout=5)

time.sleep(5)

working = True
while True:
    try:
        do_rotate = "T" if input(
            "If 1, True. If not, False") == '1' else "F"
        arduino.write(do_rotate.encode())
    except Exception:
        raise Exception
