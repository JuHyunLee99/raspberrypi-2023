import RPi.GPIO as GPIO
import time

# 핀번호
swPin = 21
ledPin = 20
buzzerPin = 13

# 인터럽트 상태
state = False

# 멜로디
music = [130, 245]

# 세팅, 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buzzerPin, GPIO.OUT)
buzz = GPIO.PWM(buzzerPin, 440) # 440Hz를 갖는 객체 생성


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
		GPIO.output(ledPin, False)
		i = 0	# led, 부저  신호		
		while state:
			buzz.start(90)  # duty cycle 90으로 pwm 출력 시작			
			GPIO.output(ledPin, i)			
			buzz.ChangeFrequency(music[i]) # 주파수변경
			time.sleep(0.3)	# 0.3초 소리 유지	

			if i:
				i = 0
			else:
				i = 1
				
		buzz.stop()
			
except KeyboardInterrupt:
	GPIO.cleanup()
