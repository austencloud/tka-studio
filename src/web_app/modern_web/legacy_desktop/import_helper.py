from __future__ import annotations
# This file ensures VS Code and Pylance can resolve imports for the legacy codebase
# Import this at the top of any legacy Python file if VS Code shows import errors

import os
import sys


def setup_legacy_imports():
    """Configure import paths for the legacy codebase."""
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Find the legacy root directory
    legacy_root = current_dir
    while legacy_root and not os.path.exists(os.path.join(legacy_root, "main.py")):
        parent = os.path.dirname(legacy_root)
        if parent == legacy_root:  # Reached filesystem root
            break
        legacy_root = parent

    # Add the src directory to Python path
    src_dir = os.path.join(legacy_root, "src")
    if os.path.exists(src_dir) and src_dir not in sys.path:
        sys.path.insert(0, src_dir)
        return src_dir

    return None


# Auto-configure paths when this module is imported
if __name__ != "__main__":
    setup_legacy_imports()
