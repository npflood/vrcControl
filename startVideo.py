#!/usr/bin/env python

import dbus, time, threading, os, pwd
from subprocess import Popen
from outputled import OutputLED


decks = [{'name': 'D1', 'ledPin': 7, 'switchPin': 8},{'name': 'D2', 'ledPin': 9, 'switchPin': 10},{'name': 'D3', 'ledPin': 11, 'switchPin': 12}]


class PlayerMonitor:
	def __init__(self, player, ledPin, switchPin):
		self.led = OutputLED(int(ledPin))
		self.player = player
		#TODO self.switchPin = switchPin
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
		

class Player:
	def __init__(self, filename, deck):
		#deck is the button (and associated LEDS) to which this video is assigned
		self.filename = filename
		self.deck = deck
		self.dbusIfaceProp = None
		self.dbusIfaceKey = None
		self.monitorThread = threading.Thread(target=PlayerMonitor, args=(self, 7, 8))
		#TODO: Change 7, 8 above to deck properties
		self.monitorThread.start()

	def play(self):
		cmd = "omxplayer %s &" %(self.filename)
		Popen([cmd], shell=True)

		done,retry = 0,0	
		while done==0:
			username = pwd.getpwuid(os.getuid()).pw_name
			print username
        		try:
                		with open('/tmp/omxplayerdbus.%s'%(username), 'r+') as f:
                        		omxplayerdbus = f.read().strip()
                		bus = dbus.bus.BusConnection(omxplayerdbus)
                		object = bus.get_object('org.mpris.MediaPlayer2.omxplayer','/org/mpris/MediaPlayer2', introspect=False)
                		self.dbusIfaceProp = dbus.Interface(object,'org.freedesktop.DBus.Properties')
                		self.dbusIfaceKey = dbus.Interface(object,'org.mpris.MediaPlayer2.Player')
                		done=1
			except:
                		retry+=1
                		if retry >= 500:
                        		print "Dbus ERROR Connecting To Player Instance"
                        		raise SystemExit
					self.dbusIfaceProp = None
					self.dbusIfaceKey = None

	def status(self):
		if self.dbusIfaceProp == None:
			return "Stopped"
		else:
			return self.dbusIfaceProp.PlaybackStatus()
	def pause(self):
		if self.dbusIfaceKey != None:
			self.dbusIfaceKey.Action(dbus.Int32("16"))
		else:
			print "Cannot reach remote player to pause"
	def stop(self):
		self.status = "Stopped"
		if self.dbusIfaceKey != None:
			self.dbusIfaceKey.Action(dbus.Int32("15"))
		else:
			print "Cannot reach remote player to stop"	

#activeDecks = []


#Start Video
d1 = Player("sample.mp4", "d1")
d1.play()

# key: pause after 5 seconds
time.sleep(15)
d1.pause()


# key: un-pause after 5 seconds
time.sleep(15)
d1.pause()

# key: quit after 5 seconds
time.sleep(15)
d1.stop()
