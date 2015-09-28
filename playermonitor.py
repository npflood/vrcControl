from outputled import OutputLED

class PlayerMonitor:
	def __init__(self, player, ledPin):
		self.led = OutputLED(int(ledPin))
		self.player = player
		self.led.off()
		self.start()

	def start(self):
		while True:
			try:
				status = self.player.status()
				if status == "Playing":
					if self.led.get_state() != "on":
						self.led.on()
				elif status == "Paused":
					if self.led.get_state() != "blinking":
						self.led.blink(0.5)
				elif status == "Stopped":
					if self.led.get_state() != "off":
						self.led.off()
				else:
					self.led.blink(0.25)
				time.sleep(0.5)
			except(dbus.exceptions.DBusException):
				#?won't be necessary when we move all dbus into the player
				self.led.off()
				break
			except(KeyboardInterrupt, SystemExit):
				raise