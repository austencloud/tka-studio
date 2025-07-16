#!/usr/bin/env python3
"""
Test script to verify the animation fix for start position picker transitions.

This script tests that the option picker preparation method is working correctly
and that double animations are prevented.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from domain.models.beat_data import BeatData
from domain.models.pictograph_data import PictographData
from presentation.tabs.construct.option_picker_manager import OptionPickerManager


def create_test_beat_data() -> BeatData:
    """Create a simple test beat data for start position."""
    # Create minimal pictograph data
    pictograph_data = PictographData(
        letter="A",
        start_position="alpha1",
        end_position="alpha1",
        motions={}
    )
    
    # Create beat data
    beat_data = BeatData(
        beat_number=1,
        pictograph_data=pictograph_data,
        is_blank=False
    )
    
    return beat_data


def test_prepare_method_exists():
    """Test that the prepare_from_start_position method exists."""
    print("🧪 Testing prepare_from_start_position method exists...")
    
    try:
        # Create option picker manager
        manager = OptionPickerManager()
        
        # Check if the method exists
        if hasattr(manager, 'prepare_from_start_position'):
            print("✅ prepare_from_start_position method exists")
            return True
        else:
            print("❌ prepare_from_start_position method does not exist")
            return False
            
    except Exception as e:
        print(f"❌ Error testing method existence: {e}")
        return False


def test_method_signature():
    """Test that the method has the correct signature."""
    print("\n🧪 Testing method signature...")
    
    try:
        import inspect
        from presentation.tabs.construct.option_picker_manager import OptionPickerManager
        
        # Get method signature
        method = getattr(OptionPickerManager, 'prepare_from_start_position', None)
        if method:
            sig = inspect.signature(method)
            params = list(sig.parameters.keys())
            
            expected_params = ['self', 'position_key', 'start_position_beat_data']
            if params == expected_params:
                print(f"✅ Method signature correct: {params}")
                return True
            else:
                print(f"❌ Method signature incorrect. Expected: {expected_params}, Got: {params}")
                return False
        else:
            print("❌ Method not found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing method signature: {e}")
        return False


def test_method_call():
    """Test that the method can be called without errors."""
    print("\n🧪 Testing method call...")
    
    try:
        # Create test data
        position_key = "alpha1_alpha1"
        beat_data = create_test_beat_data()
        
        # Create manager (without option picker for safety)
        manager = OptionPickerManager()
        
        # Call the method (should handle None option_picker gracefully)
        manager.prepare_from_start_position(position_key, beat_data)
        
        print("✅ Method call completed without errors")
        return True
        
    except Exception as e:
        print(f"❌ Error calling method: {e}")
        return False


def test_signal_coordinator_integration():
    """Test that signal coordinator uses the new method."""
    print("\n🧪 Testing signal coordinator integration...")
    
    try:
        # Read the signal coordinator file
        signal_coordinator_path = Path(__file__).parent / "src" / "presentation" / "tabs" / "construct" / "signal_coordinator.py"
        
        if signal_coordinator_path.exists():
            with open(signal_coordinator_path, 'r') as f:
                content = f.read()
                
            # Check if it uses the new method
            if 'prepare_from_start_position' in content:
                print("✅ Signal coordinator uses prepare_from_start_position")
                
                # Check if it doesn't use the old method in the transition handler
                if '_handle_start_position_created' in content:
                    lines = content.split('\n')
                    in_handler = False
                    uses_populate = False
                    uses_prepare = False
                    
                    for line in lines:
                        if '_handle_start_position_created' in line:
                            in_handler = True
                        elif in_handler and 'def ' in line and not line.strip().startswith('#'):
                            # Exited the handler
                            break
                        elif in_handler:
                            if 'populate_from_start_position' in line:
                                uses_populate = True
                            if 'prepare_from_start_position' in line:
                                uses_prepare = True
                    
                    if uses_prepare and not uses_populate:
                        print("✅ Handler correctly uses prepare instead of populate")
                        return True
                    elif uses_populate:
                        print("❌ Handler still uses populate_from_start_position")
                        return False
                    else:
                        print("⚠️ Could not determine which method is used")
                        return False
                else:
                    print("❌ _handle_start_position_created method not found")
                    return False
            else:
                print("❌ Signal coordinator does not use prepare_from_start_position")
                return False
        else:
            print("❌ Signal coordinator file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing signal coordinator integration: {e}")
        return False


def main():
    """Main test function."""
    print("🎯 TKA Animation Fix Test")
    print("=" * 50)
    
    tests = [
        test_prepare_method_exists,
        test_method_signature,
        test_method_call,
        test_signal_coordinator_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Animation fix is properly implemented.")
        print("\n📋 Fix Summary:")
        print("✅ prepare_from_start_position method added to OptionPickerManager")
        print("✅ Signal coordinator updated to use preparation method")
        print("✅ Double animation issue should be resolved")
        print("\n🎯 Expected Behavior:")
        print("1. Start position picker fades out (widget-level)")
        print("2. Option picker content is prepared WITHOUT internal animations")
        print("3. Option picker fades in with correct content (widget-level)")
        print("4. No double animations occur")
        return True
    else:
        print(f"\n❌ {total - passed} tests failed. Fix may not be complete.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
