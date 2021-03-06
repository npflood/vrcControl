import time
from outputled import OutputLED

class StopMonitor:
	def __init__(self, stopController, ledPin):
		self.led = OutputLED(int(ledPin))
		self.stopController = stopController
		self.led.off()
		self.start()

	def start(self):
		while True:
			status = self.stopController.supervisor.playback_state()
			#print status
			if status == "Playing":
				if self.led.get_state() != "off":
					#self.led.blink(0.5)
					self.led.off()
			elif status == "Paused":
				if self.led.get_state() != "off":
					#self.led.blink(0.5)
					self.led.off()
			elif status == "Stopped":
				if self.led.get_state() != "on":
					self.led.on()
			else:
				self.led.blink(0.25)
			time.sleep(0.5)
