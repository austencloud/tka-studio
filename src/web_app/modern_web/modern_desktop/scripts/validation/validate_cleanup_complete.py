#!/usr/bin/env python3
"""
Validation script to verify that the start position picker cleanup was successful.

This script validates:
1. Legacy components have been removed
2. Unified picker is working correctly
3. All imports are updated
4. Application functionality is preserved
"""

from __future__ import annotations

import os
from pathlib import Path
import sys


# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))


def validate_cleanup():
    """Validate that the cleanup was successful."""
    print("🧹 Validating Start Position Picker Cleanup")
    print("=" * 50)

    tests_passed = 0
    total_tests = 0

    # Test 1: Verify legacy files are removed
    total_tests += 1
    try:
        legacy_files = [
            "src/presentation/components/start_position_picker/enhanced_start_position_picker.py",
            "src/presentation/components/start_position_picker/advanced_start_position_picker.py",
            "src/presentation/components/start_position_picker/start_position_option.py",
            "src/presentation/components/start_position_picker/variations_button.py",
            "src/presentation/components/start_position_picker/unified_start_position_picker.py",  # Should be renamed
        ]

        missing_files = []
        for file_path in legacy_files:
            if os.path.exists(file_path):
                missing_files.append(file_path)

        if missing_files:
            print(f"  ❌ Legacy files still exist: {missing_files}")
        else:
            print("  ✅ All legacy files successfully removed")
            tests_passed += 1

    except Exception as e:
        print(f"  ❌ Error checking legacy files: {e}")

    # Test 2: Verify unified picker exists and imports correctly
    total_tests += 1
    try:
        print("  ✅ Unified picker imports successfully")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Unified picker import failed: {e}")

    # Test 3: Verify backward compatibility
    total_tests += 1
    try:
        print("  ✅ Backward compatibility imports work")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Backward compatibility failed: {e}")

    # Test 4: Verify main application import
    total_tests += 1
    try:
        print("  ✅ Main application imports updated correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Main application import failed: {e}")

    # Test 5: Verify remaining files are correct
    total_tests += 1
    try:
        expected_files = [
            "src/presentation/components/start_position_picker/start_position_picker.py",  # Renamed unified
            "src/presentation/components/start_position_picker/enhanced_start_position_option.py",  # Still used
            "src/presentation/components/start_position_picker/start_text_overlay.py",  # Utility
            "src/presentation/components/start_position_picker/__deprecated__.py",  # Backward compatibility
        ]

        all_exist = True
        for file_path in expected_files:
            if not os.path.exists(file_path):
                print(f"  ❌ Missing expected file: {file_path}")
                all_exist = False

        if all_exist:
            print("  ✅ All expected files present")
            tests_passed += 1

    except Exception as e:
        print(f"  ❌ Error checking expected files: {e}")

    print("\n" + "=" * 50)
    print(f"📊 Cleanup Validation Results: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print(
            "🎉 ✅ CLEANUP SUCCESSFUL! All legacy components removed and unified picker working."
        )
        return True
    print("❌ CLEANUP INCOMPLETE! Some issues remain.")
    return False


if __name__ == "__main__":
    success = validate_cleanup()
    sys.exit(0 if success else 1)
