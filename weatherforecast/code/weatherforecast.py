import sqlalchemy
import os
import time
import datetime

from code.config import settings

from code.classes.db.Measurement import Measurement, base
from code.classes.db.PressureMeasurement import PressureMeasurement


def main():
	running = True
	while running:
		run()
		time.sleep(settings.FORECAST_INTERVAL_CALCULATE)

def run():
	# Connect to db etc. ...
	engine  = sqlalchemy.create_engine(settings.DBNAME)
	base.prepare(engine, reflect = True)
	
	# Create the session here.
	Session = sqlalchemy.orm.sessionmaker(bind = engine)
	session = Session()
	
	# Calculate forecast
	msg = calculate_forecast(
		session,
		PressureMeasurement,
		settings.FORECAST_PAST_SECONDS)
		
	# Write msg to file and copy that file to the www location.
	with open(settings.FILENAME_FORECAST, "w") as f:
		f.write(msg)
		
	session.close()
	engine.dispose()
	

def calculate_forecast(
	_session,
	_orm_class,
	_offset_seconds):
	
	# Calculate with the data from the last 24 hours.
	min_datetime = datetime.datetime.now() - datetime.timedelta(seconds = _offset_seconds)

	# Get the current pressure from the table.
	pressure_current = _session.query(_orm_class.measurement).order_by(sqlalchemy.desc(_orm_class.id)).first()[0]

	# Get the average pressure from the 24 hours from the database.
	pressure_avg_past = _session.query(sqlalchemy.func.avg(_orm_class.measurement)).filter(
		_orm_class.timestamp >= min_datetime).first()[0]

	# Now calculate the difference between these two measurements.
	pressure_diff = abs(pressure_avg_past - pressure_current)

	# Now decide whether to add or subtract the calculated pressure from the current pressure or add it.
	# If it is the same, the weather will stay the same :D
	if pressure_current > pressure_avg_past:
		pressure_future = pressure_current + pressure_diff # Weather will be better
		msg = get_weather_msg_better(
			pressure_future,
			pressure_current)
	elif pressure_current < pressure_avg_past:
		pressure_future = pressure_current - pressure_diff # Weather will be worse
		msg = get_weather_msg_worse(
			pressure_future,
			pressure_current)
	else:
		pressure_future = pressure_current
		msg = get_weather_staying_same(pressure_future)

	return msg
		
		
def get_weather_msg_worse(
	_pressure,
	_current_pressure):
	
	if _pressure <= settings.PRESS_RANGE_WEATHER_BAD_MAX:
		if _current_pressure <= settings.PRESS_RANGE_WEATHER_BAD_MAX:
			return settings.WEATHER_STAYING_SAME_BAD
		else:
			return settings.WEATHER_GETTING_WORSE_BAD
	elif _pressure <= settings.PRESS_RANGE_WEATHER_AVERAGE_MAX:
		if _current_pressure <= settings.PRESS_RANGE_WEATHER_AVERAGE_MAX:
			return settings.WEATHER_STAYING_SAME_AVERAGE
		else:
			return settings.WEATHER_GETTING_WORSE_AVERAGE
	elif _pressure <= settings.PRESS_RANGE_WEATHER_GOOD_MAX:
		if _current_pressure <= settings.PRESS_RANGE_WEATHER_GOOD_MAX:
			return settings.WEATHER_STAYING_SAME_GOOD
		else:
			return settings.WEATHER_GETTING_WORSE_GOOD
	else:
		return settings.WEATHER_STAYING_SAME_VERY_GOOD

		
def get_weather_msg_better(
	_pressure,
	_current_pressure):
	
	if _pressure > settings.PRESS_RANGE_WEATHER_GOOD_MAX:
		if _current_pressure > settings.PRESS_RANGE_WEATHER_GOOD_MAX:
			return settings.WEATHER_STAYING_SAME_VERY_GOOD
		else:
			return settings.WEATHER_GETTING_BETTER_VERY_GOOD
	elif _pressure > settings.PRESS_RANGE_WEATHER_AVERAGE_MAX:
		if _current_pressure > settings.PRESS_RANGE_WEATHER_AVERAGE_MAX:
			return settings.WEATHER_STAYING_SAME_GOOD
		else:
			return settings.WEATHER_GETTING_BETTER_GOOD
	elif _pressure > settings.PRESS_RANGE_WEATHER_BAD_MAX:
		if _current_pressure > settings.PRESS_RANGE_WEATHER_BAD_MAX:
			return settings.WEATHER_STAYING_SAME_AVERAGE
		else:
			return settings.WEATHER_GETTING_BETTER_AVERAGE
	else:
		return settings.WEATHER_STAYING_SAME_BAD

		
def get_weather_staying_same(
	_pressure):
	
	if _pressure > settings.PRESS_RANGE_WEATHER_GOOD_MAX:
		return settings.WEATHER_STAYING_SAME_VERY_GOOD
	elif _pressure > settings.PRESS_RANGE_WEATHER_AVERAGE_MAX:
		return settings.WEATHER_STAYING_SAME_GOOD
	elif _pressure > settings.PRESS_RANGE_WEATHER_BAD_MAX:
		return settings.WEATHER_STAYING_SAME_AVERAGE
	else:
		return settings.WEATHER_STAYING_SAME_BAD
		
def write_and_copy_forecast(
	_msg):
	pass
