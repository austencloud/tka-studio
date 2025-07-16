#!/usr/bin/env python3
"""
Test script to verify the StartPositionPicker can be imported and basic functionality works.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'desktop', 'modern', 'src'))

def test_start_position_picker_import():
    """Test that StartPositionPicker can be imported."""
    print("Testing StartPositionPicker import...")
    
    try:
        from presentation.components.start_position_picker.start_position_picker import StartPositionPicker
        print("✅ StartPositionPicker imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ StartPositionPicker import failed: {e}")
        return False

def test_picker_mode_enum():
    """Test that PickerMode enum can be imported."""
    print("Testing PickerMode enum...")
    
    try:
        from application.services.start_position.start_position_mode_service import PickerMode
        print(f"✅ PickerMode enum imported: {[mode.value for mode in PickerMode]}")
        return True
        
    except Exception as e:
        print(f"❌ PickerMode enum import failed: {e}")
        return False

def test_layout_mode_enum():
    """Test that LayoutMode enum can be imported."""
    print("Testing LayoutMode enum...")
    
    try:
        from application.services.start_position.start_position_layout_service import LayoutMode
        print(f"✅ LayoutMode enum imported: {[mode.value for mode in LayoutMode]}")
        return True
        
    except Exception as e:
        print(f"❌ LayoutMode enum import failed: {e}")
        return False

def test_service_dependencies():
    """Test that all required service dependencies can be imported."""
    print("Testing service dependencies...")
    
    services_to_test = [
        ("StartPositionStyleService", "application.services.start_position.start_position_style_service"),
        ("StartPositionLayoutService", "application.services.start_position.start_position_layout_service"),
        ("StartPositionModeService", "application.services.start_position.start_position_mode_service"),
    ]
    
    success_count = 0
    
    for service_name, module_path in services_to_test:
        try:
            module = __import__(module_path, fromlist=[service_name])
            service_class = getattr(module, service_name)
            # Try to instantiate the service
            service_instance = service_class()
            print(f"✅ {service_name} imported and instantiated successfully")
            success_count += 1
        except Exception as e:
            print(f"❌ {service_name} failed: {e}")
    
    return success_count == len(services_to_test)

def test_existing_interfaces():
    """Test that existing start position interfaces can be imported."""
    print("Testing existing interfaces...")
    
    try:
        from core.interfaces.start_position_services import (
            IStartPositionDataService,
            IStartPositionOrchestrator,
            IStartPositionSelectionService,
            IStartPositionUIService,
        )
        print("✅ All start position interfaces imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Interface import failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing StartPositionPicker Integration")
    print("=" * 50)
    
    tests = [
        test_picker_mode_enum,
        test_layout_mode_enum,
        test_service_dependencies,
        test_existing_interfaces,
        test_start_position_picker_import,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All imports working! StartPositionPicker is ready for service integration.")
    else:
        print("⚠️ Some imports failed. Need to fix dependencies before proceeding.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
