from __future__ import annotations
"""
Core Import Path Initialization for TKA Legacy Application

This module sets up intelligent import path resolution for 'core.*' modules.
Import this module early in your application to enable automatic core module resolution.
"""

import sys
from pathlib import Path

# Add the legacy src directory to Python path if not already present
legacy_src_path = Path(__file__).parent.parent
if str(legacy_src_path) not in sys.path:
    sys.path.insert(0, str(legacy_src_path))

# Import and initialize the core import resolver
try:
    from core.import_path_resolver import (
        get_core_mappings,
        install_core_import_resolver,
    )

    # Install the resolver
    resolver = install_core_import_resolver()

    # Debug info
    mappings = get_core_mappings()
    print(f"🔍 Core import resolver initialized with {len(mappings)} mappings")

    # Print key mappings for debugging
    key_modules = [name for name in mappings.keys() if "glassmorphism" in name]
    if key_modules:
        print(f"✅ Found glassmorphism modules: {key_modules}")

except Exception as e:
    print(f"⚠️ Failed to initialize core import resolver: {e}")
    import traceback

    traceback.print_exc()
