import RPi.GPIO as GPIO
import time

swPin = 21
ledPin = 20
state = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)
def callbackfunc (channel):
	global state
	print("Interrupt !!")
	if state:
		state = False
	else:
		state = True
		
GPIO.add_event_detect(swPin, GPIO.RISING, callback=callbackfunc)

try:
	while True:
		GPIO.output(ledPin, state)
except KeyboardInterrupt:
	GPIO.cleanup()
