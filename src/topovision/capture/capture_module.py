"""Handles camera capture and preprocessing logic."""

import time
from typing import Optional

import cv2
import numpy as np
from numpy.typing import NDArray

from topovision.core.interfaces import Camera


class OpenCVCamera(Camera):
    """A camera implementation using OpenCV."""

    def __init__(self, camera_id: int = 0) -> None:
        """
        Initializes the OpenCV camera.

        Args:
            camera_id (int): The ID of the camera to use.
        """
        self.camera_id: int = camera_id
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running: bool = False

    def start(self) -> None:
        """Starts the camera capture."""
        if not self.is_running:
            self.cap = cv2.VideoCapture(self.camera_id)
            if not self.cap.isOpened():
                raise IOError(f"Cannot open camera {self.camera_id}")
            self.is_running = True
            print("Camera started.")

    def stop(self) -> None:
        """Stops the camera and releases resources."""
        if self.is_running:
            self.is_running = False
            if self.cap is not None:
                self.cap.release()
                self.cap = None
            print("Camera stopped.")

    def pause(self) -> None:
        """Pauses the camera (in this case, same as stop)."""
        self.stop()

    def get_frame(self) -> Optional[NDArray[np.uint8]]:
        """
        Fetches a frame from the camera.

        Returns:
            The frame as a numpy array, or None if the camera is not running.
        """
        if self.is_running:
            assert self.cap is not None, "Camera not started"
            ret, frame = self.cap.read()
            if ret:
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None


class MockCamera(Camera):
    """A mock camera for testing purposes."""

    def __init__(self, width: int = 640, height: int = 480) -> None:
        """
        Initializes the mock camera.

        Args:
            width (int): The width of the mock frame.
            height (int): The height of the mock frame.
        """
        self.width = width
        self.height = height
        self.is_running: bool = False
        self._frame_counter: int = 0

    def start(self) -> None:
        """Starts the mock camera."""
        if not self.is_running:
            self.is_running = True
            print("Mock camera started.")

    def stop(self) -> None:
        """Stops the mock camera."""
        if self.is_running:
            self.is_running = False
            print("Mock camera stopped.")

    def pause(self) -> None:
        """Pauses the mock camera."""
        self.is_running = False
        print("Mock camera paused.")

    def get_frame(self) -> Optional[NDArray[np.uint8]]:
        """
        Generates a mock frame.

        Returns:
            A mock frame as a numpy array, or None if the camera is not running.
        """
        if self.is_running:
            # Create a frame that changes over time
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            # Fill with a color that changes with the frame number
            color = (self._frame_counter * 10) % 256
            frame[:, :, self._frame_counter % 3] = color
            self._frame_counter += 1
            time.sleep(1 / 30)  # Simulate 30 FPS
            return frame
        return None
