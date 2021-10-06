# Sesnors

| Name | Information | Code | Python library |
| ---- | ----------- | ---- | -------------- |
| Capacitive moisture sensor (Grove) | https://wiki.seeedstudio.com/Grove-Capacitive_Moisture_Sensor-Corrosion-Resistant/ | https://github.com/Seeed-Studio/grove.py | `grove.py` |
| Sunlight sensor (SI1145) | https://wiki.seeedstudio.com/Grove-Sunlight_Sensor/ | https://github.com/Seeed-Studio/Seeed_Python_SI114X | `seeed-python-si114x` |
| CO₂, temperature & humidity sensor (SCD30) | https://wiki.seeedstudio.com/Grove-CO2_Temperature_Humidity_Sensor-SCD30/ | https://github.com/RequestForCoffee/scd30 | `scd30_i2c` |
| Temperature, humidity, pressure & gas sensor (BME680) | https://wiki.seeedstudio.com/Grove-Temperature_Humidity_Pressure_Gas_Sensor_BME680/ | https://github.com/pimoroni/bme680-python | `bme680` |
| 11-channel visible light sensor (AS7341) | https://wiki.dfrobot.com/Gravity_AS7341_Visible_Light_Sensor_SKU_SEN0364 | https://github.com/adafruit/Adafruit_CircuitPython_AS7341 | `adafruit-circuitpython-as7341` |

# ADC converters

| Name | Information | Code | Python library |
| ---- | ----------- | ---- | -------------- |
| MCP3008 | ADC converter that communicates via SPI interface. | https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/connecting-the-cobbler-to-a-mcp3008 | `adafruit-circuitpython-mcp3xxx` |
| Grove Base Hat for Raspberry Pi Zero | The Hat includes an ADC converter via SPI interface. https://wiki.seeedstudio.com/Grove_Base_Hat_for_Raspberry_Pi_Zero | | |

# Other

| Name | Information |
| ---- | ----------- |
| SPDT Relay (Grove) | https://wiki.seeedstudio.com/Grove-2-Channel_SPDT_Relay/ |

# I2C addresses

| Device    | Address |
| --------- | ------- |
| SCD30     | 0x61 |
| SI1145    | 0x60 |
| BME680    | 0x76 |
| Grove ADC | 0x04 |
| AS7341    | 0x39 |

# Pinout

See: https://www.raspberrypi.org/documentation/usage/gpio/

![Pinout Raspberry](https://www.raspberrypi.org/documentation/computers/images/GPIO-Pinout-Diagram-2.png)

![Pinout Raspberry Zero](https://www.asw.pt/blog/content/public/upload/rpipinout_0_o.png)

(License note: these images are linked from external web sites and may be subject to different license terms)
