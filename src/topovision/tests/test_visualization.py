"""
Unit tests for the visualization module.
"""

import unittest

import numpy as np
from PIL import Image

from topovision.core.models import (
    AnalysisResult,
    ArcLengthResult,
    GradientResult,
    RegionOfInterest,
    VolumeResult,
)
from topovision.visualization.visualizers import HeatmapVisualizer


class TestHeatmapVisualizer(unittest.TestCase):
    """Tests the HeatmapVisualizer functionality."""

    def setUp(self) -> None:
        """Set up the visualizer and test data."""
        self.visualizer = HeatmapVisualizer()
        self.original_image = Image.new("RGB", (200, 150), color="white")

        # Create a sample gradient result
        dz_dx = np.zeros((50, 80), dtype=np.float32)
        dz_dy = np.zeros((50, 80), dtype=np.float32)
        # Create a "hot" area in the center of the gradient
        dz_dx[20:30, 35:45] = 1.0
        dz_dy[20:30, 35:45] = 1.0

        self.gradient_result = GradientResult(dz_dx=dz_dx, dz_dy=dz_dy)
        self.region = RegionOfInterest(x1=50, y1=50, x2=130, y2=100)
        self.analysis_result = AnalysisResult(
            method="gradient", result_data=self.gradient_result, region=self.region
        )

    def test_visualize_output_type(self) -> None:
        """Test that the visualize method returns a PIL Image."""
        visualization = self.visualizer.visualize(
            self.analysis_result, self.original_image
        )
        self.assertIsInstance(visualization, Image.Image)

    def test_visualize_output_size(self) -> None:
        """Test that the output image has the same dimensions as the original."""
        visualization = self.visualizer.visualize(
            self.analysis_result, self.original_image
        )
        self.assertEqual(visualization.size, self.original_image.size)

    def test_visualize_blending(self) -> None:
        """
        Test that the heatmap is blended onto the original image.
        This is a basic check to see if the original image is modified.
        A more advanced test could check pixel values.
        """
        visualization = self.visualizer.visualize(
            self.analysis_result, self.original_image
        )

        # Convert to numpy arrays to compare
        vis_array = np.array(visualization)
        orig_array = np.array(self.original_image)

        # The images should not be identical because of the heatmap overlay
        self.assertFalse(np.array_equal(vis_array, orig_array))

        # Check if the area outside the region of interest remains unchanged
        # Note: This assumes the blending doesn't affect pixels outside the ROI
        top_slice_vis = vis_array[0 : self.region.y1, :]
        top_slice_orig = orig_array[0 : self.region.y1, :]
        self.assertTrue(np.array_equal(top_slice_vis, top_slice_orig))

    def test_invalid_analysis_type(self) -> None:
        """Test that the visualizer handles non-gradient analysis results gracefully."""
        # Create a dummy analysis result that is not a gradient
        non_gradient_result = AnalysisResult(
            method="volume",
            result_data=VolumeResult(
                volume=10.0
            ),  # Placeholder for a non-gradient result
            region=self.region,
        )

        # The visualizer should return the original image unmodified
        visualization = self.visualizer.visualize(
            non_gradient_result, self.original_image
        )
        self.assertIs(visualization, self.original_image)


if __name__ == "__main__":
    unittest.main()
