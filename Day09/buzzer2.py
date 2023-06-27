import RPi.GPIO as  GPIO
import time
import keyboard

buzzerPin = 13
melody = {'1':131, '2':147, '3':165, '4':175, '5':196,
					'6':220, '7':247, '8':262}

# 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin, GPIO.OUT)


def play_melody(key):
	buzz = GPIO.PWM(buzzerPin, melody[key])	# 440Hz를 갖는 객체 생성
	buzz.start(50)	# duty cycle 50으로 pwm 출력 시작	// 소리 크기 조절	
	time.sleep(0.3)	# 음길이
	buzz.stop() # 정지

try:
	while True:
		play_melody(input())
		
except KeyboardInterrupt:	# 키보드 인터럽트
	GPIO.cleanup()
