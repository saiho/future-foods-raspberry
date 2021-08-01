#!/bin/python3

# Standalone tool to take pictures from camera, for testing purposes

import sys
import os
import time

# Set the parent dir as root for looking for packages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import camera
from lib import user_config

user_config.load("../config.yml")

while True:
    picture_info, picture_data = camera.take_picture()
    with open("/tmp/picture." + picture_info.format, "wb") as picture_file:
        picture_file.write(picture_data)
        print("Picture saved in /tmp/picture." + picture_info.format)
    time.sleep(5)
