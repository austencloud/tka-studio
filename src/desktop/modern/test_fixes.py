#!/usr/bin/env python3
"""
Quick test script to verify the immediate fixes for service locator and import errors.
"""

import sys
from pathlib import Path

# Add the src directory to the path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

def test_service_locator_fix():
    """Test that the service locator global variable issue is fixed"""
    try:
        print("🧪 Testing service locator import...")
        from core.service_locator import get_data_conversion_service
        
        # This should not raise the global variable error anymore
        service = get_data_conversion_service()
        print("✅ Service locator import test PASSED")
        return True
    except Exception as e:
        print(f"❌ Service locator import test FAILED: {e}")
        return False

def test_start_position_picker_import():
    """Test that the start position picker can be imported without module errors"""
    try:
        print("🧪 Testing start position picker import...")
        from presentation.components.start_position_picker.start_position_picker import StartPositionPicker
        print("✅ Start position picker import test PASSED")
        return True
    except Exception as e:
        print(f"❌ Start position picker import test FAILED: {e}")
        return False

def test_command_imports():
    """Test that command imports work"""
    try:
        print("🧪 Testing command imports...")
        from core.commands.start_position_commands import SetStartPositionCommand
        from core.commands.sequence_commands import AddBeatCommand
        print("✅ Command imports test PASSED")
        return True
    except Exception as e:
        print(f"❌ Command imports test FAILED: {e}")
        return False

def run_quick_tests():
    """Run quick tests to verify the fixes"""
    print("🚀 Running quick tests to verify fixes...")
    
    tests = [
        ("Service Locator Fix", test_service_locator_fix),
        ("Start Position Picker Import", test_start_position_picker_import),
        ("Command Imports", test_command_imports),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"Testing: {test_name}")
        print(f"{'='*40}")
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Report results
    print(f"\n{'='*40}")
    print("QUICK TEST RESULTS")
    print(f"{'='*40}")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All quick tests PASSED! Fixes are working.")
        return True
    else:
        print(f"💥 {total - passed} tests FAILED. More fixes needed.")
        return False

if __name__ == "__main__":
    try:
        success = run_quick_tests()
        if success:
            print("\n🚀 Ready to test the full application!")
            print("   Try running the app again to see if the errors are resolved.")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"💥 Quick test suite crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
