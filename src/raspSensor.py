import RPi.GPIO as GPIO
import time


class DetectMotion:

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        self.pirpin = 7
        GPIO.setup(self.pirpin,GPIO.IN,GPIO.PUD_UP)
    

    def wait_for_motion(self):

        while True:
            if GPIO.input(self.pirpin) != GPIO.LOW:
                return True
            time.sleep(0.2)