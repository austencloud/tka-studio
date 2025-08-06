#!/usr/bin/env python3
"""
Image Export Test UI

A nice GUI for testing image rendering with different sequences and options.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys


# Add the src directory to the Python path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from PyQt6.QtCore import Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import (
    register_image_export_services,
)
from desktop.modern.core.interfaces.image_export_services import (
    IImageExportService,
    ImageExportOptions,
)


class ImageRenderWorker(QThread):
    """Worker thread for image rendering to keep UI responsive"""

    image_ready = pyqtSignal(object)  # QImage
    error_occurred = pyqtSignal(str)

    def __init__(self, export_service, sequence_data, word, options):
        super().__init__()
        self.export_service = export_service
        self.sequence_data = sequence_data
        self.word = word
        self.options = options

    def run(self):
        try:
            image = self.export_service.create_sequence_image(
                self.sequence_data, self.word, self.options
            )
            self.image_ready.emit(image)
        except Exception as e:
            self.error_occurred.emit(str(e))


class ImageExportTestUI(QMainWindow):
    """Main UI for testing image export"""

    def __init__(self):
        super().__init__()
        self.export_service = None
        self.current_image = None
        self.render_worker = None

        self.init_services()
        self.init_ui()
        self.load_default_sequence()

    def init_services(self):
        """Initialize the export service"""
        try:
            container = DIContainer()
            register_image_export_services(container)
            self.export_service = container.resolve(IImageExportService)
        except Exception as e:
            QMessageBox.critical(
                self, "Service Error", f"Failed to initialize export service: {e}"
            )
            sys.exit(1)

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Image Export Test UI")
        self.setGeometry(100, 100, 1200, 800)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create splitter for left panel and right panel
        splitter = QSplitter(Qt.Orientation.Horizontal)
        central_widget.setLayout(QHBoxLayout())
        central_widget.layout().addWidget(splitter)

        # Left panel - Controls
        left_panel = self.create_controls_panel()
        splitter.addWidget(left_panel)

        # Right panel - Image display
        right_panel = self.create_image_panel()
        splitter.addWidget(right_panel)

        # Set splitter proportions
        splitter.setSizes([400, 800])

        # Status bar
        self.statusBar().showMessage("Ready")

    def create_controls_panel(self):
        """Create the left control panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Sequence settings
        sequence_group = QGroupBox("Sequence Settings")
        sequence_layout = QVBoxLayout(sequence_group)

        # Preset sequences
        sequence_layout.addWidget(QLabel("Preset Sequences:"))
        self.sequence_combo = QComboBox()
        self.sequence_combo.addItems(
            [
                "Single Beat",
                "Simple 2-Beat",
                "Simple 4-Beat",
                "Complex 8-Beat",
                "Custom",
            ]
        )
        self.sequence_combo.currentTextChanged.connect(self.on_sequence_changed)
        sequence_layout.addWidget(self.sequence_combo)

        # Word input
        sequence_layout.addWidget(QLabel("Word:"))
        self.word_input = QLineEdit("TEST")
        self.word_input.textChanged.connect(self.auto_render)
        sequence_layout.addWidget(self.word_input)

        # Custom sequence editor
        sequence_layout.addWidget(QLabel("Custom Sequence (JSON):"))
        self.sequence_editor = QTextEdit()
        self.sequence_editor.setMaximumHeight(150)
        self.sequence_editor.textChanged.connect(self.auto_render)
        sequence_layout.addWidget(self.sequence_editor)

        layout.addWidget(sequence_group)

        # Export options
        options_group = QGroupBox("Export Options")
        options_layout = QGridLayout(options_group)

        # Checkboxes for options
        self.add_word_cb = QCheckBox("Add Word")
        self.add_word_cb.setChecked(True)
        self.add_word_cb.toggled.connect(self.auto_render)
        options_layout.addWidget(self.add_word_cb, 0, 0)

        self.add_user_info_cb = QCheckBox("Add User Info")
        self.add_user_info_cb.setChecked(True)
        self.add_user_info_cb.toggled.connect(self.auto_render)
        options_layout.addWidget(self.add_user_info_cb, 0, 1)

        self.add_difficulty_cb = QCheckBox("Add Difficulty")
        self.add_difficulty_cb.setChecked(False)
        self.add_difficulty_cb.toggled.connect(self.auto_render)
        options_layout.addWidget(self.add_difficulty_cb, 1, 0)

        self.add_beat_numbers_cb = QCheckBox("Add Beat Numbers")
        self.add_beat_numbers_cb.setChecked(True)
        self.add_beat_numbers_cb.toggled.connect(self.auto_render)
        options_layout.addWidget(self.add_beat_numbers_cb, 1, 1)

        self.add_reversals_cb = QCheckBox("Add Reversals")
        self.add_reversals_cb.setChecked(True)
        self.add_reversals_cb.toggled.connect(self.auto_render)
        options_layout.addWidget(self.add_reversals_cb, 2, 0)

        self.include_start_pos_cb = QCheckBox("Include Start Position")
        self.include_start_pos_cb.setChecked(True)
        self.include_start_pos_cb.toggled.connect(self.auto_render)
        options_layout.addWidget(self.include_start_pos_cb, 2, 1)

        # User info inputs
        options_layout.addWidget(QLabel("User Name:"), 3, 0)
        self.user_name_input = QLineEdit("Test User")
        self.user_name_input.textChanged.connect(self.auto_render)
        options_layout.addWidget(self.user_name_input, 3, 1)

        options_layout.addWidget(QLabel("Notes:"), 4, 0)
        self.notes_input = QLineEdit("Test export")
        self.notes_input.textChanged.connect(self.auto_render)
        options_layout.addWidget(self.notes_input, 4, 1)

        layout.addWidget(options_group)

        # Action buttons
        buttons_layout = QHBoxLayout()

        self.render_btn = QPushButton("Render Now")
        self.render_btn.clicked.connect(self.render_image)
        buttons_layout.addWidget(self.render_btn)

        self.save_btn = QPushButton("Save Image")
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setEnabled(False)
        buttons_layout.addWidget(self.save_btn)

        layout.addLayout(buttons_layout)

        # Auto-render checkbox
        self.auto_render_cb = QCheckBox("Auto-render on changes")
        self.auto_render_cb.setChecked(True)
        layout.addWidget(self.auto_render_cb)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Add stretch to push everything to top
        layout.addStretch()

        return panel

    def create_image_panel(self):
        """Create the right image display panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Image info
        self.image_info_label = QLabel("No image rendered")
        self.image_info_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.image_info_label)

        # Scroll area for image
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet(
            "border: 1px solid gray; background-color: white;"
        )
        self.image_label.setText("Click 'Render Now' to generate image")
        self.image_label.setMinimumSize(400, 300)

        scroll_area.setWidget(self.image_label)
        layout.addWidget(scroll_area)

        return panel

    def get_sample_sequences(self):
        """Get sample sequences for testing"""
        return {
            "Single Beat": [
                {
                    "beat": "1",
                    "red_attributes": {
                        "start_loc": "n",
                        "end_loc": "s",
                        "motion_type": "pro",
                        "turns": 0,
                    },
                    "blue_attributes": {
                        "start_loc": "s",
                        "end_loc": "n",
                        "motion_type": "pro",
                        "turns": 0,
                    },
                    "start_position": "alpha",
                    "end_position": "alpha",
                }
            ],
            "Simple 2-Beat": [
                {
                    "beat": "1",
                    "red_attributes": {
                        "start_loc": "n",
                        "end_loc": "s",
                        "motion_type": "pro",
                        "turns": 0,
                    },
                    "blue_attributes": {
                        "start_loc": "s",
                        "end_loc": "n",
                        "motion_type": "pro",
                        "turns": 0,
                    },
                    "start_position": "alpha",
                    "end_position": "alpha",
                },
                {
                    "beat": "2",
                    "red_attributes": {
                        "start_loc": "s",
                        "end_loc": "n",
                        "motion_type": "pro",
                        "turns": 0,
                    },
                    "blue_attributes": {
                        "start_loc": "n",
                        "end_loc": "s",
                        "motion_type": "pro",
                        "turns": 0,
                    },
                    "start_position": "alpha",
                    "end_position": "alpha",
                },
            ],
            "Simple 4-Beat": [
                {
                    "beat": "1",
                    "red_attributes": {
                        "start_loc": "n",
                        "end_loc": "s",
                        "motion_type": "pro",
                        "turns": 0,
                    },
                    "blue_attributes": {
                        "start_loc": "s",
                        "end_loc": "n",
                        "motion_type": "pro",
                        "turns": 0,
                    },
                    "start_position": "alpha",
                    "end_position": "alpha",
                },
                {
                    "beat": "2",
                    "red_attributes": {
                        "start_loc": "s",
                        "end_loc": "e",
                        "motion_type": "anti",
                        "turns": 1,
                    },
                    "blue_attributes": {
                        "start_loc": "n",
                        "end_loc": "w",
                        "motion_type": "anti",
                        "turns": 1,
                    },
                    "start_position": "alpha",
                    "end_position": "beta",
                },
                {
                    "beat": "3",
                    "red_attributes": {
                        "start_loc": "e",
                        "end_loc": "w",
                        "motion_type": "pro",
                        "turns": 0,
                    },
                    "blue_attributes": {
                        "start_loc": "w",
                        "end_loc": "e",
                        "motion_type": "pro",
                        "turns": 0,
                    },
                    "start_position": "beta",
                    "end_position": "gamma",
                },
                {
                    "beat": "4",
                    "red_attributes": {
                        "start_loc": "w",
                        "end_loc": "n",
                        "motion_type": "anti",
                        "turns": 1,
                    },
                    "blue_attributes": {
                        "start_loc": "e",
                        "end_loc": "s",
                        "motion_type": "anti",
                        "turns": 1,
                    },
                    "start_position": "gamma",
                    "end_position": "alpha",
                },
            ],
            "Complex 8-Beat": [
                {
                    "beat": str(i + 1),
                    "red_attributes": {
                        "start_loc": ["n", "s", "e", "w"][i % 4],
                        "end_loc": ["s", "n", "w", "e"][i % 4],
                        "motion_type": ["pro", "anti"][i % 2],
                        "turns": i % 2,
                    },
                    "blue_attributes": {
                        "start_loc": ["s", "n", "w", "e"][i % 4],
                        "end_loc": ["n", "s", "e", "w"][i % 4],
                        "motion_type": ["anti", "pro"][i % 2],
                        "turns": (i + 1) % 2,
                    },
                    "start_position": ["alpha", "beta", "gamma"][i % 3],
                    "end_position": ["beta", "gamma", "alpha"][i % 3],
                }
                for i in range(8)
            ],
        }

    def load_default_sequence(self):
        """Load the default sequence"""
        self.on_sequence_changed("Simple 4-Beat")

    def on_sequence_changed(self, sequence_name):
        """Handle sequence selection change"""
        if sequence_name == "Custom":
            self.sequence_editor.setEnabled(True)
            return

        self.sequence_editor.setEnabled(False)

        sequences = self.get_sample_sequences()
        if sequence_name in sequences:
            import json

            sequence_json = json.dumps(sequences[sequence_name], indent=2)
            self.sequence_editor.setPlainText(sequence_json)
            self.auto_render()

    def get_current_sequence(self):
        """Get the current sequence data"""
        try:
            import json

            sequence_text = self.sequence_editor.toPlainText().strip()
            if not sequence_text:
                return []
            return json.loads(sequence_text)
        except json.JSONDecodeError as e:
            self.statusBar().showMessage(f"Invalid JSON: {e}")
            return []
        except Exception as e:
            self.statusBar().showMessage(f"Error parsing sequence: {e}")
            return []

    def get_export_options(self):
        """Get current export options"""
        return ImageExportOptions(
            add_word=self.add_word_cb.isChecked(),
            add_user_info=self.add_user_info_cb.isChecked(),
            add_difficulty_level=self.add_difficulty_cb.isChecked(),
            add_beat_numbers=self.add_beat_numbers_cb.isChecked(),
            add_reversal_symbols=self.add_reversals_cb.isChecked(),
            include_start_position=self.include_start_pos_cb.isChecked(),
            user_name=self.user_name_input.text(),
            export_date=datetime.now().strftime("%m-%d-%Y"),
            notes=self.notes_input.text(),
        )

    def auto_render(self):
        """Auto-render if enabled"""
        if self.auto_render_cb.isChecked():
            # Use a timer to debounce rapid changes
            if hasattr(self, "auto_render_timer"):
                self.auto_render_timer.stop()

            self.auto_render_timer = QTimer()
            self.auto_render_timer.setSingleShot(True)
            self.auto_render_timer.timeout.connect(self.render_image)
            self.auto_render_timer.start(500)  # 500ms delay

    def render_image(self):
        """Render the image with current settings"""
        sequence_data = self.get_current_sequence()
        if not sequence_data:
            self.image_label.setText("No valid sequence data")
            self.image_info_label.setText("No valid sequence")
            return

        word = self.word_input.text() or "TEST"
        options = self.get_export_options()

        # Disable controls during rendering
        self.render_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.statusBar().showMessage("Rendering image...")

        # Start worker thread
        self.render_worker = ImageRenderWorker(
            self.export_service, sequence_data, word, options
        )
        self.render_worker.image_ready.connect(self.on_image_ready)
        self.render_worker.error_occurred.connect(self.on_render_error)
        self.render_worker.start()

    def on_image_ready(self, image):
        """Handle successful image rendering"""
        self.current_image = image

        # Convert QImage to QPixmap for display
        pixmap = QPixmap.fromImage(image)

        # Scale image to fit display while maintaining aspect ratio
        max_width = 600
        max_height = 600
        scaled_pixmap = pixmap.scaled(
            max_width,
            max_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.image_label.setPixmap(scaled_pixmap)

        # Update info
        scale_factor = (
            scaled_pixmap.width() / pixmap.width() if pixmap.width() > 0 else 1
        )
        info_text = (
            f"Image: {image.width()}×{image.height()}px | "
            f"Display: {scaled_pixmap.width()}×{scaled_pixmap.height()}px "
            f"({scale_factor:.2f}x scale)"
        )
        self.image_info_label.setText(info_text)

        # Re-enable controls
        self.render_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage("Image rendered successfully")

    def on_render_error(self, error_message):
        """Handle rendering error"""
        self.image_label.setText(f"Render Error:\n{error_message}")
        self.image_info_label.setText("Render failed")

        # Re-enable controls
        self.render_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage(f"Render failed: {error_message}")

        QMessageBox.warning(
            self, "Render Error", f"Failed to render image:\n{error_message}"
        )

    def save_image(self):
        """Save the current image"""
        if not self.current_image:
            QMessageBox.warning(
                self, "No Image", "No image to save. Please render an image first."
            )
            return

        # Get save file path
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            "PNG Images (*.png);;All Files (*)",
        )

        if file_path:
            success = self.current_image.save(file_path)
            if success:
                self.statusBar().showMessage(f"Image saved to: {file_path}")
                QMessageBox.information(
                    self, "Saved", f"Image saved successfully to:\n{file_path}"
                )
            else:
                QMessageBox.warning(self, "Save Failed", "Failed to save image.")


def main():
    """Main function to run the UI"""
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle("Fusion")

    # Create and show the main window
    window = ImageExportTestUI()
    window.show()

    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
