#!/usr/bin/env python3
"""
Quick sequence test using existing services to grab a real sequence and export it.
This will help identify any real-world font sizing issues.
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

def create_sample_sequence_from_metadata():
    """Create a sample sequence using realistic data"""
    # Create a realistic 4-beat sequence
    sequence = [
        {
            "beat": "1",
            "red_attributes": {
                "start_loc": "n",
                "end_loc": "s",
                "motion_type": "pro",
                "turns": 0
            },
            "blue_attributes": {
                "start_loc": "s", 
                "end_loc": "n",
                "motion_type": "pro",
                "turns": 0
            },
            "start_position": "alpha",
            "end_position": "alpha",
            "timing": 1.0
        },
        {
            "beat": "2",
            "red_attributes": {
                "start_loc": "s",
                "end_loc": "e", 
                "motion_type": "anti",
                "turns": 1
            },
            "blue_attributes": {
                "start_loc": "n",
                "end_loc": "w",
                "motion_type": "anti", 
                "turns": 1
            },
            "start_position": "alpha",
            "end_position": "beta",
            "timing": 1.0
        },
        {
            "beat": "3",
            "red_attributes": {
                "start_loc": "e",
                "end_loc": "w",
                "motion_type": "pro",
                "turns": 0
            },
            "blue_attributes": {
                "start_loc": "w",
                "end_loc": "e", 
                "motion_type": "pro",
                "turns": 0
            },
            "start_position": "beta",
            "end_position": "gamma",
            "timing": 1.0
        },
        {
            "beat": "4",
            "red_attributes": {
                "start_loc": "w",
                "end_loc": "n",
                "motion_type": "anti",
                "turns": 1
            },
            "blue_attributes": {
                "start_loc": "e",
                "end_loc": "s",
                "motion_type": "anti",
                "turns": 1
            },
            "start_position": "gamma", 
            "end_position": "alpha",
            "timing": 1.0
        }
    ]
    return sequence

def test_realistic_sequence_export():
    """Test export with a realistic sequence"""
    print("=== TESTING REALISTIC SEQUENCE EXPORT ===")
    
    app = QApplication(sys.argv)
    
    # Setup export service
    container = DIContainer()
    register_image_export_services(container)
    export_service = container.resolve(IImageExportService)
    
    # Create realistic sequence
    sequence = create_sample_sequence_from_metadata()
    
    print(f"Created sequence with {len(sequence)} beats")
    print("Sequence details:")
    for i, beat in enumerate(sequence):
        print(f"  Beat {i+1}: {beat['red_attributes']['start_loc']}→{beat['red_attributes']['end_loc']} / {beat['blue_attributes']['start_loc']}→{beat['blue_attributes']['end_loc']}")
    
    # Test different export configurations
    test_configs = [
        {
            "name": "Full Export",
            "options": ImageExportOptions(
                add_word=True,
                add_user_info=True,
                add_difficulty_level=True,
                add_beat_numbers=True,
                add_reversal_symbols=True,
                include_start_position=True,
                user_name="Test User",
                export_date=datetime.now().strftime("%m-%d-%Y"),
                notes="Full export test with all elements"
            ),
            "word": "EXAMPLE"
        },
        {
            "name": "Minimal Export",
            "options": ImageExportOptions(
                add_word=False,
                add_user_info=False,
                add_difficulty_level=False,
                add_beat_numbers=True,
                add_reversal_symbols=False,
                include_start_position=False,
                user_name="",
                export_date="",
                notes=""
            ),
            "word": "MINIMAL"
        },
        {
            "name": "Text Only Export",
            "options": ImageExportOptions(
                add_word=True,
                add_user_info=True,
                add_difficulty_level=False,
                add_beat_numbers=False,
                add_reversal_symbols=False,
                include_start_position=False,
                user_name="Font Test User",
                export_date=datetime.now().strftime("%m-%d-%Y"),
                notes="Testing font sizes and text rendering"
            ),
            "word": "FONTTEST"
        }
    ]
    
    output_dir = Path(__file__).parent / "realistic_sequence_test"
    output_dir.mkdir(exist_ok=True)
    
    for config in test_configs:
        print(f"\n--- {config['name']} ---")
        
        # Create image
        image = export_service.create_sequence_image(
            sequence, 
            config['word'], 
            config['options']
        )
        
        print(f"Image dimensions: {image.width()} x {image.height()}")
        print(f"Additional height top: {config['options'].additional_height_top}")
        print(f"Additional height bottom: {config['options'].additional_height_bottom}")
        
        # Save image
        filename = config['name'].lower().replace(' ', '_') + '.png'
        output_path = output_dir / filename
        success = image.save(str(output_path))
        
        if success:
            print(f"✓ Saved to: {output_path}")
        else:
            print(f"✗ Failed to save image")
    
    print(f"\nAll test images saved to: {output_dir}")
    return True

def compare_beat_sizes():
    """Compare different beat size configurations"""
    print("\n=== COMPARING BEAT SIZE CONFIGURATIONS ===")
    
    # The modern system uses beat_size = 300
    # The legacy system gets beat_size from beat_frame.start_pos_view.beat.width()
    
    modern_beat_size = 300
    print(f"Modern system beat size: {modern_beat_size}px")
    print("Legacy system beat size: Determined from actual beat frame widget")
    print()
    print("Potential issue: If legacy beat frame widgets are smaller than 300px,")
    print("the modern system might be creating larger images with larger fonts.")
    print()
    print("To verify:")
    print("1. Check the actual size of beat widgets in the legacy beat frame")
    print("2. Compare exported image dimensions between legacy and modern")
    print("3. If modern images are larger, fonts will appear larger too")

if __name__ == "__main__":
    print("Quick sequence test for font sizing analysis...")
    print("=" * 60)
    
    try:
        # Test realistic sequence export
        if test_realistic_sequence_export():
            print("\n✓ Realistic sequence export test completed")
        
        # Compare beat size configurations
        compare_beat_sizes()
        
        print("\n" + "=" * 60)
        print("🎯 ANALYSIS COMPLETE!")
        print("\nNext steps to identify font sizing issues:")
        print("1. Open the generated images and visually inspect font sizes")
        print("2. Compare with legacy exports of similar sequences")
        print("3. Check if the issue is font size or overall image scale")
        print("4. Verify beat_size value matches legacy system expectations")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED WITH ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
