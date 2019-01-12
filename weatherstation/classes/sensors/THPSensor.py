import smbus
import random
import datetime
import math
import time

from classes.sensors.Sensor import Sensor
from config import thp_settings as BME280
from config import settings

class THPSensor(Sensor):
	def __init__(self,
		_logger):
		
		super(THPSensor, self).__init__(_logger)
		
		self.i2c_bus = None
		
		self.setup_sensor()
		
		self.temp_fine = None
	
	
	def set_temperature_measurement(self,
		_measurement):
		self.temperature_measurement = _measurement
	
	
	def set_humidity_measurement(self,
		_measurement):
		self.humidity_measurement = _measurement
	
	
	def set_pressure_measurement(self,
		_measurement):
		self.pressure_measurement = _measurement

	
	def set_measurement(self):
		print("Call set_temperature_measurement(), set_humidity_measurement() and set_pressure_measurement() instead")
	
	
	def setup_pins(self):
		pass
		
		
	def read_unsigned_short(self,
		_register):
		"""Reads two registers, starting at '_register'.
		Returns an unsigned short (2 bytes).
		
		"""
		return self.i2c_bus.read_word_data(
			BME280.BME280_ID,
			_register)
	
	
	def read_signed_short(self,
		_register):
		"""Reads two registers, starting at "_register".
		Returns a signed short (2 bytes).
		
		"""
		word_data = self.read_unsigned_short(_register)
		if word_data >= math.ceil(0xFFFF / 2):
			word_data = ((word_data ^ 0xFFFF) + 1) * -1
		
		return word_data
		
	
	def read_unsigned_byte(self,
		_register):
		"""Reads one register.
		Returns an unsigned byte.
		
		"""
		return self.i2c_bus.read_byte_data(
			BME280.BME280_ID,
			_register)
		
	
	def read_signed_byte(self,
		_register):
		"""Reads one register.
		Returns a signed byte.
		
		"""
		byte = self.read_unsigned_byte(_register)
		if byte >= math.ceil(0xFF / 2):
			byte = ((byte ^ 0xFF) + 1) * -1
		
		return byte
		
	
	def setup_sensor(self):
		# Setting up sensor for weather recording.
		self.i2c_bus = smbus.SMBus(BME280.I2C_CHANNEL)
		
		# Fetch calibration data here, as we need it later on.
		# Data part 1
		self.calibration_data1 = self.i2c_bus.read_i2c_block_data(
			BME280.BME280_ID,
			BME280.DIG_T1_1,
			26)
		
		# Data part 2
		self.calibration_data2 = self.i2c_bus.read_i2c_block_data(
			BME280.BME280_ID,
			BME280.DIG_H2_1,
			7)
		
		# Calibration data
		self.T1 = self.read_unsigned_short(BME280.DIG_T1_1)
		self.T2 = self.read_signed_short(BME280.DIG_T2_1)
		self.T3 = self.read_signed_short(BME280.DIG_T3_1)
		
		self.P1 = self.read_unsigned_short(BME280.DIG_P1_1)
		self.P2 = self.read_signed_short(BME280.DIG_P2_1)
		self.P3 = self.read_signed_short(BME280.DIG_P3_1)
		self.P4 = self.read_signed_short(BME280.DIG_P4_1)
		self.P5 = self.read_signed_short(BME280.DIG_P5_1)
		self.P6	= self.read_signed_short(BME280.DIG_P6_1)		
		self.P7 = self.read_signed_short(BME280.DIG_P7_1)
		self.P8 = self.read_signed_short(BME280.DIG_P8_1)
		self.P9 = self.read_signed_short(BME280.DIG_P9_1)
	
		self.H1 = self.read_unsigned_byte(BME280.DIG_H1_1)
		self.H2 = self.read_signed_short(BME280.DIG_H2_1)
		self.H3 = self.read_unsigned_byte(BME280.DIG_H3_1)
		self.H4_1 = self.read_signed_byte(BME280.DIG_H4_1)
		self.H4_2 = self.read_signed_byte(BME280.DIG_H4_2)
		self.H5 = self.read_signed_byte(BME280.DIG_H5_1)
		self.H5_1 = self.read_signed_byte(BME280.DIG_H5_1)
		self.H5_2 = self.read_signed_byte(BME280.DIG_H5_2)
		self.H6 = self.read_signed_byte(BME280.DIG_H6_1)
	
	def measure(self):
		# Set config.
		self.i2c_bus.write_byte_data(
			BME280.BME280_ID,
			BME280.CONFIG,
			BME280.T_SB_1000 |
			BME280.FILTER)
			
		# Set humidity oversampling
		self.i2c_bus.write_byte_data(
			BME280.BME280_ID,
			BME280.CTRL_HUM,
			BME280.HUMIDITY_OVERSAMPLING_X1)
		
		# Set temp, pressure oversampling and
		# forced mode
		self.i2c_bus.write_byte_data(
			BME280.BME280_ID,
			BME280.CTRL_MEAS,
			BME280.CTRL_MEAS_OSRS_P_X1 |
			BME280.CTRL_MEAS_OSRS_T_X1 |
			BME280.CTRL_MEAS_MODE_FORCED)
			
		# Now perform measuring.
		# We need to wait until measuring is complete.
		# This the while loop.
		while self.i2c_bus.read_byte_data(
			BME280.BME280_ID,
			BME280.STATUS) & BME280.STATUS_MEASURING:
			pass
		
		# Filter, oversampling etc. copied to NVM.
		# Need to wait until its' done so that
		# we can read and convert data!
		while self.i2c_bus.read_byte_data(
			BME280.BME280_ID,
			BME280.STATUS) & BME280.STATUS_IM_UPDATE:
			pass

		
		# Read data and calculate temp, hum and press.
		raw_measurement_data = self.i2c_bus.read_i2c_block_data(
			BME280.BME280_ID,
			BME280.PRESS_MSB,
			8)
		
		pressure_msb = raw_measurement_data[0]
		pressure_lsb = raw_measurement_data[1]
		pressure_xlsb = raw_measurement_data[2]
		
		temperature_msb = raw_measurement_data[3]
		temperature_lsb = raw_measurement_data[4]
		temperature_xlsb = raw_measurement_data[5]
		
		humidity_msb = raw_measurement_data[6]
		humidity_lsb = raw_measurement_data[7]
		
		raw_temperature = ((temperature_msb << 16) | (temperature_lsb << 8) | temperature_xlsb) >> 4
		raw_pressure = ((pressure_msb << 16) | (pressure_lsb << 8) | pressure_xlsb) >> 4
		raw_humidity = (humidity_msb << 8) | (humidity_lsb)
		
		self.temperature = self.calculate_temperature(raw_temperature)
		self.pressure = self.calculate_pressure(raw_pressure)
		self.humidity = self.calculate_humidity(raw_humidity)
		
		date_time_now = datetime.datetime.now()
		
		self.temperature_measurement.measurement = self.temperature - 3 # Correction of temperature because it is by default too high.  The reason being the PCB it is soldered on.
		self.temperature_measurement.timestamp = date_time_now
		
		self.humidity_measurement.measurement = self.humidity + 20 # Correction of  humidity because it is by default too low.  Source: None, but asked google for the current humidity, and noticed it was off by 20%.
		self.humidity_measurement.timestamp = date_time_now
		
		self.pressure_measurement.measurement = self.pressure
		self.pressure_measurement.timestamp = date_time_now
		
		
	def calculate_temperature(self,
		raw_temperature):
		
		val1 = val2 = T = None
		dig_T1 = self.T1
		dig_T2 = self.T2
		dig_T3 = self.T3
		
		var1 = ((raw_temperature)/16384.0 - (dig_T1)/1024.0) * (dig_T2)
		var2 = (((raw_temperature)/131072.0 - (dig_T1)/8192.0) * ((raw_temperature)/131072.0 - (dig_T1)/8192.0)) * (dig_T3)
		self.temp_fine = (var1 + var2)
		T = (var1 + var2) / 5120.0
		return T
		
	
	def calculate_pressure(self,
		raw_pressure):
		
		var1 = var2 = p = None
		dig_P1 = self.P1
		dig_P2 = self.P2
		dig_P3 = self.P3
		dig_P4 = self.P4
		dig_P5 = self.P5
		dig_P6 = self.P6
		dig_P7 = self.P7
		dig_P8 = self.P8
		dig_P9 = self.P9	

		var1 = (self.temp_fine/2.0) - 64000.0
		var2 = var1 * var1 * (dig_P6) / 32768.0
		var2 = var2 + var1 * (dig_P5) * 2.0
		var2 = (var2/4.0)+((dig_P4) * 65536.0)
		var1 = (float(dig_P3) * var1 * var1 / 524288.0 + float(dig_P2) * var1) / 524288.0
		var1 = (1.0 + var1 / 32768.0) * float(dig_P1)
		
		if var1 == 0:
			return 0 # avoid exception caused by division by zero

		p = 1048576.0 - float(raw_pressure)
		p = (p - (var2 / 4096.0)) * 6250.0 / var1
		var1 = float(dig_P9) * p * p / 2147483648.0
		var2 = p * float(dig_P8) / 32768.0
		p = p + (var1 + var2 + float(dig_P7)) / 16.0
		
		p = p / 100.0
		
		# Correct air pressure at 487 meters.
		p = p / pow(1.0 - (settings.HEIGHT / 44330.0), 5.255)
		return p

		
	def calculate_humidity(self,
		raw_humidity):
		
		dig_H1 = self.H1
		dig_H2 = self.H2
		dig_H3 = self.H3
		
		dig_H4_1 = self.H4_1 << 4
		dig_H4_2 = self.H4_2 & 0x0F
		dig_H4 = dig_H4_1 | dig_H4_2
		
		dig_H5_1 = self.H5_1 >> 4
		dig_H5_2 = self.H5_2 << 4
		dig_H5 = dig_H5_2 | dig_H5_1
		
		dig_H6 = self.H6
		
		var_H = ((self.temp_fine) - 76800.0)
		var_H = (raw_humidity - ((dig_H4) * 64.0 + (dig_H5) / 16384.0 * var_H)) * ((dig_H2) / 65536.0 * (1.0 + (dig_H6) / 67108864.0 * var_H * (1.0 + (dig_H3) / 67108864.0 * var_H)))
		var_H = var_H * (1.0 - (dig_H1) * var_H / 524288.0)
		
		
		if var_H > 100.0:
			var_H = 100.0
			
		elif var_H < 0.0:
			var_H = 0.0
			
		return var_H
