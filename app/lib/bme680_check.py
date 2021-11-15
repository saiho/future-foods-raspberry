#!/bin/python3

# Standalone tool to read values from the BME680 sensor, for testing purposes

import sys
import os
import time

# Set the parent dir as root for looking for packages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import bme680_sensor
from lib.user_config import user_config # load logging level

bme680_sensor.init()

while True:
    bme680_sensor.read()
    time.sleep(5)
