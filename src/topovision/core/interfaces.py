"""Core interfaces for TopoVision."""

from abc import ABC, abstractmethod
from typing import Optional
import numpy as np
from numpy.typing import NDArray
from .models import FrameData, Region, Result


class ICamera(ABC):
    """Abstract interface for camera implementations."""

    @abstractmethod
    def start(self) -> None:
        """Start the camera capture."""
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """Stop the camera and release resources."""
        raise NotImplementedError

    @abstractmethod
    def pause(self) -> None:
        """Pause camera capture."""
        raise NotImplementedError

    @abstractmethod
    def get_frame(self) -> Optional[NDArray[np.uint8]]:
        """Fetch the latest frame from the camera."""
        raise NotImplementedError


class ICalculator(ABC):
    """Abstract interface for performing topographic calculations."""

    @abstractmethod
    def derivative(self, frame: FrameData, region: Region, axis: str) -> float:
        """
        Compute partial derivative along given axis ('x' or 'y').

        Args:
            frame (FrameData): The frame data to analyze.
            region (Region): The region to compute over.
            axis (str): Axis of derivative, 'x' or 'y'.

        Returns:
            float: Calculated derivative.
        """
        raise NotImplementedError

    @abstractmethod
    def gradient(self, frame: FrameData, region: Region) -> "GradientResult":
        """
        Compute gradient over the specified region.

        Args:
            frame (FrameData): The frame data to analyze.
            region (Region): The region to compute over.

        Returns:
            GradientResult: Object containing dx, dy arrays.
        """
        raise NotImplementedError

    @abstractmethod
    def volume(self, frame: FrameData, region: Region) -> float:
        """
        Compute volumetric sum (Riemann) over the region.

        Args:
            frame (FrameData): The frame data to analyze.
            region (Region): The region to compute over.

        Returns:
            float: Computed volume.
        """
        raise NotImplementedError


class IVisualizer(ABC):
    """Abstract interface for visualizing frames and analysis results."""

    @abstractmethod
    def draw_region(self, frame: FrameData, region: Region) -> NDArray[np.uint8]:
        """Draw the region rectangle on the frame."""
        raise NotImplementedError

    @abstractmethod
    def overlay_result(
        self, frame: FrameData, region: Region, result: Result
    ) -> NDArray[np.uint8]:
        """Overlay calculation result visually on the frame."""
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
