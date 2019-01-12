import sqlalchemy

from classes.db import Measurement


class RainMeasurement(Measurement.Measurement):
	"""ORM class for the rainfall measurements.
	
	"""
	__tablename__ = "RainMeasurement"
	
	
	def __init__(self,
		_logger,
		_type,
		_unit):
		"""Initialises necessary properties.
		
		"""
		super(RainMeasurement, self).__init__(
			_logger,
			_type,
			_unit)