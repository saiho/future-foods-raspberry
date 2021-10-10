#!/bin/python3

# Standalone tool to take pictures from camera, for testing purposes

import sys
import os
import time

# Set the parent dir as root for looking for packages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import camera
from lib.user_config import user_config
from lib.measurement import Measurement

if len(user_config.camera_devices) == 0:
    sys.exit("No camera device configured")

while True:
    picture: Measurement.Picture = camera.take_picture(list(user_config.camera_devices.values())[0])
    with open("/tmp/picture." + picture.format, "wb") as picture_file:
        picture_file.write(picture.data)
        print("Picture saved in /tmp/picture." + picture.format)
    time.sleep(10)
