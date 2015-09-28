import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

class InputButton:
	def __init__(self, buttonPin, controller):
		self.buttonPin = buttonPin
		self.controller = controller
		GPIO.add_event_detect(int(self.buttonPin), GPIO.FALLING, callback=self.callback, bouncetime=300) 
	
	def callback(self):
		self.controller.button_pressed()