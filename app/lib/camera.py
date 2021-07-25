from typing import Tuple
import cv2
import lib.user_config as user_config
import lib.common as common
from lib.measurement import Measurement


def take_picture() -> Tuple[Measurement.Picture, bytes]:
    print("Init Camera")
    camera = cv2.VideoCapture(0)
    try:
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, user_config.picture_width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, user_config.picture_height)
        print(f"Using supported resolution of {int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))}")

        captured, frame = camera.read()
        if not captured:
            print('Failed to retrieve picture')
            return None

        encoded, picture_data = cv2.imencode("." + common.picture_format, frame, [cv2.IMWRITE_WEBP_QUALITY, user_config.picture_quality])
        if not encoded:
            print('Failed to encode picture')
            return None

        print(f'Retrieved and encoded picture (size = {len(picture_data)})')

        picture_info: Measurement.Picture = Measurement.Picture()
        picture_info.quality = user_config.picture_quality
        picture_info.format = common.picture_format
        return (picture_info, picture_data.tobytes())
    finally:
        camera.release()
