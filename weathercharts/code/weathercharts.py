import sqlalchemy
import os
import time
import datetime

from code.classes.WeatherChart import WeatherChart
from code.config import settings

from code.classes.db.Measurement import Measurement, base
from code.classes.db.RainfallMeasurement import RainMeasurement
from code.classes.db.SoilMoistureMeasurement import SoilMeasurement
from code.classes.db.TemperatureMeasurement import TemperatureMeasurement
from code.classes.db.HumidityMeasurement import HumidityMeasurement
from code.classes.db.PressureMeasurement import PressureMeasurement


def main():
	running = True
	while running:
		run()
		time.sleep(settings.INTERVAL)

def run():
	# Connect to db etc. ...
	engine  = sqlalchemy.create_engine(settings.DBNAME)
	base.prepare(engine, reflect = True)
	
	# Create the session here.
	Session = sqlalchemy.orm.sessionmaker(bind = engine)
	session = Session()
	
	# Hourly temperature chart.
	create_chart(
		session,
		TemperatureMeasurement,
		settings.LAST_HOUR_MAX_SECONDS,
		"/home/pi/weatherstation/weathercharts/chart_last_hour_temperature.png",
		"Time",
		"°C")
	
	# Hourly humidity chart.
	create_chart(
		session,
		HumidityMeasurement,
		settings.LAST_HOUR_MAX_SECONDS,
		"/home/pi/weatherstation/weathercharts/chart_last_hour_humidity.png",
		"Time",
		"rH")
		
	# Hourly pressure chart.
	create_chart(
		session,
		PressureMeasurement,
		settings.LAST_HOUR_MAX_SECONDS,
		"/home/pi/weatherstation/weathercharts/chart_last_hour_pressure.png",
		"Time",
		"hPa")
		
	# Hourly rain chart.
	create_chart(
		session,
		RainMeasurement,
		settings.LAST_HOUR_MAX_SECONDS,
		"/home/pi/weatherstation/weathercharts/chart_last_hour_rain.png",
		"Time",
		"%")
		
	# Hourly soil chart.
	create_chart(
		session,
		SoilMeasurement,
		settings.LAST_HOUR_MAX_SECONDS,
		"/home/pi/weatherstation/weathercharts/chart_last_hour_soil.png",
		"Time",
		"%")
		
	session.close()
	engine.dispose()

def create_chart(
	_session,
	_orm_class,
	_offset_seconds,
	_filename,
	_y_label,
	_x_label):
	
	min_datetime = datetime.datetime.now() - datetime.timedelta(seconds = _offset_seconds)

	chart_data = [(str(datetime.datetime.time(i.timestamp).replace(microsecond=0)), i.measurement) for i in _session.query(_orm_class).filter(_orm_class.timestamp >= min_datetime).order_by(sqlalchemy.desc(_orm_class.id))]

	if len(chart_data) >= 2:
		timestamps = [t[0] for t in chart_data]
		timestamps.reverse()
		
		measurements = [m[1] for m in chart_data]
		measurements.reverse()
		
		wc = WeatherChart(timestamps, measurements, _filename, _y_label, _x_label)
		wc.generate()
