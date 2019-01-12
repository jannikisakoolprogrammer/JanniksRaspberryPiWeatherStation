# Constants for the BME280 sensor.

# Register addresses on the BME280 sensor that store compensation values for
# temperature, pressure and humidity.

# Register addresses containing compensation values to correctly calculate temperature:
DIG_T1_1 = 0x88
DIG_T1_2 = 0x89

DIG_T2_1 = 0x8A
DIG_T2_2 = 0x8B

DIG_T3_1 = 0x8C
DIG_T3_2 = 0x8D

# Register addresses containing compensation values to correctly calculate pressure:
DIG_P1_1 = 0x8E
DIG_P2_2 = 0x8F

DIG_P2_1 = 0x90
DIG_P2_2 = 0x91

DIG_P3_1 = 0x92
DIG_P3_2 = 0x93

DIG_P4_1 = 0x94
DIG_P4_2 = 0x95

DIG_P5_1 = 0x96
DIG_P5_2 = 0x97

DIG_P6_1 = 0x98
DIG_P6_2 = 0x99

DIG_P7_1 = 0x9A
DIG_P7_2 = 0x9B

DIG_P8_1 = 0x9C
DIG_P8_2 = 0x9D

DIG_P9_1 = 0x9E
DIG_P9_2 = 0x9F

# Register addresses containing compensation values to correctly calculate humidity.
DIG_H1_1 = 0xA1

DIG_H2_1 = 0xE1
DIG_H2_2 = 0xE2

DIG_H3_1 = 0xE3

DIG_H4_1 = 0xE4
DIG_H4_2 = 0xE5

DIG_H5_1 = 0xE5
DIG_H5_2 = 0xE6

DIG_H6_1 = 0xE7


# Memory map
HUM_LSB = 0xFE
HUM_MSB = 0xFD

TEMP_XLSB = 0xFC
TEMP_LSB = 0xFB
TEMP_MSB = 0xFA

PRESS_XLSB = 0xF9
PRESS_LSB = 0xF8
PRESS_MSB = 0xF7

CONFIG = 0xF5

CTRL_MEAS = 0xF4

STATUS = 0xF3

CTRL_HUM = 0xF2

# Not required: CALIB26 .. CALIB41 (defined above)

RESET = 0xE0

ID = 0xD0

# Not required: CALIB00 .. CALIB26 (defined above)


# Humidity oversampling
HUMIDITY_OVERSAMPLING_SKIP = 0b00000000
HUMIDITY_OVERSAMPLING_X1 = 0b00000001
HUMIDITY_OVERSAMPLING_X2 = 0b00000010
HUMIDITY_OVERSAMPLING_X4 = 0b00000011
HUMIDITY_OVERSAMPLING_X8 = 0b00000100
HUMIDITY_OVERSAMPLING_X16 = 0b00000101

# Register 0xF3 -> Status -> Read only
# These values are for comparison.
STATUS_MEASURING = 0b00001000
STATUS_IM_UPDATE = 0b00000001

# Register 0xF4 -> CTRL_MEAS -> Write
CTRL_MEAS_OSRS_P_SKIP = 0b00000000
CTRL_MEAS_OSRS_P_X1 = 0b00100000 # Oversampling X1
CTRL_MEAS_OSRS_P_X2 = 0b01000000 # x2
CTRL_MEAS_OSRS_P_X4 = 0b01100000 # x4
CTRL_MEAS_OSRS_P_X8 = 0b10000000 # x8
CTRL_MEAS_OSRS_P_X16 = 0b10100000 # x16

CTRL_MEAS_OSRS_T_SKIP = 0b00000000 # no oversampling
CTRL_MEAS_OSRS_T_X1 = 0b00000100 # x1
CTRL_MEAS_OSRS_T_X2 = 0b00001000 # x2
CTRL_MEAS_OSRS_T_X4 = 0b00001100 # x4
CTRL_MEAS_OSRS_T_X8 = 0b00010000 # X8
CTRL_MEAS_OSRS_T_X16 = 0b00010100 # x16

CTRL_MEAS_MODE_SLEEP = 0b00000000 # Sleep mode
CTRL_MEAS_MODE_FORCED = 0b00000010 # Forced mode
CTRL_MEAS_MODE_NORMAL = 0b00000011 # Normal mode


# Register 0xF5 -> Config -> Write
T_SB_05 = 0b00000000 # Inactive duration in normal mode -> 0.5ms
T_SB_625 = 0b00100000 # 62.5ms
T_SB_125 = 0b01000000 # 125ms
T_SB_250 = 0b01100000 # 250ms
T_SB_500 = 0b10000000 # 500ms
T_SB_1000 = 0b10100000 # 1000ms

# Filter settings.
FILTER = 0b00000000 # Filter off
FILTER_2 = 0b00000100 # 2
FILTER_4 = 0b00001000 # 4
FILTER_8 = 0b00001100 # 8
FILTER_16 = 0b00010000 # 16

I2C_CHANNEL = 1
BME280_ID = 0x76