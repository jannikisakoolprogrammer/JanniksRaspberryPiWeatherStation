import sqlalchemy

from code.classes.db import Measurement


class SoilMeasurement(Measurement.Measurement):
	"""ORM class for the soil moisture measurements.
	
	An instance of this class represents one measurement of the humidity.
	
	"""
	__tablename__ = "SoilMeasurement"