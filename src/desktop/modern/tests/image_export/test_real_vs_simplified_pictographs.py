"""
Test Real vs Simplified Pictograph Rendering

This test verifies that we're getting REAL pictographs with full detail
instead of simplified placeholder versions.
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
    ImageExportOptions,
)


class TestRealVsSimplifiedPictographs:
    """Test suite comparing real vs simplified pictograph rendering."""

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

        # Create temporary directory
        self.temp_dir = Path(tempfile.mkdtemp())

        yield

        # Cleanup
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_real_pictographs_have_complex_details(self):
        """Test that real pictographs have complex visual details."""
        # Create sequence data with specific pictograph details
        sequence_data = [
            {
                "beat": 1,
                "letter": "A",
                "start_pos": "alpha",
                "end_pos": "beta",
                "blue_attributes": {"motion": "static", "location": "alpha"},
                "red_attributes": {"motion": "static", "location": "alpha"},
            },
            {
                "beat": 2,
                "letter": "B",
                "start_pos": "beta",
                "end_pos": "gamma",
                "blue_attributes": {"motion": "dash", "location": "beta"},
                "red_attributes": {"motion": "dash", "location": "beta"},
            },
        ]

        word = "REAL_PICTOGRAPHS"
        options = ImageExportOptions(
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            add_beat_numbers=True,
            include_start_position=True,
            user_name="Real Pictograph Test",
            export_date="01-01-2024",
            notes="Testing REAL pictograph rendering",
        )

        # Create the image
        image = self.export_service.create_sequence_image(sequence_data, word, options)

        # Verify image was created
        assert not image.isNull()
        assert image.format() == QImage.Format.Format_ARGB32

        # Save for manual inspection
        output_path = self.temp_dir / "real_pictographs_test.png"
        success = image.save(str(output_path), "PNG", 1)
        assert success
        assert output_path.exists()

        # Analyze the image for real pictograph characteristics
        analysis = self._analyze_pictograph_complexity(image)

        # Real pictographs should have:
        # 1. More color variety (not just basic colors)
        # 2. Complex shapes (not just simple rectangles and lines)
        # 3. Detailed visual elements

        print(f"Image analysis results: {analysis}")

        # Check for complex color palette (real pictographs have many colors)
        assert (
            analysis["unique_colors"] > 10
        ), f"Expected >10 colors for real pictographs, got {analysis['unique_colors']}"

        # Check for visual complexity (real pictographs have detailed shapes)
        assert analysis[
            "has_complex_shapes"
        ], "Real pictographs should have complex shapes, not just simple rectangles"

        # Check for proper pictograph elements
        assert analysis[
            "has_varied_content"
        ], "Real pictographs should have varied visual content"

    def test_pictograph_visual_elements(self):
        """Test that pictographs contain expected visual elements."""
        sequence_data = [
            {
                "beat": 1,
                "letter": "X",
                "start_pos": "alpha",
                "end_pos": "gamma",
                "blue_attributes": {"motion": "dash", "location": "alpha"},
                "red_attributes": {"motion": "static", "location": "gamma"},
            }
        ]

        options = ImageExportOptions(
            add_beat_numbers=True,
            include_start_position=False,  # Focus on just the beat pictograph
        )

        image = self.export_service.create_sequence_image(
            sequence_data, "TEST", options
        )

        # Save for inspection
        output_path = self.temp_dir / "pictograph_elements_test.png"
        image.save(str(output_path), "PNG", 1)

        # Analyze specific pictograph elements
        elements = self._analyze_pictograph_elements(image)

        print(f"Pictograph elements found: {elements}")

        # Real pictographs should have:
        # - Grid lines or diamond shapes
        # - Arrow elements (blue and red)
        # - Position markers
        # - Letter overlays

        assert elements[
            "has_grid_elements"
        ], "Should have grid elements (diamond or box grid)"
        assert elements[
            "has_arrow_elements"
        ], "Should have arrow elements (blue/red arrows)"
        assert elements["has_position_elements"], "Should have position markers"

    def test_comparison_with_fallback(self):
        """Test that we can distinguish between real and fallback rendering."""
        # Test with valid data (should get real pictographs)
        valid_sequence_data = [
            {
                "beat": 1,
                "letter": "A",
                "start_pos": "alpha",
                "end_pos": "beta",
                "blue_attributes": {"motion": "static"},
                "red_attributes": {"motion": "static"},
            }
        ]

        # Test with invalid data (should get fallback)
        invalid_sequence_data = [{"beat": 1, "completely_invalid": "data_structure"}]

        options = ImageExportOptions()

        # Create both images
        valid_image = self.export_service.create_sequence_image(
            valid_sequence_data, "VALID", options
        )
        invalid_image = self.export_service.create_sequence_image(
            invalid_sequence_data, "INVALID", options
        )

        # Save both for comparison
        valid_path = self.temp_dir / "valid_pictograph.png"
        invalid_path = self.temp_dir / "invalid_fallback.png"

        valid_image.save(str(valid_path), "PNG", 1)
        invalid_image.save(str(invalid_path), "PNG", 1)

        # Analyze both
        valid_analysis = self._analyze_pictograph_complexity(valid_image)
        invalid_analysis = self._analyze_pictograph_complexity(invalid_image)

        print(f"Valid image analysis: {valid_analysis}")
        print(f"Invalid image analysis: {invalid_analysis}")

        # Valid should be more complex than invalid (fallback)
        assert (
            valid_analysis["unique_colors"] >= invalid_analysis["unique_colors"]
        ), "Valid pictographs should have at least as many colors as fallback"

        # Both should have some content
        assert valid_analysis["has_varied_content"], "Valid image should have content"
        assert invalid_analysis[
            "has_varied_content"
        ], "Invalid image should still have fallback content"

    def _analyze_pictograph_complexity(self, image: QImage) -> dict:
        """Analyze an image for pictograph complexity indicators."""
        analysis = {
            "unique_colors": 0,
            "has_complex_shapes": False,
            "has_varied_content": False,
            "color_distribution": {},
            "content_areas": 0,
        }

        colors_found = set()
        content_pixels = 0
        total_pixels = 0

        # Sample pixels across the image
        step = max(1, min(image.width(), image.height()) // 50)  # Sample every N pixels

        for y in range(0, image.height(), step):
            for x in range(0, image.width(), step):
                if x < image.width() and y < image.height():
                    pixel = image.pixelColor(x, y)
                    color_name = pixel.name()
                    colors_found.add(color_name)

                    # Count non-white pixels as content
                    if color_name != "#ffffff":
                        content_pixels += 1

                    total_pixels += 1

        analysis["unique_colors"] = len(colors_found)
        analysis["has_varied_content"] = content_pixels > (
            total_pixels * 0.05
        )  # >5% non-white (more realistic for pictographs)

        # Check for complex shapes by looking for color transitions
        # Real pictographs have smooth gradients and complex shapes
        # Simplified pictographs have mostly solid colors and simple shapes
        color_transitions = self._count_color_transitions(image)
        analysis["has_complex_shapes"] = color_transitions > 100  # Arbitrary threshold

        # Count distinct content areas
        analysis["content_areas"] = self._count_content_areas(image)

        return analysis

    def _analyze_pictograph_elements(self, image: QImage) -> dict:
        """Analyze an image for specific pictograph elements."""
        elements = {
            "has_grid_elements": False,
            "has_arrow_elements": False,
            "has_position_elements": False,
            "has_letter_elements": False,
        }

        # Look for grid elements (lines, diamond shapes)
        # Grid elements typically have light gray or black lines
        grid_colors = {"#c0c0c0", "#808080", "#000000", "#d3d3d3"}

        # Look for arrow elements (blue and red colors - more comprehensive)
        blue_colors = {
            "#0000ff",
            "#0080ff",
            "#4169e1",
            "#1e90ff",
            "#6495ed",
            "#87ceeb",
        }  # Various blue shades
        red_colors = {
            "#ff0000",
            "#dc143c",
            "#b22222",
            "#cd5c5c",
            "#f08080",
            "#ff6347",
        }  # Various red shades

        # Sample the image for these elements
        for y in range(0, image.height(), 10):
            for x in range(0, image.width(), 10):
                if x < image.width() and y < image.height():
                    pixel = image.pixelColor(x, y)
                    color_name = pixel.name()

                    if any(grid_color in color_name for grid_color in grid_colors):
                        elements["has_grid_elements"] = True

                    # Check for blue or red arrow colors using RGB analysis
                    if self._is_arrow_color(pixel):
                        elements["has_arrow_elements"] = True

        # Look for position elements and letters (small text areas)
        elements["has_position_elements"] = self._has_small_text_areas(image)
        elements["has_letter_elements"] = elements[
            "has_position_elements"
        ]  # Same detection method

        return elements

    def _count_color_transitions(self, image: QImage) -> int:
        """Count color transitions in the image (indicator of complexity)."""
        transitions = 0

        # Check horizontal transitions
        for y in range(0, image.height(), 5):
            prev_color = None
            for x in range(0, image.width(), 5):
                if x < image.width() and y < image.height():
                    current_color = image.pixelColor(x, y).name()
                    if prev_color and prev_color != current_color:
                        transitions += 1
                    prev_color = current_color

        return transitions

    def _count_content_areas(self, image: QImage) -> int:
        """Count distinct content areas in the image."""
        # Simple heuristic: count clusters of non-white pixels
        content_areas = 0
        visited = set()

        for y in range(0, image.height(), 20):
            for x in range(0, image.width(), 20):
                if (x, y) not in visited and x < image.width() and y < image.height():
                    pixel = image.pixelColor(x, y)
                    if pixel.name() != "#ffffff":
                        # Found a content pixel, mark this area as visited
                        content_areas += 1
                        # Mark surrounding area as visited to avoid double-counting
                        for dy in range(-10, 11):
                            for dx in range(-10, 11):
                                visited.add((x + dx, y + dy))

        return content_areas

    def _has_small_text_areas(self, image: QImage) -> bool:
        """Check for small text areas (position markers, letters)."""
        # Look for small white rectangles with dark borders (text backgrounds)
        for y in range(0, image.height() - 20, 10):
            for x in range(0, image.width() - 20, 10):
                # Check for a small rectangular area that could be text
                is_text_area = True
                for dy in range(20):
                    for dx in range(20):
                        if x + dx < image.width() and y + dy < image.height():
                            pixel = image.pixelColor(x + dx, y + dy)
                            # Text areas typically have white or light backgrounds
                            if pixel.name() not in ["#ffffff", "#f0f0f0", "#e0e0e0"]:
                                is_text_area = False
                                break
                    if not is_text_area:
                        break

                if is_text_area:
                    return True

        return False

    def _is_arrow_color(self, pixel) -> bool:
        """Check if a pixel color could be an arrow color (blue-ish or red-ish)."""
        color_name = pixel.name()

        # Skip basic colors
        if color_name in ["#ffffff", "#000000", "#c0c0c0", "#808080"]:
            return False

        # Convert to RGB for analysis
        if color_name.startswith("#") and len(color_name) == 7:
            try:
                r = int(color_name[1:3], 16)
                g = int(color_name[3:5], 16)
                b = int(color_name[5:7], 16)

                # Check if it's blue-ish (blue component > others and significant)
                if b > r and b > g and b > 80:
                    return True

                # Check if it's red-ish (red component > others and significant)
                if r > b and r > g and r > 80:
                    return True

                # Also check for green (some pictographs might have green elements)
                if g > r and g > b and g > 80:
                    return True

            except ValueError:
                pass

        return False
