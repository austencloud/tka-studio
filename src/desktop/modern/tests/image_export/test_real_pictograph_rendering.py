"""
Test Real Pictograph Rendering in Image Export

This test verifies that the updated image renderer correctly renders
actual pictographs instead of placeholder rectangles.
"""

import pytest
import tempfile
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QImage, QColor
from PyQt6.QtCore import Qt

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import (
    register_image_export_services,
)
from desktop.modern.core.interfaces.image_export_services import (
    IImageExportService,
    IImageRenderer,
    ImageExportOptions,
)


class TestRealPictographRendering:
    """Test suite for real pictograph rendering in image export."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test environment."""
        # Ensure QApplication exists
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()

        # Create DI container and register services
        self.container = DIContainer()
        register_image_export_services(self.container)

        # Get services
        self.export_service = self.container.resolve(IImageExportService)
        self.image_renderer = self.container.resolve(IImageRenderer)

        # Create temporary directory
        self.temp_dir = Path(tempfile.mkdtemp())

        yield

        # Cleanup
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_real_pictograph_rendering(self):
        """Test that real pictographs are rendered instead of placeholders."""
        # Create realistic sequence data with proper pictograph information
        sequence_data = [
            {
                "beat": 1,
                "letter": "A",
                "start_pos": "alpha",
                "end_pos": "beta",
                "blue_attributes": {"motion": "static"},
                "red_attributes": {"motion": "static"},
            },
            {
                "beat": 2,
                "letter": "B",
                "start_pos": "beta",
                "end_pos": "gamma",
                "blue_attributes": {"motion": "dash"},
                "red_attributes": {"motion": "dash"},
            },
            {
                "beat": 3,
                "letter": "C",
                "start_pos": "gamma",
                "end_pos": "alpha",
                "blue_attributes": {"motion": "static"},
                "red_attributes": {"motion": "static"},
            },
        ]

        word = "test_real_pictographs"
        options = ImageExportOptions(
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            add_beat_numbers=True,
            include_start_position=True,
            user_name="Test User",
            export_date="01-01-2024",
            notes="Real pictograph test",
        )

        # Create the image
        image = self.export_service.create_sequence_image(sequence_data, word, options)

        # Verify image was created
        assert not image.isNull()
        assert image.format() == QImage.Format.Format_ARGB32

        # Save for manual inspection
        output_path = self.temp_dir / "test_real_pictographs.png"
        success = image.save(str(output_path), "PNG", 1)
        assert success
        assert output_path.exists()

        # Verify the image has actual content (not just gray rectangles)
        has_varied_colors = self._check_for_varied_colors(image)
        assert (
            has_varied_colors
        ), "Image should have varied colors from real pictographs, not just gray placeholders"

    def test_start_position_rendering(self):
        """Test that start position is rendered correctly."""
        sequence_data = [
            {
                "beat": 1,
                "letter": "A",
                "start_pos": "alpha",
                "end_pos": "beta",
                "blue_attributes": {"motion": "static"},
                "red_attributes": {"motion": "static"},
            }
        ]

        options = ImageExportOptions(include_start_position=True, add_beat_numbers=True)

        # Create image with start position
        image = self.export_service.create_sequence_image(
            sequence_data, "start_test", options
        )

        assert not image.isNull()

        # Save for inspection
        output_path = self.temp_dir / "test_start_position.png"
        image.save(str(output_path), "PNG", 1)

        # The image should be larger (more positions) when start position is included
        # This is a basic check - more detailed verification would require image analysis
        assert image.width() > 300
        assert image.height() > 300

    def test_beat_numbers_overlay(self):
        """Test that beat numbers are properly overlaid on pictographs."""
        sequence_data = [
            {"beat": 1, "letter": "A", "start_pos": "alpha", "end_pos": "beta"},
            {"beat": 2, "letter": "B", "start_pos": "beta", "end_pos": "gamma"},
        ]

        options = ImageExportOptions(
            add_beat_numbers=True, include_start_position=False
        )

        image = self.export_service.create_sequence_image(
            sequence_data, "beat_numbers_test", options
        )

        assert not image.isNull()

        # Save for inspection
        output_path = self.temp_dir / "test_beat_numbers.png"
        image.save(str(output_path), "PNG", 1)

        # Check that there are small white rectangles (beat number backgrounds)
        has_beat_number_backgrounds = self._check_for_beat_number_backgrounds(image)
        assert has_beat_number_backgrounds, "Image should have beat number backgrounds"

    def test_fallback_to_placeholders(self):
        """Test that system falls back to placeholders when pictograph rendering fails."""
        # Create invalid sequence data that should trigger fallbacks
        invalid_sequence_data = [
            {"beat": 1, "invalid_field": "this should cause errors"},
            {"beat": 2, "another_invalid": "field"},
        ]

        options = ImageExportOptions()

        # This should not crash, but fall back to placeholders
        image = self.export_service.create_sequence_image(
            invalid_sequence_data, "fallback_test", options
        )

        assert not image.isNull()

        # Save for inspection
        output_path = self.temp_dir / "test_fallback.png"
        image.save(str(output_path), "PNG", 1)

        # Should have some content (placeholder rectangles)
        has_content = self._check_image_has_content(image)
        assert (
            has_content
        ), "Image should have placeholder content even with invalid data"

    def test_complete_visual_elements(self):
        """Test that all visual elements are rendered together."""
        sequence_data = [
            {
                "beat": 1,
                "letter": "A",
                "start_pos": "alpha",
                "end_pos": "beta",
                "blue_attributes": {"motion": "static"},
                "red_attributes": {"motion": "static"},
            },
            {
                "beat": 2,
                "letter": "B",
                "start_pos": "beta",
                "end_pos": "gamma",
                "blue_attributes": {"motion": "dash"},
                "red_attributes": {"motion": "dash"},
            },
        ]

        options = ImageExportOptions(
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            add_beat_numbers=True,
            add_reversal_symbols=True,
            include_start_position=True,
            user_name="Complete Test User",
            export_date="01-15-2024",
            notes="Complete visual elements test",
        )

        image = self.export_service.create_sequence_image(
            sequence_data, "COMPLETE", options
        )

        assert not image.isNull()

        # Save for inspection
        output_path = self.temp_dir / "test_complete_elements.png"
        image.save(str(output_path), "PNG", 1)

        # Image should be tall enough to include all text elements (updated for legacy sizing)
        assert (
            image.height() > 500
        ), "Image should be tall enough for all visual elements"

        # Should have varied colors from all the different elements
        has_varied_colors = self._check_for_varied_colors(image)
        assert (
            has_varied_colors
        ), "Image should have varied colors from all visual elements"

    def _check_for_varied_colors(self, image: QImage) -> bool:
        """Check if image has varied colors (indicating real content vs gray placeholders)."""
        colors_found = set()

        # Sample pixels across the image
        for y in range(0, image.height(), 50):
            for x in range(0, image.width(), 50):
                if x < image.width() and y < image.height():
                    pixel = image.pixelColor(x, y)
                    colors_found.add(pixel.name())

        # Should have more than just white and light gray
        non_basic_colors = colors_found - {"#ffffff", "#c0c0c0", "#000000"}
        return len(non_basic_colors) > 2

    def _check_for_beat_number_backgrounds(self, image: QImage) -> bool:
        """Check for small white rectangles that indicate beat number backgrounds."""
        # Look for small white areas that could be beat number backgrounds
        white_areas = 0

        for y in range(0, image.height(), 20):
            for x in range(0, image.width(), 20):
                if x < image.width() and y < image.height():
                    pixel = image.pixelColor(x, y)
                    if pixel.name() == "#ffffff":
                        # Check if this is part of a small white area (beat number background)
                        if self._is_small_white_area(image, x, y):
                            white_areas += 1

        return white_areas > 0

    def _is_small_white_area(self, image: QImage, x: int, y: int) -> bool:
        """Check if a pixel is part of a small white area."""
        # Check a small area around the pixel
        white_pixels = 0
        for dy in range(-5, 6):
            for dx in range(-5, 6):
                px, py = x + dx, y + dy
                if 0 <= px < image.width() and 0 <= py < image.height():
                    if image.pixelColor(px, py).name() == "#ffffff":
                        white_pixels += 1

        # If most pixels in the area are white, it's likely a beat number background
        return white_pixels > 50  # More than half of the 11x11 area

    def _check_image_has_content(self, image: QImage) -> bool:
        """Check if image has any content (non-white pixels)."""
        for y in range(0, image.height(), 10):
            for x in range(0, image.width(), 10):
                if x < image.width() and y < image.height():
                    pixel = image.pixelColor(x, y)
                    if pixel.name() != "#ffffff":
                        return True
        return False
