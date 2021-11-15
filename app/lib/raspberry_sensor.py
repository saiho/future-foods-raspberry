from logging import info
from gpiozero import CPUTemperature
from lib.measurement import Measurement

#
#  Get Raspberry CPU temperature
#

cpu: CPUTemperature


def init():
    global cpu
    info("Init CPU check")
    cpu = CPUTemperature()
    read()  # Test read


def read() -> Measurement.Raspberry:
    global cpu
    data = Measurement.Raspberry()
    data.cpu_temperature = cpu.temperature
    info(f"CPU temperature = {data.cpu_temperature}")
    return data
