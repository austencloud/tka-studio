#!/usr/bin/env python3
"""
Test runner for dependency injection unit tests.

Run this script to verify that the pictograph services are properly using
dependency injection and are testable in isolation.
"""

import sys
import os
import unittest
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def run_dependency_injection_tests():
    """Run the dependency injection tests and report results."""
    print("🧪 Running Dependency Injection Tests")
    print("=" * 50)
    
    # Discover and run tests
    test_dir = Path(__file__).parent / "tests" / "services" / "pictograph"
    loader = unittest.TestLoader()
    
    try:
        # Load the specific test module
        suite = loader.discover(str(test_dir), pattern="test_dependency_injection.py")
        
        # Run tests with detailed output
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 Test Summary:")
        print(f"   Tests run: {result.testsRun}")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
        print(f"   Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
        
        if result.wasSuccessful():
            print("✅ All dependency injection tests passed!")
            print("\n🎯 Benefits Demonstrated:")
            print("   • Services can be tested in isolation")
            print("   • Dependencies can be mocked for unit testing")
            print("   • Different implementations can be swapped at runtime")
            print("   • Error handling is properly isolated")
            return True
        else:
            print("❌ Some tests failed!")
            if result.failures:
                print("\n💥 Failures:")
                for test, traceback in result.failures:
                    print(f"   {test}: {traceback}")
            if result.errors:
                print("\n🚨 Errors:")
                for test, traceback in result.errors:
                    print(f"   {test}: {traceback}")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def check_test_environment():
    """Check that the test environment is properly set up."""
    print("🔍 Checking test environment...")
    
    # Check if test directory exists
    test_file = Path(__file__).parent / "tests" / "services" / "pictograph" / "test_dependency_injection.py"
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return False
    
    # Check if src directory exists
    src_dir = Path(__file__).parent / "src"
    if not src_dir.exists():
        print(f"❌ Source directory not found: {src_dir}")
        return False
    
    print("✅ Test environment looks good!")
    return True


def main():
    """Main test runner function."""
    print("🚀 Dependency Injection Test Runner")
    print("Testing the refactored pictograph services\n")
    
    # Check environment
    if not check_test_environment():
        print("❌ Test environment check failed!")
        sys.exit(1)
    
    # Run tests
    success = run_dependency_injection_tests()
    
    if success:
        print("\n🎉 All tests passed! The dependency injection refactoring is working correctly.")
        sys.exit(0)
    else:
        print("\n💔 Some tests failed. Please check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
