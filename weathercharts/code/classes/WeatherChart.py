import sqlalchemy
import os
import time

import matplotlib
from matplotlib import pyplot
import numpy
matplotlib.use('Agg')

class WeatherChart(object):
	"""Represents a weather chart for a specific set of data.
	
	"""
	def __init__(self, _time, _measurements, _filename, _x_label, _y_label):
		"""Initialises an instance of this class.
		
		"""
		self.time = _time
		self.measurements = _measurements
		self.filename = _filename
		self.x_label = _x_label
		self.y_label = _y_label
		self.chart = None
		
	def generate(self):
		pyplot.plot(self.time, self.measurements)
		pyplot.xticks(numpy.arange(0, len(self.time), step=12), rotation="vertical")
		pyplot.subplots_adjust(top=0.99, bottom=0.25)
		pyplot.ylabel(self.y_label)
		pyplot.xlabel(self.x_label)
		pyplot.savefig(self.filename)
		pyplot.close('all')
