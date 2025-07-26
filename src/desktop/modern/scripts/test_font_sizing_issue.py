#!/usr/bin/env python3
"""
Test script to demonstrate font sizing discrepancies between legacy and modern image export.

This script will create test images with different sequence lengths to show how
font sizes should scale based on the number of beats.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QImage
from PyQt6.QtCore import Qt

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import register_image_export_services
from desktop.modern.core.interfaces.image_export_services import (
    IImageExportService,
    ImageExportOptions
)
from datetime import datetime

def create_test_sequence(num_beats):
    """Create a test sequence with the specified number of beats"""
    sequence = []
    for i in range(num_beats):
        beat = {
            "beat": str(i + 1),
            "red_attributes": {"start_loc": "n", "end_loc": "s"},
            "blue_attributes": {"start_loc": "s", "end_loc": "n"},
            "start_position": "alpha",
            "end_position": "alpha"
        }
        sequence.append(beat)
    return sequence

def test_font_scaling_by_sequence_length():
    """Test how font sizes should scale based on sequence length"""
    print("=== TESTING FONT SCALING BY SEQUENCE LENGTH ===")
    
    app = QApplication(sys.argv)
    
    # Setup export service
    container = DIContainer()
    register_image_export_services(container)
    export_service = container.resolve(IImageExportService)
    
    # Test different sequence lengths
    test_lengths = [1, 2, 4, 8, 16]
    
    output_dir = Path(__file__).parent / "font_sizing_test"
    output_dir.mkdir(exist_ok=True)
    
    print("Creating test images with different sequence lengths...")
    print("Expected behavior: Fonts should get smaller as sequence length increases")
    print()
    
    for num_beats in test_lengths:
        print(f"Testing {num_beats} beat(s)...")
        
        # Create test sequence
        sequence = create_test_sequence(num_beats)
        
        # Create export options with text elements
        options = ImageExportOptions(
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            add_beat_numbers=True,
            add_reversal_symbols=True,
            include_start_position=True,
            user_name="Font Test User",
            export_date=datetime.now().strftime("%m-%d-%Y"),
            notes="Testing font scaling behavior"
        )
        
        # Create image
        image = export_service.create_sequence_image(sequence, f"TEST{num_beats}", options)
        
        print(f"  Image dimensions: {image.width()} x {image.height()}")
        print(f"  Additional height top: {options.additional_height_top}")
        print(f"  Additional height bottom: {options.additional_height_bottom}")
        
        # Save image
        output_path = output_dir / f"font_test_{num_beats}beats.png"
        success = image.save(str(output_path))
        
        if success:
            print(f"  ✓ Saved to: {output_path}")
        else:
            print(f"  ✗ Failed to save image")
        
        print()
    
    print("Font scaling analysis:")
    print("1 beat:  Should have SMALLEST fonts (base_font_size / 2.3)")
    print("2 beats: Should have MEDIUM fonts (base_font_size / 1.5)")
    print("3+ beats: Should have LARGEST fonts (base_font_size)")
    print()
    print("If fonts look the same size across all images, there's a scaling issue!")

def demonstrate_legacy_vs_modern_font_logic():
    """Demonstrate the difference between legacy and modern font calculations"""
    print("=== LEGACY VS MODERN FONT CALCULATION COMPARISON ===")
    
    # Legacy font sizes (from legacy code)
    legacy_word_font_base = 175  # Georgia, 175pt
    legacy_user_info_font_base = 50  # Georgia, 50pt
    
    # Modern font sizes (should be the same)
    modern_word_font_base = 175
    modern_user_info_font_base = 50
    
    print(f"Base font sizes:")
    print(f"  Word font: {legacy_word_font_base}pt (both legacy and modern)")
    print(f"  User info font: {legacy_user_info_font_base}pt (both legacy and modern)")
    print()
    
    # Test different beat counts
    beat_counts = [1, 2, 4]
    beat_scale = 1.0  # This should be the same in both systems
    
    print("Font scaling by beat count (legacy logic):")
    for num_beats in beat_counts:
        print(f"\n{num_beats} beat(s):")
        
        # Legacy calculation for word font
        if num_beats <= 1:
            word_font_size = max(1, int(legacy_word_font_base / 2.3))
        elif num_beats == 2:
            word_font_size = max(1, int(legacy_word_font_base / 1.5))
        else:
            word_font_size = legacy_word_font_base
        
        word_font_size_scaled = max(1, int(word_font_size * beat_scale))
        
        # Legacy calculation for user info font
        if num_beats <= 1:
            user_info_font_size = max(1, int(legacy_user_info_font_base / 2.3))
        elif num_beats == 2:
            user_info_font_size = max(1, int(legacy_user_info_font_base / 1.5))
        else:
            user_info_font_size = legacy_user_info_font_base
        
        user_info_font_size_scaled = max(1, int(user_info_font_size * beat_scale))
        
        print(f"  Word font: {legacy_word_font_base} → {word_font_size} → {word_font_size_scaled}pt")
        print(f"  User info font: {legacy_user_info_font_base} → {user_info_font_size} → {user_info_font_size_scaled}pt")

def create_quick_test_sequence():
    """Create a quick test sequence for immediate visual inspection"""
    print("=== CREATING QUICK TEST SEQUENCE ===")
    
    app = QApplication(sys.argv)
    
    # Setup export service
    container = DIContainer()
    register_image_export_services(container)
    export_service = container.resolve(IImageExportService)
    
    # Create a 4-beat sequence (common test case)
    sequence = create_test_sequence(4)
    
    # Create export options
    options = ImageExportOptions(
        add_word=True,
        add_user_info=True,
        add_difficulty_level=True,
        add_beat_numbers=True,
        add_reversal_symbols=True,
        include_start_position=True,
        user_name="Quick Test",
        export_date=datetime.now().strftime("%m-%d-%Y"),
        notes="Quick visual test"
    )
    
    # Create image
    image = export_service.create_sequence_image(sequence, "QUICKTEST", options)
    
    # Save image
    output_path = Path(__file__).parent / "quick_test_sequence.png"
    success = image.save(str(output_path))
    
    if success:
        print(f"✓ Quick test image saved to: {output_path}")
        print(f"  Dimensions: {image.width()} x {image.height()}")
        print(f"  Additional height top: {options.additional_height_top}")
        print(f"  Additional height bottom: {options.additional_height_bottom}")
        print("  Open this image to visually inspect font sizes!")
    else:
        print("✗ Failed to save quick test image")

if __name__ == "__main__":
    print("Testing font sizing in modern image export...")
    print("=" * 60)
    
    try:
        # Test font scaling by sequence length
        test_font_scaling_by_sequence_length()
        print()
        
        # Demonstrate calculation differences
        demonstrate_legacy_vs_modern_font_logic()
        print()
        
        # Create quick test for visual inspection
        create_quick_test_sequence()
        
        print("\n" + "=" * 60)
        print("Font sizing test complete!")
        print("\nTo identify issues:")
        print("1. Check if fonts look the same size across different beat counts")
        print("2. Compare with legacy exports if available")
        print("3. Verify that 1-beat sequences have smallest fonts")
        print("4. Verify that 3+ beat sequences have largest fonts")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED WITH ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
