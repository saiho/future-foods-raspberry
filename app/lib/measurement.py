from __future__ import annotations
from typing import List, Tuple, Dict
from datetime import datetime
import statistics
import json
from lib import common


def _median_and_stdev(values: list) -> Tuple[float, float]:
    values: list = [v for v in values if v is not None]
    if len(values) == 0:
        return (None, None)
    median: float = statistics.median(values)
    if len(values) == 1:
        return (median, None)
    stdev: float = statistics.pstdev(values)
    return (median, stdev)


def _median_and_max(values: list) -> Tuple[float, float]:
    values: float = [v for v in values if v is not None]
    if len(values) == 0:
        return (None, None)
    return (statistics.median(values), max(values))


class Measurement:

    class CapacitiveMoisture:
        value: float
        stdev: float
        num_samples: int
        port: int

        @staticmethod
        def _median(data_list: List[Dict[str, Measurement.CapacitiveMoisture]]) -> Dict[str, Measurement.CapacitiveMoisture]:
            if not data_list:
                return None
            median_data_dict: Dict[str, Measurement.CapacitiveMoisture] = {}
            for key in data_list[0]:
                values = [d[key].value for d in data_list]
                median_data = Measurement.CapacitiveMoisture()
                median_data.value, median_data.stdev = _median_and_stdev(values)
                median_data.num_samples = len(data_list)
                median_data.port = data_list[0][key].port
                median_data_dict[key] = median_data
            return median_data_dict

    class SCD30:
        co2_ppm: float
        temperature: float
        temperature_offset: float
        humidity: float
        stdev_co2_ppm: float
        stdev_temperature: float
        stdev_temperature_offset: float
        stdev_humidity: float
        num_samples: int
        firmware_version: int

        @staticmethod
        def _median(data_list: List[Measurement.SCD30]) -> Measurement.SCD30:
            if not data_list:
                return None
            median_data: Measurement.SCD30 = Measurement.SCD30()
            median_data.co2_ppm, median_data.stdev_co2_ppm = _median_and_stdev([d.co2_ppm for d in data_list])
            median_data.temperature, median_data.stdev_temperature = _median_and_stdev([d.temperature for d in data_list])
            median_data.temperature_offset, median_data.stdev_temperature_offset = _median_and_stdev(
                [d.temperature_offset for d in data_list])
            median_data.humidity, median_data.stdev_humidity = _median_and_stdev([d.humidity for d in data_list])
            median_data.num_samples = len(data_list)
            median_data.firmware_version = data_list[0].firmware_version
            return median_data

    class SI1145:
        sunlight_visible: int
        sunlight_uv: int
        sunlight_ir: int
        stdev_sunlight_visible: float
        stdev_sunlight_uv: float
        stdev_sunlight_ir: float
        num_samples: int

        @staticmethod
        def _median(data_list: List[Measurement.SI1145]) -> Measurement.SI1145:
            if not data_list:
                return None
            median_data: Measurement.SI1145 = Measurement.SI1145()
            median_data.sunlight_visible, median_data.stdev_sunlight_visible = _median_and_stdev([d.sunlight_visible for d in data_list])
            median_data.sunlight_uv, median_data.stdev_sunlight_uv = _median_and_stdev([d.sunlight_uv for d in data_list])
            median_data.sunlight_ir, median_data.stdev_sunlight_ir = _median_and_stdev([d.sunlight_ir for d in data_list])
            median_data.num_samples = len(data_list)
            return median_data

    class BME680:
        temperature: float
        pressure: float
        humidity: float
        gas_resistance: float
        stdev_temperature: float
        stdev_pressure: float
        stdev_humidity: float
        stdev_gas_resistance: float
        num_samples: int

        @staticmethod
        def _median(data_list: List[Measurement.BME680]) -> Measurement.BME680:
            if not data_list:
                return None
            median_data: Measurement.BME680 = Measurement.BME680()
            median_data.temperature, median_data.stdev_temperature = _median_and_stdev([d.temperature for d in data_list])
            median_data.pressure, median_data.stdev_pressure = _median_and_stdev([d.pressure for d in data_list])
            median_data.humidity, median_data.stdev_humidity = _median_and_stdev([d.humidity for d in data_list])
            median_data.gas_resistance, median_data.stdev_gas_resistance = _median_and_stdev([d.gas_resistance for d in data_list])
            median_data.num_samples = len(data_list)
            return median_data

    class AS7341:
        violet_415nm: int
        indigo_445nm: int
        blue_480nm: int
        cyan_515nm: int
        green_555nm: int
        yellow_590nm: int
        orange_630nm: int
        red_680nm: int
        stdev_violet_415nm: float
        stdev_indigo_445nm: float
        stdev_blue_480nm: float
        stdev_cyan_515nm: float
        stdev_green_555nm: float
        stdev_yellow_590nm: float
        stdev_orange_630nm: float
        stdev_red_680nm: float
        num_samples: int

        @staticmethod
        def _median(data_list: List[Measurement.AS7341]) -> Measurement.AS7341:
            if not data_list:
                return None
            median_data: Measurement.AS7341 = Measurement.AS7341()
            median_data.violet_415nm, median_data.stdev_violet_415nm = _median_and_stdev([d.violet_415nm for d in data_list])
            median_data.indigo_445nm, median_data.stdev_indigo_445nm = _median_and_stdev([d.indigo_445nm for d in data_list])
            median_data.blue_480nm, median_data.stdev_blue_480nm = _median_and_stdev([d.blue_480nm for d in data_list])
            median_data.cyan_515nm, median_data.stdev_cyan_515nm = _median_and_stdev([d.cyan_515nm for d in data_list])
            median_data.green_555nm, median_data.stdev_green_555nm = _median_and_stdev([d.green_555nm for d in data_list])
            median_data.yellow_590nm, median_data.stdev_yellow_590nm = _median_and_stdev([d.yellow_590nm for d in data_list])
            median_data.orange_630nm, median_data.stdev_orange_630nm = _median_and_stdev([d.orange_630nm for d in data_list])
            median_data.red_680nm, median_data.stdev_red_680nm = _median_and_stdev([d.red_680nm for d in data_list])
            median_data.num_samples = len(data_list)
            return median_data

    class Raspberry:
        cpu_temperature: float
        cpu_temperature_max: float
        num_samples: int

        @staticmethod
        def _median(data_list: List[Measurement.Raspberry]) -> Measurement.Raspberry:
            if not data_list:
                return None
            median_data: Measurement.Raspberry = Measurement.Raspberry()
            median_data.cpu_temperature, median_data.cpu_temperature_max = _median_and_max([d.cpu_temperature for d in data_list])
            median_data.num_samples = len(data_list)
            return median_data

    class Picture:
        format: str
        quality: int
        num_samples: int
        data: bytes
        video_device: int

        @staticmethod
        # Return the last picture
        def _combine(data_list: List[Dict[str, Measurement.Picture]]) -> Dict[str, Measurement.Picture]:
            if not data_list:
                return None
            return data_list[-1]

    # Values
    capacitive_moisture: Dict[str, CapacitiveMoisture]
    si1145: SI1145
    bme680: BME680
    scd30: SCD30
    as7341: AS7341
    raspberry: Raspberry
    pictures: Dict[str, Picture]
    relays_on: Dict[str, bool]

    # Metadata
    owner: str
    label: str
    version: int
    measured_from: datetime
    measured_to: datetime
    count_since_start: int

    def __init__(self, owner: str = None, label: str = None):
        self.owner = owner
        self.label = label
        self.version = common.version
        self.measured_from = datetime.now()
        self.measured_to = datetime.now()
        self.count_since_start = None

    @staticmethod
    # When aggregating, consider relay on if there is a majority of measurements as on
    def _combine_relays_on(data_list: List[Dict[str, bool]]) -> Dict[str, bool]:
        if not data_list:
            return None
        median_data_dict: Dict[str, bool] = {}
        for key in data_list[0]:
            values = [d[key] for d in data_list]
            median_data_dict[key] = values.count(True) > values.count(False)
        return median_data_dict

    @staticmethod
    def combine(measurements: List[Measurement]) -> Measurement:

        if not measurements:
            return None

        combined_measurement: Measurement = Measurement()

        combined_measurement.capacitive_moisture = Measurement.CapacitiveMoisture._median(
            [m.capacitive_moisture for m in measurements if m.capacitive_moisture])
        combined_measurement.si1145 = Measurement.SI1145._median([m.si1145 for m in measurements if m.si1145])
        combined_measurement.bme680 = Measurement.BME680._median([m.bme680 for m in measurements if m.bme680])
        combined_measurement.scd30 = Measurement.SCD30._median([m.scd30 for m in measurements if m.scd30])
        combined_measurement.as7341 = Measurement.AS7341._median([m.as7341 for m in measurements if m.as7341])
        combined_measurement.raspberry = Measurement.Raspberry._median([m.raspberry for m in measurements if m.raspberry])
        combined_measurement.pictures = Measurement.Picture._combine([m.pictures for m in measurements if m.pictures])
        combined_measurement.relays_on = Measurement._combine_relays_on([m.relays_on for m in measurements if m.relays_on])

        combined_measurement.owner = measurements[0].owner
        combined_measurement.label = measurements[0].label
        combined_measurement.version = measurements[0].version
        combined_measurement.measured_from = min([m.measured_from for m in measurements])
        combined_measurement.measured_to = max([m.measured_from for m in measurements])
        combined_measurement.count_since_start = measurements[0].count_since_start

        return combined_measurement

    def as_json(self) -> str:
        def json_converter(o):
            if isinstance(o, datetime):
                return o.astimezone().isoformat()
            elif isinstance(o, bytes):
                return None
            else:
                return o.__dict__
        return json.dumps(self.__dict__, default=json_converter)
