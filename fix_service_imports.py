#!/usr/bin/env python3
"""
Service Import Path Fixer Script
================================

This script automatically updates all import paths after the services directory reorganization.
Fixes imports from old paths to new domain-organized paths.

Usage:
    python fix_service_imports.py

Author: AI Assistant
Date: July 10, 2025
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Define the import path mappings
IMPORT_MAPPINGS = {
    # Sequence services moved from core/ to sequences/
    "from application.services.sequences.sequence_loading_service": "from application.services.sequences.sequence_loading_service",
    "from application.services.sequences.sequence_management_service": "from application.services.sequences.sequence_management_service",
    "from application.services.sequences.persister": "from application.services.sequences.persister",
    "from application.services.sequences.sequence_beat_operations": "from application.services.sequences.sequence_beat_operations",
    "from application.services.sequences.sequence_state_manager": "from application.services.sequences.sequence_state_manager",
    "from application.services.sequences.sequence_start_position_manager": "from application.services.sequences.sequence_start_position_manager",
    # Pictograph services moved from core/ to pictographs/
    "from application.services.pictographs.pictograph_management_service": "from application.services.pictographs.pictograph_management_service",
    "from application.services.pictographs.pictograph_orchestrator": "from application.services.pictographs.pictograph_orchestrator",
    "from application.services.pictographs.application_orchestrator": "from application.services.pictographs.application_orchestrator",
    # Pictograph analysis moved from data/ to pictographs/
    "from application.services.pictographs.pictograph_analysis_service": "from application.services.pictographs.pictograph_analysis_service",
    # Glyph services moved from data/ to glyphs/
    "from application.services.glyphs.glyph_data_service": "from application.services.glyphs.glyph_data_service",
    "from application.services.glyphs.glyph_generation_service": "from application.services.glyphs.glyph_generation_service",
    # Graph editor services moved from ui/graph_editor/ to graph_editor/
    "from application.services.graph_editor.graph_editor_service": "from application.services.graph_editor.graph_editor_service",
    "from application.services.graph_editor.graph_editor_data_flow_service": "from application.services.graph_editor.graph_editor_data_flow_service",
    "from application.services.graph_editor.graph_editor_hotkey_service": "from application.services.graph_editor.graph_editor_hotkey_service",
}


def find_python_files(root_dir: Path) -> List[Path]:
    """Find all Python files in the directory tree, focusing on relevant directories."""
    python_files = []

    # Only process relevant directories to avoid scanning entire codebase
    relevant_dirs = [
        "src/desktop/modern/src",
        "src/desktop/modern/tests",
        "src/desktop/modern/main.py",
        "src/desktop/modern/*.py",
    ]

    for rel_dir in relevant_dirs:
        if rel_dir.endswith(".py"):
            # Single file
            file_path = root_dir / rel_dir
            if file_path.exists():
                python_files.append(file_path)
        else:
            # Directory
            dir_path = root_dir / rel_dir
            if dir_path.exists():
                for path in dir_path.rglob("*.py"):
                    # Skip __pycache__ and .git directories
                    if "__pycache__" in str(path) or ".git" in str(path):
                        continue
                    python_files.append(path)

    return python_files


def fix_imports_in_file(
    file_path: Path, mappings: Dict[str, str]
) -> Tuple[bool, List[str]]:
    """
    Fix imports in a single file.

    Returns:
        (changed, changes_made) - boolean indicating if file was changed, list of changes
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False, []

    original_content = content
    changes_made = []

    # Apply each import mapping
    for old_import, new_import in mappings.items():
        if old_import in content:
            content = content.replace(old_import, new_import)
            changes_made.append(f"  {old_import} → {new_import}")

    # If content changed, write it back
    if content != original_content:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True, changes_made
        except Exception as e:
            print(f"❌ Error writing {file_path}: {e}")
            return False, []

    return False, []


def main():
    """Main function to fix all import paths."""
    print("🔧 Service Import Path Fixer")
    print("=" * 50)

    # Get the root directory (where this script is located)
    root_dir = Path(__file__).parent

    # Find all Python files
    print(f"🔍 Searching for Python files in {root_dir}")
    python_files = find_python_files(root_dir)
    print(f"📁 Found {len(python_files)} Python files")

    # Track statistics
    total_files = len(python_files)
    changed_files = 0
    total_changes = 0

    # Process each file
    for file_path in python_files:
        relative_path = file_path.relative_to(root_dir)

        changed, changes = fix_imports_in_file(file_path, IMPORT_MAPPINGS)

        if changed:
            changed_files += 1
            total_changes += len(changes)
            print(f"✅ {relative_path}")
            for change in changes:
                print(change)
            print()

    # Print summary
    print("=" * 50)
    print(f"📊 SUMMARY")
    print(f"Total files processed: {total_files}")
    print(f"Files changed: {changed_files}")
    print(f"Total import changes: {total_changes}")

    if changed_files > 0:
        print(
            f"✅ Successfully updated {changed_files} files with {total_changes} import changes!"
        )
    else:
        print("✅ No import changes needed - all files are up to date!")


if __name__ == "__main__":
    main()
