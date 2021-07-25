import sys
import os
import yaml
import __main__

owner: str
label: str
db_host: str
db_port: int
db_user: str
db_password: str
db_database: str
disable_monitoring: bool
disable_capacitive_moisture_sensor: bool
disable_si1145_sensor: bool
disable_bme680_sensor: bool
disable_scd30_sensor: bool
disable_as7341_sensor: bool
disable_raspberry_sensor: bool


def load(file_name):
    global owner
    global label
    global db_host
    global db_port
    global db_user
    global db_password
    global db_database
    global disable_monitoring
    global disable_capacitive_moisture_sensor
    global disable_si1145_sensor
    global disable_bme680_sensor
    global disable_scd30_sensor
    global disable_as7341_sensor
    global disable_raspberry_sensor

    # Load config_file from the directory of the main.py
    main_dir: str = os.path.dirname(os.path.abspath(__main__.__file__))
    config_path: str = os.path.join(main_dir, file_name)

    with open(config_path) as config_file:

        config_data = yaml.safe_load(config_file)

        if isinstance(config_data, dict):
            def config_get(key: str, default_value=None):
                value = config_data[key]
                return value if value is not None else default_value

            owner = config_get("owner")
            label = config_get("label")
            db_host = config_get("db_host")
            db_port = config_get("db_port")
            db_user = config_get("db_user")
            db_password = config_get("db_password")
            db_database = config_get("db_database")
            disable_monitoring = config_get("disable_monitoring", False)
            disable_capacitive_moisture_sensor = config_get("disable_capacitive_moisture_sensor", False)
            disable_si1145_sensor = config_get("disable_si1145_sensor", False)
            disable_bme680_sensor = config_get("disable_bme680_sensor", False)
            disable_scd30_sensor = config_get("disable_scd30_sensor", False)
            disable_as7341_sensor = config_get("disable_as7341_sensor", False)
            disable_raspberry_sensor = config_get("disable_raspberry_sensor", False)
        else:
            sys.exit("Configuration file is not valid")
