#!/usr/bin/env python3
"""
Integration Test for Simplified Option Picker

This test validates the simplified option picker in a realistic application context
with comprehensive debug output to verify sizing calculations.
"""

import os
import sys

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


def test_integration():
    """Integration test with realistic main window setup."""

    print("🚀 Integration Test Starting...")

    # Create QApplication
    app = QApplication(sys.argv)

    try:
        # Import our simplified components
        from presentation.components.option_picker.core.option_picker_widget import (
            OptionPickerWidget,
        )

        print("✅ Successfully imported OptionPickerWidget")

        # Create a realistic main window that simulates TKA
        class TestMainWindow(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle(
                    "TKA Modern - Simplified Option Picker Integration Test"
                )
                self.setGeometry(100, 100, 1400, 900)  # Realistic main window size

                self._setup_ui()

            def _setup_di_container(self):
                """Set up DI container with proper service registration."""
                try:
                    from application.services.core.service_registration_manager import (
                        ServiceRegistrationManager,
                    )
                    from core.dependency_injection.di_container import DIContainer

                    # Create container and register services
                    container = DIContainer()
                    service_manager = ServiceRegistrationManager()

                    # Register data services (this includes IDatasetQuery -> DatasetQuery)
                    service_manager.register_data_services(container)

                    print("✅ DI Container initialized with data services")
                    return container

                except Exception as e:
                    print(f"⚠️ Failed to setup DI container: {e}")
                    print("📝 Using fallback container")
                    # Return a minimal container for testing
                    from core.dependency_injection.di_container import DIContainer

                    return DIContainer()

            def _setup_ui(self):
                """Set up the UI components."""
                # Create central widget with layout similar to TKA
                central_widget = QWidget()
                self.setCentralWidget(central_widget)

                # Main horizontal layout (like TKA: sequence workbench + option picker)
                main_layout = QHBoxLayout(central_widget)
                main_layout.setContentsMargins(10, 10, 10, 10)
                main_layout.setSpacing(10)

                # Left side: Simulate sequence workbench (takes up remaining space)
                sequence_workbench_placeholder = QLabel(
                    "Sequence Workbench\n(Placeholder)"
                )
                sequence_workbench_placeholder.setStyleSheet(
                    """
                    QLabel {
                        background-color: #f0f0f0;
                        border: 2px solid #ccc;
                        padding: 20px;
                        font-size: 16px;
                        text-align: center;
                    }
                """
                )
                main_layout.addWidget(
                    sequence_workbench_placeholder, 1
                )  # Takes remaining space

                # Right side: Option picker (should be exactly half the main window width)
                print(
                    f"🏗️ Creating OptionPickerWidget with main window size: {self.size().width()}x{self.size().height()}"
                )

                # Initialize DI container with proper services
                container = self._setup_di_container()

                self.option_picker = OptionPickerWidget(
                    parent=central_widget,
                    mw_size_provider=lambda: self.size(),
                    progress_callback=lambda msg, progress: print(
                        f"Progress: {msg} ({progress*100:.1f}%)"
                    ),
                    container=container,
                )

                main_layout.addWidget(self.option_picker.get_widget(), 0)  # Fixed size

                print(
                    "✅ Successfully created and added OptionPickerWidget to main window"
                )

                # Set up resize monitoring
                self.resize_timer = QTimer()
                self.resize_timer.setSingleShot(True)
                self.resize_timer.timeout.connect(self.on_resize_complete)

            def resizeEvent(self, event: QResizeEvent):
                """Monitor main window resize events."""
                super().resizeEvent(event)

                new_size = event.size()
                old_size = event.oldSize()

                print(
                    f"\n🔄 [MAIN_WINDOW_RESIZE] Old size: {old_size.width()}x{old_size.height()}"
                )
                print(
                    f"🔄 [MAIN_WINDOW_RESIZE] New size: {new_size.width()}x{new_size.height()}"
                )

                # Restart timer to detect when resize is complete
                self.resize_timer.start(500)  # 500ms delay

            def on_resize_complete(self):
                """Called when resize is complete."""
                print(f"🔄 [MAIN_WINDOW_RESIZE] Resize complete - validating sizing...")
                self.validate_sizing()

            def validate_sizing(self):
                """Validate that all sizing is correct."""
                main_window_size = self.size()
                expected_option_picker_width = main_window_size.width() // 2
                actual_option_picker_width = self.option_picker.get_widget().width()

                print(
                    f"\n✅ [VALIDATION] Main window: {main_window_size.width()}x{main_window_size.height()}"
                )
                print(
                    f"✅ [VALIDATION] Expected option picker width: {expected_option_picker_width}"
                )
                print(
                    f"✅ [VALIDATION] Actual option picker width: {actual_option_picker_width}"
                )

                width_diff = abs(
                    actual_option_picker_width - expected_option_picker_width
                )
                if width_diff <= 2:  # Allow 2px tolerance
                    print(
                        f"✅ [VALIDATION] Option picker width: CORRECT (diff: {width_diff}px)"
                    )
                else:
                    print(
                        f"❌ [VALIDATION] Option picker width: INCORRECT (diff: {width_diff}px)"
                    )

                # Validate section widths
                sections = self.option_picker.option_picker_widget.sections
                for letter_type, section in sections.items():
                    section_width = section.width()

                    if section.is_groupable:
                        expected_width = expected_option_picker_width // 3
                        width_type = "GROUPED (1/3)"
                    else:
                        expected_width = expected_option_picker_width
                        width_type = "INDIVIDUAL (full)"

                    section_diff = abs(section_width - expected_width)
                    if section_diff <= 5:  # Allow 5px tolerance for sections
                        print(
                            f"✅ [VALIDATION] {letter_type} {width_type}: CORRECT ({section_width}px, expected: {expected_width}px)"
                        )
                    else:
                        print(
                            f"❌ [VALIDATION] {letter_type} {width_type}: INCORRECT ({section_width}px, expected: {expected_width}px, diff: {section_diff}px)"
                        )

        # Create and show the test main window
        window = TestMainWindow()
        window.show()

        print("\n🖼️ Integration test window displayed")
        print("👀 Visual inspection points:")
        print("   - Option picker should be exactly half the main window width")
        print(
            "   - Individual sections (Types 1-3) should fill the full option picker width"
        )
        print(
            "   - Grouped sections (Types 4-6) should each be 1/3 of the option picker width"
        )
        print("   - Try resizing the main window to test dynamic sizing")
        print("❌ Close the window to complete the test")

        # Initial validation after a short delay
        QTimer.singleShot(1000, window.validate_sizing)

        # Run the application
        return app.exec()

    except Exception as e:
        print(f"❌ Integration test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = test_integration()
    sys.exit(exit_code)
