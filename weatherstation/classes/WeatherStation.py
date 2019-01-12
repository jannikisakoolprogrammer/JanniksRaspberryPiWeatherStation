import sqlalchemy
import os
import time

import RPi.GPIO as GPIO

from classes.db.Measurement import sqlalchemy_base
from classes.db.SoilMoistureMeasurement import SoilMeasurement
from classes.db.RainfallMeasurement import RainMeasurement
from classes.db.TemperatureMeasurement import TemperatureMeasurement
from classes.db.HumidityMeasurement import HumidityMeasurement
from classes.db.PressureMeasurement import PressureMeasurement

from classes.other.Logger import Logger

from classes.sensors.THPSensor import THPSensor
from classes.sensors.SRSensor import SRSensor

from config import logging
from config import settings

GPIO.setmode(GPIO.BCM)


class WeatherStation(object):
	
	# db engine
	DB_Engine = None
	
	# Logger
	Logger = None
	
	# Session
	Session = None
	
	
	def __init__(self):
		"""Initialises the class.
		
		"""
		# Here we set the three class properties defined above.
		self.create_db_engine()
		self.create_db_session()
		self.create_logger()
		
		# Create the database if it does not yet exist.
		sqlalchemy_base.metadata.create_all(WeatherStation.DB_Engine)
		
		# Create sensor driver instance to measure temperature, humidity
		# and air pressure.
		self.thp_sensor = THPSensor(WeatherStation.Logger)

		# Create sensor driver instance to measure soil and rain.
		self.sr_sensor = SRSensor(WeatherStation.Logger)
	
	
	def create_measurement_orm_instances(self):
		"""Creates measurement instances.  Those can be passed to the
		sensors to read and insert new measurements.
		
		"""
		self.soil_moisture_measurement = SoilMeasurement(
			WeatherStation.Logger,
			settings.SOIL_MOISTURE_TYPE,
			settings.SOIL_MOISTURE_UNIT)
			
		self.rainfall_measurement = RainMeasurement(
			WeatherStation.Logger,
			settings.RAINDROPS_TYPE,
			settings.RAINDROPS_UNIT)
			
		self.temperature_measurement = TemperatureMeasurement(
			WeatherStation.Logger,
			settings.TEMPERATURE_TYPE,
			settings.TEMPERATURE_UNIT)
			
		self.humidity_measurement = HumidityMeasurement(
			WeatherStation.Logger,
			settings.HUMIDITY_TYPE,
			settings.HUMIDITY_UNIT)
		
		self.pressure_measurement = PressureMeasurement(
			WeatherStation.Logger,
			settings.PRESSURE_TYPE,
			settings.PRESSURE_UNIT)
			
	
	
	def create_db_engine(self):
		"""Creates database.
		If it already exists, it's not overwritten.
		
		"""
		WeatherStation.DB_Engine = sqlalchemy.create_engine("sqlite:////home/pi/weatherstation/weatherstation/weather.db")
	
	
	def create_db_session(self):
		"""Creates a new Session object from which a new session can be instantinated.
		Remarks:  Globally available, so use with caution.
		
		"""
		WeatherStation.Session = sqlalchemy.orm.sessionmaker(bind = WeatherStation.DB_Engine)
		
	
	def create_logger(self):
		"""Creates an instance of the logger class and assigns it to a class property.
		
		"""
		WeatherStation.Logger = Logger(logging.FILEPATH)
		
		
	def assign_measurements_to_sensors(self):
		"""Assigns ORM measurement instances to their specific sensor instances so
		measurement data can be written to them.
		
		"""
		self.thp_sensor.set_temperature_measurement(self.temperature_measurement)
		self.thp_sensor.set_humidity_measurement(self.humidity_measurement)
		self.thp_sensor.set_pressure_measurement(self.pressure_measurement)
		self.sr_sensor.set_soil_measurement(self.soil_moisture_measurement)
		self.sr_sensor.set_rain_measurement(self.rainfall_measurement)
		
	
	def run_measurement(self):
		"""Performs measurement by calling the "measure()" functions of all sensors
		available, and writes data from the sensor to their respective ORM instances
		which have been assigned in the previous step (using "assign_measurements_to_sensors())
		
		"""
		self.thp_sensor.measure()
		self.sr_sensor.measure()
	
	
	def write_measurements_to_db(self):
		"""Writes data from each of the ORM instances into the database.
		Starts a new db session first.
		In the end, the db session is commited, flushed and closed afterwards.
		
		"""
		self.db_session = WeatherStation.Session()
		
		self.db_session.add(self.sr_sensor.soil_measurement)
		self.db_session.add(self.sr_sensor.rain_measurement)
		self.db_session.add(self.thp_sensor.temperature_measurement)
		self.db_session.add(self.thp_sensor.humidity_measurement)
		self.db_session.add(self.thp_sensor.pressure_measurement)
		
		self.db_session.commit()
		self.db_session.flush()
		self.db_session.close()


	def write_measurements_to_file(self):
		"""Writes measurements to a file.
		Each measurement is separated by a comma.
		
		"""
		with open(settings.CURRENT_MEASUREMENTS_FILE, "w") as file_handle:
			file_handle.write("%s,%s,%s,%s,%s" %
				(self.sr_sensor.soil_measurement.measurement,
				self.sr_sensor.rain_measurement.measurement,
				self.thp_sensor.temperature_measurement.measurement,
				self.thp_sensor.humidity_measurement.measurement,
				self.thp_sensor.pressure_measurement.measurement))
			
		
	
	def run(self):
		"""Runs the basic logic in a while loop until program execution is aborted.
		
		"""
		running = True
		
		while running:
		
			# Let's create new measurement ORM instance objects for this cycle.
			self.create_measurement_orm_instances()
			
			# And assign those to the sensor instances.
			self.assign_measurements_to_sensors()
			
			# Measure here.
			self.run_measurement()
			
			# Write current measurements to file.
			self.write_measurements_to_file()
		
			# Write measurements to the database.
			self.write_measurements_to_db()
			
			# Measurements need only be taken at certain intervals, thus we sleep here for a while.
			time.sleep(settings.MEASUREMENT_INTERVAL)

