#!/bin/python3

import sys
import time
from datetime import datetime, timedelta
from typing import List
from lib.measurement import Measurement
import lib.raspberry_sensor as raspberry_sensor
import lib.capacitive_moisture_sensor as capacitive_moisture_sensor
import lib.si1145_sensor as si1145_sensor
import lib.bme680_sensor as bme680_sensor
import lib.scd30_sensor as scd30_sensor
import lib.as7341_sensor as as7341_sensor
import lib.database as database
import lib.common as common
import lib.user_config as user_config

user_config.load("config.yml")

if user_config.disable_monitoring:
    print("Sensor monitor service is disabled. Doing nothing.")
    time.sleep(timedelta(hours=5).total_seconds())
    sys.exit("Bored of doing nothing")

print("Starting sensor monitor service")
print("Current Time =", datetime.now())

# Init sensors
if not user_config.disable_capacitive_moisture_sensor:
    capacitive_moisture_sensor.init()
    capacitive_moisture_sensor.read() # try reading, ignore result
if not user_config.disable_si1145_sensor:
    si1145_sensor.init()
    si1145_sensor.read() # try reading, ignore result
if not user_config.disable_bme680_sensor:
    bme680_sensor.init()
    bme680_sensor.read() # try reading, ignore result
if not user_config.disable_scd30_sensor:
    scd30_sensor.init()
    scd30_sensor.read() # try reading, ignore result
if not user_config.disable_as7341_sensor:
    as7341_sensor.init()
    as7341_sensor.read() # try reading, ignore result
if not user_config.disable_raspberry_sensor:
    raspberry_sensor.init()
    raspberry_sensor.read() # try reading, ignore result

measurements: List[Measurement] = []
post_data_next: datetime = datetime.now() + common.post_data_interval

try:
    while True:

        measurement = Measurement(owner=user_config.owner, label=user_config.label)
        if not user_config.disable_capacitive_moisture_sensor:
            measurement.capacitive_moisture = capacitive_moisture_sensor.read()
        if not user_config.disable_si1145_sensor:
            measurement.si1145 = si1145_sensor.read()
        if not user_config.disable_bme680_sensor:
            measurement.bme680 = bme680_sensor.read()
        if not user_config.disable_scd30_sensor:
            measurement.scd30 = scd30_sensor.read(measurement.bme680.temperature if measurement.bme680 else None)
        if not user_config.disable_as7341_sensor:
            measurement.as7341 = as7341_sensor.read()
        if not user_config.disable_raspberry_sensor:
            measurement.raspberry = raspberry_sensor.read()
        measurements.append(measurement)

        if datetime.now() > post_data_next:
            post_data_next = datetime.now() + common.post_data_interval
            database.insert_data(Measurement.median(measurements))
            measurements = []

        # Wait for next measurement
        print("Wait for next measurement at", (datetime.now() + common.measurement_interval))
        time.sleep(common.measurement_interval.total_seconds())

finally:
    scd30_sensor.close()
