import RPi.GPIO as GPIO
import time

pwm_pin = 18
GPIO.setwarnings(False) # 오류메세지 제거
GPIO.setmode(GPIO.BCM) # GPIO 핀뜰의 뻔호를 찌쩡하는 뀨칚
GPIO.setup(pwm_pin, GPIO.OUT) # 서보핀을 출력으로 설장
pwm = GPIO.PWM(pwm_pin, 50) # 서보핀을 PWM 50Hz로 사용
pwm.start(3.0)   # 서보모터의 초기값 3으로 설정, 듀티비 최소3 ~ 최대20

for i in range(0, 3):
    for high in range(30, 125):
        pwm.ChangeDutyCycle(high/10.0)  # 3~12.4
        time.sleep(0.02)

    for low in range(124, 30, -1):
        pwm.ChangeDutyCycle(low/10.0)   # 12.4~29
        time.sleep(0.02)

pwm.ChangeDutyCycle(0)
pwm.stop()
GPIO.cleanup()