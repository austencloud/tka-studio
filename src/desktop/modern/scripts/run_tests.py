#!/usr/bin/env python3
"""
TKA Modern Desktop Test Runner

This script runs pytest with the correct PYTHONPATH configuration for the TKA Modern Desktop application.
It automatically sets up the environment and provides convenient test filtering options.

Usage:
    python run_tests.py                    # Run all working tests (excludes PyQt6 crashes)
    python run_tests.py --all              # Run all tests (including problematic ones)
    python run_tests.py --domain           # Run only domain tests
    python run_tests.py --core             # Run only core tests
    python run_tests.py --unit             # Run only unit tests
    python run_tests.py --integration      # Run only integration tests
    python run_tests.py --specification    # Run only specification tests
    python run_tests.py --fast             # Run only fast tests (exclude slow ones)
    python run_tests.py --collect          # Just collect tests, don't run them
    python run_tests.py --help             # Show pytest help
"""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


def setup_environment():
    """Set up the Python path for TKA Modern Desktop."""
    # Get the directory containing this script (should be the modern directory root)
    modern_root = Path(__file__).parent.absolute()
    src_path = modern_root / "src"

    # Add src to PYTHONPATH
    current_pythonpath = os.environ.get("PYTHONPATH", "")
    if current_pythonpath:
        os.environ["PYTHONPATH"] = f"{src_path}{os.pathsep}{current_pythonpath}"
    else:
        os.environ["PYTHONPATH"] = str(src_path)

    # Change to the modern directory root
    os.chdir(modern_root)

    print(f"✓ Set PYTHONPATH to: {src_path}")
    print(f"✓ Working directory: {modern_root}")


def get_pytest_args(args):
    """Convert script arguments to pytest arguments."""
    pytest_args = ["python", "-m", "pytest"]

    # Default arguments for better output
    pytest_args.extend(["--tb=short", "-v"])

    # Handle special argument combinations
    if "--all" in args:
        # Run all tests including problematic ones
        pass
    elif "--collect" in args:
        pytest_args.extend(["--collect-only", "-q"])
    elif "--domain" in args:
        pytest_args.append("tests/specification/domain/")
    elif "--core" in args:
        pytest_args.append("tests/specification/core/")
    elif "--unit" in args:
        pytest_args.append("tests/unit/")
    elif "--integration" in args:
        pytest_args.append("tests/integration/")
    elif "--specification" in args:
        pytest_args.append("tests/specification/")
    elif "--fast" in args:
        pytest_args.extend(["-m", "not slow"])
    elif "--help" in args:
        pytest_args.append("--help")
    else:
        # Default: run working tests (exclude PyQt6 crashes and problematic imports)
        exclude_patterns = []
        pytest_args.extend(exclude_patterns)

    # Add any remaining arguments
    for arg in args:
        if not arg.startswith("--") or arg in ["--help", "--collect"]:
            continue
        if arg not in [
            "--all",
            "--domain",
            "--core",
            "--unit",
            "--integration",
            "--specification",
            "--fast",
        ]:
            pytest_args.append(arg)

    return pytest_args


def main():
    """Main entry point."""
    args = sys.argv[1:]

    print("🧪 TKA Modern Desktop Test Runner")
    print("=" * 50)

    # Set up environment
    setup_environment()

    # Get pytest arguments
    pytest_args = get_pytest_args(args)

    print(f"🚀 Running: {' '.join(pytest_args)}")
    print("=" * 50)

    # Run pytest
    try:
        result = subprocess.run(pytest_args, check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("\n❌ Test run interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
