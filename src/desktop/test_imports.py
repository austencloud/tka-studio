#!/usr/bin/env python3
"""Test script to verify that all migrated services can be imported successfully."""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all migrated services can be imported."""
    try:
        print("Testing infrastructure services...")
        from desktop.modern.infrastructure.path_resolver import path_resolver, TKAPathResolver
        print("✅ Path resolver imported successfully")
        
        print("Testing core types...")
        from desktop.modern.application.services.core.types import Point, Size
        print("✅ Core types imported successfully")
        
        print("Testing sequence services...")
        from desktop.modern.application.services.sequence.beat_factory import BeatFactory
        from desktop.modern.application.services.sequence.sequence_persister import SequencePersister
        print("✅ Sequence services imported successfully")
        
        print("Testing data services...")
        from desktop.modern.application.services.data.data_service import DataManager
        from desktop.modern.application.services.data.modern_to_legacy_converter import ModernToLegacyConverter
        from desktop.modern.application.services.data.legacy_to_modern_converter import LegacyToModernConverter
        from desktop.modern.application.services.data.position_attribute_mapper import PositionAttributeMapper
        print("✅ Data services imported successfully")
        
        print("\n🎉 All migrated services imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)