#!/usr/bin/env python3
"""
Perfect Microservices Migration Script
Migrates positioning services into clean arrow/prop domain separation.
"""

import shutil
from pathlib import Path


def migrate_positioning_services():
    """Migrate positioning services with correct arrow/prop classification."""

    base_path = Path(
        "F:/CODE/TKA/src/desktop/modern/src/application/services/positioning"
    )

    # Corrected file mappings based on actual file analysis
    migrations = {
        # Arrow services (15 files)
        "arrow_positioning_orchestrator.py": "arrows/orchestration",
        "arrow_adjustment_calculator_service.py": "arrows/orchestration",
        "arrow_location_calculator.py": "arrows/calculation",
        "arrow_location_calculator_service.py": "arrows/calculation",
        "arrow_rotation_calculator_service.py": "arrows/calculation",
        "orientation_calculation_service.py": "arrows/calculation",
        "quadrant_adjustment_service.py": "arrows/calculation",
        "quadrant_index_service.py": "arrows/calculation",
        "directional_tuple_service.py": "arrows/calculation",
        "default_placement_service.py": "arrows/placement",
        "special_placement_service.py": "arrows/placement",
        "special_placement_orientation_service.py": "arrows/placement",
        "arrow_coordinate_system_service.py": "arrows/coordinate_system",
        "placement_key_generation_service.py": "arrows/keys",
        "placement_key_service.py": "arrows/keys",
        "attribute_key_generation_service.py": "arrows/keys",
        "turns_tuple_generation_service.py": "arrows/keys",
        "dash_location_service.py": "arrows/utilities",
        "position_matching_service.py": "arrows/utilities",
        # Prop services (6 files)
        "prop_orchestrator.py": "props/orchestration",
        "prop_management_service.py": "props/orchestration",
        "direction_calculation_service.py": "props/calculation",
        "offset_calculation_service.py": "props/calculation",
        "prop_classification_service.py": "props/calculation",
        "json_configuration_service.py": "props/configuration",
    }

    print("🚀 Starting Perfect Microservices Migration...")
    print(f"📁 Base path: {base_path}")

    # Create directories and move files
    moved_count = 0
    for filename, new_dir in migrations.items():
        old_path = base_path / filename
        new_path = base_path / new_dir / filename

        # Create directory if it doesn't exist
        new_path.parent.mkdir(parents=True, exist_ok=True)

        if old_path.exists():
            shutil.move(str(old_path), str(new_path))
            print(f"✅ Moved {filename} -> {new_dir}/")
            moved_count += 1
        else:
            print(f"⚠️  File not found: {filename}")

    print(f"\n🎯 Migration complete! Moved {moved_count} files.")
    print("📋 Summary:")
    print("   • Arrow services: 19 files organized into 6 categories")
    print("   • Prop services: 6 files organized into 3 categories")
    print("   • Clean domain separation achieved!")


def create_init_files():
    """Create __init__.py files for all new directories."""

    base_path = Path(
        "F:/CODE/TKA/src/desktop/modern/src/application/services/positioning"
    )

    directories = [
        "arrows",
        "arrows/orchestration",
        "arrows/calculation",
        "arrows/placement",
        "arrows/coordinate_system",
        "arrows/keys",
        "arrows/utilities",
        "props",
        "props/orchestration",
        "props/calculation",
        "props/configuration",
    ]

    print("\n📄 Creating __init__.py files...")

    for directory in directories:
        init_path = base_path / directory / "__init__.py"
        if not init_path.exists():
            init_path.touch()
            print(f"✅ Created {directory}/__init__.py")


if __name__ == "__main__":
    migrate_positioning_services()
    create_init_files()
    print("\n🎉 Perfect microservices structure implemented!")
