#!/usr/bin/env python3
"""
Runner script for TKA Legacy Desktop Application.

This script provides a convenient way to run the legacy desktop app from the project root.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Change to the legacy app directory and run it
legacy_dir = project_root / "src" / "desktop" / "legacy"
os.chdir(legacy_dir)

# Import and run the legacy app main module
if __name__ == "__main__":
    # Import the main module from the legacy app
    sys.path.insert(0, str(legacy_dir))
    from main import main

    main()
