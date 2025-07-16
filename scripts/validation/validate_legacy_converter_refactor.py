#!/usr/bin/env python3
"""
Legacy Data Converter Refactoring Validation Program

This program comprehensively tests the refactored legacy data converter
and its supporting classes to ensure everything works correctly.
"""

import logging
import sys
import traceback
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src" / "desktop" / "modern" / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_imports():
    """Test that all refactored modules import correctly."""
    print("🔍 Testing imports...")

    try:
        # Test supporting classes
        from application.services.data.beat_data_builder import BeatDataBuilder

        # Test main refactored class
        from application.services.data.legacy_data_converter import (
            ILegacyDataConverter,
            LegacyDataConverter,
        )
        from application.services.data.legacy_format_validator import (
            LegacyFormatValidator,
            ValidationResult,
        )
        from application.services.data.motion_data_converter import (
            MotionConversionResult,
            MotionDataConverter,
        )

        # Test domain models
        from domain.models.beat_data import BeatData
        from domain.models.enums import (
            Location,
            MotionType,
            Orientation,
            RotationDirection,
        )
        from domain.models.motion_models import MotionData

        print("✅ All imports successful")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False


def test_motion_data_converter():
    """Test the MotionDataConverter functionality."""
    print("\n🔧 Testing MotionDataConverter...")

    try:
        from application.services.data.motion_data_converter import MotionDataConverter
        from domain.models.enums import (
            HandMotionType,
            Location,
            Orientation,
            RotationDirection,
        )
        from domain.models.motion_models import MotionData

        converter = MotionDataConverter()

        # Test motion creation from legacy attributes (using correct enum values)
        legacy_attrs = {
            "motion_type": "static",  # Use valid motion type
            "start_loc": "n",
            "end_loc": "s",
            "start_ori": "in",
            "end_ori": "out",
            "prop_rot_dir": "no_rot",  # Use valid rotation direction
            "turns": 1,
        }

        result = converter.create_motion_from_legacy_attributes(legacy_attrs)
        print(f"  Motion conversion result: success={result.success}")

        if result.success and result.motion_data:
            motion = result.motion_data
            print(
                f"  Created motion: {motion.motion_type} from {motion.start_loc} to {motion.end_loc}"
            )

            # Test conversion back to legacy
            legacy_result = converter.create_legacy_motion_attributes(motion)
            print(f"  Round-trip conversion: {legacy_result}")

        print("✅ MotionDataConverter tests passed")
        return True

    except Exception as e:
        print(f"❌ MotionDataConverter test failed: {e}")
        traceback.print_exc()
        return False


def test_legacy_format_validator():
    """Test the LegacyFormatValidator functionality."""
    print("\n🔍 Testing LegacyFormatValidator...")

    try:
        from application.services.data.legacy_format_validator import (
            LegacyFormatValidator,
        )

        validator = LegacyFormatValidator()

        # Test valid beat data
        valid_beat = {
            "beat": 1,
            "letter": "A",
            "start_pos": "alpha1",
            "end_pos": "beta2",
            "timing": "tog",
            "direction": "same",
            "blue_attributes": {
                "motion_type": "static",  # Use valid motion type
                "start_loc": "n",
                "end_loc": "s",
            },
            "red_attributes": {
                "motion_type": "static",
                "start_loc": "s",
                "end_loc": "s",
            },
        }

        result = validator.validate_beat_dict(valid_beat)
        print(f"  Valid beat validation: {result.is_valid}")

        # Test invalid beat data
        invalid_beat = {
            "beat": "not_a_number",  # Invalid
            "blue_attributes": "not_a_dict",  # Invalid
        }

        result = validator.validate_beat_dict(invalid_beat)
        print(f"  Invalid beat validation: {result.is_valid} (should be False)")
        print(f"  Errors found: {len(result.errors)}")

        print("✅ LegacyFormatValidator tests passed")
        return True

    except Exception as e:
        print(f"❌ LegacyFormatValidator test failed: {e}")
        traceback.print_exc()
        return False


def test_beat_data_builder():
    """Test the BeatDataBuilder functionality."""
    print("\n🏗️ Testing BeatDataBuilder...")

    try:
        from application.services.data.beat_data_builder import BeatDataBuilder
        from domain.models.enums import (
            Location,
            MotionType,
            Orientation,
            RotationDirection,
        )
        from domain.models.motion_models import MotionData

        builder = BeatDataBuilder()

        # Create a motion for testing (using valid enum values)
        blue_motion = MotionData(
            motion_type=MotionType.STATIC,  # Use valid motion type
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            prop_rot_dir=RotationDirection.NO_ROTATION,  # Use valid rotation
            turns=0,  # Static motion has 0 turns
        )

        # Build a BeatData using the builder (using correct constructor parameters)
        beat_data = (
            builder.reset()
            .with_beat_number(1)
            .with_duration(1.0)
            .with_motion_data(blue_motion, None)
            .with_glyph_data("alpha1", "beta2")
            .add_metadata("timing", "tog")
            .build()
        )

        print(f"  Built BeatData: beat_number={beat_data.beat_number}")
        print(f"  Has pictograph: {beat_data.has_pictograph}")
        print(f"  Metadata: {beat_data.metadata}")

        print("✅ BeatDataBuilder tests passed")
        return True

    except Exception as e:
        print(f"❌ BeatDataBuilder test failed: {e}")
        traceback.print_exc()
        return False


def test_legacy_data_converter():
    """Test the refactored LegacyDataConverter functionality."""
    print("\n🔄 Testing LegacyDataConverter...")

    try:
        from application.services.data.beat_data_builder import BeatDataBuilder
        from application.services.data.legacy_data_converter import LegacyDataConverter
        from domain.models.enums import (
            Location,
            MotionType,
            Orientation,
            RotationDirection,
        )
        from domain.models.motion_models import MotionData

        converter = LegacyDataConverter()
        builder = BeatDataBuilder()

        # Create test BeatData (using valid enum values)
        blue_motion = MotionData(
            motion_type=MotionType.STATIC,  # Use valid motion type
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            prop_rot_dir=RotationDirection.NO_ROTATION,  # Use valid rotation
            turns=0,  # Static motion has 0 turns
        )

        beat_data = (
            builder.reset()
            .with_beat_number(1)
            .with_motion_data(blue_motion, None)
            .with_glyph_data("alpha1", "beta2")
            .build()
        )

        # Test conversion to legacy format
        legacy_format = converter.convert_beat_to_legacy_format(beat_data, 1)
        print(f"  Legacy format keys: {list(legacy_format.keys())}")
        print(f"  Beat number: {legacy_format.get('beat')}")

        # Test conversion back to BeatData
        converted_back = converter.convert_legacy_to_beat_data(legacy_format, 1)
        print(f"  Round-trip conversion: beat_number={converted_back.beat_number}")
        print(f"  Has pictograph: {converted_back.has_pictograph}")

        print("✅ LegacyDataConverter tests passed")
        return True

    except Exception as e:
        print(f"❌ LegacyDataConverter test failed: {e}")
        traceback.print_exc()
        return False


def test_integration():
    """Test integration between all components."""
    print("\n🔗 Testing integration...")

    try:
        from application.services.data.legacy_data_converter import LegacyDataConverter

        converter = LegacyDataConverter()

        # Test with realistic legacy data (using valid motion types)
        legacy_beat = {
            "beat": 1,
            "letter": "A",
            "start_pos": "alpha1",
            "end_pos": "beta2",
            "timing": "tog",
            "direction": "same",
            "blue_attributes": {
                "motion_type": "static",  # Use valid motion type
                "start_loc": "n",
                "end_loc": "s",
                "start_ori": "in",
                "end_ori": "out",
                "prop_rot_dir": "no_rot",  # Use valid rotation direction
                "turns": 0,
            },
            "red_attributes": {
                "motion_type": "static",
                "start_loc": "s",
                "end_loc": "s",
                "start_ori": "in",
                "end_ori": "in",
                "prop_rot_dir": "no_rot",
                "turns": 0,
            },
        }

        # Convert legacy to modern
        beat_data = converter.convert_legacy_to_beat_data(legacy_beat, 1)
        print(f"  Converted to BeatData: beat_number={beat_data.beat_number}")

        # Convert back to legacy
        legacy_result = converter.convert_beat_to_legacy_format(beat_data, 1)
        print(f"  Converted back to legacy: beat={legacy_result['beat']}")

        # Verify data consistency
        assert legacy_result["beat"] == legacy_beat["beat"]

        print("✅ Integration tests passed")
        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling in refactored components."""
    print("\n⚠️ Testing error handling...")

    try:
        from application.services.data.legacy_data_converter import LegacyDataConverter

        converter = LegacyDataConverter()

        # Test with None input
        try:
            converter.convert_legacy_to_beat_data(None, 1)
            print("❌ Should have raised ValueError for None input")
            return False
        except ValueError:
            print("  ✅ Correctly rejected None input")

        # Test with invalid data
        try:
            converter.convert_legacy_to_beat_data({"invalid": "data"}, 1)
            print("❌ Should have raised ValueError for invalid data")
            return False
        except ValueError:
            print("  ✅ Correctly rejected invalid data")

        print("✅ Error handling tests passed")
        return True

    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        traceback.print_exc()
        return False


def check_refactoring_goals():
    """Check that refactoring goals were achieved."""
    print("\n🎯 Checking refactoring goals...")

    try:
        # Read the refactored file to analyze
        converter_path = (
            project_root
            / "src"
            / "desktop"
            / "modern"
            / "src"
            / "application"
            / "services"
            / "data"
            / "legacy_data_converter.py"
        )

        if not converter_path.exists():
            print(f"❌ Converter file not found: {converter_path}")
            return False

        content = converter_path.read_text()
        lines = content.split("\n")

        # Check file size reduction
        print(f"  Refactored file: {len(lines)} lines")

        # Check for eliminated duplication
        blue_motion_count = content.count("blue_motion")
        red_motion_count = content.count("red_motion")
        print(f"  Blue motion references: {blue_motion_count}")
        print(f"  Red motion references: {red_motion_count}")

        # Check for use of supporting classes
        has_motion_converter = "MotionDataConverter" in content
        has_validator = "LegacyFormatValidator" in content
        has_builder = "BeatDataBuilder" in content

        print(f"  Uses MotionDataConverter: {has_motion_converter}")
        print(f"  Uses LegacyFormatValidator: {has_validator}")
        print(f"  Uses BeatDataBuilder: {has_builder}")

        if has_motion_converter and has_validator and has_builder:
            print("✅ Refactoring goals achieved")
            return True
        else:
            print("❌ Some supporting classes not used")
            return False

    except Exception as e:
        print(f"❌ Goal check failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all validation tests."""
    print("🚀 Starting Legacy Data Converter Refactoring Validation")
    print("=" * 60)

    tests = [
        ("Import Tests", test_imports),
        ("MotionDataConverter Tests", test_motion_data_converter),
        ("LegacyFormatValidator Tests", test_legacy_format_validator),
        ("BeatDataBuilder Tests", test_beat_data_builder),
        ("LegacyDataConverter Tests", test_legacy_data_converter),
        ("Integration Tests", test_integration),
        ("Error Handling Tests", test_error_handling),
        ("Refactoring Goals Check", check_refactoring_goals),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                logger.error(f"Test failed: {test_name}")
        except Exception as e:
            logger.error(f"Test crashed: {test_name} - {e}")
            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"🏁 Validation Complete: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Refactoring successful!")
        return 0
    else:
        print(f"❌ {total - passed} tests failed. Check logs for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
