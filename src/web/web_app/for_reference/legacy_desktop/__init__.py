from __future__ import annotations
"""
Legacy TKA source code package.

This package contains the legacy implementation of The Kinetic Alphabet.
All imports should work relative to this src directory.
"""

# Ensure imports work by adding src to path if needed
import os
import sys

_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)
