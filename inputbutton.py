import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

class InputButton:
	def __init__(self, buttonPin, controller):
		self.buttonPin = buttonPin
		GPIO.setup(int(self.buttonPin), GPIO.IN, pull_up_down=GPIO.PUD_UP)
		self.controller = controller
		GPIO.add_event_detect(int(self.buttonPin), GPIO.FALLING, callback=self.callback, bouncetime=300) 
	
	def callback(self, channel):
		self.controller.button_pressed()
