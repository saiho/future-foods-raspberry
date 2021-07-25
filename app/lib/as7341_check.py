#!/bin/python3

# Standalone tool to read values from the AS7341 sensor, for testing purposes

import sys
import os
import time

# Set the parent dir as root for looking for packages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import as7341_sensor

as7341_sensor.init()

while True:
    as7341_sensor.read()
    time.sleep(5)
