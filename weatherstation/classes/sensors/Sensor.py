import abc
import datetime
from config import messages


class Sensor(abc.ABC):
	def __init__(self, _logger):
		self.logger = _logger
	
	
	def set_measurement(self,
		_measurement):
		self.measurement = _measurement
	
	
	@abc.abstractmethod
	def setup_pins(self):
		pass
	
	
	@abc.abstractmethod
	def measure(self, _sensor, _measurement_data):
		txt = ', '.join(["%s: %s" % (x, getattr(_sensor, x)) for x in _measurement_data])

		msg = messages.LOG_MSG_MEASUREMENT_TAKEN % (datetime.datetime.now(),
													_sensor.__class__.__name__,
													txt)
		self.logger.log_message(msg)