import os
import cv2
from .base_camera import BaseCamera
import numpy as np
from PIL import Image


class Camera(BaseCamera):

    def __init__(self, videoname):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        if videoname == '0':
            Camera.video_source = '0'
        else:
            Camera.video_source = videoname
        # 判断camera是否存在
        Camera.camera = cv2.VideoCapture(Camera.video_source)
        if not Camera.camera.isOpened():
            return None
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        try:
            camera = Camera.camera
            while True:
                # read current frame
                ref, frame = camera.read()
                if frame is not None and ref:
                    yield cv2.imencode('.jpg', frame)[1].tobytes()
                else:
                    print('loss package. Restarting....')
                    camera.release()
                    camera = cv2.VideoCapture(Camera.video_source)
                    continue
        except Exception as e:
            raise e
