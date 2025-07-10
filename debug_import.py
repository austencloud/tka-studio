#!/usr/bin/env python3
"""Simple test to debug import issue."""

import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(src_path))

print(f"Python path: {sys.path[0]}")
print(f"Looking for: {src_path}")
print(f"Path exists: {src_path.exists()}")

# Try importing step by step
try:
    import application

    print("✅ application module imported")

    import application.services

    print("✅ application.services module imported")

    import application.services.pictographs

    print("✅ application.services.pictographs module imported")

    from application.services.pictographs.pictograph_management_service import (
        PictographManagementService,
    )

    print("✅ PictographManagementService imported")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
