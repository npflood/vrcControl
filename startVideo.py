#!/usr/bin/env python

import time
from deckcontroller import DeckController
from stopcontroller import StopController

class Supervisor:
	def __init__(self):
		self.stopButton = StopController(self, 11, 12)
		#todo: implement stopController parameters from configuration file
		self.deck_list = []
		self.deck_list.append(DeckController("Deck 1", "sample.mp4", 8, 7))
		#todo: implement deck parameters from configuration file
		#todo: implement power on button
		#todo: implement power off button
		self.self_check()

	def playback_state(self):
		states = map((lambda x: x.status), self.deck_list)

		if "Playing" in states:
			return "Playing"
		elif "Paused" in states: 
			return "Paused"
		else:
			return "Stopped"

	def stop_all(self):
		for deck in self.deck_list:
			deck.stop()

	def self_check(self):
		#todo: have the system cycle all the lights
		print "We should be self checking."



supervisor = Supervisor()

#Start Video
deck1 = supervisor.deck_list[0]
deck1.start()

# key: pause after 5 seconds
time.sleep(15)
deck1.pause()


# key: un-pause after 5 seconds
time.sleep(15)
deck1.pause()

# key: quit after 5 seconds
time.sleep(15)
supervisor.stop_all()

time.sleep(5)
deck1.start()
time.sleep(10)
supervisor.stop_all()

time.sleep(10)
