from typing import Dict
from datetime import datetime
from grove.gpio import GPIO
from lib.user_config import user_config

ports: Dict[str, GPIO]


def init():
    global ports

    print("Init relay switch")
    ports = {k: GPIO(d.port, GPIO.OUT) for k, d in user_config.relay_switch_devices.items()}
    check()


def check() -> Dict[str, bool]:
    global ports

    relays_on: Dict[str, bool] = {}
    for k, d in user_config.relay_switch_devices.items():
        if d.on_time is not None and d.off_time is not None and d.on_time <= datetime.now().time() <= d.off_time:
            print(f"Relay of '{k}' is ON")
            relays_on[k] = True
            ports[k].write(1 if d.on_as_one else 0)
        else:
            print(f"Relay of '{k}' is OFF")
            relays_on[k] = False
            ports[k].write(0 if d.on_as_one else 1)
    return relays_on
