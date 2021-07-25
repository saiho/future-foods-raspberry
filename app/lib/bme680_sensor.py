import time
import bme680
from lib.measurement import Measurement

#
#  Temperature, humidity, pressure & gas sensor (BME680)
#

bme680_sensor: bme680.BME680


def init():
    global bme680_sensor

    print("Init BME680 sensor")
    try:
        bme680_sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    except IOError:
        bme680_sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

    bme680_sensor.set_humidity_oversample(bme680.OS_2X)
    bme680_sensor.set_pressure_oversample(bme680.OS_4X)
    bme680_sensor.set_temperature_oversample(bme680.OS_8X)
    bme680_sensor.set_filter(bme680.FILTER_SIZE_3)
    bme680_sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
    bme680_sensor.set_gas_heater_temperature(320)
    bme680_sensor.set_gas_heater_duration(150)
    bme680_sensor.select_gas_heater_profile(0)


def read() -> Measurement.BME680:
    global bme680_sensor

    print("BME680 wait for measurement")
    max_count: int = 20
    while (not bme680_sensor.get_sensor_data() or not bme680_sensor.data.heat_stable) and max_count > 0:
        max_count = max_count - 1
        time.sleep(1)

    if max_count > 0:
        data = Measurement.BME680()
        data.gas_resistance = bme680_sensor.data.gas_resistance
        data.temperature = bme680_sensor.data.temperature
        data.humidity = bme680_sensor.data.humidity
        data.pressure = bme680_sensor.data.pressure
        print(f"VOC = {data.gas_resistance}, temperature = {data.temperature}, humidity = {data.humidity}, pressure = {data.pressure}")
        return data
    else:
        print("Failed to read BME680 data, sensor not ready.")
        return None
