"""Gradient computation utilities."""

import numpy as np
from numpy.typing import NDArray

from .finite_diff import finite_diff_x, finite_diff_y

def compute_gradient(z: NDArray[np.float64], h: float = 1.0):
    """
    Computes the gradient of a height map z.

    Args:
        z: 2D array representing height values.
        h: spacing step.

    Returns:
        (dzdx, dzdy, magnitude, direction)
    """
    dzdx = finite_diff_x(z, h)
    dzdy = finite_diff_y(z, h)

    magnitude = np.sqrt(dzdx**2 + dzdy**2)
    direction = np.arctan2(dzdy, dzdx)

    return dzdx, dzdy, magnitude, direction