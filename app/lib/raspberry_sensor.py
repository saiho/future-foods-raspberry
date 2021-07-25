from gpiozero import CPUTemperature
from lib.measurement import Measurement

#
#  Get Raspberry CPU temperature
#

cpu: CPUTemperature


def init():
    global cpu
    print("Init CPU check")
    cpu = CPUTemperature()


def read() -> Measurement.Raspberry:
    global cpu
    data = Measurement.Raspberry()
    data.cpu_temperature = cpu.temperature
    print(f"CPU temperature = {data.cpu_temperature}")
    return data
