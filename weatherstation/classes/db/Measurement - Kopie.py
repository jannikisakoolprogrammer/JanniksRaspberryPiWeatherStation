import datetime
import sqlalchemy
import sqlalchemy.ext
import sqlalchemy.ext.declarative
from sqlalchemy import event

from config import messages


sqlalchemy_base = sqlalchemy.ext.declarative.declarative_base()


class Measurement(sqlalchemy_base):
	"""Abstract class.
	
	"""
	__abstract__ = True
	
	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	measurement = sqlalchemy.Column(sqlalchemy.Float)
	timestamp = sqlalchemy.Column(sqlalchemy.DateTime)
	type = sqlalchemy.Column(sqlalchemy.Integer)
	unit = sqlalchemy.Column(sqlalchemy.Integer)
	
	logger = None
	
	
	def __init__(self, _logger):
		self.logger = _logger
		self.sensor = None
	
	
	def set_sensor(self, _sensor):
		self.sensor = _sensor
	
	
	def set_sensor_data(self):
		self.measurement = self.sensor.measurement
		self.timestamp = self.sensor.timestamp
		self.type = self.sensor.type
		self.unit = self.sensor.unit
	

	def receive_after_insert(mapper, connection, object):
	
		txt = ', '.join(["%s = %s" % ( c.name, getattr(object, c.name)) for c in object.__table__.c])
		
		msg = messages.LOG_MSG_RECORD_CREATED % (datetime.datetime.now(),
												 object.__table__.name,
												 txt)
		object.logger.log_message(msg)
	
	
	def receive_after_update(mapper, connection, object):
		txt = ', '.join(["%s = %s" % ( c.name, getattr(object, c.name)) for c in object.__table__.c])
		
		msg = messages.LOG_MSG_RECORD_UPDATED % (datetime.datetime.now(),
												 object.__table__.name,
												 txt)
		object.logger.log_message(msg)


# Eventlistener for logging.
sqlalchemy.event.listen(Measurement, 'after_insert', Measurement.receive_after_insert, propagate = True)
sqlalchemy.event.listen(Measurement, 'after_update', Measurement.receive_after_update, propagate = True)