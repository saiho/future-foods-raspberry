#!/bin/python3

# Standalone tool to read values from SCD30 sensor, for testing purposes

import sys
import os
import time

# Set the parent dir as root for looking for packages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import scd30_sensor

scd30_sensor.init()

try:
    while True:
        scd30_sensor.read()
        time.sleep(5)
finally:
    scd30_sensor.close()
