#!/usr/bin/env python3
"""
Quick regression test for core import hook.
This should be run from within your TKA environment where PyQt6 is available.
"""

import os
import sys
from pathlib import Path

# Add TKA root to path
tka_root = Path(__file__).parent
sys.path.insert(0, str(tka_root))

# Install the hook
try:
    from core_import_hook import install_core_import_hook

    install_core_import_hook()
    print("✅ Core import hook installed")
except Exception as e:
    print(f"❌ Failed to install hook: {e}")
    sys.exit(1)

# Test the actual import that was failing
try:
    from core.glassmorphism_styler import GlassmorphismStyler

    print("✅ Successfully imported GlassmorphismStyler from core!")

    # Test basic functionality
    if hasattr(GlassmorphismStyler, "_get_coordinator"):
        print("✅ GlassmorphismStyler has expected methods")

    # Test that we can get the coordinator
    coordinator = GlassmorphismStyler._get_coordinator()
    if coordinator:
        print("✅ GlassmorphismStyler coordinator works")

    print("🎉 All tests passed! Core import hook is working correctly.")

except ImportError as e:
    print(f"❌ Import failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
