# 7세그먼트
import RPi.GPIO as GPIO
import time

BUTTON=21   # 스위치
FND = [2,3,4,5,6,7,8,9] #7seg핀번호 abcdefgdp
SEGTABLE = [0x3F, 0x06, 0x5B, 0x4F, 0x66,0x6D, 0x7D, 0x07,
            0x7F, 0x6f, 0x77, 0x7C, 0X58, 0x5E, 0x79, 0x71,
            0x00]   # 표현 숫자[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15, 16] 

count = -1

def clickHandler(channel):
    global count, SEGTABLE    # 클릭 횟수, 표현 숫자
    count = count + 1

    mask = 0x01

    for pin in FND:
        flage = SEGTABLE[count] & mask
        print(flage & mask, end=' ')
        GPIO.output(pin, SEGTABLE[count] & mask)
        mask <<= 1 
        
    print()
    if(count>=16):
        count = -1

GPIO.setwarnings(False) # 쓸데없는 경고표시 로그 사라짐
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # 스위치 입력핀 설정 
for pin in FND:        # 7seg 출력핀 설정
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False) # 7seg 모든 핀 False
GPIO.add_event_detect(BUTTON, GPIO.RISING, callback=clickHandler)

while(1):
    time.sleep(1)


