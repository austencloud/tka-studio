#!/usr/bin/env python3
"""
Test script to open and interact with the settings dialog to diagnose sizing issues.
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import just the components we need to avoid circular imports
    from PyQt6.QtWidgets import (
        QDialog,
        QVBoxLayout,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QStackedWidget,
        QListWidget,
    )
    from PyQt6.QtCore import Qt, QTimer
    from PyQt6.QtGui import QFont

    # Import individual components instead of the full dialog
    from modern.presentation.components.ui.settings.components.header import (
        SettingsHeader,
    )
    from modern.presentation.components.ui.settings.components.sidebar import (
        SettingsSidebar,
    )
    from modern.presentation.components.ui.settings.components.content_area import (
        SettingsContentArea,
    )
    from modern.presentation.components.ui.settings.components.action_buttons import (
        SettingsActionButtons,
    )
    from modern.presentation.components.ui.settings.components.styles import (
        GlassmorphismStyles,
    )

    print("Successfully imported settings components!")

except ImportError as e:
    print(f"Import error: {e}")
    print("Will create a simplified test dialog instead")
    IMPORT_SUCCESS = False
else:
    IMPORT_SUCCESS = True


class MockUserService:
    """Mock user service for testing."""

    def get_current_user(self):
        return "Test User"

    def set_current_user(self, user):
        print(f"Setting user to: {user}")


class TestSettingsDialog(QDialog):
    """Test settings dialog that mimics the real one."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)

        # Apply the same responsive sizing logic
        self._setup_responsive_sizing()

        # Create the dialog structure
        self._create_ui()

        # Apply styling
        self._apply_styling()

        # Track size changes
        self.size_history = []
        self.current_tab = "General"

    def _setup_responsive_sizing(self):
        """Apply the same responsive sizing logic as the real settings dialog."""
        screen = self.screen()
        if screen:
            screen_geometry = screen.availableGeometry()
            # Use 60% width, 50% height for better fit
            dialog_width = int(screen_geometry.width() * 0.60)
            dialog_height = int(screen_geometry.height() * 0.50)

            # Set tighter bounds to prevent oversized dialogs
            dialog_width = max(800, min(dialog_width, 1400))
            dialog_height = max(500, min(dialog_height, 800))

            print(f"Screen: {screen_geometry.width()}x{screen_geometry.height()}")
            print(f"Calculated: {dialog_width}x{dialog_height}")
        else:
            dialog_width, dialog_height = 1000, 650

        # Use resize instead of setFixedSize
        self.resize(dialog_width, dialog_height)
        self.setMinimumSize(800, 500)
        self.setMaximumSize(1400, 800)

        self.size_history.append(f"Initial: {dialog_width}x{dialog_height}")

    def _create_ui(self):
        """Create the dialog UI structure."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Container with glassmorphism
        self.container = QWidget()
        self.container.setObjectName("glassmorphism_container")
        main_layout.addWidget(self.container)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(12)

        # Header
        if IMPORT_SUCCESS:
            self.header = SettingsHeader("Settings")
        else:
            self.header = QLabel("Settings")
            self.header.setStyleSheet(
                "font-size: 18px; font-weight: bold; color: white;"
            )
        container_layout.addWidget(self.header)

        # Content area
        self._create_content_area(container_layout)

        # Action buttons
        if IMPORT_SUCCESS:
            self.action_buttons = SettingsActionButtons()
        else:
            self.action_buttons = self._create_simple_buttons()
        container_layout.addWidget(self.action_buttons)

    def _create_content_area(self, parent_layout):
        """Create the content area with sidebar and tabs."""
        content_layout = QHBoxLayout()
        content_layout.setSpacing(16)

        # Sidebar
        if IMPORT_SUCCESS:
            self.sidebar = SettingsSidebar(
                ["General", "Prop Type", "Visibility", "Image Export"]
            )
            self.sidebar.currentRowChanged.connect(self._on_tab_changed)
        else:
            self.sidebar = self._create_simple_sidebar()
        content_layout.addWidget(self.sidebar)

        # Content area
        if IMPORT_SUCCESS:
            self.content_area = SettingsContentArea()
        else:
            self.content_area = self._create_simple_content()
        content_layout.addWidget(self.content_area)

        parent_layout.addLayout(content_layout)

    def _create_simple_sidebar(self):
        """Create a simple sidebar for testing."""
        sidebar = QListWidget()
        sidebar.setFixedWidth(220)
        for tab in ["General", "Prop Type", "Visibility", "Image Export"]:
            sidebar.addItem(tab)
        sidebar.setCurrentRow(0)
        sidebar.currentRowChanged.connect(self._on_tab_changed)
        return sidebar

    def _create_simple_content(self):
        """Create simple content area for testing."""
        content = QStackedWidget()
        content.setMinimumWidth(400)

        for i, tab_name in enumerate(
            ["General", "Prop Type", "Visibility", "Image Export"]
        ):
            tab_widget = QWidget()
            layout = QVBoxLayout(tab_widget)
            layout.addWidget(QLabel(f"{tab_name} Settings"))
            layout.addWidget(QLabel("This is a test tab to measure dialog sizing."))
            layout.addStretch()
            content.addWidget(tab_widget)

        return content

    def _create_simple_buttons(self):
        """Create simple action buttons."""
        button_widget = QWidget()
        layout = QHBoxLayout(button_widget)
        layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        return button_widget

    def _on_tab_changed(self, index):
        """Handle tab changes and measure size."""
        tab_names = ["General", "Prop Type", "Visibility", "Image Export"]
        if 0 <= index < len(tab_names):
            self.current_tab = tab_names[index]
            if hasattr(self.content_area, "setCurrentIndex"):
                self.content_area.setCurrentIndex(index)

            # Measure size after tab change
            QTimer.singleShot(100, self._measure_size_after_tab_change)

    def _measure_size_after_tab_change(self):
        """Measure size after tab change."""
        size = self.size()
        self.size_history.append(
            f"{self.current_tab} tab: {size.width()}x{size.height()}"
        )
        print(f"Tab changed to {self.current_tab}: {size.width()}x{size.height()}")

    def _apply_styling(self):
        """Apply glassmorphism styling."""
        if IMPORT_SUCCESS:
            self.setStyleSheet(GlassmorphismStyles.get_dialog_styles())
        else:
            self.setStyleSheet("""
                QDialog {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(20, 20, 30, 0.95),
                        stop:1 rgba(10, 10, 20, 0.95));
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 16px;
                }
                QLabel { color: white; }
                QPushButton {
                    background: rgba(42, 130, 218, 0.8);
                    border: 1px solid rgba(42, 130, 218, 1.0);
                    border-radius: 8px;
                    color: white;
                    padding: 8px 16px;
                }
            """)

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


class TestMainWindow(QDialog):
    """Test main window to launch settings dialog."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings Dialog Size Test")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout(self)

        # Info label
        info_label = QLabel(
            "Click the button to open the settings dialog and observe its behavior:"
        )
        info_label.setFont(QFont("Arial", 12))
        layout.addWidget(info_label)

        # Screen info
        screen = self.screen()
        if screen:
            geometry = screen.availableGeometry()
            screen_info = QLabel(f"Screen size: {geometry.width()}x{geometry.height()}")
            screen_info.setFont(QFont("Arial", 10))
            layout.addWidget(screen_info)

            # Calculate expected dialog size
            dialog_width = int(geometry.width() * 0.70)
            dialog_height = int(geometry.height() * 0.60)
            dialog_width = max(900, min(dialog_width, 1600))
            dialog_height = max(600, min(dialog_height, 1000))

            expected_info = QLabel(
                f"Expected dialog size: {dialog_width}x{dialog_height}"
            )
            expected_info.setFont(QFont("Arial", 10))
            layout.addWidget(expected_info)

        # Test button
        test_button = QPushButton("Open Settings Dialog")
        test_button.clicked.connect(self.open_settings_dialog)
        layout.addWidget(test_button)

        # Results area
        self.results_label = QLabel("Results will appear here...")
        self.results_label.setFont(QFont("Courier", 10))
        self.results_label.setWordWrap(True)
        layout.addWidget(self.results_label)

        layout.addStretch()

        self.settings_dialog = None

    def open_settings_dialog(self):
        """Open the settings dialog and analyze its behavior."""
        try:
            print("Opening settings dialog...")

            # Create mock services
            user_service = MockUserService()

            # Create test settings dialog
            self.settings_dialog = TestSettingsDialog(self)

            # Get initial size
            initial_size = self.settings_dialog.size()
            print(
                f"Initial dialog size: {initial_size.width()}x{initial_size.height()}"
            )

            # Show dialog
            self.settings_dialog.show()

            # Schedule automated tab testing
            QTimer.singleShot(500, self.test_tab_switching)

        except Exception as e:
            error_msg = f"Error opening settings dialog: {e}"
            print(error_msg)
            self.results_label.setText(error_msg)
            import traceback

            traceback.print_exc()

    def test_tab_switching(self):
        """Automatically test switching between tabs."""
        if not self.settings_dialog:
            return

        print("\\nStarting automated tab testing...")

        # Test each tab
        for i in range(4):  # General, Prop Type, Visibility, Image Export
            QTimer.singleShot(i * 1000, lambda idx=i: self.switch_to_tab(idx))

        # Final analysis after all tabs tested
        QTimer.singleShot(5000, self.final_analysis)

    def switch_to_tab(self, index):
        """Switch to a specific tab and measure."""
        if self.settings_dialog and hasattr(self.settings_dialog, "sidebar"):
            self.settings_dialog.sidebar.setCurrentRow(index)

    def final_analysis(self):
        """Perform final analysis of dialog behavior."""
        if not self.settings_dialog:
            return

        print("\\n" + "=" * 50)
        print("FINAL SETTINGS DIALOG ANALYSIS")
        print("=" * 50)

        # Get final size
        final_size = self.settings_dialog.size()

        # Get screen info
        screen = self.settings_dialog.screen()
        if screen:
            screen_geometry = screen.availableGeometry()
            width_percent = (final_size.width() / screen_geometry.width()) * 100
            height_percent = (final_size.height() / screen_geometry.height()) * 100

            analysis = f"""
SCREEN INFORMATION:
- Screen Size: {screen_geometry.width()}x{screen_geometry.height()}

DIALOG SIZE ANALYSIS:
- Final Size: {final_size.width()}x{final_size.height()}
- Screen Percentage: {width_percent:.1f}% x {height_percent:.1f}%
- Target: 60% x 50%
- Width Status: {"✅ GOOD" if 55 <= width_percent <= 65 else "❌ NEEDS ADJUSTMENT"}
- Height Status: {"✅ GOOD" if 45 <= height_percent <= 55 else "❌ NEEDS ADJUSTMENT"}

SIZE HISTORY:
"""
            for entry in self.settings_dialog.size_history:
                analysis += f"- {entry}\\n"

            analysis += f"""
RESPONSIVENESS TEST:
- Minimum Size: {self.settings_dialog.minimumSize().width()}x{self.settings_dialog.minimumSize().height()}
- Maximum Size: {self.settings_dialog.maximumSize().width()}x{self.settings_dialog.maximumSize().height()}
- Current Size: {final_size.width()}x{final_size.height()}

OVERALL STATUS: {"✅ DIALOG SIZING IS GOOD" if 45 <= height_percent <= 55 and 55 <= width_percent <= 65 else "❌ DIALOG SIZING NEEDS ADJUSTMENT"}
"""

            print(analysis)
            self.results_label.setText(analysis)

        print("\\nTest completed! Check the results above.")

    def check_dialog_size_after_show(self):
        """Check dialog size immediately after showing."""
        if self.settings_dialog:
            size = self.settings_dialog.size()
            print(f"Size after show(): {size.width()}x{size.height()}")

            # Check if it's visible and positioned correctly
            geometry = self.settings_dialog.geometry()
            print(
                f"Dialog geometry: x={geometry.x()}, y={geometry.y()}, w={geometry.width()}, h={geometry.height()}"
            )

    def check_dialog_size_after_delay(self):
        """Check dialog size after a short delay to see if it expanded."""
        if self.settings_dialog:
            size = self.settings_dialog.size()
            print(f"Size after 500ms: {size.width()}x{size.height()}")

            # Check content size
            container = getattr(self.settings_dialog, "container", None)
            if container:
                container_size = container.size()
                print(
                    f"Container size: {container_size.width()}x{container_size.height()}"
                )

    def final_size_check(self):
        """Final size check and analysis."""
        if self.settings_dialog:
            size = self.settings_dialog.size()
            print(f"Final size after 1000ms: {size.width()}x{size.height()}")

            # Get screen info for comparison
            screen = self.screen()
            if screen:
                screen_geometry = screen.availableGeometry()
                width_percent = (size.width() / screen_geometry.width()) * 100
                height_percent = (size.height() / screen_geometry.height()) * 100

                results = f"""SETTINGS DIALOG SIZE ANALYSIS:
                
Final Size: {size.width()}x{size.height()}
Screen Size: {screen_geometry.width()}x{screen_geometry.height()}
Percentage: {width_percent:.1f}% x {height_percent:.1f}%

Expected: 70% x 60% of screen
Actual: {width_percent:.1f}% x {height_percent:.1f}%

Height Analysis:
- Target: {int(screen_geometry.height() * 0.60)}px
- Actual: {size.height()}px
- Difference: {size.height() - int(screen_geometry.height() * 0.60)}px

Status: {"✅ GOOD" if abs(height_percent - 60) < 5 else "❌ NEEDS ADJUSTMENT"}
"""

                print(results)
                self.results_label.setText(results)


def main():
    """Main test function."""
    app = QApplication(sys.argv)

    # Create test window
    window = TestMainWindow()
    window.show()

    print("Test window opened. Click the button to test the settings dialog.")
    print("Watch the console for size measurements and analysis.")

    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
