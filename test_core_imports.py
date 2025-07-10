#!/usr/bin/env python3
"""Test script for core imports after path setup."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and use the path setup
from setup_paths import setup_tka_paths

print("Setting up TKA paths...")
count = setup_tka_paths()
print(f"Added {count} paths to sys.path")

# Test core imports
try:
    from core.application_context import ApplicationContext
    print("✅ ApplicationContext import successful!")
except ImportError as e:
    print(f"❌ ApplicationContext import failed: {e}")

try:
    from core.glassmorphism_styler import GlassmorphismStyler
    print("✅ GlassmorphismStyler import successful!")
except ImportError as e:
    print(f"❌ GlassmorphismStyler import failed: {e}")

print("\nAll core import tests completed!")
