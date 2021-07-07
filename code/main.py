import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as mcp3008
from adafruit_mcp3xxx.analog_in import AnalogIn
import seeed_si114x
import bme680
import scd30_i2c
import psycopg2
import time
from datetime import datetime, timedelta

### Global settings
owner = 'lAl'
label = 'eden-level-1'
measurement_interval = 3600 # 1 hour
scd30_measurement_interval = 1600 # 26 min 40 seg
temperature_offset_correction_interval = 54000 # 15 hours
temperature_offset_max = 2
db_host = 'your db host'
db_port = 5432
db_user = 'your db user'
db_password = 'your db password'
db_database = 'your db name'
version = 3

print('Starting sensor monitor service')
print('Current Time =', datetime.now())


### Read moisture through SPI interface with MCP3008
print('Init SPI bus')
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)
# create the mcp object
mcp = mcp3008.MCP3008(spi, cs)
# create an analog input channel on pin 0 to 3
chan0 = AnalogIn(mcp, mcp3008.P0)
chan1 = AnalogIn(mcp, mcp3008.P1)
chan2 = AnalogIn(mcp, mcp3008.P2)
chan3 = AnalogIn(mcp, mcp3008.P3)

def get_moisture():
	global moisture_0
	global moisture_1
	global moisture_2
	global moisture_3

	moisture_0 = chan0.value
	moisture_1 = chan1.value
	moisture_2 = chan2.value
	moisture_3 = chan3.value

	print('Moisture values: {0}, {1}, {2}, {3}'.format(moisture_0, moisture_1, moisture_2, moisture_3))


### Sunlight Sensor (SI1145)
print('Init SI1145 sensor')
SI1145 = seeed_si114x.grove_si114x()

def get_si1145_measurement():
	global si1145_visible
	global si1145_uv
	global si1145_ir

	si1145_visible = SI1145.ReadVisible
	si1145_uv = SI1145.ReadUV
	si1145_ir = SI1145.ReadIR

	print('Sunlight values: visible = {0}, UV = {1}, IR = {2}'.format(si1145_visible, si1145_uv, si1145_ir))


### Temperature, Humidity, Pressure & Gas Sensor (BME680)
print('Init BME680 sensor')
try:
	bme680_sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
	bme680_sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

bme680_sensor.set_humidity_oversample(bme680.OS_2X)
bme680_sensor.set_pressure_oversample(bme680.OS_4X)
bme680_sensor.set_temperature_oversample(bme680.OS_8X)
bme680_sensor.set_filter(bme680.FILTER_SIZE_3)
bme680_sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
bme680_sensor.set_gas_heater_temperature(320)
bme680_sensor.set_gas_heater_duration(150)
bme680_sensor.select_gas_heater_profile(0)

def get_bme680_measurement():
	global bme680_temperature
	global bme680_pressure
	global bme680_humidity
	global bme680_gas_resistance

	print('BME680 wait for measurement')
	max_count = 200
	while (not bme680_sensor.get_sensor_data() or not bme680_sensor.data.heat_stable) and max_count > 0:
		max_count = max_count - 1
		time.sleep(1)

	bme680_temperature = bme680_sensor.data.temperature
	bme680_pressure = bme680_sensor.data.pressure
	bme680_humidity = bme680_sensor.data.humidity
	bme680_gas_resistance = bme680_sensor.data.gas_resistance

	print('VOC = {0}, temperature = {1}, humidity = {2}, pressure = {3}'.format(bme680_gas_resistance, bme680_temperature, bme680_humidity, bme680_pressure))


### CO2 & Temperature & Humidity Sensor (SCD30)
print('Init SCD30 sensor')
scd30 = scd30_i2c.SCD30()
scd30.set_measurement_interval(scd30_measurement_interval)
scd30.set_temperature_offset(0)
scd30.set_auto_self_calibration(True)
print('SCD30 Start measuring')
scd30.start_periodic_measurement()
temperature_offset_correction_next = datetime.now() + timedelta(seconds = temperature_offset_correction_interval)

def get_scd30_measurement():
	global scd30_co2_ppm
	global scd30_temperature
	global scd30_humidity
	global temperature_offset_correction_next

	scd30_co2_ppm = None
	scd30_temperature = None
	scd30_humidity = None

	print('SCD30 wait for measurement')
	# Because SCD30 stores measurements every 1600 seconds but we want every 3600, we read all stored values to get the last
	max_count = 10
	while max_count > 0:
		max_count = max_count - 1
		time.sleep(2)
		if scd30.get_data_ready():
			m = scd30.read_measurement()
			if m is not None and m[0] != 0:
				scd30_co2_ppm = m[0]
				scd30_temperature = m[1]
				scd30_humidity = m[2]

				# Reajust temperature offset
				if datetime.now() > temperature_offset_correction_next:
					temperature_offset = scd30_temperature + scd30.get_temperature_offset() - bme680_temperature
					print('Recalculated offset temperature ', temperature_offset)
					if temperature_offset < 0 or bme680_temperature == 0:
						temperature_offset = 0
					if temperature_offset > temperature_offset_max:
						temperature_offset = temperature_offset_max
					scd30.set_temperature_offset(temperature_offset)
					temperature_offset_correction_next = datetime.now() + timedelta(seconds = temperature_offset_correction_interval)
				else:
					temperature_offset = scd30.get_temperature_offset()

				print('CO2 = {0}, temperature = {1}, temperature_offset = {2}, humidity = {3}'.format(scd30_co2_ppm, scd30_temperature, temperature_offset, scd30_humidity))

def insert_data():
	print('Connecting to DB') 
	connection = psycopg2.connect(
		host = db_host,
		port = db_port,
		user = db_user,
		password = db_password,
		database = db_database)

	cursor = connection.cursor()
	print('Inserting data') 
	cursor.execute('''
		INSERT INTO measurement (
			"owner",
			"label",
			create_date,
			value_capacitive_moisture_1,
			value_capacitive_moisture_2,
			value_capacitive_moisture_3,
			value_capacitive_moisture_4,
			value_scd30_co2,
			value_scd30_temperature,
			value_scd30_humidity,
			value_si1145_sunlight_visible,
			value_si1145_sunlight_uv,
			value_si1145_sunlight_ir,
			value_bme680_temperature,
			value_bme680_pressure,
			value_bme680_humidity,
			value_bme680_voc,
			"version"
		) VALUES (%s, %s, current_timestamp, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
			owner,
			label,
			moisture_0,
			moisture_1,
			moisture_2,
			moisture_3,
			scd30_co2_ppm,
			scd30_temperature,
			scd30_humidity,
			si1145_visible,
			si1145_uv,
			si1145_ir,
			bme680_temperature,
			bme680_pressure,
			bme680_humidity,
			bme680_gas_resistance,
			version
		))

	connection.commit()
	cursor.close()
	connection.close()
	print('Connection closed')


try:
	while True:

		get_moisture()
		get_si1145_measurement()
		get_bme680_measurement() # Must go before reading SCD30, because the temperature obtained here is used to calibrate the SCD30 sensor
		get_scd30_measurement()
		insert_data()

		# wait for next measurement
		print('Wait for next measurement at', (datetime.now() + timedelta(seconds = measure_interval)))
		time.sleep(measurement_interval)

finally:
	print('SCD30 Stop measuring')
	scd30.stop_periodic_measurement()
