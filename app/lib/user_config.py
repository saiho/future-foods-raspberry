import sys
import os
from datetime import time
import yaml
import __main__

owner: str
label: str
database_host: str
database_port: int
database_name: str
database_user: str
database_password: str
picture_take_time: time = time(12, 00)
picture_width: int = 1920
picture_height: int = 1080
picture_quality: int = 100
picture_video_device: int = -1
enable_monitoring: bool = True
enable_capacitive_moisture_sensor: bool = True
enable_si1145_sensor: bool = True
enable_bme680_sensor: bool = True
enable_scd30_sensor: bool = True
enable_as7341_sensor: bool = True
enable_raspberry_sensor: bool = True
enable_picture_take: bool = True


def load(file_name):
    global owner
    global label
    global database_host
    global database_port
    global database_name
    global database_user
    global database_password
    global picture_take_time
    global picture_width
    global picture_height
    global picture_quality
    global picture_video_device
    global enable_monitoring
    global enable_capacitive_moisture_sensor
    global enable_si1145_sensor
    global enable_bme680_sensor
    global enable_scd30_sensor
    global enable_as7341_sensor
    global enable_raspberry_sensor
    global enable_picture_take

    # Load config_file from the directory of the main.py
    main_dir: str = os.path.dirname(os.path.abspath(__main__.__file__))
    config_path: str = os.path.join(main_dir, file_name)

    with open(config_path) as config_file:

        config_data = yaml.safe_load(config_file)

        if isinstance(config_data, dict):
            def to_time(obj) -> time:
                if isinstance(obj, time):
                    return obj
                else:
                    return time.fromisoformat(obj)

            owner = config_data.get("owner")
            label = config_data.get("label")
            database_host = config_data.get("database_host")
            database_port = config_data.get("database_port")
            database_name = config_data.get("database_name")
            database_user = config_data.get("database_user")
            database_password = config_data.get("database_password")
            picture_take_time = to_time(config_data.get("picture_take_time", picture_take_time))
            picture_width = config_data.get("picture_width", picture_width)
            picture_height = config_data.get("picture_height", picture_height)
            picture_quality = config_data.get("picture_quality", picture_quality)
            picture_video_device = config_data.get("picture_video_device", picture_video_device)
            enable_monitoring = config_data.get("enable_monitoring", enable_monitoring)
            enable_capacitive_moisture_sensor = config_data.get("enable_capacitive_moisture_sensor", enable_capacitive_moisture_sensor)
            enable_si1145_sensor = config_data.get("enable_si1145_sensor", enable_si1145_sensor)
            enable_bme680_sensor = config_data.get("enable_bme680_sensor", enable_bme680_sensor)
            enable_scd30_sensor = config_data.get("enable_scd30_sensor", enable_scd30_sensor)
            enable_as7341_sensor = config_data.get("enable_as7341_sensor", enable_as7341_sensor)
            enable_raspberry_sensor = config_data.get("enable_raspberry_sensor", enable_raspberry_sensor)
            enable_picture_take = config_data.get("enable_picture_take", enable_picture_take)
        else:
            sys.exit("Configuration file is not valid")
