#!/usr/bin/env python3
"""
Comprehensive test script for debugging Advanced Start Position Picker visibility issues.

This script creates a standalone test window to verify that pictographs are visible
in the Advanced Start Position Picker component.
"""

import logging
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# Configure logging to capture all debug information
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("advanced_picker_debug.log"),
    ],
)

logger = logging.getLogger(__name__)


class AdvancedPickerTestWindow(QMainWindow):
    """Test window for debugging Advanced Start Position Picker visibility."""

    def __init__(self):
        super().__init__()
        self.advanced_picker = None
        self.pool_manager = None
        self.log_output = None

        self.setWindowTitle("Advanced Start Position Picker - Visibility Test")
        self.setGeometry(100, 100, 1200, 800)

        self._setup_ui()
        self._setup_logging_capture()

    def _setup_ui(self):
        """Set up the test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        # Left panel - Controls and info
        left_panel = self._create_left_panel()
        layout.addWidget(left_panel, 1)

        # Right panel - Advanced picker
        right_panel = self._create_right_panel()
        layout.addWidget(right_panel, 2)

    def _create_left_panel(self):
        """Create the left control panel."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Title
        title = QLabel("Visibility Test Controls")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        # Test buttons
        self.create_picker_btn = QPushButton("Create Advanced Picker")
        self.create_picker_btn.clicked.connect(self._create_advanced_picker)
        layout.addWidget(self.create_picker_btn)

        self.toggle_diamond_btn = QPushButton("Switch to Diamond Mode")
        self.toggle_diamond_btn.clicked.connect(self._toggle_diamond_mode)
        self.toggle_diamond_btn.setEnabled(False)
        layout.addWidget(self.toggle_diamond_btn)

        self.toggle_box_btn = QPushButton("Switch to Box Mode")
        self.toggle_box_btn.clicked.connect(self._toggle_box_mode)
        self.toggle_box_btn.setEnabled(False)
        layout.addWidget(self.toggle_box_btn)

        self.check_visibility_btn = QPushButton("Check Visibility Status")
        self.check_visibility_btn.clicked.connect(self._check_visibility_status)
        self.check_visibility_btn.setEnabled(False)
        layout.addWidget(self.check_visibility_btn)

        self.force_update_btn = QPushButton("Force Update Display")
        self.force_update_btn.clicked.connect(self._force_update_display)
        self.force_update_btn.setEnabled(False)
        layout.addWidget(self.force_update_btn)

        # Status info
        self.status_label = QLabel("Status: Ready to test")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        # Log output
        log_label = QLabel("Debug Log Output:")
        log_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(log_label)

        self.log_output = QTextEdit()
        self.log_output.setMaximumHeight(300)
        self.log_output.setFont(QFont("Consolas", 9))
        layout.addWidget(self.log_output)

        layout.addStretch()
        return widget

    def _create_right_panel(self):
        """Create the right panel for the advanced picker."""
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)

        placeholder = QLabel("Advanced Picker will appear here")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("border: 2px dashed #ccc; padding: 20px;")
        self.right_layout.addWidget(placeholder)

        return self.right_widget

    def _setup_logging_capture(self):
        """Set up logging to capture output in the UI."""

        class LogHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget

            def emit(self, record):
                msg = self.format(record)
                if self.text_widget:
                    self.text_widget.append(msg)
                    # Auto-scroll to bottom
                    scrollbar = self.text_widget.verticalScrollBar()
                    scrollbar.setValue(scrollbar.maximum())

        if self.log_output:
            handler = LogHandler(self.log_output)
            handler.setFormatter(
                logging.Formatter("%(levelname)s - %(name)s - %(message)s")
            )
            logging.getLogger().addHandler(handler)

    def _create_advanced_picker(self):
        """Create and display the advanced picker."""
        try:
            logger.info("Creating Advanced Start Position Picker...")

            # Import here to avoid circular imports
            from application.services.pictograph_pool_manager import (
                PictographPoolManager,
            )
            from presentation.components.start_position_picker.enhanced_start_position_picker import (
                EnhancedStartPositionPicker,
            )

            # Create pool manager
            logger.info("Creating PictographPoolManager...")
            self.pool_manager = PictographPoolManager()

            # Create enhanced picker (which contains the advanced picker)
            logger.info("Creating EnhancedStartPositionPicker...")
            self.enhanced_picker = EnhancedStartPositionPicker(self.pool_manager)

            # Clear the right panel and add the picker
            for i in reversed(range(self.right_layout.count())):
                item = self.right_layout.itemAt(i)
                if item:
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)

            self.right_layout.addWidget(self.enhanced_picker)

            # Trigger the advanced picker by clicking variations button
            logger.info("Triggering advanced picker...")
            self.enhanced_picker._handle_variations_clicked()
            self.advanced_picker = self.enhanced_picker.advanced_picker

            # Enable other buttons
            self.toggle_diamond_btn.setEnabled(True)
            self.toggle_box_btn.setEnabled(True)
            self.check_visibility_btn.setEnabled(True)
            self.force_update_btn.setEnabled(True)
            self.create_picker_btn.setEnabled(False)

            self.status_label.setText("Status: Advanced Picker Created")
            logger.info("Advanced picker created successfully!")

            # Schedule a visibility check after a short delay
            QTimer.singleShot(1000, self._check_visibility_status)

        except Exception as e:
            logger.error(f"Failed to create advanced picker: {e}")
            self.status_label.setText(f"Status: Error - {e}")

    def _toggle_diamond_mode(self):
        """Switch to diamond mode."""
        if self.advanced_picker:
            logger.info("Switching to diamond mode...")
            self.advanced_picker.set_grid_mode("diamond")
            self.status_label.setText("Status: Switched to Diamond Mode")
            QTimer.singleShot(500, self._check_visibility_status)

    def _toggle_box_mode(self):
        """Switch to box mode."""
        if self.advanced_picker:
            logger.info("Switching to box mode...")
            self.advanced_picker.set_grid_mode("box")
            self.status_label.setText("Status: Switched to Box Mode")
            QTimer.singleShot(500, self._check_visibility_status)

    def _check_visibility_status(self):
        """Check and report visibility status of all components."""
        if not self.advanced_picker:
            logger.warning("No advanced picker to check")
            return

        logger.info("=== VISIBILITY STATUS CHECK ===")

        # Check main picker
        picker_visible = self.advanced_picker.isVisible()
        picker_size = self.advanced_picker.size()
        logger.info(f"Advanced Picker - Visible: {picker_visible}, Size: {picker_size}")

        # Check container
        container = self.advanced_picker.positions_container
        container_visible = container.isVisible()
        container_size = container.size()
        logger.info(
            f"Positions Container - Visible: {container_visible}, Size: {container_size}"
        )

        # Check layout
        layout = self.advanced_picker.positions_layout
        layout_count = layout.count()
        logger.info(f"Positions Layout - Item count: {layout_count}")

        # Check individual position options
        options = self.advanced_picker.position_options
        logger.info(f"Position Options - Count: {len(options)}")

        visible_count = 0
        for i, option in enumerate(options):
            option_visible = option.isVisible()
            option_size = option.size()
            if option_visible:
                visible_count += 1
            logger.info(f"  Option {i}: Visible: {option_visible}, Size: {option_size}")

            # Check pictograph component
            if (
                hasattr(option, "_pictograph_component")
                and option._pictograph_component
            ):
                pic_visible = option._pictograph_component.isVisible()
                pic_size = option._pictograph_component.size()
                logger.info(f"    Pictograph: Visible: {pic_visible}, Size: {pic_size}")

        logger.info(f"Summary: {visible_count}/{len(options)} options are visible")
        self.status_label.setText(
            f"Status: {visible_count}/{len(options)} options visible"
        )

        logger.info("=== END VISIBILITY CHECK ===")

    def _force_update_display(self):
        """Force update the display."""
        if not self.advanced_picker:
            return

        logger.info("Forcing display update...")

        # Force updates
        self.advanced_picker.update()
        self.advanced_picker.positions_container.update()

        for option in self.advanced_picker.position_options:
            option.update()
            option.show()
            if (
                hasattr(option, "_pictograph_component")
                and option._pictograph_component
            ):
                option._pictograph_component.update()
                option._pictograph_component.show()

        # Schedule another visibility check
        QTimer.singleShot(500, self._check_visibility_status)


def main():
    """Run the visibility test."""
    app = QApplication(sys.argv)

    # Set up application
    app.setApplicationName("Advanced Picker Visibility Test")

    # Create and show test window
    window = AdvancedPickerTestWindow()
    window.show()

    logger.info(
        "Test application started. Click 'Create Advanced Picker' to begin testing."
    )

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
