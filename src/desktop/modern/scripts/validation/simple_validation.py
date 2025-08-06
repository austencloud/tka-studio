"""
Simple service validation test
"""

from __future__ import annotations

from pathlib import Path
import sys


# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

print("Testing basic imports...")

try:
    print("✅ Interface import successful")

    from shared.application.services.start_position.start_position_data_service import (
        StartPositionDataService,
    )

    print("✅ Service import successful")

    service = StartPositionDataService()
    print("✅ Service instantiation successful")

    print("🎉 Basic validation passed!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
