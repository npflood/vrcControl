##
# Ruby Interface To SerLCD Module by sparkfun
# Currently set up for a 4 line 20 character display
##

require 'pp'
require 'rubygems'
require 'serialport'
require 'socket'
require 'daemons'


class LCD
	def initialize(port, baud_rate=9600, data_bits=8, stop_bits=1, parity=SerialPort::NONE)
		@buffer=["","","","",""]
		@serial_port = SerialPort.new(port, baud_rate, data_bits, stop_bits, parity)
	end

	def buffer
		return @buffer
	end

	def setLine(line, value)
		@buffer[line] = value.to_s
	end

	def getLine(line)
		return @buffer[line].to_s
	end

	def clearBufferLine(line)
		@buffer[line] = ""
	end

	def update
		#puts "Clearing LCD"
		#clearLCD
		#sleep 1

		buffer.each_with_index do |value, line|
			#puts "Writing Line #{line} wtih #{value}"
			#sleep 1
			writeLine line, value
			#sleep 5
		end
	end


	def configureLCD
		##Makes it work with the 20X4 Display.
		@serial_port.write("\x7C")
		@serial_port.write("\x03")
		@serial_port.write("\x7C")
		@serial_port.write("\x05")
	end

	def selectLine(line)	
		case line
		when 1
			serCommand
			@serial_port.write("\x80")
		when 2
			serCommand
			@serial_port.write("\xC0")
		when 3
			serCommand
			@serial_port.write("\x94")
		when 4
			serCommand
			@serial_port.write("\xD4")
		else
			#Do Nothing
		end
	end

	def clearLine(line)
		selectLine line
		@serial_port.write('')
	end

	def writeLine(line, value)
		#clearLine line
		selectLine line
		@serial_port.write value
	end

	def clearLCD
		serCommand
		@serial_port.write("\x01")
	end

	def backlightOn
		@serial_port.write("\x7C")
		@serial_port.write("\x9D")
	end

	def backlightOff
		@serial_port.write("\x7C")
		@serial_port.write("\x80")
	end

	def backlightDim
		@serial_port.write("\x7C")
		@serial_port.write("\x8F")
	end

	def serCommand
		@serial_port.write("\xFE")
	end


end

Daemons.run_proc('lcdServer.rb')do
	piLCD = LCD.new("/dev/ttyAMA0")

	sleep 2
	piLCD.backlightOn
	sleep 1
	piLCD.clearLCD
	sleep 1

	while true
		t = Time.now
		piLCD.setLine 1, t.strftime("%m/%d/%Y")
		piLCD.setLine 2, t.strftime("%I:%M:%S%p")
		piLCD.setLine 3, UDPSocket.open {|s| s.connect("64.233.187.99", 1); s.addr.last}
		piLCD.setLine 4, "Raspberry Pi"

		#pp piLCD.buffer

		piLCD.update
		sleep 1
	end
end