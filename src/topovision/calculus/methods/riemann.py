"""Riemann integration methods for surface area approximation."""

import numpy as np
from topovision.core.interfaces import ITopographicData 

class RiemannVolumeCalculator:
    def __init__(self, scale_xy: float=1.0, scale_z: float=1.0) -> None:
        self.dx = scale_xy
        self.dy = scale_xy
        self.scale_z = scale_z

    def calculate_volume(self, frame_data: ITopographicData, region: tuple=None) -> float:
        matrix = frame_data.processed_matrix

        if region:
            x_min, y_min, x_max, y_max = region

            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = min(frame_data.width, x_max)
            y_max = min(frame_data.height, y_max)

            z_values = matrix[y_min:y_max, x_min:x_max]
        else:
            z_values = matrix

        z_values_float = z_values.astype(np.float64)

        heights = z_values_float * self.scale_z

        area_base = self.dx * self.dy
        total_volume = np.sum(heights) * area_base

        return float(total_volume)