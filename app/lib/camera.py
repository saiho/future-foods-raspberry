from typing import Tuple
import os
import tempfile
import subprocess
import lib.user_config as user_config
import lib.common as common
from lib.measurement import Measurement

temp_dir: tempfile.TemporaryDirectory = None


def init():
    global temp_dir

    temp_dir = tempfile.TemporaryDirectory()
    print("Created temporay directory for camera", temp_dir.name)


def close():
    global temp_dir

    if temp_dir is not None:
        print("Clean temporay directory of camera")
        temp_dir.cleanup()


def take_picture() -> Tuple[Measurement.Picture, bytes]:
    print("Take picture")
    temp_file = os.path.join(temp_dir.name, 'capture')

    result: subprocess.CompletedProcess

    # Take picture as PNG
    result = subprocess.run(['fswebcam', '-d', f'/dev/video{user_config.picture_video_device}', '-r',
                            f'{user_config.picture_width}x{user_config.picture_height}', '--png', '0', '-F', str(common.picture_samples), temp_file])
    if result.returncode != 0:
        print("Error taking picture")
        return None

    # Convert PNG to WEBP
    result = subprocess.run(['cwebp', '-q', str(user_config.picture_quality), temp_file, '-o', '-'], stdout=subprocess.PIPE)
    if result.returncode != 0:
        print("Error converting to WEBP")
        return None
    picture_data: bytes = result.stdout

    # Delete temporary PNG
    result = subprocess.run(['rm', temp_file])

    print(f"Retrieved and encoded picture (size = {len(picture_data)})")
    
    picture_info: Measurement.Picture = Measurement.Picture()
    picture_info.quality = user_config.picture_quality
    picture_info.format = common.picture_format
    return (picture_info, picture_data)
