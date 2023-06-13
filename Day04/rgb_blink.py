import RPi.GPIO as GPIO
import time
red =17
green = 27
blue = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(red,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)
GPIO.setup(blue,GPIO.OUT)

# 초기화
GPIO.output(green, True) 
GPIO.output(blue, True)
GPIO.output(red, True)
        

try:
    while True:
        # RED
        GPIO.output(green, True)   
        GPIO.output(blue, True)
        GPIO.output(red, False)
        time.sleep(2)
        # GREEN
        GPIO.output(blue, True)
        GPIO.output(red, True)
        GPIO.output(green, False)
        time.sleep(2)

        # BLUE
        GPIO.output(red, True)
        GPIO.output(green, True)
        GPIO.output(blue, False)
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.output(green, True)   
    GPIO.output(blue, True)

    GPIO.cleanup()

