"""
Test Modern Image Export System

This script runs a comprehensive test of the modern image export system
to validate that it works correctly before using it for production.
"""

import sys
import tempfile
import json
from pathlib import Path
from datetime import datetime

# Add the modern src directory to the path
modern_src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QImage

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import register_image_export_services
from desktop.modern.core.interfaces.image_export_services import (
    IImageExportService,
    ImageExportOptions
)


def create_test_data(test_dir: Path) -> None:
    """Create test sequence data for validation."""
    print("Creating test data...")
    
    # Create test sequences with different lengths and complexities
    test_sequences = {
        "apple": [
            {
                "sequence": [
                    {"beat": 1, "position": "start", "movement": "basic"},
                    {"beat": 2, "position": "middle", "movement": "turn"},
                    {"beat": 3, "position": "end", "movement": "basic"}
                ],
                "difficulty_level": 2,
                "author": "Test System",
                "creation_date": "2024-01-01"
            },
            {
                "sequence": [
                    {"beat": i, "position": f"apple_pos_{i}", "movement": "complex" if i % 3 == 0 else "basic"}
                    for i in range(1, 9)
                ],
                "difficulty_level": 3,
                "author": "Test System",
                "creation_date": "2024-01-01"
            }
        ],
        "banana": [
            {
                "sequence": [
                    {"beat": i, "position": f"banana_pos_{i}", "movement": "basic"}
                    for i in range(1, 17)
                ],
                "difficulty_level": 4,
                "author": "Test System",
                "creation_date": "2024-01-01"
            }
        ],
        "cherry": [
            {
                "sequence": [
                    {"beat": 1, "position": "simple", "movement": "basic"}
                ],
                "difficulty_level": 1,
                "author": "Test System",
                "creation_date": "2024-01-01"
            }
        ]
    }
    
    # Create directory structure and files
    for word, sequences in test_sequences.items():
        word_dir = test_dir / word
        word_dir.mkdir(parents=True, exist_ok=True)
        
        for i, seq_data in enumerate(sequences):
            seq_length = len(seq_data["sequence"])
            filename = f"{word}_length_{seq_length}"
            
            # Create JSON file
            json_file = word_dir / f"{filename}.json"
            with open(json_file, 'w') as f:
                json.dump(seq_data, f, indent=2)
            
            # Create placeholder PNG file
            png_file = word_dir / f"{filename}.png"
            png_file.touch()
    
    print(f"Created test data in {test_dir}")


def test_single_export(export_service: IImageExportService, export_dir: Path) -> bool:
    """Test exporting a single sequence."""
    print("\n--- Testing Single Export ---")
    
    try:
        # Create test sequence
        sequence_data = [
            {"beat": 1, "position": "start", "movement": "basic"},
            {"beat": 2, "position": "middle", "movement": "turn"},
            {"beat": 3, "position": "end", "movement": "basic"}
        ]
        
        word = "test_single"
        output_path = export_dir / "test_single.png"
        
        options = ImageExportOptions(
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            add_beat_numbers=True,
            user_name="Test User",
            export_date="01-15-2024",
            notes="Single export test"
        )
        
        print(f"Exporting single sequence to {output_path}")
        result = export_service.export_sequence_image(sequence_data, word, output_path, options)
        
        if result.success:
            print("✅ Single export successful")
            
            # Verify the exported image
            image = QImage(str(output_path))
            if image.isNull():
                print("❌ Exported image is invalid")
                return False
            
            print(f"   Image dimensions: {image.width()}x{image.height()}")
            print(f"   Image format: {image.format()}")
            return True
        else:
            print(f"❌ Single export failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Single export error: {e}")
        return False


def test_batch_export(export_service: IImageExportService, test_data_dir: Path, export_dir: Path) -> bool:
    """Test batch export functionality."""
    print("\n--- Testing Batch Export ---")
    
    try:
        options = ImageExportOptions(
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            add_beat_numbers=True,
            add_reversal_symbols=True,
            include_start_position=True,
            user_name="Batch Test User",
            export_date=datetime.now().strftime("%m-%d-%Y"),
            notes="Batch export test"
        )
        
        # Track progress
        progress_updates = []
        def progress_callback(progress):
            progress_updates.append(progress.percentage)
            print(f"   Progress: {progress.percentage:.1f}% - {progress.message}")
        
        print(f"Running batch export from {test_data_dir} to {export_dir}")
        results = export_service.export_all_sequences(
            test_data_dir, export_dir, options, progress_callback
        )
        
        if results["success"]:
            print("✅ Batch export successful")
            print(f"   Total files: {results['total_files']}")
            print(f"   Successful: {results['successful']}")
            print(f"   Failed: {results['failed']}")
            print(f"   Skipped: {results['skipped']}")
            
            # Verify some exported files
            exported_files = list(export_dir.rglob("*.png"))
            print(f"   Found {len(exported_files)} exported images")
            
            if len(exported_files) == 0:
                print("❌ No images were exported")
                return False
            
            # Test a few random images
            for i, image_path in enumerate(exported_files[:3]):
                image = QImage(str(image_path))
                if image.isNull():
                    print(f"❌ Invalid exported image: {image_path}")
                    return False
                print(f"   ✅ Valid image {i+1}: {image_path.name} ({image.width()}x{image.height()})")
            
            return True
        else:
            print(f"❌ Batch export failed")
            return False
            
    except Exception as e:
        print(f"❌ Batch export error: {e}")
        return False


def test_different_options(export_service: IImageExportService, export_dir: Path) -> bool:
    """Test export with different option combinations."""
    print("\n--- Testing Different Options ---")
    
    try:
        sequence_data = [
            {"beat": i, "position": f"pos_{i}", "movement": "basic"}
            for i in range(1, 9)
        ]
        word = "options_test"
        
        # Test different option combinations
        option_sets = [
            ("minimal", ImageExportOptions(
                add_word=False,
                add_user_info=False,
                add_difficulty_level=False,
                add_beat_numbers=False
            )),
            ("standard", ImageExportOptions(
                add_word=True,
                add_user_info=True,
                add_difficulty_level=True,
                add_beat_numbers=True
            )),
            ("full", ImageExportOptions(
                add_word=True,
                add_user_info=True,
                add_difficulty_level=True,
                add_beat_numbers=True,
                add_reversal_symbols=True,
                include_start_position=True,
                user_name="Full Test User",
                notes="Full options test"
            ))
        ]
        
        for option_name, options in option_sets:
            output_path = export_dir / f"options_{option_name}.png"
            
            print(f"   Testing {option_name} options...")
            result = export_service.export_sequence_image(sequence_data, word, output_path, options)
            
            if result.success:
                image = QImage(str(output_path))
                if not image.isNull():
                    print(f"   ✅ {option_name} options: {image.width()}x{image.height()}")
                else:
                    print(f"   ❌ {option_name} options: invalid image")
                    return False
            else:
                print(f"   ❌ {option_name} options: export failed")
                return False
        
        print("✅ All option combinations successful")
        return True
        
    except Exception as e:
        print(f"❌ Options test error: {e}")
        return False


def test_layout_calculations(export_service: IImageExportService) -> bool:
    """Test layout calculations for different sequence lengths."""
    print("\n--- Testing Layout Calculations ---")
    
    try:
        from desktop.modern.core.interfaces.image_export_services import IImageLayoutCalculator
        
        # Get the layout calculator from the DI container
        container = DIContainer()
        register_image_export_services(container)
        layout_calculator = container.resolve(IImageLayoutCalculator)
        
        # Test known layout cases
        test_cases = [
            (1, False, 1, 1),
            (4, False, 2, 2),
            (8, False, 4, 2),
            (16, False, 4, 4),
            (16, True, 5, 4),  # 16 + start position = 17 total
        ]
        
        for num_beats, include_start, expected_cols, expected_rows in test_cases:
            cols, rows = layout_calculator.calculate_layout(num_beats, include_start)
            
            if cols == expected_cols and rows == expected_rows:
                print(f"   ✅ {num_beats} beats (start={include_start}): {cols}x{rows}")
            else:
                print(f"   ❌ {num_beats} beats (start={include_start}): expected {expected_cols}x{expected_rows}, got {cols}x{rows}")
                return False
        
        print("✅ All layout calculations correct")
        return True
        
    except Exception as e:
        print(f"❌ Layout test error: {e}")
        return False


def main():
    """Main test runner."""
    print("=" * 60)
    print("MODERN IMAGE EXPORT SYSTEM TEST")
    print("=" * 60)
    
    # Initialize Qt application
    app = QApplication([])
    
    # Set up dependency injection
    container = DIContainer()
    register_image_export_services(container)
    export_service = container.resolve(IImageExportService)
    
    # Create temporary test environment
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_data_dir = temp_path / "test_data"
        export_dir = temp_path / "exports"
        export_dir.mkdir(parents=True)
        
        # Create test data
        create_test_data(test_data_dir)
        
        # Run tests
        tests = [
            ("Layout Calculations", lambda: test_layout_calculations(export_service)),
            ("Single Export", lambda: test_single_export(export_service, export_dir)),
            ("Different Options", lambda: test_different_options(export_service, export_dir)),
            ("Batch Export", lambda: test_batch_export(export_service, test_data_dir, export_dir)),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                else:
                    print(f"❌ {test_name} FAILED")
            except Exception as e:
                print(f"❌ {test_name} ERROR: {e}")
        
        # Final results
        print("\n" + "=" * 60)
        print("TEST RESULTS")
        print("=" * 60)
        print(f"Passed: {passed}/{total}")
        print(f"Success rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Modern image export system is ready.")
            return True
        else:
            print("❌ Some tests failed. Please review the issues above.")
            return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
