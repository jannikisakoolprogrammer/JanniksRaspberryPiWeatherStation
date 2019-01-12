import sqlalchemy

from classes.db import Measurement


class THPMeasurement(Measurement.Measurement):
	"""ORM class for the thp measurements.
	
	"""
	__tablename__ = "THPMeasurement"
	
	drops = sqlalchemy.Column(sqlalchemy.Integer)
	
	
	def __init__(self, _logger):	
		super(THPMeasurement, self).__init__(_logger)