from typing import Dict
from datetime import datetime
from grove.gpio import GPIO
from lib.user_config import user_config

ports: Dict[str, GPIO]


def init():
    global ports

    print("Init relay switch")
    ports = {key: GPIO(relay.port, GPIO.OUT) for key, relay in user_config.relay_switch_devices.items()}
    check()


def check() -> Dict[str, bool]:
    global ports

    relays_on: Dict[str, bool] = {}
    for key, relay in user_config.relay_switch_devices.items():
        if relay.on_time is not None and relay.off_time is not None and relay.on_time <= datetime.now().time() <= relay.off_time:
            print(f"Relay of '{key}' is ON")
            relays_on[key] = True
            ports[key].write(1 if relay.on_as_one else 0)
        else:
            print(f"Relay of '{key}' is OFF")
            relays_on[key] = False
            ports[key].write(0 if relay.on_as_one else 1)
    return relays_on
