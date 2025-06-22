"""
TKA Modern Desktop Test Configuration
====================================

This conftest.py file sets up the test environment for the TKA Modern Desktop application.
It ensures proper Python path configuration for relative imports and provides common fixtures.
"""

import sys
from pathlib import Path

# Add the src directory to Python path for relative imports
# This allows tests to use: from domain.models.core_models import BeatData
modern_root = Path(__file__).parent.parent
src_path = modern_root / "src"
sys.path.insert(0, str(src_path))

# Verify the path setup works
try:
    from domain.models.core_models import BeatData
    print(f"✅ TKA Modern test environment configured successfully")
    print(f"   Source path: {src_path}")
except ImportError as e:
    print(f"❌ Failed to configure TKA Modern test environment: {e}")
    print(f"   Source path: {src_path}")
    print(f"   Current sys.path: {sys.path[:3]}...")
