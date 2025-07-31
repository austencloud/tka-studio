#!/usr/bin/env python3
"""
TKA Paths - Legacy Compatibility Wrapper
========================================

This file maintains backward compatibility for existing imports of tka_paths.

WARNING: This is a compatibility layer. New code should import from:
    from src.infrastructure.paths import tka_paths

This file will be removed in a future version.
"""

from pathlib import Path
import sys
import warnings

# Add src to path to enable the new import
_tka_root = Path(__file__).parent
_src_path = str(_tka_root / "src")
if _src_path not in sys.path:
    sys.path.insert(0, _src_path)

# Issue deprecation warning
warnings.warn(
    "Importing 'tka_paths' from root is deprecated. "
    "Use 'from src.infrastructure.paths import tka_paths' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Ensure automatic setup still works
# Import and re-export everything from the new location
from src.infrastructure.paths.tka_paths import *  # noqa: F403, F401
from src.infrastructure.paths.tka_paths import setup_all_paths

setup_all_paths(verbose=False)
