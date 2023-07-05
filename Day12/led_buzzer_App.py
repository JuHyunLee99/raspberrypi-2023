import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
import RPi.GPIO as GPIO
import time

LEDPIN=20
BUZZERPIN=13

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEDPIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BUZZERPIN, GPIO.OUT)
led_state = False
buzzer_state = False
buzz = GPIO.PWM(BUZZERPIN, 440)

class qtApp(QWidget):
	def __init__(self):
		super().__init__()
		uic.loadUi('./Day12/led_buzzer.ui', self)

		self.BtnBuzzer.clicked.connect(self.BtnBuzzerClicked)
		self.BtnLED.clicked.connect(self.BtnLEDClicked)

	def BtnBuzzerClicked(self):
		global buzzer_state
		if buzzer_state:
			buzz.stop()
			self.LblBuzzer.setText("Music OFF")
			self.LblBuzzer.setStyleSheet("color: GRAY; font-weight:bold;")
			self.BtnBuzzer.setText("PLAY")
		else:
			buzz.start(50)
			buzz.ChangeFrequency(10)
			self.LblBuzzer.setText("Music ON")
			self.LblBuzzer.setStyleSheet("color: red; font-weight:bold;")
			self.BtnBuzzer.setText("STOP")

		buzzer_state = not buzzer_state


	def BtnLEDClicked(self):
		global led_state
		if led_state:
			GPIO.output(LEDPIN, GPIO.LOW)
			self.LblLED.setText("OFF")
			self.LblLED.setStyleSheet("color: gray; font-weight: bold;")
			self.BtnLED.setText("LED ON")
		else:
			GPIO.output(LEDPIN, GPIO.HIGH)
			self.LblLED.setText("On")
			self.LblLED.setStyleSheet("color: blue; font-weight: bold;")
			self.BtnLED.setText("LED OFF")

		led_state = not led_state
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = qtApp()
	ex.show()
	sys.exit(app.exec_())
		
