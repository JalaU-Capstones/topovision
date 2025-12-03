"""
This module provides utility functions for mathematical calculations,
optimized for performance using NumPy.
"""

from typing import List, Tuple, Union

import numpy as np
from numpy.typing import NDArray


def calculate_arc_length(
    points: Union[NDArray[np.float64], List[Tuple[float, float]]],
) -> float:
    """
    Calculates the arc length of a curve defined by a series of 2D points.

    This function is optimized to use NumPy for fast, vectorized computation.

    Args:
        points: A NumPy array of shape (N, 2) or a list of (x, y) tuples
                representing the points on the curve.

    Returns:
        The total length of the curve as a float.

    Raises:
        ValueError: If the input `points` array has fewer than two points.
    """
    # Convert list to NumPy array if necessary
    points_arr = np.asarray(points, dtype=np.float64)

    if points_arr.ndim != 2 or points_arr.shape[1] != 2:
        raise ValueError("Input `points` must be a 2D array or a list of 2D tuples.")

    if len(points_arr) < 2:
        return 0.0

    # Calculate the differences between consecutive points (dx, dy)
    # `np.diff` computes the difference between adjacent elements
    deltas = np.diff(points_arr, axis=0)

    # Calculate the Euclidean distance for each segment
    # hypot is equivalent to sqrt(x**2 + y**2) but more stable
    segment_lengths = np.hypot(deltas[:, 0], deltas[:, 1])

    # Sum the lengths of all segments to get the total arc length
    total_length = np.sum(segment_lengths)

    return float(total_length)
