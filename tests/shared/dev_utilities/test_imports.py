#!/usr/bin/env python3
"""
Test script to validate that all imports work correctly.
Run this from the project root to check if your configuration is working.
"""

import sys
import os

# Add project paths (same as in .pylintrc)
project_root = os.path.abspath(".")
launcher_path = os.path.join(project_root, "launcher")
modern_src_path = os.path.join(project_root, "src", "desktop", "modern", "src")

for path in [project_root, launcher_path, modern_src_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

print("🔍 Testing import resolution...")
print(f"Project root: {project_root}")
print(f"Launcher path: {launcher_path}")
print(f"Modern src path: {modern_src_path}")

try:
    print("\n✅ Testing PyQt6 imports...")
    from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
    from PyQt6.QtCore import Qt, pyqtSignal
    from PyQt6.QtGui import QFont, QPixmap
    print("   ✓ PyQt6 imports successful")
except ImportError as e:
    print(f"   ❌ PyQt6 import failed: {e}")

try:
    print("\n✅ Testing ui.components import...")
    from ui.components import ReliableApplicationCard
    print("   ✓ ui.components import successful")
except ImportError as e:
    print(f"   ❌ ui.components import failed: {e}")

try:
    print("\n✅ Testing ui.reliable_effects import...")
    from ui.reliable_effects import get_animation_manager
    print("   ✓ ui.reliable_effects import successful")
except ImportError as e:
    print(f"   ❌ ui.reliable_effects import failed: {e}")

print("\n🎯 Import test complete!")
print("Run test_imports_enhanced.py for comprehensive testing.")
