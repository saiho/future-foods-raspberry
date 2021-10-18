from typing import Dict
import sys
import os
from datetime import datetime, time
import yaml

CONFIG_FILE_NAME = "../config.yml"


def _to_time(obj) -> time:
    if obj is None:
        return None
    elif isinstance(obj, time):
        return obj
    else:
        return datetime.strptime(obj, "%H:%M").time()

# Convert keys with dots in multiline sections. For example:
#
# camera.enabled: true
# camera.take_time: "18:00"
#
# Is treated as:
#
# camera:
#   enabled: true
#   take_time: "18:00"
#


def _split_dot_keys(obj):
    if isinstance(obj, dict):
        for key in [key for key in obj if isinstance(key, str) and ("." in key)]:
            value = obj.pop(key)
            subkey1, subkey2 = key.split(".", 1)
            if subkey1 in obj:
                obj[subkey1][subkey2] = value
            else:
                obj[subkey1] = {subkey2: value}
        for value in obj.values():
            _split_dot_keys(value)

    elif isinstance(obj, list):
        for value in obj:
            _split_dot_keys(value)


class Config:

    class Database:
        host: str
        port: int
        name: str
        user: str
        password: str

        def __init__(self, config_data: dict):
            self.host = config_data.get("host")
            self.port = config_data.get("port")
            self.name = config_data.get("name")
            self.user = config_data.get("user")
            self.password = config_data.get("password")

    class CapacitiveMoistureSensor:
        port: int

        def __init__(self, config_data: dict):
            self.port = config_data.get("port")

    class CameraDevice:
        video_device: int
        width: int
        height: int
        quality: int
        num_samples: int

        def __init__(self, config_data: dict):
            self.video_device = config_data.get("video_device", -1)
            self.width = config_data.get("width", 1920)
            self.height = config_data.get("height", 1080)
            self.quality = config_data.get("quality", 100)
            self.num_samples = config_data.get("num_samples", 1)

    class RelaySwitchDevice:
        port: int
        on_time: time
        off_time: time
        on_as_one: bool

        def __init__(self, config_data: dict):
            self.port = config_data.get("port")
            self.on_time = _to_time(config_data.get("on_time"))
            self.off_time = _to_time(config_data.get("off_time"))
            self.on_as_one = config_data.get("on_as_one", True)

    owner: str
    label: str

    database: Database

    monitoring_enabled: bool
    capacitive_moisture_sensor_enabled: bool
    si1145_sensor_enabled: bool
    bme680_sensor_enabled: bool
    scd30_sensor_enabled: bool
    as7341_sensor_enabled: bool
    raspberry_sensor_enabled: bool

    capacitive_moisture_sensors: Dict[str, CapacitiveMoistureSensor]

    camera_enabled: bool
    camera_take_time: time
    camera_devices: Dict[str, CameraDevice]

    relay_switch_enabled: bool
    relay_switch_devices: Dict[str, RelaySwitchDevice]

    def __init__(self, config_data: dict):

        self.owner = config_data.get("owner")
        self.label = config_data.get("label")

        self.database = Config.Database(config_data.get("database", {}))

        self.monitoring_enabled = config_data.get("monitoring", {}).get("enabled", True)

        capacitive_moisture_config_data: dict = config_data.get("capacitive_moisture_sensor", {})
        self.capacitive_moisture_sensor_enabled = capacitive_moisture_config_data.get("enabled", True)
        self.capacitive_moisture_sensors = {
            key: Config.CapacitiveMoistureSensor(sensor) for key, sensor in capacitive_moisture_config_data.get("devices", {}).items()}

        self.si1145_sensor_enabled = config_data.get("si1145_sensor", {}).get("enabled", True)
        self.bme680_sensor_enabled = config_data.get("bme680_sensor", {}).get("enabled", True)
        self.scd30_sensor_enabled = config_data.get("scd30_sensor", {}).get("enabled", True)
        self.as7341_sensor_enabled = config_data.get("as7341_sensor", {}).get("enabled", True)
        self.raspberry_sensor_enabled = config_data.get("raspberry_sensor", {}).get("enabled", True)

        camera_config_data: dict = config_data.get("camera", {})
        self.camera_enabled = camera_config_data.get("enabled", True)
        self.camera_take_time = _to_time(camera_config_data.get("take_time", time(12, 00)))
        self.camera_devices = {key: Config.CameraDevice(camera) for key, camera in camera_config_data.get("devices", {}).items()}

        relay_switch_config_data: dict = config_data.get("relay_switch", {})
        self.relay_switch_enabled = relay_switch_config_data.get("enabled", True)
        self.relay_switch_devices = {
            key: Config.RelaySwitchDevice(relay) for key, relay in relay_switch_config_data.get("devices", {}).items()}


user_config: Config

# Load CONFIG_FILE_NAME from the directory of the main.py
main_dir: str = os.path.dirname(os.path.abspath(__file__))
config_path: str = os.path.join(main_dir, CONFIG_FILE_NAME)

with open(config_path) as config_file:
    try:
        config_data = yaml.safe_load(config_file)
        _split_dot_keys(config_data)
        user_config = Config(config_data)
    except:
        sys.exit("Configuration file is not valid")
