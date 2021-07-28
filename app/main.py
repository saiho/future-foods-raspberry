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
import lib.camera as camera
import lib.database as database
import lib.common as common
import lib.user_config as user_config

user_config.load("config.yml")

if user_config.disable_monitoring:
    print("Sensor monitor service is disabled. Doing nothing.")
    time.sleep(timedelta(hours=5).total_seconds())
    sys.exit("Bored of doing nothing")

print("Starting sensor monitor service")
print("Current Time =", datetime.now().astimezone())

# Init sensors
if not user_config.disable_capacitive_moisture_sensor:
    capacitive_moisture_sensor.init()
    capacitive_moisture_sensor.read()  # try reading, ignore result
if not user_config.disable_si1145_sensor:
    si1145_sensor.init()
    si1145_sensor.read()  # try reading, ignore result
if not user_config.disable_bme680_sensor:
    bme680_sensor.init()
    bme680_sensor.read()  # try reading, ignore result
if not user_config.disable_scd30_sensor:
    scd30_sensor.init()
    scd30_sensor.read()  # try reading, ignore result
if not user_config.disable_as7341_sensor:
    as7341_sensor.init()
    as7341_sensor.read()  # try reading, ignore result
if not user_config.disable_raspberry_sensor:
    raspberry_sensor.init()
    raspberry_sensor.read()  # try reading, ignore result

measurements: List[Measurement] = []

post_data_next: datetime = datetime.now() + common.post_data_interval

picture_take_next: datetime = datetime.combine(datetime.now(), user_config.picture_take_time)
if picture_take_next < datetime.now():
    picture_take_next = picture_take_next + common.picture_take_interval

try:
    while True:

        measurement_next: datetime = datetime.now() + common.measurement_interval

        measurement: Measurement = Measurement(owner=user_config.owner, label=user_config.label)
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

        picture_info: Measurement.Picture = None
        picture_data: bytes = None
        if not user_config.disable_picture_take and datetime.now() > picture_take_next:
            picture_take_next = picture_take_next + common.picture_take_interval
            picture_info, picture_data = camera.take_picture()

        if datetime.now() > post_data_next:
            post_data_next = datetime.now() + common.post_data_interval
            combined_measurement: Measurement = Measurement.combine(measurements)
            if picture_data:
                combined_measurement.picture = picture_info
            database.insert_data(combined_measurement, picture_data)
            measurements = []

        # Wait for next measurement
        print("Wait for next measurement at", measurement_next.astimezone())
        time.sleep((measurement_next - datetime.now()).total_seconds())

finally:
    scd30_sensor.close()
