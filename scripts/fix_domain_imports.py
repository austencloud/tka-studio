#!/usr/bin/env python3
"""Script to fix domain model imports in the modern desktop codebase."""

import os
import re
from pathlib import Path


def fix_imports_in_file(file_path: Path) -> bool:
    """Fix domain model imports in a single file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Patterns to fix
        patterns = [
            (
                r"from domain\.models\.core_models import",
                "from src.desktop.modern.src.domain.models.core_models import",
            ),
            (
                r"from domain\.models\.pictograph_models import",
                "from src.desktop.modern.src.domain.models.pictograph_models import",
            ),
            (
                r"from domain\.models\.positioning_models import",
                "from src.desktop.modern.src.domain.models.positioning_models import",
            ),
            (
                r"from domain\.models\.settings_models import",
                "from src.desktop.modern.src.domain.models.settings_models import",
            ),
            (
                r"from domain\.models\.sequence_operations import",
                "from src.desktop.modern.src.domain.models.sequence_operations import",
            ),
        ]

        original_content = content
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed imports in: {file_path}")
            return True
        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Fix all domain imports in the modern desktop codebase."""
    base_path = Path("src/desktop/modern")

    if not base_path.exists():
        print(f"Path {base_path} does not exist")
        return

    fixed_count = 0
    total_count = 0

    # Find all Python files
    for py_file in base_path.rglob("*.py"):
        total_count += 1
        if fix_imports_in_file(py_file):
            fixed_count += 1

    print(f"\nProcessed {total_count} Python files")
    print(f"Fixed imports in {fixed_count} files")


if __name__ == "__main__":
    main()
