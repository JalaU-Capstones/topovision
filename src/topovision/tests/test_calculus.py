"""
Unit tests for the calculus module and its analysis strategies.
"""

import unittest

import numpy as np

from topovision.calculus.calculus_module import AnalysisContext
from topovision.calculus.strategies import (
    ArcLengthStrategy,
    GradientStrategy,
    VolumeStrategy,
)
from topovision.core.models import ArcLengthResult, GradientResult, VolumeResult


class TestCalculusModule(unittest.TestCase):
    """Tests the CalculusModule and its strategy-switching capabilities."""

    def setUp(self) -> None:
        """Set up the calculus module for each test."""
        self.calculus_module = AnalysisContext()
        self.data = np.array([[1, 2], [3, 4]], dtype=np.uint8)

    def test_set_and_get_strategy(self) -> None:
        """Test that strategies can be set and retrieved correctly."""
        self.calculus_module.set_strategy("gradient")
        self.assertIsInstance(self.calculus_module.strategy, GradientStrategy)

        self.calculus_module.set_strategy("volume")
        self.assertIsInstance(self.calculus_module.strategy, VolumeStrategy)

        self.calculus_module.set_strategy("arc_length")
        self.assertIsInstance(self.calculus_module.strategy, ArcLengthStrategy)

    def test_invalid_strategy(self) -> None:
        """Test that setting an invalid strategy raises an error."""
        with self.assertRaises(ValueError):
            self.calculus_module.set_strategy("invalid_strategy")

    def test_calculation_delegation(self) -> None:
        """
        Test that the calculate method correctly delegates to the current
        strategy.
        """
        # Test with GradientStrategy
        self.calculus_module.set_strategy("gradient")
        result = self.calculus_module.calculate(self.data, z_factor=1.0)
        self.assertIsInstance(result, GradientResult)

        # Test with VolumeStrategy
        self.calculus_module.set_strategy("volume")
        result = self.calculus_module.calculate(self.data, z_factor=1.0)
        self.assertIsInstance(result, VolumeResult)

        # Test with ArcLengthStrategy
        self.calculus_module.set_strategy("arc_length")
        points = np.array([[0, 0], [1, 1]])
        result = self.calculus_module.calculate(points)
        self.assertIsInstance(result, ArcLengthResult)


class TestAnalysisStrategies(unittest.TestCase):
    """Tests the individual analysis strategies."""

    def test_gradient_strategy(self) -> None:
        """Test the gradient calculation."""
        strategy = GradientStrategy()
        # Create a horizontal ramp where values change across columns but are
        # constant across rows
        data = np.tile(np.linspace(0, 255, 10, dtype=np.uint8), (10, 1))
        result = strategy.analyze(data, z_factor=1.0)

        self.assertIsInstance(result, GradientResult)
        self.assertEqual(result.dz_dx.shape, (10, 10))
        self.assertEqual(result.dz_dy.shape, (10, 10))
        # For a horizontal ramp, dz_dy should be close to zero
        self.assertTrue(np.allclose(result.dz_dy, 0, atol=1e-5))
        # And dz_dx should be non-zero
        self.assertTrue(np.mean(np.abs(result.dz_dx)) > 0)

    def test_volume_strategy(self) -> None:
        """Test the volume calculation (Riemann sum)."""
        strategy = VolumeStrategy()
        # A flat plane of height 10
        data = np.full((5, 5), 10, dtype=np.uint8)
        result = strategy.analyze(data, z_factor=1.0)

        self.assertIsInstance(result, VolumeResult)
        # Volume should be width * height * average_intensity
        self.assertAlmostEqual(result.volume, 5 * 5 * 10)

        # Test with a Z-factor
        result_z_factor = strategy.analyze(data, z_factor=2.0)
        self.assertAlmostEqual(result_z_factor.volume, 5 * 5 * 10 * 2.0)

    def test_arc_length_strategy(self) -> None:
        """Test the arc length calculation."""
        strategy = ArcLengthStrategy()
        # A simple path along a straight line y=x
        points = np.array([[i, i] for i in range(10)])
        result = strategy.analyze(points)

        self.assertIsInstance(result, ArcLengthResult)
        # The length of the diagonal of a 9x9 square
        self.assertAlmostEqual(result.length, 9 * np.sqrt(2))

        # A path along a horizontal line
        points_horiz = np.array([[i, 5] for i in range(10)])
        result_horiz = strategy.analyze(points_horiz)
        self.assertAlmostEqual(result_horiz.length, 9.0)


if __name__ == "__main__":
    unittest.main()
