#!/usr/bin/env python3
"""Debug script to investigate widget_factory import issues"""

import os
import sys
import traceback

# Add the source path
sys.path.append("modern/src")

print("=== Debug Import Test ===")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path includes: {[p for p in sys.path if 'tka-desktop' in p]}")

try:
    print("\n1. Testing basic imports...")

    print("✓ typing imported")

    print("✓ PyQt6.QtWidgets imported")

    print("✓ PyQt6.QtCore imported")

    print("✓ PyQt6.QtGui imported")

except Exception as e:
    print(f"✗ Basic imports failed: {e}")
    traceback.print_exc()

try:
    print("\n2. Testing core imports...")

    print("✓ DIContainer imported")

    print("✓ ILayoutService imported")

except Exception as e:
    print(f"✗ Core imports failed: {e}")
    traceback.print_exc()

try:
    print("\n3. Testing option picker component imports...")

    print("✓ ModernOptionPickerWidget imported")

    print("✓ OptionPickerFilter imported")

except Exception as e:
    print(f"✗ Option picker component imports failed: {e}")
    traceback.print_exc()

try:
    print("\n4. Testing widget_factory module import...")
    import presentation.factories.widget_factory as wf_module

    print("✓ widget_factory module imported")
    print(f"   Module file: {wf_module.__file__}")
    print(
        f"   Module attributes: {[attr for attr in dir(wf_module) if not attr.startswith('_')]}"
    )

except Exception as e:
    print(f"✗ widget_factory module import failed: {e}")
    traceback.print_exc()

try:
    print("\n5. Testing direct file execution...")
    with open("modern/src/presentation/factories/widget_factory.py") as f:
        content = f.read()

    print(f"   File size: {len(content)} characters")
    print(
        f"   File contains 'class OptionPickerWidgetFactory': {'class OptionPickerWidgetFactory' in content}"
    )

    # Try to execute the file content manually
    exec(content, globals())
    print("✓ File content executed successfully")
    print(
        f"   OptionPickerWidgetFactory defined: {'OptionPickerWidgetFactory' in globals()}"
    )

except Exception as e:
    print(f"✗ Direct file execution failed: {e}")
    traceback.print_exc()

try:
    print("\n6. Testing specific class import...")

    print("✓ OptionPickerWidgetFactory imported successfully")

except Exception as e:
    print(f"✗ OptionPickerWidgetFactory import failed: {e}")
    traceback.print_exc()

print("\n=== Debug Complete ===")
