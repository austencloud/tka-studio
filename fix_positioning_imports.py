#!/usr/bin/env python3
"""
Advanced import fixing script for positioning services migration.
Handles complex cases and validates changes.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple


def fix_positioning_imports():
    """Fix all positioning imports with validation."""

    # Define the mapping of old → new paths
    import_mappings = {
        # Arrow services
        "arrow_positioning_orchestrator": "arrows.orchestration.arrow_positioning_orchestrator",
        "arrow_adjustment_calculator_service": "arrows.orchestration.arrow_adjustment_calculator_service",
        "arrow_location_calculator": "arrows.calculation.arrow_location_calculator",
        "arrow_location_calculator_service": "arrows.calculation.arrow_location_calculator_service",
        "arrow_rotation_calculator_service": "arrows.calculation.arrow_rotation_calculator_service",
        "orientation_calculation_service": "arrows.calculation.orientation_calculation_service",
        "quadrant_adjustment_service": "arrows.calculation.quadrant_adjustment_service",
        "quadrant_index_service": "arrows.calculation.quadrant_index_service",
        "directional_tuple_service": "arrows.calculation.directional_tuple_service",
        "default_placement_service": "arrows.placement.default_placement_service",
        "special_placement_service": "arrows.placement.special_placement_service",
        "special_placement_orientation_service": "arrows.placement.special_placement_orientation_service",
        "arrow_coordinate_system_service": "arrows.coordinate_system.arrow_coordinate_system_service",
        "placement_key_generation_service": "arrows.keys.placement_key_generation_service",
        "placement_key_service": "arrows.keys.placement_key_service",
        "attribute_key_generation_service": "arrows.keys.attribute_key_generation_service",
        "turns_tuple_generation_service": "arrows.keys.turns_tuple_generation_service",
        "dash_location_service": "arrows.utilities.dash_location_service",
        "position_matching_service": "arrows.utilities.position_matching_service",
        # Prop services
        "prop_orchestrator": "props.orchestration.prop_orchestrator",
        "prop_management_service": "props.orchestration.prop_management_service",
        "direction_calculation_service": "props.calculation.direction_calculation_service",
        "offset_calculation_service": "props.calculation.offset_calculation_service",
        "prop_classification_service": "props.calculation.prop_classification_service",
        "json_configuration_service": "props.configuration.json_configuration_service",
    }

    base_path = Path("F:/CODE/TKA/src/desktop/modern/src")
    fixes_applied = []

    print("🔧 Starting positioning imports fix...")
    print(f"📂 Scanning directory: {base_path}")

    # Process all Python files
    for file_path in base_path.rglob("*.py"):
        changes = fix_file_imports(file_path, import_mappings)
        if changes:
            fixes_applied.extend(changes)
    # Report results
    print("✅ Import fixes complete!")
    print(
        f"📊 Fixed {len(fixes_applied)} import statements across {len(set(fix[0] for fix in fixes_applied))} files"
    )

    # Show sample fixes
    if fixes_applied:
        print("\n📝 Sample fixes applied:")
        for file_path, old_import, new_import in fixes_applied[:10]:
            rel_path = Path(file_path).relative_to(base_path)
            print(f"  📁 {rel_path}")
            print(f"    - {old_import}")
            print(f"    + {new_import}")

        if len(fixes_applied) > 10:
            print(f"    ... and {len(fixes_applied) - 10} more")
    else:
        print("ℹ️  No import fixes needed - all imports are already correct!")


def fix_file_imports(
    file_path: Path, mappings: Dict[str, str]
) -> List[Tuple[str, str, str]]:
    """Fix imports in a single file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content
        changes = []

        # Determine relative path depth for positioning services
        positioning_path = Path(
            "F:/CODE/TKA/src/desktop/modern/src/application/services/positioning"
        )

        # Fix relative imports (from .service_name)
        for old_service, new_path in mappings.items():
            # Pattern: from .service_name import ...
            old_pattern = rf"from \.{re.escape(old_service)}"

            if (
                positioning_path in file_path.parents
                or file_path.parent == positioning_path
            ):
                # For files within positioning directory structure
                try:
                    rel_path = file_path.relative_to(positioning_path)
                    depth = (
                        len(rel_path.parts) - 1
                    )  # -1 because the file itself doesn't count

                    if depth == 0:
                        # File is in positioning root
                        new_import = f"from .{new_path}"
                    else:
                        # File is in subdirectory, need to go up
                        dots = "." + "." * depth
                        new_import = f"from {dots}{new_path}"
                except ValueError:
                    # File is not under positioning path
                    new_import = f"from .{new_path}"
            else:
                # For files outside positioning, keep as relative
                new_import = f"from .{new_path}"

            matches = re.findall(old_pattern, content)
            if matches:
                content = re.sub(old_pattern, new_import.split(" import")[0], content)
                changes.append(
                    (str(file_path), old_pattern, new_import.split(" import")[0])
                )

        # Fix absolute imports (from application.services.positioning.service)
        for old_service, new_path in mappings.items():
            old_pattern = (
                rf"from application\.services\.positioning\.{re.escape(old_service)}"
            )
            new_import = f"from application.services.positioning.{new_path}"

            matches = re.findall(old_pattern, content)
            if matches:
                content = re.sub(old_pattern, new_import, content)
                changes.append((str(file_path), old_pattern, new_import))

        # Fix import statements with class names (from X import Y)
        for old_service, new_path in mappings.items():
            # Handle "from .service import Class" patterns
            old_pattern = rf"from \.{re.escape(old_service)} import"

            if (
                positioning_path in file_path.parents
                or file_path.parent == positioning_path
            ):
                try:
                    rel_path = file_path.relative_to(positioning_path)
                    depth = len(rel_path.parts) - 1

                    if depth == 0:
                        new_import = f"from .{new_path} import"
                    else:
                        dots = "." + "." * depth
                        new_import = f"from {dots}{new_path} import"
                except ValueError:
                    new_import = f"from .{new_path} import"
            else:
                new_import = f"from .{new_path} import"

            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_import, content)
                changes.append((str(file_path), old_pattern, new_import))

            # Handle "from application.services.positioning.service import Class" patterns
            old_abs_pattern = rf"from application\.services\.positioning\.{re.escape(old_service)} import"
            new_abs_import = f"from application.services.positioning.{new_path} import"

            if re.search(old_abs_pattern, content):
                content = re.sub(old_abs_pattern, new_abs_import, content)
                changes.append((str(file_path), old_abs_pattern, new_abs_import))

        # Write changes if any were made
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

        return changes

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return []


def validate_positioning_structure():
    """Validate that the positioning structure exists."""
    positioning_path = Path(
        "F:/CODE/TKA/src/desktop/modern/src/application/services/positioning"
    )

    if not positioning_path.exists():
        print(f"❌ Positioning directory not found: {positioning_path}")
        return False

    # Check for new structure
    arrows_path = positioning_path / "arrows"
    props_path = positioning_path / "props"

    if not arrows_path.exists() or not props_path.exists():
        print("❌ New positioning structure not found. Run migration script first!")
        return False

    print("✅ Positioning structure validated!")
    return True


def search_remaining_old_imports():
    """Search for any remaining old import patterns."""
    base_path = Path("F:/CODE/TKA/src/desktop/modern/src")

    old_patterns = [
        r"from \.arrow_positioning_orchestrator",
        r"from \.prop_orchestrator",
        r"from \.direction_calculation_service",
        r"from \.placement_key_generation_service",
        r"from application\.services\.positioning\.arrow_location_calculator[^.]",
        r"from application\.services\.positioning\.prop_management_service[^.]",
    ]

    remaining_issues = []

    for file_path in base_path.rglob("*.py"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            for pattern in old_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    remaining_issues.append((str(file_path), pattern, matches))
        except Exception:
            continue

    if remaining_issues:
        print(
            f"\n⚠️  Found {len(remaining_issues)} files with remaining old import patterns:"
        )
        for file_path, pattern, matches in remaining_issues[:5]:
            rel_path = Path(file_path).relative_to(base_path)
            print(f"  📁 {rel_path}: {pattern}")

        if len(remaining_issues) > 5:
            print(f"    ... and {len(remaining_issues) - 5} more")
    else:
        print("\n✅ No remaining old import patterns found!")

    return len(remaining_issues) == 0


if __name__ == "__main__":
    print("🚀 Positioning Services Import Fixer")
    print("=" * 50)

    # Validate structure exists
    if not validate_positioning_structure():
        print("\n💡 Please run the migration script first:")
        print("   python migrate_positioning_microservices.py")
        exit(1)

    # Fix imports
    fix_positioning_imports()

    # Validate no old patterns remain
    print("\n🔍 Checking for remaining old import patterns...")
    all_clean = search_remaining_old_imports()

    if all_clean:
        print("\n🎉 All positioning imports successfully updated!")
        print("💡 You can now run tests to verify everything works:")
        print(
            "   pytest src/desktop/modern/tests/unit/application/services/positioning/ -v"
        )
    else:
        print("\n⚠️  Some import patterns may need manual fixing.")
        print("💡 Check the files listed above and fix any remaining issues.")
