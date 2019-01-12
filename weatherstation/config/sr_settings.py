# Constants for the ADS1115
I2C_CHANNEL = 1
ADS1115_ADDRESS = 0x49 # Run i2cdetect -y 1 to detect the address.

# Output codes for measuring humidity of soil and also rainfall.
ADS1115_OUTPUT_CODE_MAX = 32767
ADS1115_OUTPUT_CODE_MIN_SOIL = 14018
ADS1115_OUTPUT_CODE_MIN_RAIN = 5393

# Register addresses
ADS1115_CONVERSION_REGISTER = 0b00000000
ADS1115_CONFIG_REGISTER = 0b00000001

# I don't have much time, so I will just define the configurations here.
# I will refinne everything later on.
ADS1115_CONFIG_REGISTER_WRITE_SOIL_BYTE_1 = 0b11000011 # MSB
ADS1115_CONFIG_REGISTER_WRITE_SOIL_BYTE_2 = 0b10000011
ADS1115_CONFIG_REGISTER_READ_SOIL_BYTE_1 = 0b01000011 # MSB - performing a conversion

ADS1115_CONFIG_REGISTER_WRITE_RAIN_BYTE_1 = 0b11010011 # MSB
ADS1115_CONFIG_REGISTER_WRITE_RAIN_BYTE_2 = 0b10000111
ADS1115_CONFIG_REGISTER_READ_RAIN_BYTE_1 = 0b01010011 # MSB - performing a conversion
