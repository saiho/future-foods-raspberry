import sys
import os
from datetime import time
import yaml
import __main__

owner: str
label: str
db_host: str
db_port: int
db_user: str
db_password: str
db_database: str
picture_take_time: time = time(12, 00)
picture_width: int = 1920
picture_height: int = 1080
picture_quality: int = 100
disable_monitoring: bool = False
disable_capacitive_moisture_sensor: bool = False
disable_si1145_sensor: bool = False
disable_bme680_sensor: bool = False
disable_scd30_sensor: bool = False
disable_as7341_sensor: bool = False
disable_raspberry_sensor: bool = False
disable_picture_take: bool = False


def load(file_name):
    global owner
    global label
    global db_host
    global db_port
    global db_user
    global db_password
    global db_database
    global picture_take_time
    global picture_width
    global picture_height
    global picture_quality
    global disable_monitoring
    global disable_capacitive_moisture_sensor
    global disable_si1145_sensor
    global disable_bme680_sensor
    global disable_scd30_sensor
    global disable_as7341_sensor
    global disable_raspberry_sensor
    global disable_picture_take

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
            db_host = config_data.get("db_host")
            db_port = config_data.get("db_port")
            db_user = config_data.get("db_user")
            db_password = config_data.get("db_password")
            db_database = config_data.get("db_database")
            picture_take_time = to_time(config_data.get("picture_take_time", picture_take_time))
            picture_width = config_data.get("picture_width", picture_width)
            picture_height = config_data.get("picture_height", picture_height)
            picture_quality = config_data.get("picture_quality", picture_quality)
            disable_monitoring = config_data.get("disable_monitoring", disable_monitoring)
            disable_capacitive_moisture_sensor = config_data.get("disable_capacitive_moisture_sensor", disable_capacitive_moisture_sensor)
            disable_si1145_sensor = config_data.get("disable_si1145_sensor", disable_si1145_sensor)
            disable_bme680_sensor = config_data.get("disable_bme680_sensor", disable_bme680_sensor)
            disable_scd30_sensor = config_data.get("disable_scd30_sensor", disable_scd30_sensor)
            disable_as7341_sensor = config_data.get("disable_as7341_sensor", disable_as7341_sensor)
            disable_raspberry_sensor = config_data.get("disable_raspberry_sensor", disable_raspberry_sensor)
            disable_picture_take = config_data.get("disable_picture_take", disable_picture_take)
        else:
            sys.exit("Configuration file is not valid")
