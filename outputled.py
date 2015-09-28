import threading
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class OutputLED:
	def __init__(self, ledPin):
		self.ledPin = ledPin
		GPIO.setup(self.ledPin, GPIO.OUT)
		self.e = threading.Event()
		self.off()
	def on(self):
		self.e.set()
		GPIO.output(self.ledPin,True)
		self.state = "on"
	def off(self):
		self.e.set()
		GPIO.output(self.ledPin,False)
		self.state = "off"
	def blink(self, rate):
		if self.state == "blinking":
			self.e.set()
			time.sleep(float(rate))
		self.e.clear()
		tempThread = threading.Thread(target=self.blinkThread, args=(self.e, float(rate)))
		tempThread.start()
		self.state = "blinking"
	def get_state(self):
		return self.state
	def blinkThread(self, e, t):
		while not e.isSet():
			GPIO.output(self.ledPin,True)
			event_is_set = e.wait(t)
			if event_is_set:
				return 0
			else:
				GPIO.output(self.ledPin,False)
				time.sleep(t)
