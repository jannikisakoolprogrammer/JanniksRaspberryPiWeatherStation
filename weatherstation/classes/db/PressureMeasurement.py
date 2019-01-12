import sqlalchemy

from classes.db import Measurement


class PressureMeasurement(Measurement.Measurement):
	"""ORM class for the air pressure measurements.
	
	"""
	__tablename__ = "PressureMeasurement"
	
	
	def __init__(self,
		_logger,
		_type,
		_unit):
		"""Initialises necessary properties.
		
		"""
		super(PressureMeasurement, self).__init__(
			_logger,
			_type,
			_unit)