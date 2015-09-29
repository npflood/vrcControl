from inputbutton import InputButton
from player import Player

class DeckController:
	def __init__(self, name, filename, inputPin, outputPin):
		self.name = name
		self.inputPin = inputPin
		self.outputPin = outputPin
		self.filename = filename
		self.player = Player(self)
		#self.status = self.player.status()
		self.inputbutton = InputButton(self.inputPin, self)

	def button_pressed(self):
		print "Button pressed on deck: %s" %(self.name)
		if self.status() == "Stopped":
			self.start()
		elif self.status() == "Playing" or self.status() == "Paused":
			self.pause()

	def start(self):
		self.player.play()

	def stop(self):
		self.player.stop()

	def pause(self):
		self.player.pause()

	def status(self):
		return self.player.status()
