"""
This module defines various analysis strategies that implement the
IAnalysisStrategy interface. Each strategy encapsulates a specific
topographic calculation method.
"""

from typing import Any, List, Tuple, Union

import numpy as np
from numpy.typing import NDArray

from topovision.core.interfaces import IAnalysisStrategy
from topovision.core.models import ArcLengthResult, GradientResult, VolumeResult
from topovision.utils.math import calculate_arc_length


class GradientStrategy(IAnalysisStrategy):
    """
    Calculates the gradient (rate of change) of the input data.
    The gradient indicates the direction of the steepest ascent and its magnitude.
    """

    def analyze(self, data: NDArray[np.uint8], **kwargs: Any) -> GradientResult:
        """
        Computes the gradient (dz/dx, dz/dy) of the 2D data.

        Args:
            data (NDArray[np.uint8]): The input 2D array representing
                                      height/intensity values.
            **kwargs: Not used for gradient calculation, but kept for
                      interface consistency.

        Returns:
            GradientResult: An object containing the dz_dx and dz_dy components.
        """
        if data.ndim != 2:
            raise ValueError("GradientStrategy expects 2D data.")

        dz_dy, dz_dx = np.gradient(data.astype(np.float32))
        # Optionally, calculate magnitude
        magnitude = np.sqrt(dz_dx**2 + dz_dy**2)
        return GradientResult(dz_dx=dz_dx, dz_dy=dz_dy, magnitude=magnitude)


class VolumeStrategy(IAnalysisStrategy):
    """
    Calculates the approximate volume under the surface defined by the input data
    using a scaled Riemann sum.
    """

    def analyze(self, data: NDArray[np.uint8], **kwargs: Any) -> VolumeResult:
        """
        Computes the volume under the 2D data surface.

        Args:
            data (NDArray[np.uint8]): The input 2D array representing
                                      height/intensity values.
            z_factor (float): A scaling factor for the height (z-axis) values.
                              Defaults to 1.0.

        Returns:
            VolumeResult: An object containing the calculated volume.
        """
        if data.ndim != 2:
            raise ValueError("VolumeStrategy expects 2D data.")

        z_factor = kwargs.get("z_factor", 1.0)
        if not isinstance(z_factor, (int, float)) or z_factor <= 0:
            raise ValueError("z_factor must be a positive number.")

        # The volume is approximated by summing all intensity values (heights)
        # and scaling them by the z_factor. Assuming dx=dy=1 for each pixel.
        volume = np.sum(data.astype(np.float32)) * z_factor
        return VolumeResult(volume=float(volume), units="cubic_pixels")


class ArcLengthStrategy(IAnalysisStrategy):
    """
    Calculates the arc length of a path defined by a series of 2D points.
    """

    def analyze(
        self, data: Union[NDArray[np.float64], List[Tuple[float, float]]], **kwargs: Any
    ) -> ArcLengthResult:
        """
        Computes the arc length of the given path.

        Args:
            data (Union[NDArray[np.float64], List[Tuple[float, float]]]):
                A NumPy array of shape (N, 2) or a list of (x, y) tuples.
            **kwargs: Not used for arc length calculation, but kept for
                      interface consistency.

        Returns:
            ArcLengthResult: An object containing the calculated arc length.
        """
        # The `calculate_arc_length` utility function handles conversion and validation.
        length = calculate_arc_length(data)

        # If data is a numpy array, we can store it directly.
        # If it's a list of tuples, convert to numpy array for consistency.
        path_points_array = (
            np.asarray(data, dtype=np.float64) if isinstance(data, list) else data
        )

        return ArcLengthResult(length=length, path_points=path_points_array)
