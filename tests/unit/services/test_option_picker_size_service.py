"""
Unit tests for OptionPickerSizeService.
Tests the platform-agnostic sizing logic extracted from OptionPickerSizeManager.
"""

import unittest
from unittest.mock import Mock, patch

from desktop.modern.application.services.option_picker.option_picker_size_service import (
    OptionPickerSizeService,
)


class TestOptionPickerSizeService(unittest.TestCase):
    """Test suite for OptionPickerSizeService."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock the mw_size_provider dependency
        self.mock_mw_size_provider = Mock()
        self.mock_mw_size_provider.return_value = Mock()
        self.mock_mw_size_provider.return_value.width.return_value = 1200
        self.mock_mw_size_provider.return_value.height.return_value = 800

        self.service = OptionPickerSizeService(self.mock_mw_size_provider)

        # Mock dependencies
        self.mock_scroll_area = Mock()
        self.mock_scroll_area.width.return_value = 800
        self.mock_scroll_area.height.return_value = 600
        self.mock_scroll_area.viewport.return_value.width.return_value = 780

        self.mock_widget_container = Mock()
        self.mock_widget_container.width.return_value = 750
        self.mock_widget_container.height.return_value = 400

        self.mock_content_widget = Mock()
        self.mock_content_widget.width.return_value = 700
        self.mock_content_widget.height.return_value = 350

        self.mock_scroll_bar = Mock()
        self.mock_scroll_bar.width.return_value = 20
        self.mock_scroll_bar.isVisible.return_value = True

    def test_calculate_optimal_width_basic(self):
        """Test basic optimal width calculation."""
        result = self.service.calculate_optimal_width(parent_width=800)

        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)
        self.assertLessEqual(result, 1200)  # Should not exceed main window width

    def test_calculate_optimal_width_with_parent_width(self):
        """Test optimal width calculation with parent width."""
        result = self.service.calculate_optimal_width(parent_width=700)

        self.assertIsInstance(result, int)
        self.assertEqual(result, 700)  # Should use parent width when provided

    def test_calculate_optimal_width_no_parent_width(self):
        """Test optimal width calculation without parent width."""
        result = self.service.calculate_optimal_width()

        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)

    def test_calculate_optimal_width_minimum_enforced(self):
        """Test that minimum width is enforced."""
        # Test with very small parent width
        result = self.service.calculate_optimal_width(parent_width=50)

        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)

    def test_is_width_accurate_basic(self):
        """Test width accuracy validation."""
        # First calculate a width
        optimal_width = self.service.calculate_optimal_width(parent_width=800)

        # Should be accurate for the calculated width
        result = self.service.is_width_accurate(optimal_width)
        self.assertTrue(result)

    def test_is_width_accurate_inaccurate(self):
        """Test width accuracy validation with inaccurate width."""
        # Calculate a width first
        self.service.calculate_optimal_width(parent_width=800)

        # Test with very different width
        result = self.service.is_width_accurate(200)
        self.assertFalse(result)

    def test_should_defer_sizing_basic(self):
        """Test sizing deferral logic."""
        result = self.service.should_defer_sizing()

        self.assertIsInstance(result, bool)

    def test_reset_deferred_count(self):
        """Test resetting deferred count."""
        # Should not raise any exceptions
        try:
            self.service.reset_deferred_count()
        except Exception as e:
            self.fail(f"reset_deferred_count should not raise exception: {e}")

    def test_get_sizing_delay_normal(self):
        """Test getting sizing delay for normal operation."""
        delay = self.service.get_sizing_delay(during_startup=False)

        self.assertIsInstance(delay, int)
        self.assertGreaterEqual(delay, 0)

    def test_get_sizing_delay_startup(self):
        """Test getting sizing delay during startup."""
        delay = self.service.get_sizing_delay(during_startup=True)

        self.assertIsInstance(delay, int)
        self.assertGreaterEqual(delay, 0)

    def test_get_layout_constraints(self):
        """Test layout constraints retrieval."""
        constraints = self.service.get_layout_constraints()

        self.assertIsInstance(constraints, dict)
        # Should contain some constraint information
        self.assertGreater(len(constraints), 0)

    def test_calculate_optimal_width_performance(self):
        """Test that optimal width calculation is performant."""
        import time

        start_time = time.time()
        for _ in range(100):
            self.service.calculate_optimal_width(parent_width=800)
        end_time = time.time()

        # Should complete 100 calculations in under 1 second
        self.assertLess(end_time - start_time, 1.0)


if __name__ == "__main__":
    unittest.main()
