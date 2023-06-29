import RPi.GPIO as GPIO
import time

TRIG = 22
ECHO = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


try:
	while True:
		GPIO.output(TRIG, True)
		time.sleep(0.00001)	# 10uS의 펄스 발생을 위한 딜레이
		GPIO.output(TRIG, False)

		while GPIO.input(ECHO)==0:
			start = time.time()	# Echo핀 상승 시간값 저장

		while GPIO.input(ECHO)==1:
			stop = time.time()	# Echo핀 하강 시간값 저장

		check_time = stop - start
		distance = check_time * 34300/2
		print("Distance : %.1f cm" %distance)
		time.sleep(0.4)

except KeyboardInterrupt:
	print("거리 측정 완료")
	GPIO.cleanup()
