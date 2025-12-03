""" tests for preprocessing images."""

import numpy as np
import cv2
from topovision.capture.preprocessing import (
    to_gray_average,
    to_gray_luminosity,
    to_gray_opencv,
    gaussian_blur,
    median_blur,
    bilateral_filter,
    benchmark_filter,
)


def sample_image():
    """Small BGR test image."""
    return np.array(
        [[[10, 20, 30], [200, 150, 100]], [[50, 60, 70], [0, 255, 128]]], dtype=np.uint8
    )


def test_gray_average():
    img = sample_image()
    gray = to_gray_average(img)
    assert gray.shape == (2, 2)
    assert gray.dtype == np.uint8


def test_gray_luminosity():
    img = sample_image()
    gray = to_gray_luminosity(img)
    assert gray.shape == (2, 2)
    assert gray.dtype == np.uint8


def test_gray_opencv():
    img = sample_image()
    gray = to_gray_opencv(img)
    assert gray.shape == (2, 2)
    assert gray.dtype == np.uint8


def test_gaussian_blur():
    img = to_gray_opencv(sample_image())
    blurred = gaussian_blur(img, ksize=5)
    assert blurred.shape == img.shape


def test_median_blur():
    img = to_gray_opencv(sample_image())
    blurred = median_blur(img, ksize=5)
    assert blurred.shape == img.shape


def test_bilateral_filter():
    img = to_gray_opencv(sample_image())
    filtered = bilateral_filter(img, d=5, sigma_color=50, sigma_space=50)
    assert filtered.shape == img.shape


def test_benchmark():
    img = to_gray_opencv(sample_image())

    stats = benchmark_filter(lambda x: gaussian_blur(x, 5), img, runs=5)

    assert "fps" in stats
    assert "time_per_frame_ms" in stats
    assert stats["runs"] == 5

