import smbus
import random
import datetime
import math
import time

from classes.sensors.Sensor import Sensor
from config import sr_settings
from config import settings

class SRSensor(Sensor):
	def __init__(self,
		_logger):
		
		super(SRSensor, self).__init__(_logger)
		
		self.i2c_bus = None
		self.i2c_address = None
		self.setup_sensor()
	
	
	def set_soil_measurement(self,
		_measurement):
		self.soil_measurement = _measurement
	
	
	def set_rain_measurement(self,
		_measurement):
		self.rain_measurement = _measurement

	
	def setup_pins(self):
		pass
		
		
	def setup_sensor(self):
		# Setting up sensor for weather recording.
		self.i2c_bus = smbus.SMBus(sr_settings.I2C_CHANNEL)
		self.i2c_address = sr_settings.ADS1115_ADDRESS

	
	def measure(self):
		# Soil moisture
		# Set config and start measuring immediately.
		self.i2c_bus.write_i2c_block_data(
			self.i2c_address,
			sr_settings.ADS1115_CONFIG_REGISTER,
			[sr_settings.ADS1115_CONFIG_REGISTER_WRITE_SOIL_BYTE_1,
			 sr_settings.ADS1115_CONFIG_REGISTER_WRITE_SOIL_BYTE_2])
		
		while self.i2c_bus.read_i2c_block_data(
			self.i2c_address,
			sr_settings.ADS1115_CONFIG_REGISTER,
			1)[0] == sr_settings.ADS1115_CONFIG_REGISTER_READ_SOIL_BYTE_1:
			time.sleep(0.001) # Sleep for a tiny bit; still performing the conversion.
		
		# Measuring finished; read integer value now.
		byte1, byte2 = self.i2c_bus.read_i2c_block_data(
			self.i2c_address,
			sr_settings.ADS1115_CONVERSION_REGISTER,
			2)
		measurement = (byte1 << 8) + byte2
		self.soil_measurement.measurement = self.calc_percentage(
			sr_settings.ADS1115_OUTPUT_CODE_MIN_SOIL,
			sr_settings.ADS1115_OUTPUT_CODE_MAX,
			measurement)
		
		# Raindrops
		self.i2c_bus.write_i2c_block_data(
			self.i2c_address,
			sr_settings.ADS1115_CONFIG_REGISTER,
			[sr_settings.ADS1115_CONFIG_REGISTER_WRITE_RAIN_BYTE_1,
			sr_settings.ADS1115_CONFIG_REGISTER_WRITE_RAIN_BYTE_2])
		
		while self.i2c_bus.read_i2c_block_data(
			self.i2c_address,
			sr_settings.ADS1115_CONFIG_REGISTER,
			1)[0] == sr_settings.ADS1115_CONFIG_REGISTER_READ_RAIN_BYTE_1:
			time.sleep(0.001) # Sleep for a tiny bit; still performing the conversion
		
		# Measureing finished; read integer value now.
		byte1, byte2 = self.i2c_bus.read_i2c_block_data(
			self.i2c_address,
			sr_settings.ADS1115_CONVERSION_REGISTER,
			2)
		measurement = (byte1 << 8) + byte2
		self.rain_measurement.measurement = self.calc_percentage(
			sr_settings.ADS1115_OUTPUT_CODE_MIN_RAIN,
			sr_settings.ADS1115_OUTPUT_CODE_MAX,
			measurement)
		
		# Set date and time for both measurements for later DB write.
		date_time_now = datetime.datetime.now()
		self.soil_measurement.timestamp = date_time_now
		self.rain_measurement.timestamp = date_time_now
	
	
	def calc_percentage(self,
		_min,
		_max,
		_current):
		"""Calcs the percentage of humidity and returns a value between 0 and 100 (100 meaning completely
		under water :))"""
		
		one_percent = (_max - _min) / 100
		
		if one_percent == 0:
			return 100 # We assume 100% humidity here.

		m1 = _current - _min
		m2 = m1 // one_percent
		m3 = int(100 - m2)
		
		return m3 # Return humidity in percentage
