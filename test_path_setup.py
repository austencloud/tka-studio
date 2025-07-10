#!/usr/bin/env python3
"""
Regression test for TKA path setup.
Tests that core imports work correctly from different directories.
"""

import os
import sys
from pathlib import Path


def test_path_setup():
    """Test that setup_paths correctly enables core imports."""

    print("🔍 Testing TKA path setup...")

    # Add project root and run setup
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    try:
        from setup_paths import setup_tka_paths

        paths_added = setup_tka_paths()
        print(f"✅ Setup paths added {paths_added} directories to sys.path")
    except Exception as e:
        print(f"❌ Failed to run setup_paths: {e}")
        return False

    # Test specific imports that were failing
    test_imports = [
        ("core.application_context", "ApplicationContext"),
        ("core.glassmorphism_styler", "GlassmorphismStyler"),
    ]

    success_count = 0

    for module_name, class_name in test_imports:
        try:
            print(f"  Testing import: from {module_name} import {class_name}")
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  ✅ {module_name}.{class_name} imported successfully")
            success_count += 1
        except ImportError as e:
            print(f"  ❌ Failed to import {module_name}.{class_name}: {e}")
        except AttributeError as e:
            print(f"  ❌ {class_name} not found in {module_name}: {e}")
        except Exception as e:
            print(f"  ⚠️ Unexpected error importing {module_name}.{class_name}: {e}")

    print(f"\n📊 Test Results: {success_count}/{len(test_imports)} imports successful")

    if success_count == len(test_imports):
        print("🎉 All core imports working correctly!")
        return True
    else:
        print("❌ Some imports failed - check path setup")
        return False


if __name__ == "__main__":
    success = test_path_setup()
    sys.exit(0 if success else 1)
