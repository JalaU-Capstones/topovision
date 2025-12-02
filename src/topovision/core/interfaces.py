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


class ITopographicData(ABC):
    """
    Any class intended to be consumed by the Riemann calculator must implement
    this interface.
    """

    @property
    @abstractmethod
    def width(self) -> int:
        """Returns the width of the data matrix (X-axis)."""
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        """Returns the height of the data matrix (Y-axis)."""
        pass

    @property
    @abstractmethod
    def processed_matrix(self) -> NDArray[np.uint8]:
        """
        Returns the processed numerical matrix (NumPy Array).
        Represents the Z values (height/intensity) at each (x, y) coordinate.
        """
        pass
