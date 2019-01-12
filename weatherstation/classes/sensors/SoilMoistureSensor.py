import RPi.GPIO as GPIO
import random
import datetime

from classes.sensors.Sensor import Sensor


GPIO.setmode(GPIO.BCM)


class SoilMoistureSensor(Sensor):
	def __init__(self,
		_channel,
		_mode,
		_logger):

		
		self.channel = _channel
		self.mode = _mode
		
		super(SoilMoistureSensor, self).__init__(_logger)
		
		self.setup_pins()
	
	
	def setup_pins(self):
		GPIO.setup(self.channel,
				   self.mode)
		
	
	def measure(self):
		if GPIO.input(self.channel):
			self.measurement.measurement = 0
		else:
			self.measurement.measurement = 100
		
		self.measurement.timestamp = datetime.datetime.now()
		
		fields = ["measurement",
				  "timestamp",
				  "type",
				  "unit"]
