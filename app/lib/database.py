from typing import List
import psycopg2
from lib.measurement import Measurement
from lib.user_config import user_config

count_since_start: int = 0


def insert_data(measurement: Measurement):
    global count_since_start

    count_since_start = count_since_start + 1
    measurement.count_since_start = count_since_start

    print("Connecting to DB")
    connection = psycopg2.connect(
        host=user_config.database.host,
        port=user_config.database.port,
        database=user_config.database.name,
        user=user_config.database.user,
        password=user_config.database.password)

    create_date = measurement.measured_to.astimezone()

    cursor = connection.cursor()
    print("Inserting measurement")
    cursor.execute("""
        INSERT INTO measurement
            ("owner", create_date, "label", full_content)
        VALUES
            (%s, %s, %s, %s)""", (
        measurement.owner,
        create_date,
        measurement.label,
        measurement.as_json()
    ))

    if measurement.capacitive_moisture:
        print("Inserting measurement_soil_moisture")
        capacitive_moisture_values: List[float] = [None] * 6
        capacitive_moisture_stdevs: List[float] = [None] * 6
        capacitive_moisture_tags: List[str] = [None] * 6
        for key, sensor in measurement.capacitive_moisture.items():
            if sensor.port < 6:
                capacitive_moisture_values[sensor.port] = sensor.value
                capacitive_moisture_stdevs[sensor.port] = sensor.stdev
                capacitive_moisture_tags[sensor.port] = key
        cursor.execute("""
            INSERT INTO measurement_soil_moisture
                ("owner", create_date, value_1, stdev_1, tag_1, value_2, stdev_2, tag_2, value_3, stdev_3, tag_3, value_4, stdev_4, tag_4, value_5, stdev_5, tag_5, value_6, stdev_6, tag_6)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            measurement.owner,
            create_date,
            capacitive_moisture_values[0],
            capacitive_moisture_stdevs[0],
            capacitive_moisture_tags[0],
            capacitive_moisture_values[1],
            capacitive_moisture_stdevs[1],
            capacitive_moisture_tags[1],
            capacitive_moisture_values[2],
            capacitive_moisture_stdevs[2],
            capacitive_moisture_tags[2],
            capacitive_moisture_values[3],
            capacitive_moisture_stdevs[3],
            capacitive_moisture_tags[3],
            capacitive_moisture_values[4],
            capacitive_moisture_stdevs[4],
            capacitive_moisture_tags[4],
            capacitive_moisture_values[5],
            capacitive_moisture_stdevs[5],
            capacitive_moisture_tags[5]
        ))

    if measurement.si1145:
        print("Inserting measurement_si1145")
        cursor.execute("""
            INSERT INTO measurement_si1145
                ("owner", create_date, sunlight_visible, stdev_sunlight_visible, sunlight_uv, stdev_sunlight_uv, sunlight_ir, stdev_sunlight_ir)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)""", (
            measurement.owner,
            create_date,
            measurement.si1145.sunlight_visible,
            measurement.si1145.stdev_sunlight_visible,
            measurement.si1145.sunlight_uv,
            measurement.si1145.stdev_sunlight_uv,
            measurement.si1145.sunlight_ir,
            measurement.si1145.stdev_sunlight_ir
        ))

    if measurement.bme680:
        print("Inserting measurement_bme680")
        cursor.execute("""
            INSERT INTO measurement_bme680
                ("owner", create_date, temperature, stdev_temperature, pressure, stdev_pressure, humidity, stdev_humidity, gas_resistance, stdev_gas_resistance)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            measurement.owner,
            create_date,
            measurement.bme680.temperature,
            measurement.bme680.stdev_temperature,
            measurement.bme680.pressure,
            measurement.bme680.stdev_pressure,
            measurement.bme680.humidity,
            measurement.bme680.stdev_humidity,
            measurement.bme680.gas_resistance,
            measurement.bme680.stdev_gas_resistance
        ))

    if measurement.scd30:
        print("Inserting measurement_scd30")
        cursor.execute("""
            INSERT INTO measurement_scd30
                ("owner", create_date, co2_ppm, stdev_co2_ppm, temperature, stdev_temperature, humidity, stdev_humidity)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)""", (
            measurement.owner,
            create_date,
            measurement.scd30.co2_ppm,
            measurement.scd30.stdev_co2_ppm,
            measurement.scd30.temperature,
            measurement.scd30.stdev_temperature,
            measurement.scd30.humidity,
            measurement.scd30.stdev_humidity
        ))

    if measurement.as7341:
        print("Inserting measurement_as7341")
        cursor.execute("""
            INSERT INTO measurement_as7341
                ("owner", create_date, violet_415nm, stdev_violet_415nm, indigo_445nm, stdev_indigo_445nm, blue_480nm, stdev_blue_480nm, cyan_515nm, stdev_cyan_515nm, green_555nm, stdev_green_555nm, yellow_590nm, stdev_yellow_590nm, orange_630nm, stdev_orange_630nm, red_680nm, stdev_red_680nm)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            measurement.owner,
            create_date,
            measurement.as7341.violet_415nm,
            measurement.as7341.stdev_violet_415nm,
            measurement.as7341.indigo_445nm,
            measurement.as7341.stdev_indigo_445nm,
            measurement.as7341.blue_480nm,
            measurement.as7341.stdev_blue_480nm,
            measurement.as7341.cyan_515nm,
            measurement.as7341.stdev_cyan_515nm,
            measurement.as7341.green_555nm,
            measurement.as7341.stdev_green_555nm,
            measurement.as7341.yellow_590nm,
            measurement.as7341.stdev_yellow_590nm,
            measurement.as7341.orange_630nm,
            measurement.as7341.stdev_orange_630nm,
            measurement.as7341.red_680nm,
            measurement.as7341.stdev_red_680nm
        ))

    if measurement.pictures:
        print("Inserting measurement_picture")
        for key, pict in measurement.pictures.items():
            cursor.execute("""
                INSERT INTO measurement_picture
                    ("owner", create_date, tag, picture)
                VALUES
                    (%s, %s, %s, %s)""", (
                measurement.owner,
                create_date,
                key,
                pict.data
            ))

    connection.commit()
    cursor.close()
    connection.close()
    print("Connection closed")
