from grove.adc import ADC
from lib.measurement import Measurement

#
# Grove capacitive moisture sensor
#

adc: ADC


def init():
    global adc
    print("Init ADC channel")
    adc = ADC()
    read()  # Test read


def read() -> Measurement.CapacitiveMoisture:
    global adc
    data = Measurement.CapacitiveMoisture()
    data.values = [
        adc.read_voltage(0),
        adc.read_voltage(1),
        adc.read_voltage(2),
        adc.read_voltage(3),
        adc.read_voltage(4),
        adc.read_voltage(5)]
    print("Moisture values: ", data.values)
    return data
