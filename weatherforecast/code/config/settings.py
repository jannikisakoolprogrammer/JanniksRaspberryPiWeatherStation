DBNAME = "sqlite:////home/pi/weatherstation/weatherstation/weather.db"
# DBNAME = "sqlite:///weather.db"
# Settings for the forecast
FORECAST_PAST_SECONDS = 3600 * 24 # one day.
FORECAST_INTERVAL_CALCULATE = 60 * 10 # 10 minutes.

WEATHER_GETTING_WORSE_BAD = "The weather is getting much worse.  It will be raining/snowing."
WEATHER_GETTING_WORSE_AVERAGE = "The weather is getting worse.  It will mostly be cloudy."
WEATHER_GETTING_WORSE_GOOD = "The weather is getting slightly worse, but it will still be sunny mostly."

WEATHER_GETTING_BETTER_AVERAGE = "The weather is getting slightly better.  It will mostly be cloudy."
WEATHER_GETTING_BETTER_GOOD = "The weather is getting better, the sun will most likely come out."
WEATHER_GETTING_BETTER_VERY_GOOD = "The weather is getting better, there will barely be a cloud in the sky."

WEATHER_STAYING_SAME_BAD = "The weather will continue to stay bad and it will continue to rain/snow."
WEATHER_STAYING_SAME_AVERAGE = "It will continue to be cloudy, but rain/snow is not in sight."
WEATHER_STAYING_SAME_GOOD = "It will continue to be good weather, only a few clouds might be on the sky."
WEATHER_STAYING_SAME_VERY_GOOD = "The weather will continue to be exceptionally good, blue sky ahead."

PRESS_RANGE_WEATHER_BAD_MAX = 1010
PRESS_RANGE_WEATHER_AVERAGE_MAX = 1020
PRESS_RANGE_WEATHER_GOOD_MAX = 1030

FILENAME_FORECAST = "/home/pi/weatherstation/weatherforecast/weatherforecast.txt"
