import sqlalchemy

from code.classes.db import Measurement


class RainMeasurement(Measurement.Measurement):
	"""ORM class for the rainfall measurements.
	
	"""
	__tablename__ = "RainMeasurement"