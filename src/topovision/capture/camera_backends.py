"""Camera backends (OpenCV, MockCamera, etc.)."""

import cv2
import numpy as np
from abc import ABC, abstractmethod


class BaseCamera(ABC):
    """Interfaz que define el comportamiento común para cualquier cámara."""

    @abstractmethod
    def start(self):
        """Inicializa la cámara."""
        pass

    @abstractmethod
    def read(self):
        """Devuelve un None si falla."""
        pass

    @abstractmethod
    def stop(self):
        """Libera recursos."""
        pass


class OpenCVCamera(BaseCamera):
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = None
        self.running = False

    def start(self):
        self.cap = cv2.VideoCapture(self.camera_id)

        if not self.cap.isOpened():
            raise RuntimeError(f"No se pudo abrir la cámara con ID={self.camera_id}")

        self.running = True

    def read(self):
        if not self.running or self.cap is None:
            return None

        ret, frame = self.cap.read()
        return frame if ret else None

    def stop(self):
        if self.cap:
            self.cap.release()
        self.running = False
        self.cap = None



class MockCamera(BaseCamera):
    def __init__(self, width=640, height=480):
        self.running = False
        self.width = width
        self.height = height
        self.counter = 0

    def start(self):
        self.running = True

    def read(self):
        if not self.running:
            return None

        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        cv2.putText(frame, f"Mock Frame {self.counter}",
                    (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2)
        self.counter += 1
        return frame

    def stop(self):
        self.running = False