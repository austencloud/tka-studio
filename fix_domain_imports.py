#!/usr/bin/env python3
"""
Test and fix domain models import
"""

import sys
import os
import shutil
from pathlib import Path

def clean_python_cache():
    """Clean Python cache files"""
    print("🧹 Cleaning Python cache...")
    
    base_path = Path("F:/CODE/TKA/src/desktop/modern/src/domain")
    
    # Remove __pycache__ directories
    for pycache_dir in base_path.rglob("__pycache__"):
        if pycache_dir.is_dir():
            print(f"  Removing {pycache_dir}")
            shutil.rmtree(pycache_dir)
    
    # Remove .pyc files
    for pyc_file in base_path.rglob("*.pyc"):
        print(f"  Removing {pyc_file}")
        pyc_file.unlink()
    
    print("✅ Cache cleaned!")

def test_imports():
    """Test the domain models imports"""
    print("🔍 Testing domain models imports...")
    
    # Add path
    sys.path.insert(0, 'F:/CODE/TKA/src/desktop/modern/src')
    
    try:
        # Test basic core models import
        from domain.models.core_models import (
            Location,
            MotionData, 
            MotionType,
            Orientation,
            RotationDirection,
        )
        print("✅ Core models import successful!")
        print(f"  MotionType.PRO = {MotionType.PRO}")
        print(f"  Location.NORTH = {Location.NORTH}")
        
        # Test package import 
        from domain.models import MotionType as MT2
        print("✅ Package import successful!")
        print(f"  Package MotionType.PRO = {MT2.PRO}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Domain Models Import Fix")
    print("=" * 40)
    
    # Clean cache first
    clean_python_cache()
    
    # Test imports
    if test_imports():
        print("\n🎉 SUCCESS! Domain models are working correctly.")
        print("You can now run your TKA application.")
    else:
        print("\n❌ FAILED! There are still import issues.")
        print("Check the error messages above for details.")
