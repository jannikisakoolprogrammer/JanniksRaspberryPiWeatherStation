import sqlalchemy	
import sqlalchemy.ext.automap

base = sqlalchemy.ext.automap.automap_base()


class Measurement(base):
	"""Abstract class.
	
	"""
	__abstract__ = True
	
	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	measurement = sqlalchemy.Column(sqlalchemy.Float)
	timestamp = sqlalchemy.Column(sqlalchemy.DateTime)
	type = sqlalchemy.Column(sqlalchemy.String)
	unit = sqlalchemy.Column(sqlalchemy.String)
	
	logger = None
	
	
	def __init__(self):
		"""Initialises necessary properties.
		
		"""
		pass