#!/bin/python3

# Standalone tool to switch lights, for testing purposes

import sys
import os
import time

# Set the parent dir as root for looking for packages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import ligths_switch
from lib import user_config

user_config.load("../config.yml")

ligths_switch.init()

while True:
    ligths_switch.check()
    time.sleep(5)
