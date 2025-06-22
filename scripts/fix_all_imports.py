#!/usr/bin/env python3
"""
TKA All Files Import Fixer
==========================

Fixes import paths for ALL Python files in the TKA structure.

Usage:
    python scripts/fix_all_imports.py [--dry-run] [--verbose]
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Set


class AllImportFixer:
    """Fixes import statements in all Python files for correct TKA structure."""

    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.fixes_applied = 0
        self.files_processed = 0

        # Define import transformation rules for correct TKA structure
        self.import_rules = [
            # Rule 1: Fix relative imports to absolute desktop.modern.src imports
            (r"^from domain\.", "from desktop.modern.src.domain."),
            (r"^from application\.", "from desktop.modern.src.application."),
            (r"^from presentation\.", "from desktop.modern.src.presentation."),
            (r"^from core\.", "from desktop.modern.src.core."),
            (r"^from infrastructure\.", "from desktop.modern.src.infrastructure."),
            # Rule 2: Fix src. prefixed imports
            (r"^from src\.application\.", "from desktop.modern.src.application."),
            (r"^from src\.domain\.", "from desktop.modern.src.domain."),
            (r"^from src\.presentation\.", "from desktop.modern.src.presentation."),
            (r"^from src\.core\.", "from desktop.modern.src.core."),
            (r"^from src\.infrastructure\.", "from desktop.modern.src.infrastructure."),
            # Rule 3: Fix tka.desktop imports to desktop.modern.src imports
            (r"^from tka\.desktop\.", "from desktop.modern.src."),
        ]

    def find_python_files(self, root_dir: Path) -> List[Path]:
        """Find all Python files."""
        python_files = []
        for file_path in root_dir.rglob("*.py"):
            # Skip __pycache__ and .git directories
            if "__pycache__" in str(file_path) or ".git" in str(file_path):
                continue
            python_files.append(file_path)
        return sorted(python_files)

    def analyze_file(self, file_path: Path) -> Tuple[List[str], List[str], bool]:
        """Analyze a file and return original lines, fixed lines, and whether changes were made."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_lines = f.readlines()
        except Exception as e:
            if self.verbose:
                print(f"Error reading {file_path}: {e}")
            return [], [], False

        fixed_lines = []
        changes_made = False

        for line_num, line in enumerate(original_lines, 1):
            original_line = line
            fixed_line = line

            # Apply import transformation rules
            for pattern, replacement in self.import_rules:
                new_line = re.sub(pattern, replacement, fixed_line)
                if new_line != fixed_line:
                    fixed_line = new_line
                    changes_made = True
                    if self.verbose:
                        print(
                            f"  Import fix at line {line_num}: {original_line.strip()} -> {fixed_line.strip()}"
                        )

            fixed_lines.append(fixed_line)

        return original_lines, fixed_lines, changes_made

    def fix_file(self, file_path: Path) -> bool:
        """Fix imports in a single file. Returns True if changes were made."""
        if self.verbose:
            print(f"\nProcessing: {file_path}")

        original_lines, fixed_lines, changes_made = self.analyze_file(file_path)

        if not changes_made:
            if self.verbose:
                print(f"  No changes needed")
            return False

        if self.dry_run:
            print(f"DRY RUN: Would fix {file_path}")
            return True

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(fixed_lines)
            print(f"Fixed: {file_path}")
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False

    def fix_all_files(self, root_dir: Path = None) -> None:
        """Fix imports in all Python files."""
        if root_dir is None:
            root_dir = Path.cwd()

        print(f"Scanning for Python files in: {root_dir}")
        python_files = self.find_python_files(root_dir)

        if not python_files:
            print("No Python files found!")
            return

        print(f"Found {len(python_files)} Python files")

        if self.dry_run:
            print("DRY RUN MODE - No files will be modified")

        for file_path in python_files:
            self.files_processed += 1
            if self.fix_file(file_path):
                self.fixes_applied += 1

        print(f"\nSummary:")
        print(f"   Files processed: {self.files_processed}")
        print(f"   Files fixed: {self.fixes_applied}")
        print(f"   Files unchanged: {self.files_processed - self.fixes_applied}")

        if self.dry_run:
            print(f"\nRun without --dry-run to apply fixes")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fix import paths in all TKA Python files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed information about changes",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd() / "src",
        help="Root directory to scan for Python files",
    )

    args = parser.parse_args()

    print("TKA All Files Import Fixer")
    print("=" * 50)

    fixer = AllImportFixer(dry_run=args.dry_run, verbose=args.verbose)
    fixer.fix_all_files(args.root)


if __name__ == "__main__":
    main()
