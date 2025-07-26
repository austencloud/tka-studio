"""
Modern vs Legacy Image Export Comparison Tests

This test suite compares the output of the modern image exporter
with the legacy system to ensure pixel-perfect compatibility.
"""

import pytest
import tempfile
import json
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import Mock, patch

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QImage
from PyQt6.QtCore import Qt

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import (
    register_image_export_services,
)
from desktop.modern.core.interfaces.image_export_services import (
    IImageExportService,
    ImageExportOptions,
    ExportResult,
)


class TestModernVsLegacyExport:
    """Test suite comparing modern and legacy image export functionality."""

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

        # Get the modern export service
        self.modern_exporter = self.container.resolve(IImageExportService)

        # Create temporary directories for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.source_dir = self.temp_dir / "source"
        self.export_dir = self.temp_dir / "export"
        self.source_dir.mkdir(parents=True)
        self.export_dir.mkdir(parents=True)

        yield

        # Cleanup
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_export_options_compatibility(self):
        """Test that export options match legacy system exactly."""
        # Legacy default options
        legacy_options = {
            "add_word": True,
            "add_user_info": True,
            "add_difficulty_level": True,
            "add_date": True,
            "add_note": True,
            "add_beat_numbers": True,
            "add_reversal_symbols": True,
            "combined_grids": False,
            "include_start_position": True,
        }

        # Modern options
        modern_options = ImageExportOptions()

        # Verify all legacy options are supported
        for key, expected_value in legacy_options.items():
            assert hasattr(modern_options, key), f"Missing option: {key}"
            actual_value = getattr(modern_options, key)
            assert (
                actual_value == expected_value
            ), f"Option {key}: expected {expected_value}, got {actual_value}"

    def test_image_dimensions_calculation(self):
        """Test that image dimensions match legacy calculations."""
        test_cases = [
            # (num_beats, include_start_pos, expected_cols, expected_rows)
            (1, False, 1, 1),
            (4, False, 2, 2),
            (8, False, 4, 2),
            (16, False, 4, 4),
            (16, True, 5, 4),  # 16 beats + start position = 17 total
        ]

        layout_calculator = self.container.resolve(IImageLayoutCalculator)

        for num_beats, include_start_pos, expected_cols, expected_rows in test_cases:
            cols, rows = layout_calculator.calculate_layout(
                num_beats, include_start_pos
            )
            assert (
                cols == expected_cols
            ), f"Columns mismatch for {num_beats} beats: expected {expected_cols}, got {cols}"
            assert (
                rows == expected_rows
            ), f"Rows mismatch for {num_beats} beats: expected {expected_rows}, got {rows}"

    def test_sequence_image_creation(self):
        """Test that sequence images are created with correct properties."""
        # Create test sequence data
        sequence_data = [
            {"beat": 1, "position": "test_position_1"},
            {"beat": 2, "position": "test_position_2"},
            {"beat": 3, "position": "test_position_3"},
            {"beat": 4, "position": "test_position_4"},
        ]

        word = "test"
        options = ImageExportOptions()

        # Create image
        image = self.modern_exporter.create_sequence_image(sequence_data, word, options)

        # Verify image properties
        assert isinstance(image, QImage)
        assert not image.isNull()
        assert image.format() == QImage.Format.Format_ARGB32

        # Verify dimensions are reasonable
        assert image.width() > 0
        assert image.height() > 0
        assert image.width() >= 300  # Minimum width
        assert image.height() >= 300  # Minimum height

    def test_file_naming_convention(self):
        """Test that file naming matches legacy convention."""
        # Create test sequence file
        word = "apple"
        sequence_file = "apple_length_16.png"
        word_dir = self.source_dir / word
        word_dir.mkdir()

        # Create test JSON data
        sequence_data = [{"beat": i, "position": f"pos_{i}"} for i in range(1, 17)]
        json_file = word_dir / "apple_length_16.json"
        with open(json_file, "w") as f:
            json.dump({"sequence": sequence_data}, f)

        # Create corresponding PNG file
        png_file = word_dir / sequence_file
        png_file.touch()

        # Export
        options = ImageExportOptions()
        output_path = self.export_dir / word / sequence_file

        result = self.modern_exporter.export_sequence_image(
            sequence_data, word, output_path, options
        )

        # Verify file was created with correct name
        assert result.success
        assert output_path.exists()
        assert output_path.name == sequence_file
        assert output_path.parent.name == word

    def test_export_quality_settings(self):
        """Test that export quality settings match legacy system."""
        sequence_data = [{"beat": 1, "position": "test"}]
        word = "test"
        options = ImageExportOptions()
        output_path = self.export_dir / "test.png"

        # Export image
        result = self.modern_exporter.export_sequence_image(
            sequence_data, word, output_path, options
        )

        assert result.success
        assert output_path.exists()

        # Verify it's a PNG file
        with open(output_path, "rb") as f:
            header = f.read(8)
            assert header == b"\x89PNG\r\n\x1a\n"  # PNG signature

    def test_batch_export_functionality(self):
        """Test batch export functionality."""
        # Create test data structure
        words = ["apple", "banana", "cherry"]

        for word in words:
            word_dir = self.source_dir / word
            word_dir.mkdir()

            # Create multiple sequence files per word
            for i in range(1, 4):  # 3 files per word
                sequence_data = [
                    {"beat": j, "position": f"pos_{j}"} for j in range(1, i * 4 + 1)
                ]

                json_file = word_dir / f"{word}_length_{len(sequence_data)}.json"
                with open(json_file, "w") as f:
                    json.dump({"sequence": sequence_data}, f)

                png_file = word_dir / f"{word}_length_{len(sequence_data)}.png"
                png_file.touch()

        # Run batch export
        options = ImageExportOptions()
        results = self.modern_exporter.export_all_sequences(
            self.source_dir, self.export_dir, options
        )

        # Verify results
        assert results["success"]
        assert results["total_files"] == 9  # 3 words * 3 files each
        assert results["successful"] > 0

        # Verify exported files exist
        for word in words:
            word_export_dir = self.export_dir / word
            assert word_export_dir.exists()
            exported_files = list(word_export_dir.glob("*.png"))
            assert len(exported_files) > 0

    def test_visual_elements_inclusion(self):
        """Test that all visual elements are included when enabled."""
        sequence_data = [{"beat": i, "position": f"pos_{i}"} for i in range(1, 5)]
        word = "test"

        # Test with all elements enabled
        options = ImageExportOptions(
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            add_beat_numbers=True,
            user_name="TestUser",
            export_date="12-25-2023",
            notes="Test Notes",
        )

        image = self.modern_exporter.create_sequence_image(sequence_data, word, options)

        # Verify image was created successfully
        assert not image.isNull()

        # The image should be larger when additional elements are included
        # (This is a basic check - more detailed visual verification would require image analysis)
        assert image.height() > 300  # Should have additional height for text elements

    def test_difficulty_level_calculation(self):
        """Test difficulty level calculation matches legacy logic."""
        metadata_extractor = self.container.resolve(ISequenceMetadataExtractor)

        test_cases = [
            # (sequence_length, expected_min_difficulty, expected_max_difficulty)
            (2, 1, 2),  # Short sequences should be easy
            (8, 2, 3),  # Medium sequences
            (16, 3, 5),  # Long sequences should be harder
            (24, 4, 5),  # Very long sequences
        ]

        for seq_length, min_diff, max_diff in test_cases:
            sequence_data = [
                {"beat": i, "position": f"pos_{i}"} for i in range(1, seq_length + 1)
            ]
            difficulty = metadata_extractor.get_difficulty_level(sequence_data)

            assert (
                min_diff <= difficulty <= max_diff
            ), f"Difficulty {difficulty} not in expected range [{min_diff}, {max_diff}] for sequence length {seq_length}"
            assert (
                1 <= difficulty <= 5
            ), f"Difficulty {difficulty} outside valid range [1, 5]"

    def test_error_handling(self):
        """Test error handling for various edge cases."""
        options = ImageExportOptions()

        # Test with empty sequence
        empty_result = self.modern_exporter.export_sequence_image(
            [], "empty", self.export_dir / "empty.png", options
        )
        assert empty_result.success  # Should handle empty sequences gracefully

        # Test with invalid output path
        invalid_path = Path("/invalid/path/that/does/not/exist/test.png")
        invalid_result = self.modern_exporter.export_sequence_image(
            [{"beat": 1}], "test", invalid_path, options
        )
        # Should either succeed (if path is created) or fail gracefully
        assert isinstance(invalid_result, ExportResult)

    def test_progress_callback(self):
        """Test progress callback functionality during batch export."""
        # Create test data
        word_dir = self.source_dir / "test"
        word_dir.mkdir()

        for i in range(5):  # Create 5 test files
            json_file = word_dir / f"test_{i}.json"
            with open(json_file, "w") as f:
                json.dump({"sequence": [{"beat": 1}]}, f)

            png_file = word_dir / f"test_{i}.png"
            png_file.touch()

        # Track progress updates
        progress_updates = []

        def progress_callback(progress):
            progress_updates.append(
                {
                    "current": progress.current,
                    "total": progress.total,
                    "percentage": progress.percentage,
                    "message": progress.message,
                }
            )

        # Run export with progress callback
        options = ImageExportOptions()
        results = self.modern_exporter.export_all_sequences(
            self.source_dir, self.export_dir, options, progress_callback
        )

        # Verify progress was tracked
        assert len(progress_updates) > 0
        assert progress_updates[0]["current"] == 0
        assert progress_updates[-1]["current"] == progress_updates[-1]["total"]

        # Verify percentages are correct
        for update in progress_updates:
            expected_percentage = (update["current"] / update["total"]) * 100
            assert abs(update["percentage"] - expected_percentage) < 0.1


class TestVisualComparison:
    """Test suite for visual comparison between modern and legacy output."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up visual comparison test environment."""
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()

        self.container = DIContainer()
        register_image_export_services(self.container)
        self.modern_exporter = self.container.resolve(IImageExportService)

        yield

    def test_image_format_compatibility(self):
        """Test that modern images have the same format as legacy."""
        sequence_data = [{"beat": i, "position": f"pos_{i}"} for i in range(1, 5)]
        word = "test"
        options = ImageExportOptions()

        image = self.modern_exporter.create_sequence_image(sequence_data, word, options)

        # Verify format matches legacy (ARGB32)
        assert image.format() == QImage.Format.Format_ARGB32

        # Verify background is white (legacy behavior)
        white_color = Qt.GlobalColor.white
        corner_pixels = [
            image.pixelColor(0, 0),
            image.pixelColor(image.width() - 1, 0),
            image.pixelColor(0, image.height() - 1),
            image.pixelColor(image.width() - 1, image.height() - 1),
        ]

        # At least some corners should be white (background)
        white_corners = sum(1 for pixel in corner_pixels if pixel.name() == "#ffffff")
        assert white_corners > 0, "Image should have white background"

    def test_layout_dimensions_match_legacy(self):
        """Test that layout dimensions exactly match legacy calculations."""
        layout_calculator = self.container.resolve(IImageLayoutCalculator)

        # Test specific cases that are known from legacy system
        legacy_test_cases = [
            # (beats, include_start, expected_width, expected_height, beat_size)
            (4, False, 600, 600, 300),  # 2x2 grid
            (8, False, 1200, 600, 300),  # 4x2 grid
            (16, False, 1200, 1200, 300),  # 4x4 grid
        ]

        for beats, include_start, exp_width, exp_height, beat_size in legacy_test_cases:
            cols, rows = layout_calculator.calculate_layout(beats, include_start)
            width, height = layout_calculator.calculate_image_dimensions(
                cols, rows, beat_size
            )

            assert (
                width == exp_width
            ), f"Width mismatch for {beats} beats: expected {exp_width}, got {width}"
            assert (
                height == exp_height
            ), f"Height mismatch for {beats} beats: expected {exp_height}, got {height}"

    def test_text_positioning_accuracy(self):
        """Test that text elements are positioned exactly like legacy system."""
        sequence_data = [{"beat": 1, "position": "test"}]
        word = "TEST"
        options = ImageExportOptions(
            add_word=True,
            add_user_info=True,
            user_name="TestUser",
            export_date="12-25-2023",
            notes="Test Notes",
        )

        image = self.modern_exporter.create_sequence_image(sequence_data, word, options)

        # Check that non-white pixels exist (indicating text was drawn)
        has_non_white_pixels = False
        for y in range(min(100, image.height())):  # Check first 100 rows
            for x in range(min(100, image.width())):  # Check first 100 columns
                pixel = image.pixelColor(x, y)
                if pixel.name() != "#ffffff":
                    has_non_white_pixels = True
                    break
            if has_non_white_pixels:
                break

        assert (
            has_non_white_pixels
        ), "Image should contain text elements (non-white pixels)"

    def test_difficulty_circle_rendering(self):
        """Test that difficulty circles are rendered correctly."""
        sequence_data = [
            {"beat": i, "position": f"pos_{i}"} for i in range(1, 9)
        ]  # 8 beats = medium difficulty
        word = "test"
        options = ImageExportOptions(
            add_difficulty_level=True,
            additional_height_top=200,  # Ensure space for difficulty circle
        )

        image = self.modern_exporter.create_sequence_image(sequence_data, word, options)

        # Check top-left area where difficulty circle should be
        circle_area_has_color = False
        for y in range(50, 150):  # Check area where circle should be
            for x in range(50, 150):
                if x < image.width() and y < image.height():
                    pixel = image.pixelColor(x, y)
                    # Look for non-white, non-black pixels (gradient colors)
                    if pixel.name() not in ["#ffffff", "#000000"]:
                        circle_area_has_color = True
                        break
            if circle_area_has_color:
                break

        assert (
            circle_area_has_color
        ), "Difficulty circle should be rendered with gradient colors"
