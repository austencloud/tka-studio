#!/usr/bin/env python3
"""
Test Runner for Improved Architecture

This script runs all tests to verify that the clumsy workbench_getter/workbench_setter 
pattern has been successfully eliminated and replaced with proper dependency injection 
using IWorkbenchStateManager.

Usage:
    python run_improved_architecture_tests.py

Expected Results:
    ✅ All services use IWorkbenchStateManager instead of getter/setter functions
    ✅ Workbench properly implements WorkbenchProtocol
    ✅ Construct tab connects workbench to state manager
    ✅ Qt adapters use clean dependency injection
    ✅ Architecture is more testable, type-safe, and maintainable
"""

import sys
import os
import unittest
import subprocess

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def run_tests():
    """Run all tests for the improved architecture."""
    
    print("🚀 Running Improved Architecture Test Suite")
    print("=" * 60)
    print("🎯 Goal: Verify elimination of clumsy getter/setter pattern")
    print("✨ Expected: Clean dependency injection with IWorkbenchStateManager")
    print()
    
    # Test files to run
    test_files = [
        'test_improved_architecture.py',
        'test_construct_tab_integration.py'
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_file in test_files:
        print(f"📋 Running {test_file}...")
        print("-" * 40)
        
        try:
            # Discover and run tests in the file
            loader = unittest.TestLoader()
            start_dir = os.path.dirname(__file__)
            suite = loader.discover(start_dir, pattern=test_file)
            
            # Run the tests
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            
            # Track results
            total_tests += result.testsRun
            failed_tests += len(result.failures) + len(result.errors)
            passed_tests = total_tests - failed_tests
            
            if result.wasSuccessful():
                print(f"✅ {test_file} - ALL TESTS PASSED")
            else:
                print(f"❌ {test_file} - SOME TESTS FAILED")
                for failure in result.failures:
                    print(f"   FAILURE: {failure[0]}")
                for error in result.errors:
                    print(f"   ERROR: {error[0]}")
            
            print()
            
        except Exception as e:
            print(f"❌ Error running {test_file}: {e}")
            failed_tests += 1
            print()
    
    # Print summary
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print()
    
    if failed_tests == 0:
        print("🎉 SUCCESS! Improved architecture is working correctly!")
        print("✅ Clumsy getter/setter pattern eliminated")
        print("✅ Clean dependency injection implemented")
        print("✅ Type-safe interfaces in use")
        print("✅ Better testability achieved")
        print("✅ Loose coupling established")
        return True
    else:
        print("⚠️ Some tests failed. Please review the architecture changes.")
        return False


def check_imports():
    """Check that the improved imports are working."""
    print("🔍 Checking imports...")
    
    try:
        # Test core service imports
        from shared.application.services.sequence.sequence_loader_service import SequenceLoaderService
        from shared.application.services.sequence.sequence_beat_operations_service import SequenceBeatOperationsService
        print("✅ Core services import correctly")
        
        # Test adapter imports  
        from desktop.modern.presentation.adapters.qt.sequence_loader_adapter import QtSequenceLoaderAdapter
        from desktop.modern.presentation.adapters.qt.sequence_beat_operations_adapter import QtSequenceBeatOperationsAdapter
        print("✅ Qt adapters import correctly")
        
        # Test interface imports
        from desktop.modern.core.interfaces.workbench_services import IWorkbenchStateManager
        print("✅ Workbench interfaces import correctly")
        
        # Test construct tab imports
        from desktop.modern.presentation.tabs.construct.layout_manager import ConstructTabLayoutManager
        print("✅ Construct tab imports correctly")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def verify_architecture_changes():
    """Verify that the architecture changes are present in the code."""
    print("🔍 Verifying architecture changes in source code...")
    
    # Check that services no longer use getter/setter pattern
    try:
        from shared.application.services.sequence.sequence_loader_service import SequenceLoaderService
        service = SequenceLoaderService.__init__.__code__.co_varnames
        
        if 'workbench_state_manager' in service:
            print("✅ SequenceLoaderService uses workbench_state_manager")
        else:
            print("❌ SequenceLoaderService doesn't use workbench_state_manager")
            return False
            
        if 'workbench_getter' in service or 'workbench_setter' in service:
            print("❌ SequenceLoaderService still has old getter/setter pattern")
            return False
        else:
            print("✅ SequenceLoaderService getter/setter pattern eliminated")
            
    except Exception as e:
        print(f"❌ Error checking SequenceLoaderService: {e}")
        return False
    
    return True


if __name__ == '__main__':
    print("🧪 IMPROVED ARCHITECTURE TEST RUNNER")
    print("====================================")
    print()
    
    # Step 1: Check imports
    if not check_imports():
        print("❌ Import check failed. Please ensure all modules are properly updated.")
        sys.exit(1)
    
    print()
    
    # Step 2: Verify architecture changes
    if not verify_architecture_changes():
        print("❌ Architecture verification failed. Please review the code changes.")
        sys.exit(1)
    
    print()
    
    # Step 3: Run tests
    success = run_tests()
    
    if success:
        print()
        print("🎊 CONGRATULATIONS! 🎊")
        print("The improved architecture is working perfectly!")
        print("You have successfully eliminated the clumsy getter/setter pattern!")
        sys.exit(0)
    else:
        print()
        print("💡 Some tests failed, but this might be expected during development.")
        print("Please review the test output and fix any remaining issues.")
        sys.exit(1)
