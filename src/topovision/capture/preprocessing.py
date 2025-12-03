"""
This module provides image preprocessing utilities, such as filtering,
to improve the quality of frames before analysis.
"""

from abc import ABC, abstractmethod

import cv2
import numpy as np
from numpy.typing import NDArray


class IPreprocessor(ABC):
    """
    Abstract interface for an image pre-processing filter.
    """

    @abstractmethod
    def process(self, image: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """
        Applies a pre-processing step to an image.

        Args:
            image (NDArray[np.uint8]): The input image.

        Returns:
            NDArray[np.uint8]: The processed image.
        """
        raise NotImplementedError


class DenoisingStrategy(IPreprocessor):
    """
    An abstract base class for different denoising strategies.
    """

    pass


class GaussianBlurStrategy(DenoisingStrategy):
    """
    Denoises an image using a Gaussian blur filter.
    This is effective for reducing high-frequency noise.
    """

    def __init__(self, kernel_size: tuple[int, int] = (5, 5)):
        """
        Initializes the preprocessor with a Gaussian blur kernel.

        Args:
            kernel_size (tuple[int, int]): The size of the Gaussian kernel.
                                           Must be a tuple of two positive,
                                           odd integers.
        """
        if not (
            isinstance(kernel_size, tuple)
            and len(kernel_size) == 2
            and all(k > 0 and k % 2 != 0 for k in kernel_size)
        ):
            raise ValueError(
                "kernel_size must be a tuple of two positive, odd integers."
            )
        self.kernel_size = kernel_size

    def process(self, image: NDArray[np.uint8]) -> NDArray[np.uint8]:
        return cv2.GaussianBlur(image, self.kernel_size, 0)


class MedianBlurStrategy(DenoisingStrategy):
    """
    Denoises an image using a median blur filter.
    This is particularly effective against salt-and-pepper noise.
    """

    def __init__(self, kernel_size: int = 5):
        """
        Initializes the preprocessor with a median blur kernel.

        Args:
            kernel_size (int): The size of the median kernel.
                               Must be a positive, odd integer.
        """
        if not (
            isinstance(kernel_size, int) and kernel_size > 0 and kernel_size % 2 != 0
        ):
            raise ValueError("kernel_size must be a positive, odd integer.")
        self.kernel_size = kernel_size

    def process(self, image: NDArray[np.uint8]) -> NDArray[np.uint8]:
        return cv2.medianBlur(image, self.kernel_size)


class ImagePreprocessor:
    """
    A class to handle image preprocessing tasks using a selected strategy.
    """

    def __init__(self, strategy: DenoisingStrategy):
        """
        Initializes the ImagePreprocessor with a specific denoising strategy.

        Args:
            strategy (DenoisingStrategy): The denoising strategy to use.
        """
        if not isinstance(strategy, DenoisingStrategy):
            raise TypeError("The provided strategy is not a valid DenoisingStrategy.")
        self.strategy = strategy

    def denoise(self, frame: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """
        Applies the selected denoising strategy to the image.

        Args:
            frame (NDArray[np.uint8]): The input image frame.

        Returns:
            NDArray[np.uint8]: The denoised image frame.
        """
        return self.strategy.process(frame)
