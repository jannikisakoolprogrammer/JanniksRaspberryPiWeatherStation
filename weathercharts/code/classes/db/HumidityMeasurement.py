import sqlalchemy

from code.classes.db import Measurement


class HumidityMeasurement(Measurement.Measurement):
	"""ORM class for the humidity measurements.
	
	"""
	__tablename__ = "HumidityMeasurement"