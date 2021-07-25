from datetime import timedelta

version: int = 202107251918
measurement_interval: timedelta = timedelta(minutes=5)
post_data_interval: timedelta = timedelta(hours=2)
scd30_temperature_offset_correction_interval: timedelta = timedelta(hours=6)
scd30_temperature_offset_max: float = 2  # ℃
