#!/usr/bin/env python3
"""
TKA Relative Import Fixer
=========================

This script fixes import inconsistencies in the TKA modern desktop application
by converting all absolute imports to the established relative import pattern.

FIXES:
- Converts "from desktop.modern.src.domain..." to "from domain..."
- Converts "from src.desktop.modern.src.domain..." to "from domain..."
- Ensures all imports within modern directory use relative patterns
- Preserves TKA's clean architecture principles

USAGE:
    python scripts/fix_relative_imports.py
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict


class TKARelativeImportFixer:
    """Fixes import patterns to match TKA's established relative import convention."""

    def __init__(self):
        """Initialize the import fixer with TKA-specific patterns."""

        # Define import transformation rules for TKA relative imports
        self.import_rules = [
            # Rule 1: Fix absolute desktop.modern.src imports to relative
            (r"from desktop\.modern\.src\.domain\.", "from domain."),
            (r"from desktop\.modern\.src\.application\.", "from application."),
            (r"from desktop\.modern\.src\.presentation\.", "from presentation."),
            (r"from desktop\.modern\.src\.core\.", "from core."),
            (r"from desktop\.modern\.src\.infrastructure\.", "from infrastructure."),
            # Rule 2: Fix src.desktop.modern.src imports to relative
            (r"from src\.desktop\.modern\.src\.domain\.", "from domain."),
            (r"from src\.desktop\.modern\.src\.application\.", "from application."),
            (r"from src\.desktop\.modern\.src\.presentation\.", "from presentation."),
            (r"from src\.desktop\.modern\.src\.core\.", "from core."),
            (
                r"from src\.desktop\.modern\.src\.infrastructure\.",
                "from infrastructure.",
            ),
            # Rule 3: Fix any remaining src. prefixed imports
            (r"from src\.application\.", "from application."),
            (r"from src\.domain\.", "from domain."),
            (r"from src\.presentation\.", "from presentation."),
            (r"from src\.core\.", "from core."),
            (r"from src\.infrastructure\.", "from infrastructure."),
        ]

    def find_python_files(self, root_dir: Path) -> List[Path]:
        """Find all Python files in the directory tree."""
        python_files = []
        for file_path in root_dir.rglob("*.py"):
            # Skip __pycache__ and .git directories
            if "__pycache__" in str(file_path) or ".git" in str(file_path):
                continue
            python_files.append(file_path)
        return sorted(python_files)

    def fix_imports_in_file(self, file_path: Path) -> bool:
        """Fix import patterns in a single file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content
            lines = content.split("\n")
            modified_lines = []
            changes_made = False

            for line in lines:
                modified_line = line
                for pattern, replacement in self.import_rules:
                    new_line = re.sub(pattern, replacement, modified_line)
                    if new_line != modified_line:
                        print(
                            f"  {file_path.name}: {modified_line.strip()} -> {new_line.strip()}"
                        )
                        modified_line = new_line
                        changes_made = True

                modified_lines.append(modified_line)

            if changes_made:
                new_content = "\n".join(modified_lines)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                return True

            return False

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False

    def fix_all_imports(self, root_dir: Path) -> Dict[str, int]:
        """Fix imports in all Python files in the directory."""
        print(f"🔧 Fixing imports in {root_dir}")

        python_files = self.find_python_files(root_dir)
        stats = {"total_files": len(python_files), "modified_files": 0, "errors": 0}

        for file_path in python_files:
            try:
                if self.fix_imports_in_file(file_path):
                    stats["modified_files"] += 1
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
                stats["errors"] += 1

        return stats


def main():
    """Main function to fix TKA import consistency."""
    print("🚀 TKA Relative Import Fixer")
    print("=" * 50)

    # Target the modern directory
    modern_dir = Path("src/desktop/modern")

    if not modern_dir.exists():
        print(f"❌ Directory {modern_dir} does not exist")
        sys.exit(1)

    fixer = TKARelativeImportFixer()
    stats = fixer.fix_all_imports(modern_dir)

    print("\n📊 Summary:")
    print(f"  Total files processed: {stats['total_files']}")
    print(f"  Files modified: {stats['modified_files']}")
    print(f"  Errors: {stats['errors']}")

    if stats["modified_files"] > 0:
        print(f"\n✅ Successfully fixed imports in {stats['modified_files']} files")
    else:
        print("\n✅ No import fixes needed - all files already use correct patterns")


if __name__ == "__main__":
    main()
