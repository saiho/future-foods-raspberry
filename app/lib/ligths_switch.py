from datetime import datetime
from grove.gpio import GPIO
import lib.user_config as user_config

port: GPIO


def init():
    global port
    print("Init Light Switch")
    port = GPIO(user_config.lights_switch_port, GPIO.OUT)


def check() -> bool:
    lights_on = user_config.lights_switch_on_time <= datetime.now().time() <= user_config.lights_switch_off_time
    if lights_on:
        print("Ligths are ON")
        port.write(1 if user_config.lights_switch_on_one else 0)
    else:
        print("Ligths are OFF")
        port.write(0 if user_config.lights_switch_on_one else 1)
    return lights_on
