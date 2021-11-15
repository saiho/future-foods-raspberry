#!/bin/python3

import sys
import time
from logging import info, exception
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
import lib.relay_switch as relay_switch
import lib.database as database
import lib.common as common
from lib.user_config import user_config

if not user_config.monitoring_enabled:
    info("Sensor monitor service is disabled. Doing nothing.")
    time.sleep(timedelta(hours=5).total_seconds())
    sys.exit("Bored of doing nothing")

info("Starting sensor monitor service")
info(f"Version {common.version}")
info(f"Current Time = {datetime.now().astimezone()}")

# Init sensors
if user_config.capacitive_moisture_sensor_enabled:
    capacitive_moisture_sensor.init()
if user_config.si1145_sensor_enabled:
    si1145_sensor.init()
if user_config.bme680_sensor_enabled:
    bme680_sensor.init()
if user_config.scd30_sensor_enabled:
    scd30_sensor.init()
if user_config.as7341_sensor_enabled:
    as7341_sensor.init()
if user_config.raspberry_sensor_enabled:
    raspberry_sensor.init()
if user_config.camera_enabled:
    camera.init()
if user_config.relay_switch_enabled:
    relay_switch.init()

measurements: List[Measurement] = []

post_data_next: datetime = datetime.now() + common.post_data_interval

try:
    while True:

        measurement_next: datetime = datetime.now() + common.measurement_interval

        measurement: Measurement = Measurement(owner=user_config.owner, label=user_config.label)
        if user_config.capacitive_moisture_sensor_enabled:
            try:
                measurement.capacitive_moisture = capacitive_moisture_sensor.read()
            except Exception as e:
                measurement.add_error('capacitive_moisture')
                exception(e)
        if user_config.si1145_sensor_enabled:
            try:
                measurement.si1145 = si1145_sensor.read()
            except Exception as e:
                measurement.add_error('si1145_sensor')
                exception(e)
        if user_config.bme680_sensor_enabled:
            try:
                measurement.bme680 = bme680_sensor.read()
            except Exception as e:
                measurement.add_error('bme680_sensor')
                exception(e)
        if user_config.scd30_sensor_enabled:
            try:
                measurement.scd30 = scd30_sensor.read(measurement.bme680.temperature if measurement.bme680 else None)
            except Exception as e:
                measurement.add_error('scd30_sensor')
                exception(e)
        if user_config.as7341_sensor_enabled:
            try:
                measurement.as7341 = as7341_sensor.read()
            except Exception as e:
                measurement.add_error('as7341_sensor')
                exception(e)
        if user_config.raspberry_sensor_enabled:
            try:
                measurement.raspberry = raspberry_sensor.read()
            except Exception as e:
                measurement.add_error('raspberry_sensor')
                exception(e)
        if user_config.camera_enabled:
            try:
                measurement.pictures = camera.take_pictures_if_scheduled()
            except Exception as e:
                measurement.add_error('camera')
                exception(e)
        if user_config.relay_switch_enabled:
            try:
                measurement.relays_on = relay_switch.check()
            except Exception as e:
                measurement.add_error('relay_switch')
                exception(e)
        measurements.append(measurement)

        if datetime.now() > post_data_next:
            post_data_next = datetime.now() + common.post_data_interval
            combined_measurement: Measurement = Measurement.combine(measurements)
            database.insert_data(combined_measurement)
            measurements = []

        # Wait for next measurement
        info(f"Wait for next measurement at {measurement_next.astimezone()}")
        time.sleep((measurement_next - datetime.now()).total_seconds())

finally:
    scd30_sensor.close()
