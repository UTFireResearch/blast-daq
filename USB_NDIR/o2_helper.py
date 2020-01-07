import board
import busio
import adafruit_ads1x15.ads1115 as ADS1
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn


# Data collection setup
RATE = 250
RATEB = 250
SAMPLES = 1000

# Create the I2C bus with a fast frequency
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)

# Create the ADC object using the I2C bus
ads1115 = ADS1.ADS1115(i2c, address=0x4a)

chanB3 = AnalogIn(ads1115, ADS1.P3)

# ADC Configuration
ads1115.mode = Mode.SINGLE
ads1115.data_rate = RATEB
ads1115.gain = 16

O2_Baseline = chanB3.voltage

def GetO2Voltage():
    vv =chanB3.voltage
    O2 = 20.9*vv/O2_Baseline
    return O2, vv
