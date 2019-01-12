import sqlalchemy
import sqlalchemy.ext
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import os.path
from sqlalchemy import event

from classes.db import Measurement

import datetime


class SoilMeasurement(Measurement.Measurement):
	"""ORM class for the soil moisture measurements.
	
	An instance of this class represents one measurement of the humidity.
	
	"""
	__tablename__ = "SoilMeasurement"
	
	
	def __init__(self,
		_logger,
		_type,
		_unit):
		"""Initialises necessary properties.
		
		"""
		super(SoilMeasurement, self).__init__(
			_logger,
			_type,
			_unit)