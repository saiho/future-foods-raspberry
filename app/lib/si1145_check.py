#!/bin/python3

# Standalone tool to read values from SI1145 sensor, for testing purposes

import sys
import os
import time

# Set the parent dir as root for looking for packages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import si1145_sensor
from lib.user_config import user_config # load logging level

si1145_sensor.init()

while True:
    si1145_sensor.read()
    time.sleep(5)
