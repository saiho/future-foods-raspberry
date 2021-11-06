from typing import Dict
from datetime import datetime
import subprocess
from lib.user_config import user_config, Config
import lib.common as common
from lib.measurement import Measurement

picture_take_next: datetime = None


def init():
    global picture_take_next
    picture_take_next = datetime.combine(datetime.now(), user_config.camera_take_time)
    while picture_take_next < datetime.now():
        picture_take_next = picture_take_next + common.picture_take_interval
    print("Next picture to be taken at", picture_take_next.astimezone())

    # Test camera
    for d in user_config.camera_devices.values():
        take_picture(d)


def take_pictures_if_scheduled() -> Dict[str, Measurement.Picture]:
    global picture_take_next
    if picture_take_next is None or datetime.now() < picture_take_next:
        return None
    picture_take_next = picture_take_next + common.picture_take_interval
    print("Next picture to be taken at", picture_take_next.astimezone())

    return {key: take_picture(camera) for key, camera in user_config.camera_devices.items()}


def take_picture(device_config: Config.CameraDevice) -> Measurement.Picture:
    print("Take picture")

    picture: Measurement.Picture = Measurement.Picture()
    picture.quality = device_config.quality
    picture.format = common.picture_format
    picture.num_samples = device_config.num_samples
    picture.video_device = device_config.video_device

    # Take picture as PNG
    process_fswebcam: subprocess.Popen = subprocess.Popen(
        ["fswebcam", "-d", f"/dev/video{device_config.video_device}", "-r", f"{device_config.width}x{device_config.height}", "--png", "0",
         "-F", str(device_config.num_samples), "--no-banner", "--rotate", str(device_config.rotation), "--save", "-"], stdout=subprocess.PIPE)
    # Convert PNG to WEBP
    process_cwebp: subprocess.Popen = subprocess.Popen(
        ["cwebp", "-q", str(device_config.quality), "-o", "-", "--", "-"], stdin=process_fswebcam.stdout, stdout=subprocess.PIPE)
    picture.data = process_cwebp.communicate()[0]
    if process_cwebp.returncode != 0:
        print("Error taking picture")
        return None

    print(f"Retrieved and encoded picture (size = {len(picture.data)})")
    return picture
