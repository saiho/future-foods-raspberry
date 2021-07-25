#!/bin/python3

# Standalone tool to read values from the moisture sensors, for testing purposes

import sys
import os
import time

# Set the parent dir as root for looking for packages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import capacitive_moisture_sensor

capacitive_moisture_sensor.init()

while True:
    capacitive_moisture_sensor.read()
    time.sleep(5)
