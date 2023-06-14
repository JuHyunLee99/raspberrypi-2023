# MQTT 패키지 설치 - paho-mqtt
# sudo pip install paho-mqtt
## 동시에 publish(데이터 전송[출판]) / subcribe(데이터 수신[구독]) 처리

from threading import Thread, Timer
import time # time.sleep()
import json # 파이썬에서는 기본 제공 c#에서는 Newthon soft
import datetime as dt

import paho.mqtt.client as mqtt
import Adafruit_DHT as dht

sensor = dht.DHT11 # 초 저가 센서
rcv_pin = 10


class publisher(Thread):
    def __init__(self):
        Thread.__init__(self) # Thread 초끼화
        self.host = '210.119.12.55' # 본인pc ip
        self.port = 1883 # 회사에서는 이 포트 그대로 사용하면 안됨
        self.clientId = 'IOT55'
        self.count = 0
        print('publisher 스레드 시작')
        self.client = mqtt.Client(client_id= self.clientId) # 설계대로

    def run(self): # 실행시키는 함수
        self.client.connect(self.host, self.port)

        # self.client.username_pw_set() // id/pw로 로그인할때는 필요
        self.publish_data_auto()

    def publish_data_auto(self):
        humid, temp = dht.read_retry(sensor, rcv_pin)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 2023-06-14 10:39:54
        origin_data = {'DEV_ID' : self.clientId,
                        'CURR_DT' : curr,
                        'TYPE' : 'TEMPHUMID',
                        'STAT' : f'{temp} | {humid}'} #sample data
        pub_data = json.dumps(origin_data) # MQTT로 전송할 데이터를 json으로 변환
        self.client.publish(topic='pknu/rpi/control/', payload=pub_data)
        print(f'Data Published # {self.count}')
        self.count = self.count +1
        Timer(2.0, self.publish_data_auto).start() # 2초 마다 출판

class subcriber(Thread):
    pass # ToBeContinued...

if __name__ =='__main__':
    thPub = publisher() # publisher 객체생성
    thPub.start() # run() 자동실행