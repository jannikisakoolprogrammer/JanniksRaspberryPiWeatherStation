import sqlalchemy

from classes.db import Measurement


class HumidityMeasurement(Measurement.Measurement):
	"""ORM class for the humidity measurements.
	
	"""
	__tablename__ = "HumidityMeasurement"
	
	
	def __init__(self,
		_logger,
		_type,
		_unit):
		"""Initialises necessary properties.
		
		"""
		super(HumidityMeasurement, self).__init__(
			_logger,
			_type,
			_unit)