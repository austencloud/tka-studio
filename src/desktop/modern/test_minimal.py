#!/usr/bin/env python3
"""
Minimal test to check if our simplified components work
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_minimal():
    """Minimal test."""
    
    print("🧪 Minimal Test Starting...")
    
    try:
        print("📦 Testing imports...")
        
        # Test basic imports
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QSize
        print("✅ PyQt6 imports successful")
        
        # Test our types
        from presentation.components.option_picker.types.letter_types import LetterType
        print("✅ LetterType import successful")
        print(f"📋 Letter types: {LetterType.ALL_TYPES}")
        
        # Test our simplified components one by one
        print("📦 Testing SimplifiedOptionFactory...")
        from presentation.components.option_picker.core.simplified_option_factory import SimplifiedOptionFactory
        print("✅ SimplifiedOptionFactory import successful")
        
        print("📦 Testing SimplifiedOptionPickerWidget...")
        from presentation.components.option_picker.core.simplified_option_picker_widget import SimplifiedOptionPickerWidget
        print("✅ SimplifiedOptionPickerWidget import successful")
        
        print("🎉 All imports successful!")
        return 0
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = test_minimal()
    sys.exit(exit_code)
