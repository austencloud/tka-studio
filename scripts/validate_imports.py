#!/usr/bin/env python3
"""
Import consistency validation for TKA codebase.
Prevents enum object identity issues by enforcing SSOT imports.

Usage:
    python scripts/validate_imports.py                    # Validate all files
    python scripts/validate_imports.py --fix             # Auto-fix violations
    python scripts/validate_imports.py --check-file path # Check specific file
"""

import ast
import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Canonical import locations (Single Source of Truth)
# Updated for modern clean import pattern
CANONICAL_IMPORTS = {
    "Location": "domain.models.core_models",
    "MotionType": "domain.models.core_models",
    "RotationDirection": "domain.models.core_models",
    "Orientation": "domain.models.core_models",
    "BeatData": "domain.models.core_models",
    "SequenceData": "domain.models.core_models",
    "MotionData": "domain.models.core_models",
    "ArrowData": "domain.models.pictograph_models",
    "PictographData": "domain.models.pictograph_models",
    "GridData": "domain.models.pictograph_models",
    "GridMode": "domain.models.pictograph_models",
}

# Forbidden import sources that cause enum identity issues
FORBIDDEN_SOURCES = {
    "data.types",
    "packages.shared-types.python.tka_types",
    "tka_types",
    "desktop.modern.src.infrastructure.api.models",
}

# Import replacements for auto-fix
IMPORT_REPLACEMENTS = {
    r"from data\.types import (Location|MotionType|RotationDirection)": r"from desktop.modern.src.domain.models.core_models import \1",
    r"from packages\.shared-types\.python\.tka_types import (Location|MotionType|RotationDirection)": r"from desktop.modern.src.domain.models.core_models import \1",
    r"from tka_types import (Location|MotionType|RotationDirection)": r"from desktop.modern.src.domain.models.core_models import \1",
}


class ImportViolation:
    def __init__(
        self, file_path: Path, line_number: int, message: str, severity: str = "ERROR"
    ):
        self.file_path = file_path
        self.line_number = line_number
        self.message = message
        self.severity = severity

    def __str__(self):
        return f"{self.file_path}:{self.line_number} [{self.severity}] {self.message}"


def validate_file_imports(file_path: Path) -> List[ImportViolation]:
    """Validate imports in a single file."""
    violations = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            tree = ast.parse(content)
    except Exception as e:
        return [ImportViolation(file_path, 0, f"Failed to parse: {e}", "ERROR")]

    lines = content.split("\n")

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            line_content = lines[node.lineno - 1] if node.lineno <= len(lines) else ""

            # Check for forbidden sources
            if module in FORBIDDEN_SOURCES:
                violations.append(
                    ImportViolation(
                        file_path,
                        node.lineno,
                        f"Forbidden import from '{module}' - causes enum identity issues",
                        "ERROR",
                    )
                )

            # Check for canonical import violations
            for alias in node.names:
                name = alias.name
                if name in CANONICAL_IMPORTS:
                    expected_module = CANONICAL_IMPORTS[name]
                    if module != expected_module and not _is_relative_equivalent(
                        module, expected_module, file_path
                    ):
                        violations.append(
                            ImportViolation(
                                file_path,
                                node.lineno,
                                f"'{name}' should be imported from '{expected_module}', not '{module}'",
                                "ERROR",
                            )
                        )

    return violations


def _is_relative_equivalent(
    actual_module: str, expected_module: str, file_path: Path
) -> bool:
    """Check if relative import is equivalent to expected absolute import."""
    # Allow relative imports within desktop.modern.src
    if "desktop/modern/src" in str(file_path) or "desktop\\modern\\src" in str(
        file_path
    ):
        # The actual module should match the expected module exactly for clean imports
        return actual_module == expected_module
    return False


def fix_file_imports(file_path: Path) -> bool:
    """Fix import statements in a file. Returns True if changes were made."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        for pattern, replacement in IMPORT_REPLACEMENTS.items():
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True

    except Exception as e:
        print(f"❌ Failed to fix {file_path}: {e}")

    return False


def scan_directory(
    directory: Path, exclude_patterns: Set[str] = None
) -> List[ImportViolation]:
    """Scan directory for import violations."""
    if exclude_patterns is None:
        exclude_patterns = {
            ".git",
            "__pycache__",
            ".pytest_cache",
            "node_modules",
            ".venv",
            "venv",
        }

    violations = []

    for root, dirs, files in os.walk(directory):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_patterns]

        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                violations.extend(validate_file_imports(file_path))

    return violations


def print_summary(violations: List[ImportViolation]):
    """Print summary of violations."""
    if not violations:
        print("✅ All imports are consistent - no enum identity issues detected!")
        return

    print(f"❌ Found {len(violations)} import consistency violations:")
    print()

    # Group by severity
    errors = [v for v in violations if v.severity == "ERROR"]
    warnings = [v for v in violations if v.severity == "WARNING"]

    if errors:
        print(f"🚨 ERRORS ({len(errors)}):")
        for violation in errors:
            print(f"  {violation}")
        print()

    if warnings:
        print(f"⚠️  WARNINGS ({len(warnings)}):")
        for violation in warnings:
            print(f"  {violation}")
        print()

    # Group by file for easier fixing
    files_with_violations = {}
    for violation in violations:
        if violation.file_path not in files_with_violations:
            files_with_violations[violation.file_path] = []
        files_with_violations[violation.file_path].append(violation)

    print(f"📁 Files affected: {len(files_with_violations)}")
    for file_path, file_violations in files_with_violations.items():
        print(f"  {file_path} ({len(file_violations)} violations)")


def main():
    parser = argparse.ArgumentParser(description="Validate TKA import consistency")
    parser.add_argument(
        "--fix", action="store_true", help="Auto-fix violations where possible"
    )
    parser.add_argument("--check-file", type=str, help="Check specific file")
    parser.add_argument(
        "--directory",
        type=str,
        default=".",
        help="Directory to scan (default: current)",
    )

    args = parser.parse_args()

    if args.check_file:
        # Check specific file
        file_path = Path(args.check_file)
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            sys.exit(1)

        violations = validate_file_imports(file_path)
        print_summary(violations)

        if violations:
            sys.exit(1)
    else:
        # Scan directory
        directory = Path(args.directory)
        if not directory.exists():
            print(f"❌ Directory not found: {directory}")
            sys.exit(1)

        print(f"🔍 Scanning {directory} for import consistency violations...")
        violations = scan_directory(directory)

        if args.fix:
            print("\n🔧 Attempting to auto-fix violations...")
            fixed_files = 0

            # Get unique files with violations
            files_to_fix = set(v.file_path for v in violations)

            for file_path in files_to_fix:
                if fix_file_imports(file_path):
                    print(f"✅ Fixed imports in {file_path}")
                    fixed_files += 1

            print(f"\n📊 Auto-fixed {fixed_files} files")

            # Re-scan to check remaining violations
            print("\n🔍 Re-scanning for remaining violations...")
            violations = scan_directory(directory)

        print_summary(violations)

        if violations:
            print("\n💡 To fix remaining violations:")
            print("  1. Review the violations above")
            print("  2. Update imports to use canonical paths")
            print("  3. Run this script again to verify fixes")
            print("\n📖 See docs/architecture/import-consistency-guide.md for details")
            sys.exit(1)


if __name__ == "__main__":
    main()
