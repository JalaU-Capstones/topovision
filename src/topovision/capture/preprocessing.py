"""Image preprocessing utilities (grayscale, filters)."""

import cv2
import numpy as np
import time


# RGB to gray
def to_gray_luminosity(img: np.ndarray) -> np.ndarray:
    """Gray by luminosity formula."""
    b = img[:, :, 0]
    g = img[:, :, 1]
    r = img[:, :, 2]
    lum = 0.114 * b + 0.587 * g + 0.299 * r
    return lum.astype(np.uint8)


def to_gray_average(img: np.ndarray) -> np.ndarray:
    """Gray by channel average."""
    return img.mean(axis=2).astype(np.uint8)


def to_gray_opencv(img: np.ndarray) -> np.ndarray:
    """Gray using OpenCV conversion."""
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# filtros
def gaussian_blur(img: np.ndarray, ksize: int = 5) -> np.ndarray:
    """Gaussian smoothing."""
    return cv2.GaussianBlur(img, (ksize, ksize), 0)


def median_blur(img: np.ndarray, ksize: int = 5) -> np.ndarray:
    """Median filter for noise removal."""
    return cv2.medianBlur(img, ksize)


def bilateral_filter(
    img: np.ndarray, d=9, sigma_color=75, sigma_space=75
) -> np.ndarray:
    """Bilateral filter: smooth while preserving edges."""
    return cv2.bilateralFilter(img, d, sigma_color, sigma_space)


# rendimiento de filtros


def benchmark_filter(filter_fn, img: np.ndarray, runs: int = 50) -> dict:
    """
    Measure performance of a filter function.
    Returns average time per frame and FPS.
    """
    start = time.perf_counter()

    for _ in range(runs):
        _ = filter_fn(img)

    end = time.perf_counter()
    total = end - start

    time_ms = (total / runs) * 1000
    fps = runs / total if total > 0 else float("inf")

    return {
        "time_per_frame_ms": round(time_ms, 4),
        "fps": round(fps, 2),
        "runs": runs,
    }


