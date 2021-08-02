from typing import Tuple
import subprocess
import lib.user_config as user_config
import lib.common as common
from lib.measurement import Measurement


def take_picture() -> Tuple[Measurement.Picture, bytes]:
    print("Take picture")

    # Take picture as PNG
    process_fswebcam: subprocess.Popen = subprocess.Popen(
        ['fswebcam', '-d', f'/dev/video{user_config.picture_video_device}', '-r', f'{user_config.picture_width}x{user_config.picture_height}',
            '--png', '0', '-F', str(user_config.picture_num_samples), '--no-banner', '--save', '-'],
        stdout=subprocess.PIPE)
    # Convert PNG to WEBP
    process_cwebp: subprocess.Popen = subprocess.Popen(
        ['cwebp', '-q', str(user_config.picture_quality), '-o', '-', '--', '-'],
        stdin=process_fswebcam.stdout, stdout=subprocess.PIPE)
    picture_data: bytes = process_cwebp.communicate()[0]
    if process_cwebp.returncode != 0:
        print("Error taking picture")
        return None

    print(f"Retrieved and encoded picture (size = {len(picture_data)})")

    picture_info: Measurement.Picture = Measurement.Picture()
    picture_info.quality = user_config.picture_quality
    picture_info.format = common.picture_format
    picture_info.num_samples = user_config.picture_num_samples
    return (picture_info, picture_data)
