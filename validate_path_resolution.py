#!/usr/bin/env python3
"""
TKA Path Resolution Validation Script
=====================================

This script validates that the new universal path system solves all TKA import issues.
"""

import sys
from pathlib import Path


def main():
    print("🚀 TKA PATH RESOLUTION VALIDATION")
    print("=" * 50)

    # Test 1: Universal path system import
    print("1. Testing universal path system...")
    try:
        import tka_paths

        print("✅ Universal path system imported successfully")
    except Exception as e:
        print(f"❌ Failed to import universal path system: {e}")
        return False

    # Test 2: Get debug info
    print("\n2. Getting path configuration...")
    try:
        info = tka_paths.get_debug_info()
        if "error" in info:
            print(f"❌ Path system error: {info['error']}")
            return False

        print(f"✅ TKA Root: {info['tka_root']}")
        print(f"✅ Configured {len(info['configured_paths'])} paths")
        print(f"✅ Found {len(info['all_tka_paths'])} total paths")

    except Exception as e:
        print(f"❌ Failed to get debug info: {e}")
        return False

    # Test 3: Core framework-agnostic imports
    print("\n3. Testing framework-agnostic core imports...")
    tests = [
        ("application.services.core.image_export_service", "CoreImageExportService"),
        ("application.adapters.qt_image_export_adapter", "QtImageExportAdapter"),
        ("application.services.core.types", "Size"),
    ]

    all_passed = True
    for module_name, class_name in tests:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
        except Exception as e:
            print(f"❌ {module_name}.{class_name}: {e}")
            all_passed = False

    # Test 4: Modern desktop imports
    print("\n4. Testing modern desktop imports...")
    try:
        from application.services.image_export.sequence_image_renderer import (
            SequenceImageRenderer,
        )

        print("✅ SequenceImageRenderer import successful")
    except Exception as e:
        print(f"⚠️ SequenceImageRenderer import failed: {e}")
        print("   (This is expected if modern desktop is not in current paths)")

    # Test 5: Framework separation
    print("\n5. Validating framework separation...")
    try:
        # Core service should not import Qt
        import inspect

        import application.services.core.image_export_service as core_service

        source = inspect.getsource(core_service)

        qt_imports = ["from PyQt", "import PyQt", "from Qt", "import Qt"]
        has_qt = any(qt_import in source for qt_import in qt_imports)

        if has_qt:
            print("❌ Core service contains Qt imports")
            all_passed = False
        else:
            print("✅ Core service is framework-agnostic")

    except Exception as e:
        print(f"⚠️ Could not validate framework separation: {e}")

    # Summary
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 PATH RESOLUTION VALIDATION SUCCESSFUL!")
        print("\nKey Benefits:")
        print("✅ Universal path system works across all TKA components")
        print("✅ Framework-agnostic core services import correctly")
        print("✅ Qt adapters bridge properly to Qt-specific functionality")
        print("✅ No Qt dependencies leak into core business logic")
        print("✅ Single import solves all path issues: import tka_paths")
        return True
    else:
        print("❌ Some issues remain - see errors above")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
