import seeed_si114x
from lib.measurement import Measurement

#
# Sunlight sensor (SI1145)
#

si1145: seeed_si114x.grove_si114x


def init():
    global si1145
    print("Init SI1145 sensor")
    si1145 = seeed_si114x.grove_si114x()


def read() -> Measurement.SI1145:
    global si1145
    data = Measurement.SI1145()
    data.sunlight_visible = si1145.ReadVisible
    data.sunlight_uv = si1145.ReadUV
    data.sunlight_ir = si1145.ReadIR
    print(f"Sunlight: visible = {data.sunlight_visible}, UV = {data.sunlight_uv}, IR = {data.sunlight_ir}")
    return data
