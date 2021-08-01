from datetime import timedelta

version: int = 202108012000
measurement_interval: timedelta = timedelta(minutes=5)
post_data_interval: timedelta = timedelta(hours=2)
picture_take_interval: timedelta = timedelta(days=1)
picture_format: str = "webp"
picture_samples: int = 5
scd30_temperature_offset_correction_interval: timedelta = timedelta(hours=6)
scd30_temperature_offset_max: float = 2  # ℃
