#!/usr/bin/env python3
"""Debug import paths for Image Export Service testing."""

import sys
from pathlib import Path


def setup_project_paths():
    """Setup project paths for imports."""
    current_file = Path(__file__).resolve()

    # Find TKA root
    tka_root = current_file
    while tka_root.name != "TKA" and tka_root.parent != tka_root:
        tka_root = tka_root.parent

    if tka_root.name == "TKA":
        paths_to_add = [
            str(tka_root),
            str(tka_root / "src"),
            str(tka_root / "src" / "desktop" / "modern" / "src"),
        ]

        for path in paths_to_add:
            if path not in sys.path:
                sys.path.insert(0, path)

        print(f"✅ Project paths configured from: {tka_root}")
        print("Added paths:")
        for path in paths_to_add:
            print(f"  - {path}")
        return tka_root
    else:
        print("❌ Could not find TKA root directory")
        return None


# Setup paths
tka_root = setup_project_paths()

print("\nCurrent sys.path:")
for i, path in enumerate(sys.path[:10]):  # Show first 10 entries
    print(f"  {i}: {path}")

print("\nChecking file existence:")
files_to_check = [
    "src/application/services/core/image_export_service.py",
    "src/application/adapters/qt_image_export_adapter.py",
    "src/desktop/modern/src/application/services/image_export/sequence_image_renderer.py",
]

for file_path in files_to_check:
    full_path = tka_root / file_path
    exists = full_path.exists()
    print(f"  {file_path}: {'✅ exists' if exists else '❌ missing'}")

print("\nTesting imports:")
try:
    print(
        "Testing: from application.services.core.image_export_service import CoreImageExportService"
    )
    from application.services.core.image_export_service import CoreImageExportService

    print("✅ SUCCESS: Core service import works")
except Exception as e:
    print(f"❌ FAILED: {e}")

try:
    print(
        "Testing: from application.adapters.qt_image_export_adapter import QtImageExportAdapter"
    )
    from application.adapters.qt_image_export_adapter import QtImageExportAdapter

    print("✅ SUCCESS: Qt adapter import works")
except Exception as e:
    print(f"❌ FAILED: {e}")

try:
    print(
        "Testing: from application.services.image_export.sequence_image_renderer import SequenceImageRenderer"
    )
    from application.services.image_export.sequence_image_renderer import (
        SequenceImageRenderer,
    )

    print("✅ SUCCESS: Sequence renderer import works")
except Exception as e:
    print(f"❌ FAILED: {e}")
