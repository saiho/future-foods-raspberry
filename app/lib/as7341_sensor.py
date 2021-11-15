from logging import info
import board
from adafruit_as7341 import AS7341
from lib.measurement import Measurement

#
# 11-channel visible light sensor (AS7341)
#

as7341: AS7341


def init():
    global as7341
    info("Init AS7341 sensor")
    as7341 = AS7341(board.I2C())
    read()  # Test read


def read() -> Measurement.AS7341():
    global as7341
    all_channels = as7341.all_channels
    data = Measurement.AS7341()
    data.violet_415nm = all_channels[0]
    data.indigo_445nm = all_channels[1]
    data.blue_480nm = all_channels[2]
    data.cyan_515nm = all_channels[3]
    data.green_555nm = all_channels[4]
    data.yellow_590nm = all_channels[5]
    data.orange_630nm = all_channels[6]
    data.red_680nm = all_channels[7]

    info(f"Visible light: violet = {data.violet_415nm}, indigo = {data.indigo_445nm}, blue = {data.blue_480nm}, cyan = {data.cyan_515nm}, green = {data.green_555nm}, yellow = {data.yellow_590nm}, orange = {data.orange_630nm}, red = {data.red_680nm}")

    return data
