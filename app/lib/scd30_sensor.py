from datetime import datetime
import time
import scd30_i2c
from lib import common
from lib.measurement import Measurement

#
# CO₂, temperature & humidity sensor (SCD30)
#

scd30: scd30_i2c.SCD30
firmware_version: int
temperature_offset_correction_next: datetime


def init():
    global scd30
    global firmware_version

    print("Init SCD30 sensor")
    scd30 = scd30_i2c.SCD30()
    scd30.stop_periodic_measurement()  # just in case was left active in a previous run
    firmware_version = scd30.get_firmware_version()
    if firmware_version is None:
        print("Problem communicating with SCD30 sensor, trying to reset")
        scd30.soft_reset()
        time.sleep(5)
        firmware_version = scd30.get_firmware_version()
        if firmware_version is None:
            raise Exception("Not able to communcate with SCD30 sensor")

    scd30.set_measurement_interval(int(common.measurement_interval.total_seconds()))
    scd30.set_temperature_offset(0)
    scd30.set_auto_self_calibration(True)
    scd30.start_periodic_measurement()
    print(f"SCD30 Started measuring every {scd30.get_measurement_interval()} seconds")

    global temperature_offset_correction_next
    temperature_offset_correction_next = datetime.now() + common.scd30_temperature_offset_correction_interval

    read()  # Test read


def close():
    global scd30

    if scd30:
        print("SCD30 Stop measuring")
        scd30.stop_periodic_measurement()


def read(real_temperature: float = None) -> Measurement.SCD30:
    global scd30
    global temperature_offset_correction_next

    data = None

    print("SCD30 wait for measurement")
    max_count: int = 10
    while max_count > 0:
        max_count = max_count - 1
        time.sleep(2)
        if scd30.get_data_ready():
            m = scd30.read_measurement()
            if m and m[0] != 0:
                data = Measurement.SCD30()
                data.co2_ppm = m[0]
                data.temperature = m[1]
                data.humidity = m[2]
                data.firmware_version = firmware_version

                # Reajust temperature offset
                if real_temperature and datetime.now() > temperature_offset_correction_next:
                    temperature_offset_correction_next = datetime.now() + common.scd30_temperature_offset_correction_interval
                    data.temperature_offset = data.temperature + scd30.get_temperature_offset() - real_temperature
                    print("Recalculated offset temperature ", data.temperature_offset)
                    if data.temperature_offset < 0:
                        data.temperature_offset = 0
                    if data.temperature_offset > common.scd30_temperature_offset_max:
                        data.temperature_offset = common.scd30_temperature_offset_max
                    scd30.set_temperature_offset(data.temperature_offset)
                else:
                    data.temperature_offset = scd30.get_temperature_offset()

                print(f"CO2 = {data.co2_ppm}, temperature = {data.temperature}, temperature_offset = {data.temperature_offset}, humidity = {data.humidity}")

    if not data:
        print("Failed to read SCD30 data, sensor not ready")
    return data
