import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

pirpin = 7
GPIO.setup(pirpin,GPIO.IN,GPIO.PUD_UP)

while True:
    if GPIO.input(pirpin) == GPIO.LOW:
        print('1111')
    else:
        print('2222')
    time.sleep(0.2)