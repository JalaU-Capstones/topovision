"""Finite difference methods for partial derivatives."""

import numpy as np
from numpy.typing import NDArray


def finite_diff_x(z: NDArray[np.float64], h: float = 1.0) -> NDArray[np.float64]:
    """
    Computes ∂z/∂x using centered finite differences.

    Args:
        z: 2D array of height values.
        h: step size (default 1 pixel).

    Returns:
        2D array with ∂z/∂x.
    """
    dzdx = np.zeros_like(z, dtype=np.float64)

    dzdx[:, 1:-1] = (z[:, 2:] - z[:, :-2]) / (2 * h)

    dzdx[:, 0] = (z[:, 1] - z[:, 0]) / h
    dzdx[:, -1] = (z[:, -1] - z[:, -2]) / h

    return dzdx


def finite_diff_y(z: NDArray[np.float64], h: float = 1.0) -> NDArray[np.float64]:
    """
    Computes ∂z/∂y using centered finite differences.

    Args:
        z: 2D array of height values.
        h: step size (default 1 pixel).

    Returns:
        2D array with ∂z/∂y.
    """
    dzdy = np.zeros_like(z, dtype=np.float64)

    dzdy[1:-1, :] = (z[2:, :] - z[:-2, :]) / (2 * h)

    dzdy[0, :] = (z[1, :] - z[0, :]) / h
    dzdy[-1, :] = (z[-1, :] - z[-2, :]) / h

    return dzdy