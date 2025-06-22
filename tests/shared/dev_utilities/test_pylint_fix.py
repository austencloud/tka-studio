#!/usr/bin/env python3
"""Test script to verify import resolution is working."""

import sys
import os

# Add the legacy src to path (simulating what pylintrc should do)
legacy_src = os.path.join(os.path.dirname(__file__), "src", "desktop", "legacy", "src")
if os.path.exists(legacy_src) and legacy_src not in sys.path:
    sys.path.insert(0, legacy_src)

print("Testing import resolution after fix...")
print(f"Legacy src path: {legacy_src}")
print(f"Path exists: {os.path.exists(legacy_src)}")

try:
    from enums.letter.letter import Letter
    print("✅ Letter imported successfully")
except ImportError as e:
    print(f"❌ Letter import failed: {e}")

try:
    from enums.prop_type import PropType  
    print("✅ PropType imported successfully")
except ImportError as e:
    print(f"❌ PropType import failed: {e}")

try:
    from main_window.main_widget.tab_name import TabName
    print("✅ TabName imported successfully")
except ImportError as e:
    print(f"❌ TabName import failed: {e}")

print("\nIf imports work here, pylint should work too!")
