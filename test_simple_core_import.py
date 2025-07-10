#!/usr/bin/env python3
"""
Simple test to verify core import hook works.
"""

import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Install the hook
from core_import_hook import install_core_import_hook

install_core_import_hook()

print("Testing core import hook...")

try:
    # This should work now
    from core.glassmorphism_styler import GlassmorphismStyler

    print("✅ Successfully imported GlassmorphismStyler from core!")
    print(f"✅ GlassmorphismStyler class: {GlassmorphismStyler}")

    # Test that we can access class methods
    if hasattr(GlassmorphismStyler, "_get_coordinator"):
        print("✅ GlassmorphismStyler has expected methods")
    else:
        print("⚠️ GlassmorphismStyler missing expected methods")

except ImportError as e:
    print(f"❌ Failed to import from core: {e}")
    import traceback

    traceback.print_exc()
