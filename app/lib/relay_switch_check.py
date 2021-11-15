#!/bin/python3

# Standalone tool to switch relays, for testing purposes

import sys
import os
import time

# Set the parent dir as root for looking for packages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import relay_switch
from lib.user_config import user_config # load logging level

relay_switch.init()

while True:
    relay_switch.check()
    time.sleep(5)
