"""
Format Settings Card - Format and quality settings component

Handles format selection and quality settings for export.
Part of the refactored export panel system.
"""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QComboBox, QFrame, QLabel, QLineEdit, QVBoxLayout


class FormatSettingsCard(QFrame):
    """
    Format settings card containing format and quality controls.

    Provides controls for:
    - Export format selection (PNG, JPG, etc.)
    - Quality/resolution settings
    """

    # Signal emitted when format settings change
    format_changed = pyqtSignal(str, str)  # setting_name, value

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("format_settings_card")

        # Control references
        self.format_combo = None
        self.quality_input = None

        self._setup_ui()
        self._setup_connections()
        self._apply_styling()

    def _setup_ui(self):
        """Setup the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("Format Settings")
        title.setObjectName("subsection_title")
        title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Format selection
        format_label = QLabel("Export Format:")
        format_label.setObjectName("setting_label")
        layout.addWidget(format_label)

        self.format_combo = QComboBox()
        self.format_combo.setObjectName("setting_combo")
        self.format_combo.addItems(["PNG", "JPG", "PDF", "SVG"])
        self.format_combo.setCurrentText("PNG")
        layout.addWidget(self.format_combo)

        # Quality/Resolution setting
        quality_label = QLabel("Quality/Resolution:")
        quality_label.setObjectName("setting_label")
        layout.addWidget(quality_label)

        self.quality_input = QLineEdit()
        self.quality_input.setObjectName("setting_input")
        self.quality_input.setPlaceholderText("e.g., 300 DPI, 1920x1080")
        self.quality_input.setText("300 DPI")
        layout.addWidget(self.quality_input)

    def _setup_connections(self):
        """Setup signal connections."""
        self.format_combo.currentTextChanged.connect(
            lambda text: self.format_changed.emit("format", text)
        )
        self.quality_input.textChanged.connect(
            lambda text: self.format_changed.emit("quality", text)
        )

    def _apply_styling(self):
        """Apply glassmorphism styling."""
        self.setStyleSheet("""
            QFrame#format_settings_card {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                margin: 5px;
            }

            QLabel#subsection_title {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 10px;
                background: transparent;
                border: none;
            }

            QLabel#setting_label {
                color: rgba(255, 255, 255, 0.8);
                font-size: 12px;
                margin-top: 5px;
                margin-bottom: 3px;
                background: transparent;
                border: none;
            }

            QComboBox#setting_combo {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                color: rgba(255, 255, 255, 0.9);
                font-size: 13px;
                padding: 6px 10px;
                min-height: 20px;
            }

            QComboBox#setting_combo:hover {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }

            QComboBox#setting_combo:focus {
                border: 1px solid rgba(100, 200, 255, 0.6);
                background: rgba(255, 255, 255, 0.12);
            }

            QComboBox#setting_combo::drop-down {
                border: none;
                width: 20px;
            }

            QComboBox#setting_combo::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid rgba(255, 255, 255, 0.7);
                margin-right: 8px;
            }

            QComboBox#setting_combo QAbstractItemView {
                background: rgba(40, 40, 40, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                color: rgba(255, 255, 255, 0.9);
                selection-background-color: rgba(100, 200, 255, 0.3);
                outline: none;
            }

            QLineEdit#setting_input {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                color: rgba(255, 255, 255, 0.9);
                font-size: 13px;
                padding: 6px 10px;
                min-height: 20px;
            }

            QLineEdit#setting_input:hover {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }

            QLineEdit#setting_input:focus {
                border: 1px solid rgba(100, 200, 255, 0.6);
                background: rgba(255, 255, 255, 0.12);
            }

            QLineEdit#setting_input::placeholder {
                color: rgba(255, 255, 255, 0.5);
            }
        """)

    def get_format_settings(self) -> dict:
        """Get current format settings as a dictionary."""
        return {
            "format": self.format_combo.currentText(),
            "quality": self.quality_input.text(),
        }

    def set_format_settings(self, settings: dict):
        """Set format settings from a dictionary."""
        if "format" in settings:
            self.format_combo.setCurrentText(settings["format"])
        if "quality" in settings:
            self.quality_input.setText(settings["quality"])
