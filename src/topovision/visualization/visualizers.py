"""
Visualizers for TopoVision.

This module provides concrete implementations of the IVisualizer interface
to render analysis results, such as heatmaps, onto original images.
"""

import numpy as np
from numpy.typing import NDArray
from PIL import Image

from topovision.core.interfaces import IVisualizer
from topovision.core.models import AnalysisResult, GradientResult, RegionOfInterest
from topovision.gui.i18n import DEFAULT_LANG

from .heatmap import generate_heatmap
from .overlay import overlay_image


class HeatmapVisualizer(IVisualizer):
    """
    Visualizes gradient analysis results as a heatmap overlaid on an image.
    """

    def visualize(
        self,
        analysis_result: AnalysisResult,
        original_image: Image.Image,
    ) -> Image.Image:
        """
        Creates a heatmap visualization of the gradient analysis result
        and overlays it onto the original image.

        Args:
            analysis_result (AnalysisResult): The result of the analysis,
                                              expected to contain GradientResult.
            original_image (Image.Image): The original image (PIL Image)
                                          on which to overlay the visualization.

        Returns:
            Image.Image: The image with the heatmap visualization overlaid.

        Raises:
            ValueError: If the analysis_result is not a GradientResult.
        """
        if not isinstance(analysis_result.result_data, GradientResult):
            # For now, if it's not a gradient, return the original image.
            # Future visualizers could handle other types.
            return original_image
            # raise ValueError("HeatmapVisualizer can only visualize GradientResult.")

        gradient_data: GradientResult = analysis_result.result_data
        region: RegionOfInterest = analysis_result.region

        # Calculate magnitude from dz_dx and dz_dy
        magnitude = np.sqrt(gradient_data.dz_dx**2 + gradient_data.dz_dy**2)

        # Generate the heatmap from the magnitude data
        # The heatmap is generated for the size of the region data
        # Pass label_key and lang for i18n
        heatmap_pil = generate_heatmap(
            magnitude,
            cmap="plasma",
            label_key="gradient_magnitude_label",
            lang=DEFAULT_LANG,
        )

        # Resize heatmap to match the selected region on the original image
        # The region coordinates are relative to the original image
        x1, y1, x2, y2 = region.x1, region.y1, region.x2, region.y2

        # Ensure target dimensions are positive
        target_width = max(1, x2 - x1)
        target_height = max(1, y2 - y1)

        heatmap_resized = heatmap_pil.resize(
            (target_width, target_height), Image.Resampling.LANCZOS
        )

        # Make the heatmap semi-transparent for overlay
        heatmap_resized.putalpha(128)

        # Overlay the heatmap onto the original image at the specified region
        return overlay_image(original_image, heatmap_resized, (x1, y1))
