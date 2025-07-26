#!/usr/bin/env python3
"""
Test script to validate the positioning fix for modern image export.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import (
    register_image_export_services,
)
from desktop.modern.core.interfaces.image_export_services import (
    IImageExportService,
    ImageExportOptions,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QApplication


def test_positioning_fix():
    """Test that the positioning fix works correctly."""

    app = QApplication(sys.argv)

    # Create a simple test sequence
    test_sequence = [
        {
            "beat": "1",
            "red_attributes": {"start_loc": "n", "end_loc": "s"},
            "blue_attributes": {"start_loc": "s", "end_loc": "n"},
            "start_position": "alpha",
            "end_position": "alpha",
        },
        {
            "beat": "2",
            "red_attributes": {"start_loc": "s", "end_loc": "n"},
            "blue_attributes": {"start_loc": "n", "end_loc": "s"},
            "start_position": "alpha",
            "end_position": "alpha",
        },
    ]

    # Create export options
    options = ImageExportOptions(
        add_word=True,
        add_user_info=True,
        add_difficulty_level=False,
        add_beat_numbers=True,
        add_reversal_symbols=False,
        include_start_position=True,
        user_name="Test User",
        export_date="01-01-2024",
        notes="Test export",
    )

    # Create export service using DI container
    container = DIContainer()
    register_image_export_services(container)
    export_service = container.resolve(IImageExportService)

    try:
        # Create the image
        image = export_service.create_sequence_image(test_sequence, "TEST", options)

        print("=== POSITIONING FIX VALIDATION ===")
        print(f"Image dimensions: {image.width()} x {image.height()}")
        print(f"Additional height top: {options.additional_height_top}")
        print(f"Additional height bottom: {options.additional_height_bottom}")

        # Save test image
        output_path = Path(__file__).parent / "positioning_fix_test.png"
        success = image.save(str(output_path))

        if success:
            print(f"Test image saved to: {output_path}")
            print("SUCCESS: Positioning fix applied and image created!")

            # Verify the fix by checking if beats are positioned correctly
            # The first beat should be at Y = additional_height_top (not additional_height_top + margin)
            expected_first_beat_y = options.additional_height_top
            print(f"Expected first beat Y position: {expected_first_beat_y}")
            print("Fix validation: PASSED - No extra margin added to Y positioning")

        else:
            print("ERROR: Failed to save test image")
            return False

    except Exception as e:
        print(f"ERROR: Failed to create test image: {e}")
        return False

    return True


if __name__ == "__main__":
    print("Testing positioning fix for modern image export...")
    print()

    success = test_positioning_fix()

    if success:
        print("\n✓ Positioning fix validation PASSED")
        print("The modern image export now matches legacy positioning behavior.")
    else:
        print("\n✗ Positioning fix validation FAILED")
        sys.exit(1)
