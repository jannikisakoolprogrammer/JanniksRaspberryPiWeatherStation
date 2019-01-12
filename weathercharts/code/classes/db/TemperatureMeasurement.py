import sqlalchemy

from code.classes.db import Measurement


class TemperatureMeasurement(Measurement.Measurement):
	"""ORM class for temperature measurements.
	
	"""
	__tablename__ = "TemperatureMeasurement"