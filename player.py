import dbus, time, threading, os, pwd
from subprocess import Popen
from playermonitor import PlayerMonitor

class Player:
	def __init__(self, deck):
		#deck is the button (and associated LEDS) to which this video is assigned
		self.deck = deck
		self.filename = self.deck.filename
		self.dbusIfaceProp = None
		self.dbusIfaceKey = None
		self.monitorThread = threading.Thread(target=PlayerMonitor, args=(self, int(self.deck.outputPin)))
		self.monitorThread.daemon = True
		self.monitorThread.start()

	def play(self):
		cmd = "omxplayer %s &" %(self.filename)
		Popen([cmd], shell=True)

		done,retry = 0,0	
		while done==0:
			username = pwd.getpwuid(os.getuid()).pw_name
			#print username
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
			try:
				return str(self.dbusIfaceProp.PlaybackStatus())
			except dbus.exceptions.DBusException:
				return "Stopped"
	def pause(self):
		if self.dbusIfaceKey != None:
			self.dbusIfaceKey.Action(dbus.Int32("16"))
		else:
			print "ERROR: Cannot reach remote player to pause"
	def stop(self):
		#self.status = "Stopped"
		if self.dbusIfaceKey != None:
			self.dbusIfaceKey.Action(dbus.Int32("15"))
		else:
			print "ERROR: Cannot reach remote player to stop"	
