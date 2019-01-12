import abc
import os


class Logger(object):
	def __init__(self,
		_filepath):
		self.filepath = _filepath
		
		self.setup_file()
		
	
	def setup_file(self):
		self.file_handle = open(
			self.filepath,
			"a")

	
	def log_message(self, _msg):
		self.file_handle.write(_msg + '\n')
		self.file_handle.flush()
		os.fsync(self.file_handle.fileno())