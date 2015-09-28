import threading
from inputbutton import InputButton
from stopmonitor import StopMonitor

class StopController:
	def __init__(self, supervisor, inputPin, outputPin):
		self.supervisor = supervisor
		self.inputPin = inputPin
		self.outputPin = outputPin
		self.inputbutton = InputButton(self.inputPin, self)
		self.monitorThread = threading.Thread(target=StopMonitor, args=(self, int(self.outputPin)))
		self.monitorThread.start()
	def button_pressed(self):
		print "Stop Button Pressed."
		self.supervisor.stop_all()
