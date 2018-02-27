"""camera.py
A class to constantly take photos, for quik access
"""
import threading

from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2

from settings import RESOLUTIONX, RESOLUTIONY


class ConstantCamera(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.camera = PiCamera(*args, **kwargs)
        self.camera.resolution = (RESOLUTIONX, RESOLUTIONY)
        self.camera.rotation = 180
        self._camarray = PiRGBArray(self.camera, size=(RESOLUTIONX, RESOLUTIONY))
        self._image = None
        self.preview = False
        self._imgot = False
        self._lock = threading.Lock()
        self._close_event = threading.Event()
        self._ready_event = threading.Event()

    def run(self):
        # capture frames from the camera
        for frame in self.camera.capture_continuous(self._camarray, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            with self._lock:
                # capture_continuous yields buffer array
                self._image = frame.array

            if not self._ready_event.is_set():
                self._ready_event.set()

            if self.preview:
                cv2.imshow("PREVIEW", self._image)
                cv2.waitKey(1)
            
            # clear the stream in preparation for the next frame
            self._camarray.truncate(0)
            if self._close_event.is_set():
                break
        self.camera.close()

    def get_image(self):
        # Avoid catching it halfway thru
        with self._lock:
            returnval = self._image
        # Return appropriate array...
        return returnval


    def is_ready(self):
        return self._ready_event.is_set()
    
    def wait_for_ready(self):
        self._ready_event.wait()

    def start_preview(self):
        with self._lock:
            self.preview = True
    def stop_preview(self):
        with self._lock:
            self.preview = False
