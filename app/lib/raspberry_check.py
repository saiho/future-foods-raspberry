#!/bin/python3

# Standalone tool to read the temperature of the CPU, for testing purposes

import sys
import os
import time

# Set the parent dir as root for looking for packages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import raspberry_sensor
from lib.user_config import user_config # load logging level

raspberry_sensor.init()

while True:
    raspberry_sensor.read()
    time.sleep(5)
