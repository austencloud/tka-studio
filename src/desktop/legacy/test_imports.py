#!/usr/bin/env python3
"""
Test script to verify legacy imports work correctly.
Run this from the legacy directory to test import resolution.
"""

import sys
import os

# Add the src directory to Python path (same as main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
if os.path.exists(src_dir) and src_dir not in sys.path:
    sys.path.insert(0, src_dir)

print("Python path configured. Testing imports...")
print(f"Current directory: {current_dir}")
print(f"Source directory: {src_dir}")
print(f"Source directory exists: {os.path.exists(src_dir)}")

try:
    from data.constants import BLUE, RED
    print("✓ SUCCESS: data.constants imports work")
    print(f"  BLUE = {BLUE}")
    print(f"  RED = {RED}")
except ImportError as e:
    print(f"✗ FAILED: data.constants import failed: {e}")

try:
    from letter_determination.determination_result import DeterminationResult
    print("✓ SUCCESS: letter_determination imports work")
except ImportError as e:
    print(f"✗ FAILED: letter_determination import failed: {e}")

try:
    from letter_determination.strategies.base_strategy import LetterDeterminationStrategy
    print("✓ SUCCESS: letter_determination.strategies imports work")
except ImportError as e:
    print(f"✗ FAILED: letter_determination.strategies import failed: {e}")

print("\nAll import tests completed.")
