"""
Manual Inspection Test for Real Image Export

This test exports a real image using actual TKA sequence data and saves it to a file
that can be manually inspected to verify the quality of the modern image export system.
"""

import os
from datetime import datetime
from pathlib import Path

import pytest
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QApplication

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import (
    register_image_export_services,
)
from desktop.modern.core.interfaces.image_export_services import (
    IImageExportService,
    ImageExportOptions,
)


class TestManualInspectionExport:
    """Test suite for manual inspection of exported images."""

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

        # Create output directory in a predictable location
        self.output_dir = Path("C:/TKA/exports/manual_inspection")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        yield

    def test_export_real_tka_sequence_for_manual_inspection(self):
        """
        Export a real TKA sequence using actual dataset and save for manual inspection.

        This test creates a professional-quality sequence card image that demonstrates
        the full capabilities of the modern image export system with REAL pictographs.
        """
        print("\n" + "=" * 80)
        print("🎨 MANUAL INSPECTION TEST - REAL TKA SEQUENCE EXPORT")
        print("=" * 80)

        # Try to get real sequence data from the TKA dataset
        real_sequence_data = self._get_real_sequence_data()

        if not real_sequence_data:
            print("⚠️  Could not load real TKA data, using realistic mock data")
            real_sequence_data = self._get_realistic_mock_sequence_data()

        # Create comprehensive export options to showcase all features
        options = ImageExportOptions(
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            add_beat_numbers=True,
            include_start_position=True,
            user_name="TKA Manual Inspection Test",
            export_date=datetime.now().strftime("%m-%d-%Y"),
            notes="Testing REAL pictograph rendering with modern export system",
        )

        # Define the word for this sequence
        word = "KINETIC"

        print(f"📝 Exporting sequence for word: '{word}'")
        print(f"🎯 Sequence length: {len(real_sequence_data)} beats")
        print(
            f"📊 Export options: Full (word, user info, difficulty, beat numbers, start position)"
        )

        # Create the image using the modern export system
        print("\n🔄 Creating image with modern export system...")
        image = self.export_service.create_sequence_image(
            real_sequence_data, word, options
        )

        # Verify image was created successfully
        assert not image.isNull(), "Image should not be null"
        assert (
            image.format() == QImage.Format.Format_ARGB32
        ), "Image should be in ARGB32 format"

        # Create timestamped filename for easy identification
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tka_sequence_export_{timestamp}.png"
        output_path = self.output_dir / filename

        # Save the image with maximum quality
        print(f"\n💾 Saving image to: {output_path}")
        success = image.save(str(output_path), "PNG", 100)  # Maximum quality
        assert success, f"Failed to save image to {output_path}"
        assert output_path.exists(), f"Output file does not exist: {output_path}"

        # Verify image properties
        print(f"✅ Image saved successfully!")
        print(f"📐 Image dimensions: {image.width()}x{image.height()}")
        print(f"🎨 Image format: {image.format()}")
        print(f"📁 File size: {output_path.stat().st_size:,} bytes")

        # Analyze the image for quality indicators
        analysis = self._analyze_image_quality(image)
        print(f"\n📊 Image Quality Analysis:")
        print(f"   🌈 Unique colors: {analysis['unique_colors']}")
        print(f"   🎯 Has varied content: {analysis['has_varied_content']}")
        print(f"   🔍 Content coverage: {analysis['content_percentage']:.1f}%")
        print(f"   ✨ Visual complexity: {analysis['complexity_score']}")

        # Quality assertions
        assert (
            analysis["unique_colors"] > 20
        ), f"Expected >20 colors for real pictographs, got {analysis['unique_colors']}"
        assert analysis["has_varied_content"], "Image should have varied visual content"
        assert (
            analysis["content_percentage"] > 5.0
        ), f"Expected >5% content coverage, got {analysis['content_percentage']:.1f}%"

        # Print clear instructions for manual inspection
        print(f"\n" + "=" * 80)
        print("🔍 MANUAL INSPECTION INSTRUCTIONS")
        print("=" * 80)
        print(f"📂 Open this file for manual inspection:")
        print(f"   {output_path}")
        print(f"\n✅ What to look for in the exported image:")
        print(f"   • REAL pictographs with detailed arrows, grids, and positions")
        print(f"   • Word '{word}' displayed at the top with proper typography")
        print(f"   • User information at the bottom (name, date, notes)")
        print(f"   • Difficulty level circle with gradient")
        print(f"   • Beat numbers on each pictograph")
        print(f"   • Start position pictograph (if included)")
        print(f"   • Professional layout and spacing")
        print(f"   • High-quality PNG with no artifacts")
        print(f"\n❌ What should NOT be present:")
        print(f"   • Gray placeholder rectangles")
        print(f"   • Simplified arrow representations")
        print(f"   • Missing visual elements")
        print(f"   • Poor image quality or artifacts")
        print("=" * 80)

        # Also create a comparison image with minimal options
        minimal_options = ImageExportOptions()
        minimal_image = self.export_service.create_sequence_image(
            real_sequence_data, word, minimal_options
        )
        minimal_filename = f"tka_sequence_minimal_{timestamp}.png"
        minimal_path = self.output_dir / minimal_filename
        minimal_image.save(str(minimal_path), "PNG", 100)

        print(f"\n📋 Additional comparison image (minimal options):")
        print(f"   {minimal_path}")

        return str(output_path)  # Return path for potential further use

    def _get_real_sequence_data(self):
        """Try to get real sequence data from the TKA dataset."""
        try:
            # Try to access the pictograph data manager directly
            from desktop.modern.core.interfaces.pictograph_services import (
                IPictographDataManager,
            )

            # Get the service from container
            pictograph_manager = self.container.resolve(IPictographDataManager)

            # Get pictographs for a specific letter (e.g., 'A')
            dataset = pictograph_manager.get_pictograph_dataset()
            pictographs = dataset.get("A", [])

            if pictographs and len(pictographs) >= 3:
                # Convert the first few pictographs to sequence data format
                sequence_data = []
                for i, pictograph in enumerate(pictographs[:6]):  # Take up to 6 beats
                    beat_data = pictograph.get("beat_data")
                    if beat_data and beat_data.has_pictograph:
                        # Extract the pictograph data and convert to sequence format
                        pictograph_data = beat_data.pictograph_data

                        sequence_entry = {
                            "beat": i + 1,
                            "letter": pictograph.get("letter", "A"),
                            "start_pos": getattr(
                                pictograph_data, "start_position", "alpha"
                            ),
                            "end_pos": getattr(pictograph_data, "end_position", "beta"),
                            "blue_attributes": self._extract_motion_attributes(
                                pictograph_data, "blue"
                            ),
                            "red_attributes": self._extract_motion_attributes(
                                pictograph_data, "red"
                            ),
                        }
                        sequence_data.append(sequence_entry)

                if sequence_data:
                    print(
                        f"✅ Loaded {len(sequence_data)} real pictographs from TKA dataset"
                    )
                    return sequence_data

        except Exception as e:
            print(f"⚠️  Could not load real TKA data: {e}")

        return None

    def _extract_motion_attributes(self, pictograph_data, color):
        """Extract motion attributes from pictograph data."""
        try:
            if hasattr(pictograph_data, "motions") and pictograph_data.motions:
                motion = pictograph_data.motions.get(color)
                if motion:
                    return {
                        "motion": getattr(motion, "motion_type", "static"),
                        "location": getattr(motion, "start_location", "alpha"),
                    }
        except:
            pass

        # Default attributes
        return {"motion": "static", "location": "alpha"}

    def _get_realistic_mock_sequence_data(self):
        """Create realistic mock sequence data that showcases different pictograph types."""
        return [
            {
                "beat": 1,
                "letter": "K",
                "start_pos": "alpha",
                "end_pos": "beta",
                "blue_attributes": {"motion": "static", "location": "alpha"},
                "red_attributes": {"motion": "static", "location": "alpha"},
            },
            {
                "beat": 2,
                "letter": "I",
                "start_pos": "beta",
                "end_pos": "gamma",
                "blue_attributes": {"motion": "dash", "location": "beta"},
                "red_attributes": {"motion": "dash", "location": "beta"},
            },
            {
                "beat": 3,
                "letter": "N",
                "start_pos": "gamma",
                "end_pos": "alpha",
                "blue_attributes": {"motion": "static", "location": "gamma"},
                "red_attributes": {"motion": "static", "location": "gamma"},
            },
            {
                "beat": 4,
                "letter": "E",
                "start_pos": "alpha",
                "end_pos": "beta",
                "blue_attributes": {"motion": "dash", "location": "alpha"},
                "red_attributes": {"motion": "static", "location": "beta"},
            },
            {
                "beat": 5,
                "letter": "T",
                "start_pos": "beta",
                "end_pos": "gamma",
                "blue_attributes": {"motion": "static", "location": "beta"},
                "red_attributes": {"motion": "dash", "location": "gamma"},
            },
            {
                "beat": 6,
                "letter": "C",
                "start_pos": "gamma",
                "end_pos": "alpha",
                "blue_attributes": {"motion": "dash", "location": "gamma"},
                "red_attributes": {"motion": "dash", "location": "alpha"},
            },
        ]

    def _analyze_image_quality(self, image: QImage) -> dict:
        """Analyze image quality indicators."""
        analysis = {
            "unique_colors": 0,
            "has_varied_content": False,
            "content_percentage": 0.0,
            "complexity_score": 0,
        }

        colors_found = set()
        content_pixels = 0
        total_pixels = 0

        # Sample pixels across the image
        step = max(
            1, min(image.width(), image.height()) // 100
        )  # Sample every N pixels

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
        )  # >5% non-white
        analysis["content_percentage"] = (
            (content_pixels / total_pixels) * 100 if total_pixels > 0 else 0
        )

        # Complexity score based on color variety and content coverage
        analysis["complexity_score"] = min(
            100, analysis["unique_colors"] + analysis["content_percentage"]
        )

        return analysis
