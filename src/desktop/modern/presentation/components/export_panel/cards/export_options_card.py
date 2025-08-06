"""
Export Options Card - Export settings checkboxes component

Handles all the export option checkboxes and settings.
Part of the refactored export panel system.
"""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QCheckBox, QFrame, QLabel, QVBoxLayout


class ExportOptionsCard(QFrame):
    """
    Export options card containing all export setting checkboxes.

    Provides checkboxes for:
    - Include start position
    - Add beat numbers
    - Add reversal symbols
    - Add user info
    - Add word
    - Use last save directory
    """

    # Signal emitted when any option changes
    option_changed = pyqtSignal(str, bool)  # option_name, value

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("export_options_card")

        # Checkbox references
        self.include_start_position_cb = None
        self.add_beat_numbers_cb = None
        self.add_reversal_symbols_cb = None
        self.add_user_info_cb = None
        self.add_word_cb = None
        self.use_last_save_directory_cb = None

        self._setup_ui()
        self._setup_connections()
        self._apply_styling()

    def _setup_ui(self):
        """Setup the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("Export Options")
        title.setObjectName("subsection_title")
        title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Include start position checkbox
        self.include_start_position_cb = QCheckBox("Include start position")
        self.include_start_position_cb.setObjectName("export_checkbox")
        self.include_start_position_cb.setChecked(True)
        layout.addWidget(self.include_start_position_cb)

        # Add beat numbers checkbox
        self.add_beat_numbers_cb = QCheckBox("Add beat numbers")
        self.add_beat_numbers_cb.setObjectName("export_checkbox")
        self.add_beat_numbers_cb.setChecked(True)
        layout.addWidget(self.add_beat_numbers_cb)

        # Add reversal symbols checkbox
        self.add_reversal_symbols_cb = QCheckBox("Add reversal symbols")
        self.add_reversal_symbols_cb.setObjectName("export_checkbox")
        self.add_reversal_symbols_cb.setChecked(True)
        layout.addWidget(self.add_reversal_symbols_cb)

        # Add user info checkbox
        self.add_user_info_cb = QCheckBox("Add user info")
        self.add_user_info_cb.setObjectName("export_checkbox")
        self.add_user_info_cb.setChecked(True)
        layout.addWidget(self.add_user_info_cb)

        # Add word checkbox
        self.add_word_cb = QCheckBox("Add word")
        self.add_word_cb.setObjectName("export_checkbox")
        self.add_word_cb.setChecked(True)
        layout.addWidget(self.add_word_cb)

        # Use last save directory checkbox
        self.use_last_save_directory_cb = QCheckBox("Use last save directory")
        self.use_last_save_directory_cb.setObjectName("export_checkbox")
        self.use_last_save_directory_cb.setChecked(True)
        layout.addWidget(self.use_last_save_directory_cb)

    def _setup_connections(self):
        """Setup signal connections."""
        self.include_start_position_cb.toggled.connect(
            lambda checked: self.option_changed.emit("include_start_position", checked)
        )
        self.add_beat_numbers_cb.toggled.connect(
            lambda checked: self.option_changed.emit("add_beat_numbers", checked)
        )
        self.add_reversal_symbols_cb.toggled.connect(
            lambda checked: self.option_changed.emit("add_reversal_symbols", checked)
        )
        self.add_user_info_cb.toggled.connect(
            lambda checked: self.option_changed.emit("add_user_info", checked)
        )
        self.add_word_cb.toggled.connect(
            lambda checked: self.option_changed.emit("add_word", checked)
        )
        self.use_last_save_directory_cb.toggled.connect(
            lambda checked: self.option_changed.emit("use_last_save_directory", checked)
        )

    def _apply_styling(self):
        """Apply glassmorphism styling."""
        self.setStyleSheet("""
            QFrame#export_options_card {
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

            QCheckBox#export_checkbox {
                color: rgba(255, 255, 255, 0.9);
                font-size: 13px;
                spacing: 8px;
                background: transparent;
                border: none;
                padding: 4px 0px;
            }

            QCheckBox#export_checkbox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 3px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                background: rgba(255, 255, 255, 0.1);
            }

            QCheckBox#export_checkbox::indicator:hover {
                border: 2px solid rgba(255, 255, 255, 0.5);
                background: rgba(255, 255, 255, 0.15);
            }

            QCheckBox#export_checkbox::indicator:checked {
                border: 2px solid rgba(100, 200, 255, 0.8);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(100, 200, 255, 0.6),
                    stop:1 rgba(50, 150, 255, 0.4));
            }

            QCheckBox#export_checkbox::indicator:checked:hover {
                border: 2px solid rgba(120, 220, 255, 0.9);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(120, 220, 255, 0.7),
                    stop:1 rgba(70, 170, 255, 0.5));
            }
        """)

    def get_options(self) -> dict:
        """Get current export options as a dictionary."""
        return {
            "include_start_position": self.include_start_position_cb.isChecked(),
            "add_beat_numbers": self.add_beat_numbers_cb.isChecked(),
            "add_reversal_symbols": self.add_reversal_symbols_cb.isChecked(),
            "add_user_info": self.add_user_info_cb.isChecked(),
            "add_word": self.add_word_cb.isChecked(),
            "use_last_save_directory": self.use_last_save_directory_cb.isChecked(),
        }

    def set_options(self, options: dict):
        """Set export options from a dictionary."""
        if "include_start_position" in options:
            self.include_start_position_cb.setChecked(options["include_start_position"])
        if "add_beat_numbers" in options:
            self.add_beat_numbers_cb.setChecked(options["add_beat_numbers"])
        if "add_reversal_symbols" in options:
            self.add_reversal_symbols_cb.setChecked(options["add_reversal_symbols"])
        if "add_user_info" in options:
            self.add_user_info_cb.setChecked(options["add_user_info"])
        if "add_word" in options:
            self.add_word_cb.setChecked(options["add_word"])
        if "use_last_save_directory" in options:
            self.use_last_save_directory_cb.setChecked(
                options["use_last_save_directory"]
            )
