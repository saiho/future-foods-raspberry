from typing import Dict
from logging import info
from grove.adc import ADC
from lib.measurement import Measurement
from lib.user_config import user_config

#
# Grove capacitive moisture sensor
#

adc: ADC


def init():
    global adc
    info("Init ADC channel")
    adc = ADC()
    read()  # Test read


def read() -> Dict[str, Measurement.CapacitiveMoisture]:
    global adc
    data: Dict[str, Measurement.CapacitiveMoisture] = {}
    for key, sensor in user_config.capacitive_moisture_sensors.items():
        data[key] = Measurement.CapacitiveMoisture()
        data[key].value = adc.read_voltage(sensor.port)
        data[key].port = sensor.port
    info("Moisture values: %s", {key: sensor.value for key, sensor in data.items()})
    return data
