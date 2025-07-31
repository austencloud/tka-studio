#!/usr/bin/env python3
"""
Test script for Browse tab manager logic.

This script tests the business logic of the manager classes
without requiring Qt widgets.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))


def test_browse_data_manager_logic():
    """Test BrowseDataManager logic without Qt dependencies."""
    print("🧪 Testing BrowseDataManager logic...")

    try:
        from desktop.modern.presentation.views.browse.managers import BrowseDataManager
        from desktop.modern.presentation.views.browse.models import FilterType

        # Create test data directory
        data_dir = Path("data")

        # This should work even if directory doesn't exist
        data_manager = BrowseDataManager(data_dir)
        print("✅ BrowseDataManager created successfully")

        # Test filter application (should not crash even with no data)
        try:
            sequences = data_manager.apply_filter(FilterType.STARTING_LETTER, "A")
            print(
                f"✅ Filter application successful, returned {len(sequences)} sequences"
            )
        except Exception as e:
            print(f"⚠️ Filter application failed (expected with no data): {e}")

        return True

    except Exception as e:
        print(f"❌ BrowseDataManager test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_browse_navigation_manager_logic():
    """Test BrowseNavigationManager logic."""
    print("🧪 Testing BrowseNavigationManager logic...")

    try:
        from desktop.modern.presentation.views.browse.managers import (
            BrowseNavigationManager,
            BrowsePanel,
        )

        # Create a mock stacked widget
        class MockStackedWidget:
            def __init__(self):
                self.current_index = 0
                self.widget_count = 3

            def setCurrentIndex(self, index):
                self.current_index = index

            def count(self):
                return self.widget_count

        mock_widget = MockStackedWidget()
        nav_manager = BrowseNavigationManager(mock_widget)
        print("✅ BrowseNavigationManager created successfully")

        # Test navigation methods
        nav_manager.navigate_to_browser()
        assert nav_manager.get_current_panel() == BrowsePanel.BROWSER
        print("✅ Navigation to browser successful")

        nav_manager.navigate_to_viewer()
        assert nav_manager.get_current_panel() == BrowsePanel.VIEWER
        print("✅ Navigation to viewer successful")

        # Test back navigation
        can_go_back = nav_manager.can_go_back()
        print(f"✅ Can go back: {can_go_back}")

        if can_go_back:
            nav_manager.go_back()
            print("✅ Back navigation successful")

        return True

    except Exception as e:
        print(f"❌ BrowseNavigationManager test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_browse_action_handler_logic():
    """Test BrowseActionHandler logic."""
    print("🧪 Testing BrowseActionHandler logic...")

    try:
        from desktop.modern.core.dependency_injection.di_container import DIContainer
        from desktop.modern.presentation.views.browse.managers import (
            BrowseActionHandler,
        )

        # Create test parameters
        container = DIContainer()
        sequences_dir = Path("data/sequences")

        # Create a mock parent widget
        class MockWidget:
            pass

        mock_parent = MockWidget()

        action_handler = BrowseActionHandler(container, sequences_dir, mock_parent)
        print("✅ BrowseActionHandler created successfully")

        # Test edit sequence handling
        sequence_id = action_handler.handle_edit_sequence("test_sequence_id")
        assert sequence_id == "test_sequence_id"
        print("✅ Edit sequence handling successful")

        return True

    except Exception as e:
        print(f"❌ BrowseActionHandler test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_manager_integration():
    """Test that managers can work together."""
    print("🧪 Testing manager integration...")

    try:
        from desktop.modern.core.dependency_injection.di_container import DIContainer
        from desktop.modern.presentation.views.browse.managers import (
            BrowseActionHandler,
            BrowseDataManager,
            BrowseNavigationManager,
            BrowsePanel,
        )

        # Create mock components
        class MockStackedWidget:
            def __init__(self):
                self.current_index = 0

            def setCurrentIndex(self, index):
                self.current_index = index

            def count(self):
                return 3

        class MockWidget:
            pass

        # Create managers
        data_manager = BrowseDataManager(Path("data"))
        nav_manager = BrowseNavigationManager(MockStackedWidget())
        action_handler = BrowseActionHandler(
            DIContainer(), Path("data/sequences"), MockWidget()
        )

        print("✅ All managers created successfully")

        # Test workflow simulation
        nav_manager.navigate_to_filter_selection()
        assert nav_manager.get_current_panel() == BrowsePanel.FILTER_SELECTION

        nav_manager.navigate_to_browser()
        assert nav_manager.get_current_panel() == BrowsePanel.BROWSER

        nav_manager.navigate_to_viewer()
        assert nav_manager.get_current_panel() == BrowsePanel.VIEWER

        print("✅ Manager integration workflow successful")

        return True

    except Exception as e:
        print(f"❌ Manager integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all logic tests."""
    print("🚀 Starting Browse tab manager logic tests...")

    tests = [
        test_browse_data_manager_logic,
        test_browse_navigation_manager_logic,
        test_browse_action_handler_logic,
        test_manager_integration,
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
        print("🎉 All logic tests passed! Manager refactoring is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
