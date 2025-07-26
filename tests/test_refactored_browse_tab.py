#!/usr/bin/env python3
"""
Test script for the refactored Browse tab.

This script tests the basic functionality of the refactored Browse tab
to ensure the manager-based architecture works correctly.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

def test_browse_tab_imports():
    """Test that all Browse tab components can be imported."""
    print("🧪 Testing Browse tab imports...")
    
    try:
        from desktop.modern.presentation.tabs.browse import BrowseTab
        print("✅ BrowseTab import successful")
        
        from desktop.modern.presentation.tabs.browse.managers import (
            BrowseTabController,
            BrowseDataManager,
            BrowseActionHandler,
            BrowseNavigationManager,
            BrowsePanel,
        )
        print("✅ All manager classes import successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_browse_tab_instantiation():
    """Test that Browse tab can be instantiated."""
    print("🧪 Testing Browse tab instantiation...")
    
    try:
        from desktop.modern.presentation.tabs.browse import BrowseTab
        from desktop.modern.core.dependency_injection.di_container import DIContainer
        from pathlib import Path
        
        # Create test parameters
        sequences_dir = Path("data/sequences")
        settings_file = Path("settings.json")
        container = DIContainer()
        
        # This should not fail even if directories don't exist
        browse_tab = BrowseTab(
            sequences_dir=sequences_dir,
            settings_file=settings_file,
            container=container,
        )
        
        print("✅ BrowseTab instantiation successful")
        print(f"📋 BrowseTab type: {type(browse_tab)}")
        
        # Check if controller was created
        if hasattr(browse_tab, 'controller'):
            print(f"📋 Controller type: {type(browse_tab.controller)}")
        else:
            print("⚠️ Controller not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Instantiation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_manager_classes():
    """Test that manager classes can be instantiated."""
    print("🧪 Testing manager class instantiation...")
    
    try:
        from desktop.modern.presentation.tabs.browse.managers import (
            BrowseDataManager,
            BrowseNavigationManager,
        )
        from PyQt6.QtWidgets import QApplication, QStackedWidget
        from pathlib import Path
        
        # Create minimal Qt application
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Test BrowseDataManager
        data_dir = Path("data")
        data_manager = BrowseDataManager(data_dir)
        print("✅ BrowseDataManager instantiation successful")
        
        # Test BrowseNavigationManager
        stacked_widget = QStackedWidget()
        nav_manager = BrowseNavigationManager(stacked_widget)
        print("✅ BrowseNavigationManager instantiation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Manager class test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 Starting refactored Browse tab tests...")
    
    tests = [
        test_browse_tab_imports,
        test_browse_tab_instantiation,
        test_manager_classes,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("✅ Test passed\n")
            else:
                print("❌ Test failed\n")
        except Exception as e:
            print(f"❌ Test error: {e}\n")
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Refactoring appears successful.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
