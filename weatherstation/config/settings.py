import RPi.GPIO as GPIO


# Defines the interval in seconds at which measurement occurs.
MEASUREMENT_INTERVAL = 300

# Settings for the soil moisture sensor and the related ORM class.
SOIL_MOISTURE_TYPE = "soil_moisture"
SOIL_MOISTURE_UNIT = "%"
SOIL_MOISTURE_GPIO_PIN = 7
SOIL_MOISTURE_GPIO_PIN_MODE = GPIO.IN

# Settings for the raindrop sensor and the related ORM class.
RAINDROPS_TYPE = "raindrops"
RAINDROPS_UNIT = "%"
RAINDROPS_GPIO_PIN = 8
RAINDROPS_GPIO_PIN_MODE = GPIO.IN

# Settings for the temperature, humidity and pressure ORM class.
TEMPERATURE_TYPE = "temperature"
TEMPERATURE_UNIT = "C"
HUMIDITY_TYPE = "humidity"
HUMIDITY_UNIT = "rH"
PRESSURE_TYPE = "pressure"
PRESSURE_UNIT = "hPa"

# Set the height of the location of where the weather station has been placed.
# Check online for how much you're above (or below) sea-level.
# Height needs to be given as a float, with the first part defining meters.
HEIGHT = 487.00

# Measurements text file.
CURRENT_MEASUREMENTS_FILE = "/home/pi/weatherstation/weatherstation/current_measurements.txt"
