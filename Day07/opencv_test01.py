# OpenCV 테스트 템플릿 소스
import cv2
from picamera2 import Picamera2 # 카메라센서

cam = Picamera2()
cam.preview_configuration.main.size=(800, 600)
cam.preview_configuration.main.format='RGB888'
cam.preview_configuration.align()

cam.configure('preview')
cam.start()

while True:
    frame = cam.capture_array()
    cv2.imshow('picam', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()