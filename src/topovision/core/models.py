"""Core data models for TopoVision."""

from dataclasses import dataclass
from typing import Optional
import numpy as np
from numpy.typing import NDArray


@dataclass
class FrameData:
    """Represents a single video frame."""

    image: NDArray[np.uint8]
    timestamp: Optional[float] = None


@dataclass
class Region:
    """Represents a rectangular region in a frame."""

    x1: int
    y1: int
    x2: int
    y2: int


@dataclass
class GradientResult:
    """Holds gradient values over a region."""

    dx: NDArray[np.float32]
    dy: NDArray[np.float32]


@dataclass
class Result:
    """Generic calculation result for a region."""

    derivative: Optional[float] = None
    gradient: Optional[GradientResult] = None
    volume: Optional[float] = None
