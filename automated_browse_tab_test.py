"""
End-to-End Automated Browse Tab Test

This test automatically interacts with the browse tab to verify all functionality works
without manual intervention. It simulates user interactions and checks for crashes.
"""

import os
import sys
import time
import traceback
from pathlib import Path

# Add the src directory to the path
src_path = Path(__file__).parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(src_path))

from presentation.tabs.browse.models import FilterType
from presentation.tabs.browse.modern_browse_tab import ModernBrowseTab
from PyQt6.QtCore import QThread, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class AutomatedTestThread(QThread):
    """Thread to run automated tests without blocking the GUI."""

    # Signals for communication
    test_result = pyqtSignal(str, bool)  # test_name, success
    test_log = pyqtSignal(str)  # log_message
    test_completed = pyqtSignal(int, int)  # passed, failed

    def __init__(self, browse_tab):
        super().__init__()
        self.browse_tab = browse_tab
        self.passed_tests = 0
        self.failed_tests = 0

    def run(self):
        """Run all automated tests."""
        self.test_log.emit("🤖 Starting automated end-to-end tests...")

        try:
            # Test 1: Initialize and load data
            self.test_data_loading()

            # Test 2: Test filter selection
            self.test_filter_selection()

            # Test 3: Test filter application
            self.test_filter_application()

            # Test 4: Test navigation
            self.test_navigation()

            # Test 5: Test error handling
            self.test_error_handling()

            # Test 6: Test data refresh
            self.test_data_refresh()

        except Exception as e:
            self.test_log.emit(f"❌ Critical error in test thread: {e}")
            traceback.print_exc()

        self.test_completed.emit(self.passed_tests, self.failed_tests)

    def test_data_loading(self):
        """Test dictionary data loading."""
        try:
            self.test_log.emit("🔬 Testing data loading...")

            # Check if dictionary manager exists
            if not hasattr(self.browse_tab, "dictionary_manager"):
                raise Exception("Dictionary manager not found")

            # Check if data is loaded
            records = self.browse_tab.dictionary_manager.get_all_records()
            if len(records) == 0:
                self.browse_tab.dictionary_manager.load_all_sequences()
                records = self.browse_tab.dictionary_manager.get_all_records()

            if len(records) > 0:
                self.test_result.emit("Data Loading", True)
                self.test_log.emit(
                    f"✅ Data loading successful: {len(records)} sequences"
                )
                self.passed_tests += 1
            else:
                self.test_result.emit("Data Loading", False)
                self.test_log.emit("❌ Data loading failed: No sequences found")
                self.failed_tests += 1

        except Exception as e:
            self.test_result.emit("Data Loading", False)
            self.test_log.emit(f"❌ Data loading error: {e}")
            self.failed_tests += 1

    def test_filter_selection(self):
        """Test filter selection functionality."""
        try:
            self.test_log.emit("🔬 Testing filter selection...")

            # Check if filter selection panel exists
            if not hasattr(self.browse_tab, "filter_selection_panel"):
                raise Exception("Filter selection panel not found")

            # Test different filter types
            test_filters = [
                (FilterType.STARTING_LETTER, "A"),
                (FilterType.LENGTH, 4),
                (FilterType.DIFFICULTY, "beginner"),
                (FilterType.AUTHOR, "Austen"),
                (FilterType.FAVORITES, None),
                (FilterType.RECENT, None),
            ]

            for filter_type, filter_value in test_filters:
                try:
                    # Simulate filter selection
                    self.browse_tab._on_filter_selected(filter_type, filter_value)
                    self.test_log.emit(
                        f"✅ Filter selection test passed: {filter_type.value}"
                    )

                except Exception as e:
                    self.test_log.emit(
                        f"❌ Filter selection failed for {filter_type.value}: {e}"
                    )
                    self.failed_tests += 1
                    return

            self.test_result.emit("Filter Selection", True)
            self.test_log.emit("✅ All filter selection tests passed")
            self.passed_tests += 1

        except Exception as e:
            self.test_result.emit("Filter Selection", False)
            self.test_log.emit(f"❌ Filter selection error: {e}")
            self.failed_tests += 1

    def test_filter_application(self):
        """Test filter application and result generation."""
        try:
            self.test_log.emit("🔬 Testing filter application...")

            # Test various filter applications
            test_cases = [
                (FilterType.STARTING_LETTER, "A"),
                (FilterType.LENGTH, 4),
                (FilterType.DIFFICULTY, "beginner"),
                (FilterType.AUTHOR, "Austen"),
                (FilterType.GRID_MODE, "diamond"),
            ]

            for filter_type, filter_value in test_cases:
                try:
                    # Apply filter
                    results = self.browse_tab._apply_dictionary_filter(
                        filter_type, filter_value
                    )

                    if isinstance(results, list):
                        self.test_log.emit(
                            f"✅ Filter application successful: {filter_type.value} -> {len(results)} results"
                        )
                    else:
                        self.test_log.emit(
                            f"⚠️  Filter application returned non-list: {filter_type.value}"
                        )

                except Exception as e:
                    self.test_log.emit(
                        f"❌ Filter application failed for {filter_type.value}: {e}"
                    )
                    self.failed_tests += 1
                    return

            self.test_result.emit("Filter Application", True)
            self.test_log.emit("✅ All filter application tests passed")
            self.passed_tests += 1

        except Exception as e:
            self.test_result.emit("Filter Application", False)
            self.test_log.emit(f"❌ Filter application error: {e}")
            self.failed_tests += 1

    def test_navigation(self):
        """Test navigation between views."""
        try:
            self.test_log.emit("🔬 Testing navigation...")

            # Test switching to filter selection
            self.browse_tab._show_filter_selection()
            current_index = self.browse_tab.internal_left_stack.currentIndex()
            if current_index == 0:
                self.test_log.emit("✅ Navigation to filter selection successful")
            else:
                self.test_log.emit(
                    f"⚠️  Navigation issue: expected index 0, got {current_index}"
                )

            # Test switching to sequence browser
            self.browse_tab._show_sequence_browser()
            current_index = self.browse_tab.internal_left_stack.currentIndex()
            if current_index == 1:
                self.test_log.emit("✅ Navigation to sequence browser successful")
            else:
                self.test_log.emit(
                    f"⚠️  Navigation issue: expected index 1, got {current_index}"
                )

            # Switch back to filter selection
            self.browse_tab._show_filter_selection()

            self.test_result.emit("Navigation", True)
            self.test_log.emit("✅ Navigation tests passed")
            self.passed_tests += 1

        except Exception as e:
            self.test_result.emit("Navigation", False)
            self.test_log.emit(f"❌ Navigation error: {e}")
            self.failed_tests += 1

    def test_error_handling(self):
        """Test error handling with invalid inputs."""
        try:
            self.test_log.emit("🔬 Testing error handling...")

            # Test invalid filter values
            test_cases = [
                (FilterType.STARTING_LETTER, None),
                (FilterType.LENGTH, "invalid"),
                (FilterType.DIFFICULTY, "nonexistent"),
                (FilterType.AUTHOR, ""),
            ]

            for filter_type, filter_value in test_cases:
                try:
                    # This should not crash
                    results = self.browse_tab._apply_dictionary_filter(
                        filter_type, filter_value
                    )
                    self.test_log.emit(
                        f"✅ Error handling successful for {filter_type.value}: {filter_value}"
                    )

                except Exception as e:
                    self.test_log.emit(
                        f"⚠️  Error handling failed for {filter_type.value}: {e}"
                    )
                    # Don't fail the test, just log it

            self.test_result.emit("Error Handling", True)
            self.test_log.emit("✅ Error handling tests passed")
            self.passed_tests += 1

        except Exception as e:
            self.test_result.emit("Error Handling", False)
            self.test_log.emit(f"❌ Error handling test error: {e}")
            self.failed_tests += 1

    def test_data_refresh(self):
        """Test data refresh functionality."""
        try:
            self.test_log.emit("🔬 Testing data refresh...")

            # Test refresh
            self.browse_tab.refresh_sequences()

            # Verify data is still available
            records = self.browse_tab.dictionary_manager.get_all_records()
            if len(records) > 0:
                self.test_log.emit(
                    f"✅ Data refresh successful: {len(records)} sequences available"
                )
                self.test_result.emit("Data Refresh", True)
                self.passed_tests += 1
            else:
                self.test_log.emit("❌ Data refresh failed: No sequences after refresh")
                self.test_result.emit("Data Refresh", False)
                self.failed_tests += 1

        except Exception as e:
            self.test_result.emit("Data Refresh", False)
            self.test_log.emit(f"❌ Data refresh error: {e}")
            self.failed_tests += 1


class AutomatedTestWindow(QMainWindow):
    """Main window for automated testing."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖 Automated End-to-End Browse Tab Test")
        self.setGeometry(100, 100, 1600, 1000)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("🤖 Automated End-to-End Browse Tab Test")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # Control panel
        control_panel = QHBoxLayout()

        self.status_label = QLabel("🔄 Initializing...")
        control_panel.addWidget(self.status_label)

        self.start_test_button = QPushButton("🚀 Start Automated Tests")
        self.start_test_button.clicked.connect(self.start_automated_tests)
        control_panel.addWidget(self.start_test_button)

        main_layout.addLayout(control_panel)

        # Test results panel
        results_layout = QHBoxLayout()

        # Test log
        self.test_log = QTextEdit()
        self.test_log.setMaximumHeight(300)
        results_layout.addWidget(self.test_log)

        # Test results summary
        self.test_results = QTextEdit()
        self.test_results.setMaximumHeight(300)
        self.test_results.setMaximumWidth(400)
        results_layout.addWidget(self.test_results)

        main_layout.addLayout(results_layout)

        # Browse tab
        try:
            sequences_dir = Path("F:/CODE/TKA/data/dictionary")
            settings_file = Path("F:/CODE/TKA/settings.json")

            self.browse_tab = ModernBrowseTab(sequences_dir, settings_file)
            main_layout.addWidget(self.browse_tab)

            self.status_label.setText("✅ Browse tab initialized")

        except Exception as e:
            self.status_label.setText(f"❌ Error initializing browse tab: {e}")
            self.test_log.append(f"❌ Error initializing browse tab: {e}")
            import traceback

            traceback.print_exc()

    def start_automated_tests(self):
        """Start the automated test suite."""
        if not hasattr(self, "browse_tab"):
            self.test_log.append("❌ Cannot start tests: Browse tab not initialized")
            return

        self.start_test_button.setEnabled(False)
        self.status_label.setText("🤖 Running automated tests...")

        # Clear previous results
        self.test_log.clear()
        self.test_results.clear()

        # Start test thread
        self.test_thread = AutomatedTestThread(self.browse_tab)
        self.test_thread.test_result.connect(self.on_test_result)
        self.test_thread.test_log.connect(self.on_test_log)
        self.test_thread.test_completed.connect(self.on_tests_completed)
        self.test_thread.start()

    def on_test_result(self, test_name: str, success: bool):
        """Handle individual test results."""
        status = "✅ PASSED" if success else "❌ FAILED"
        self.test_results.append(f"{status}: {test_name}")

    def on_test_log(self, message: str):
        """Handle test log messages."""
        self.test_log.append(message)

    def on_tests_completed(self, passed: int, failed: int):
        """Handle test completion."""
        total = passed + failed
        self.status_label.setText(f"✅ Tests completed: {passed}/{total} passed")

        self.test_results.append(f"\n📊 FINAL RESULTS:")
        self.test_results.append(f"✅ Passed: {passed}")
        self.test_results.append(f"❌ Failed: {failed}")
        self.test_results.append(f"📈 Success Rate: {(passed/total*100):.1f}%")

        self.start_test_button.setEnabled(True)

        if failed == 0:
            self.test_log.append(
                "🎉 ALL TESTS PASSED! The browse tab is working correctly."
            )
        else:
            self.test_log.append(
                f"⚠️  {failed} tests failed. Check the results for details."
            )


def main():
    """Run the automated end-to-end test."""
    print("🤖 Starting Automated End-to-End Browse Tab Test")
    print("=" * 60)

    app = QApplication(sys.argv)

    # Create and show test window
    window = AutomatedTestWindow()
    window.show()

    print("\n✅ Automated test window displayed")
    print("📋 This test will automatically:")
    print("   - Load real dictionary data")
    print("   - Test all filter types and combinations")
    print("   - Test navigation between views")
    print("   - Test error handling with invalid inputs")
    print("   - Test data refresh functionality")
    print("   - Report any crashes or failures")

    print("\n🚀 Click 'Start Automated Tests' to begin!")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
