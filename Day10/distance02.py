import RPi.GPIO as GPIO
import time
# 핀번호
TRIGPIN = 22
ECHOPIN = 23
BUZZERPIN = 13
# 멜로디
music = [130, 245]

# 세팅
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGPIN, GPIO.OUT)
GPIO.setup(ECHOPIN, GPIO.IN)
GPIO.setup(BUZZERPIN, GPIO.OUT)
buzz = GPIO.PWM(BUZZERPIN, 440)

try:
	while True:
		GPIO.output(TRIGPIN, True)
		time.sleep(0.00001)	# 10uS의 펄스 발생을 위한 딜레이
		GPIO.output(TRIGPIN, False)

		while GPIO.input(ECHOPIN)==0:
			start = time.time()	# Echo핀 상승 시간값 저장

		while GPIO.input(ECHOPIN)==1:
			stop = time.time()	# Echo핀 하강 시간값 저장

		check_time = stop - start
		distance = check_time * 34300/2
		print("Distance : %.1f cm" %distance)

		if distance <= 5.0:
			print("주의 너무 가까워용")
			buzz.start(90)
			for i in music:
				buzz.ChangeFrequency(i)
				time.sleep(0.3)
		else:
			buzz.stop()
				
		time.sleep(0.4)

except KeyboardInterrupt:
	print("거리 측정 완료")
	GPIO.cleanup()
