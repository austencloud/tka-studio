#!/usr/bin/env python3
"""
Auto line length fixer using autopep8
This script can be run manually or integrated into VS Code
"""
import subprocess
import sys
from pathlib import Path


def fix_line_length(file_path):
    """Fix line length issues in a Python file using autopep8."""
    try:
        # Use autopep8 to fix only line length issues
        result = subprocess.run([
            sys.executable, '-m', 'autopep8',
            '--in-place',
            '--select=E501',
            '--max-line-length=88',
            '--aggressive',
            str(file_path)
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✅ Fixed line length issues in {file_path}")
        else:
            print(f"❌ Error fixing {file_path}: {result.stderr}")

    except FileNotFoundError:
        print("❌ autopep8 not found. Please install it with: pip install autopep8")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_line_length.py <python_file>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    if not file_path.suffix == '.py':
        print(f"❌ Not a Python file: {file_path}")
        sys.exit(1)

    fix_line_length(file_path)

if __name__ == "__main__":
    main()
