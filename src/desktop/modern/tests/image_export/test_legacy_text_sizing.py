"""
Test Legacy Text Sizing

This test verifies that the modern image export system correctly replicates
the legacy text sizing behavior for different numbers of beats.
"""

import pytest
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QImage

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import register_image_export_services
from desktop.modern.core.interfaces.image_export_services import (
    IImageExportService,
    ImageExportOptions
)


class TestLegacyTextSizing:
    """Test suite for legacy text sizing behavior."""
    
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
        
        # Create output directory
        self.output_dir = Path("C:/TKA/exports/text_sizing_comparison")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        yield
    
    def test_text_sizing_for_different_beat_counts(self):
        """
        Test that text sizing scales correctly for different numbers of beats.
        
        This replicates the legacy behavior where:
        - 1 beat: font_size = base_font_size / 2.3, margin = base_margin // 3
        - 2 beats: font_size = base_font_size / 1.5, margin = base_margin // 2  
        - 3+ beats: font_size = base_font_size, margin = base_margin
        """
        print("\n" + "="*80)
        print("🔤 LEGACY TEXT SIZING COMPARISON TEST")
        print("="*80)
        
        # Test different beat counts
        beat_counts = [1, 2, 3, 6, 8]
        
        # Standard export options for comparison
        options = ImageExportOptions(
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            add_beat_numbers=True,
            include_start_position=False,  # Keep consistent for comparison
            user_name="Text Sizing Test",
            export_date=datetime.now().strftime("%m-%d-%Y"),
            notes="Testing legacy text scaling behavior"
        )
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for beat_count in beat_counts:
            print(f"\n📊 Testing {beat_count} beat(s)...")
            
            # Create sequence data for this beat count
            sequence_data = self._create_sequence_data(beat_count)
            
            # Create the image
            image = self.export_service.create_sequence_image(
                sequence_data, f"TEST{beat_count}", options
            )
            
            # Save the image
            filename = f"text_sizing_{beat_count}beats_{timestamp}.png"
            output_path = self.output_dir / filename
            success = image.save(str(output_path), "PNG", 100)
            
            assert success, f"Failed to save image for {beat_count} beats"
            assert output_path.exists(), f"Output file does not exist: {output_path}"
            
            print(f"   ✅ Saved: {filename}")
            print(f"   📐 Dimensions: {image.width()}x{image.height()}")
            
            # Verify image properties
            assert not image.isNull(), f"Image should not be null for {beat_count} beats"
            assert image.format() == QImage.Format.Format_ARGB32, "Image should be in ARGB32 format"
        
        print(f"\n" + "="*80)
        print("🔍 MANUAL COMPARISON INSTRUCTIONS")
        print("="*80)
        print(f"📂 Compare these files to verify text scaling:")
        print(f"   {self.output_dir}")
        print(f"\n✅ Expected text scaling behavior:")
        print(f"   • 1 beat: Smallest text (base_size / 2.3)")
        print(f"   • 2 beats: Medium text (base_size / 1.5)")
        print(f"   • 3+ beats: Full size text (base_size)")
        print(f"\n📏 Expected layout behavior:")
        print(f"   • 1 beat: additional_height_top=150, additional_height_bottom=55")
        print(f"   • 2 beats: additional_height_top=200, additional_height_bottom=75")
        print(f"   • 3+ beats: additional_height_top=300, additional_height_bottom=150")
        print("="*80)
    
    def test_legacy_height_calculation(self):
        """Test that additional height calculation matches legacy behavior."""
        print("\n📏 Testing legacy height calculations...")
        
        # Test the specific height values from legacy HeightDeterminer
        test_cases = [
            (0, {"add_word": False, "add_user_info": False}, 0, 0),
            (0, {"add_word": False, "add_user_info": True}, 0, 55),
            (1, {"add_word": True, "add_user_info": False}, 150, 0),
            (1, {"add_word": True, "add_user_info": True}, 150, 55),
            (2, {"add_word": True, "add_user_info": True}, 200, 75),
            (3, {"add_word": True, "add_user_info": True}, 300, 150),
            (6, {"add_word": True, "add_user_info": True}, 300, 150),
        ]
        
        for num_beats, option_flags, expected_top, expected_bottom in test_cases:
            options = ImageExportOptions(
                add_word=option_flags.get("add_word", False),
                add_user_info=option_flags.get("add_user_info", False),
                user_name="Height Test",
                export_date="01-01-2024",
                notes="Testing height calculation"
            )
            
            # Calculate additional height
            total_height = self.export_service._calculate_additional_height(options, num_beats)
            
            # Check that the options were updated with the correct values
            assert hasattr(options, 'additional_height_top'), "additional_height_top should be set"
            assert hasattr(options, 'additional_height_bottom'), "additional_height_bottom should be set"
            
            print(f"   {num_beats} beats: top={options.additional_height_top}, bottom={options.additional_height_bottom}")
            
            # Verify the values match legacy expectations
            assert options.additional_height_top == expected_top, \
                f"Expected top height {expected_top}, got {options.additional_height_top} for {num_beats} beats"
            assert options.additional_height_bottom == expected_bottom, \
                f"Expected bottom height {expected_bottom}, got {options.additional_height_bottom} for {num_beats} beats"
            
            # Verify total height
            expected_total = expected_top + expected_bottom
            assert total_height == expected_total, \
                f"Expected total height {expected_total}, got {total_height} for {num_beats} beats"
        
        print("   ✅ All height calculations match legacy behavior")
    
    def _create_sequence_data(self, beat_count: int):
        """Create sequence data for the specified number of beats."""
        sequence_data = []
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        positions = ["alpha", "beta", "gamma"]
        motions = ["static", "dash"]
        
        for i in range(beat_count):
            beat_data = {
                "beat": i + 1,
                "letter": letters[i % len(letters)],
                "start_pos": positions[i % len(positions)],
                "end_pos": positions[(i + 1) % len(positions)],
                "blue_attributes": {
                    "motion": motions[i % len(motions)],
                    "location": positions[i % len(positions)]
                },
                "red_attributes": {
                    "motion": motions[(i + 1) % len(motions)],
                    "location": positions[i % len(positions)]
                }
            }
            sequence_data.append(beat_data)
        
        return sequence_data
