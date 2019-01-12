import sqlalchemy

from classes.db import Measurement


class TemperatureMeasurement(Measurement.Measurement):
	"""ORM class for temperature measurements.
	
	"""
	__tablename__ = "TemperatureMeasurement"
	
	
	def __init__(self,
		_logger,
		_type,
		_unit):
		"""Initialises necessary properties.
		
		"""
		super(TemperatureMeasurement, self).__init__(
			_logger,
			_type,
			_unit)