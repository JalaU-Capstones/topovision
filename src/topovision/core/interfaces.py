"""Core interfaces and models for TopoVision."""

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np
from numpy.typing import NDArray


class Camera(ABC):
    """
    Abstract base class for camera implementations.

    This interface defines the contract for camera devices, allowing for
    interchangeable concrete implementations (e.g., a real OpenCV camera
    or a mock camera for testing).
    """

    @abstractmethod
    def start(self) -> None:
        """Starts the camera capture stream."""
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """Stops the camera capture stream and releases resources."""
        raise NotImplementedError

    @abstractmethod
    def pause(self) -> None:
        """Pauses the camera capture stream."""
        raise NotImplementedError

    @abstractmethod
    def get_frame(self) -> Optional[NDArray[np.uint8]]:
        """
        Fetches the latest frame from the camera.

        Returns:
            A numpy array representing the frame, or None if no frame is available.
        """
        raise NotImplementedError
