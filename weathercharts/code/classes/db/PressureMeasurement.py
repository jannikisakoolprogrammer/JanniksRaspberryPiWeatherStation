import sqlalchemy

from code.classes.db import Measurement


class PressureMeasurement(Measurement.Measurement):
	"""ORM class for the air pressure measurements.
	
	"""
	__tablename__ = "PressureMeasurement"