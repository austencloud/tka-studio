#!/usr/bin/env python3
"""
Settings Dialog Visibility Test - Real Dimensions & Structure
============================================================

This test creates a proper settings dialog that matches the real TKA settings
dialog dimensions and structure, ensuring the visibility tab sizes correctly.
"""

import sys
import os
import logging
import time
from typing import Dict, Any, Optional

# Add TKA to path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("settings_dialog_test.log"), logging.StreamHandler()],
)

# Import PyQt6
try:
    from PyQt6.QtWidgets import (
        QApplication,
        QMainWindow,
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QSplitter,
        QFrame,
        QStackedWidget,
    )
    from PyQt6.QtCore import Qt, QTimer
    from PyQt6.QtGui import QFont, QKeySequence, QShortcut

    QT_AVAILABLE = True
except ImportError:
    print("⚠️ PyQt6 not available")
    QT_AVAILABLE = False
    sys.exit(1)

# Import TKA components
try:
    from core.application.application_factory import ApplicationFactory
    from core.testing.ai_agent_helpers import TKAAITestHelper
    from core.interfaces.tab_settings_interfaces import IVisibilityService

    from application.services.settings.visibility_state_manager import (
        ModernVisibilityStateManager,
    )
    from presentation.components.ui.settings.visibility.visibility_tab import (
        VisibilityTab,
    )

    TKA_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ TKA components not available: {e}")
    TKA_AVAILABLE = False
    sys.exit(1)


class SettingsDialogTest(QMainWindow):
    """Test window that replicates the exact settings dialog structure and dimensions."""

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("SettingsDialogTest")
        self.start_time = time.time()

        # Initialize TKA services
        self.logger.info("Initializing TKA services...")
        self.container = ApplicationFactory.create_test_app()
        self.visibility_service = self.container.resolve(IVisibilityService)

        # Create visibility components
        self.state_manager = ModernVisibilityStateManager(self.visibility_service)
        self.visibility_tab = VisibilityTab(self.state_manager)

        # Validate system
        helper = TKAAITestHelper(use_test_mode=True)
        try:
            validation_result = helper.run_comprehensive_test_suite()
            self.logger.info(f"TKA system validation: {validation_result.success}")
        except Exception as e:
            self.logger.warning(f"TKA system validation failed: {e}")

        self.setup_ui()
        self.setup_shortcuts()

        # Log initialization time
        init_time = time.time() - self.start_time
        self.logger.info(f"Settings dialog test initialized in {init_time:.3f}s")

    def setup_ui(self):
        """Setup UI with exact settings dialog structure and dimensions."""
        # Set exact window properties from screenshot
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 1000, 700)  # Exact dimensions from screenshot

        # Apply exact styling from real settings dialog
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #3c3c3c;
                color: white;
            }
            QWidget {
                background-color: #3c3c3c;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
            }
        """
        )

        # Create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create main layout with exact margins from screenshot
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)

        # Create content area (horizontal split)
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)

        # Left sidebar (settings categories) - exact width from screenshot
        sidebar = self.create_sidebar()
        content_layout.addWidget(sidebar)

        # Right content area (settings panels)
        content_area = self.create_content_area()
        content_layout.addWidget(content_area)

        # Add content to main layout
        main_layout.addWidget(content_widget)

        # Add bottom button bar
        button_bar = self.create_button_bar()
        main_layout.addWidget(button_bar)

        self.logger.info("Settings dialog UI setup complete")

    def create_sidebar(self):
        """Create the left sidebar with settings categories."""
        sidebar = QFrame()
        sidebar.setFixedWidth(200)  # Exact width from screenshot
        sidebar.setStyleSheet(
            """
            QFrame {
                background-color: #2d2d2d;
                border-radius: 8px;
            }
            QPushButton {
                text-align: left;
                padding: 12px 16px;
                border: none;
                border-radius: 4px;
                margin: 2px 4px;
                background-color: transparent;
                color: #cccccc;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
            QPushButton.selected {
                background-color: #4a90e2;
                color: white;
                font-weight: bold;
            }
        """
        )

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(8, 12, 8, 12)
        layout.setSpacing(2)

        # Settings categories from screenshot
        categories = [
            "General",
            "Prop Type",
            "Visibility",
            "Beat Layout",
            "Image Export",
            "Background",
            "Codex Exporter",
        ]

        for category in categories:
            btn = QPushButton(category)
            if category == "Visibility":
                btn.setProperty("class", "selected")
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #4a90e2;
                        color: white;
                        font-weight: bold;
                    }
                """
                )
            layout.addWidget(btn)

        layout.addStretch()
        return sidebar

    def create_content_area(self):
        """Create the right content area with visibility settings."""
        content_frame = QFrame()
        content_frame.setStyleSheet(
            """
            QFrame {
                background-color: #3c3c3c;
                border: none;
            }
        """
        )

        layout = QVBoxLayout(content_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add the visibility tab (this will now size properly)
        layout.addWidget(self.visibility_tab)

        return content_frame

    def create_button_bar(self):
        """Create bottom button bar matching real settings dialog."""
        button_frame = QFrame()
        button_frame.setFixedHeight(60)
        button_frame.setStyleSheet(
            """
            QFrame {
                background-color: #3c3c3c;
                border-top: 1px solid #555555;
            }
        """
        )

        layout = QHBoxLayout(button_frame)
        layout.setContentsMargins(0, 12, 0, 12)
        layout.addStretch()

        # Create buttons with exact styling from screenshot
        button_style = """
            QPushButton {
                background-color: #555555;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                margin: 0px 4px;
                font-size: 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
        """

        ok_button_style = """
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                margin: 0px 4px;
                font-size: 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #5ba0f2;
            }
        """

        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.setStyleSheet(button_style)

        apply_btn = QPushButton("Apply")
        apply_btn.setStyleSheet(button_style)

        ok_btn = QPushButton("OK")
        ok_btn.setStyleSheet(ok_button_style)
        ok_btn.clicked.connect(self.close)

        layout.addWidget(reset_btn)
        layout.addWidget(apply_btn)
        layout.addWidget(ok_btn)

        return button_frame

    def setup_shortcuts(self):
        """Setup keyboard shortcuts for testing."""
        # F5 to capture state
        capture_shortcut = QShortcut(QKeySequence("F5"), self)
        capture_shortcut.activated.connect(self.capture_state)

        # Escape to close
        close_shortcut = QShortcut(QKeySequence("Escape"), self)
        close_shortcut.activated.connect(self.close)

    def capture_state(self):
        """Capture current state for debugging."""
        self.logger.info("=== STATE CAPTURE ===")
        self.logger.info(f"Window size: {self.size().width()}x{self.size().height()}")
        self.logger.info(
            f"Visibility tab size: {self.visibility_tab.size().width()}x{self.visibility_tab.size().height()}"
        )

        # Get preview component size
        if hasattr(self.visibility_tab, "preview"):
            preview_size = self.visibility_tab.preview.size()
            self.logger.info(
                f"Preview size: {preview_size.width()}x{preview_size.height()}"
            )


def main():
    """Main entry point."""
    if not QT_AVAILABLE or not TKA_AVAILABLE:
        print("❌ Required dependencies not available")
        return 1

    print("🔧 Settings Dialog Visibility Test")
    print("=" * 50)
    print("📋 Press F5 to capture state")
    print("📋 Press Escape to close")
    print("=" * 50)

    app = QApplication(sys.argv)

    # Apply application-wide styling
    app.setStyleSheet(
        """
        QApplication {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
    """
    )

    window = SettingsDialogTest()
    window.show()

    print("✅ Settings dialog test launched successfully")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
