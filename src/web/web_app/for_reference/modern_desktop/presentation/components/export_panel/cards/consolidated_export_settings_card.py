"""
Consolidated Export Settings Card - All export settings in one component

Combines export options, format settings, and user settings into a single,
organized card for better space utilization.
Part of the refactored export panel system.
"""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class ConsolidatedExportSettingsCard(QFrame):
    """
    Consolidated export settings card containing all export settings.

    Combines:
    - Export options (checkboxes)
    - Format settings (format, quality)
    - User settings (name, notes)

    Uses a grid layout for optimal space utilization.
    """

    # Signals
    setting_changed = pyqtSignal(str, object)  # setting_name, value

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("consolidated_export_settings_card")

        # Export options checkboxes
        self.include_start_position_cb = None
        self.add_beat_numbers_cb = None
        self.add_reversal_symbols_cb = None
        self.add_user_info_cb = None
        self.add_word_cb = None
        self.use_last_save_directory_cb = None

        # Format settings
        self.format_combo = None
        self.quality_input = None

        # User settings
        self.user_combo = None
        self.notes_input = None

        self._setup_ui()
        self._setup_connections()
        self._apply_styling()

    def _setup_ui(self):
        """Setup the UI layout using a compact grid design."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Title
        title = QLabel("Export Settings")
        title.setObjectName("main_title")
        title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # Create grid layout for efficient space usage
        grid_widget = QWidget()
        grid_widget.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(15)

        # Column 1: Export Options
        options_section = self._create_export_options_section()
        grid_layout.addWidget(options_section, 0, 0)

        # Column 2: Format & User Settings
        settings_section = self._create_format_user_settings_section()
        grid_layout.addWidget(settings_section, 0, 1)

        main_layout.addWidget(grid_widget)

    def _create_export_options_section(self) -> QWidget:
        """Create the export options section."""
        section = QFrame()
        section.setObjectName("options_section")
        section.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )

        layout = QVBoxLayout(section)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Section title
        title = QLabel("Export Options")
        title.setObjectName("section_title")
        title.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        layout.addWidget(title)

        # Create checkboxes
        checkboxes = [
            ("include_start_position", "Include start position", True),
            ("add_beat_numbers", "Add beat numbers", True),
            ("add_reversal_symbols", "Add reversal symbols", True),
            ("add_user_info", "Add user info", True),
            ("add_word", "Add word", True),
            ("use_last_save_directory", "Use last save directory", True),
        ]

        for key, label, default in checkboxes:
            checkbox = QCheckBox(label)
            checkbox.setObjectName("export_checkbox")
            checkbox.setChecked(default)
            layout.addWidget(checkbox)

            # Store reference
            setattr(self, f"{key}_cb", checkbox)

        layout.addStretch()  # Push content to top
        return section

    def _create_format_user_settings_section(self) -> QWidget:
        """Create the format and user settings section."""
        section = QFrame()
        section.setObjectName("settings_section")
        section.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )

        layout = QVBoxLayout(section)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Format Settings subsection
        format_title = QLabel("Format Settings")
        format_title.setObjectName("section_title")
        format_title.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        layout.addWidget(format_title)

        # Format controls in compact layout
        format_layout = QVBoxLayout()
        format_layout.setSpacing(6)

        # Format selection
        format_label = QLabel("Format:")
        format_label.setObjectName("field_label")
        format_layout.addWidget(format_label)

        self.format_combo = QComboBox()
        self.format_combo.setObjectName("setting_combo")
        self.format_combo.addItems(["PNG", "JPG", "PDF", "SVG"])
        self.format_combo.setCurrentText("PNG")
        format_layout.addWidget(self.format_combo)

        # Quality input
        quality_label = QLabel("Quality/Resolution:")
        quality_label.setObjectName("field_label")
        format_layout.addWidget(quality_label)

        self.quality_input = QLineEdit()
        self.quality_input.setObjectName("setting_input")
        self.quality_input.setPlaceholderText("e.g., 300 DPI")
        self.quality_input.setText("300 DPI")
        format_layout.addWidget(self.quality_input)

        layout.addLayout(format_layout)

        # Separator
        layout.addSpacing(8)

        # User Settings subsection
        user_title = QLabel("User Settings")
        user_title.setObjectName("section_title")
        user_title.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        layout.addWidget(user_title)

        # User controls in compact layout
        user_layout = QVBoxLayout()
        user_layout.setSpacing(6)

        # User name
        user_label = QLabel("User Name:")
        user_label.setObjectName("field_label")
        user_layout.addWidget(user_label)

        self.user_combo = QComboBox()
        self.user_combo.setObjectName("setting_combo")
        self.user_combo.setEditable(True)
        self.user_combo.addItems(["Default User", "Admin", "Guest"])
        self.user_combo.setCurrentText("Default User")
        user_layout.addWidget(self.user_combo)

        # Notes
        notes_label = QLabel("Notes:")
        notes_label.setObjectName("field_label")
        user_layout.addWidget(notes_label)

        self.notes_input = QLineEdit()
        self.notes_input.setObjectName("setting_input")
        self.notes_input.setPlaceholderText("Optional notes...")
        user_layout.addWidget(self.notes_input)

        layout.addLayout(user_layout)
        layout.addStretch()  # Push content to top

        return section

    def _setup_connections(self):
        """Setup signal connections."""
        # Export option checkboxes
        self.include_start_position_cb.toggled.connect(
            lambda checked: self.setting_changed.emit("include_start_position", checked)
        )
        self.add_beat_numbers_cb.toggled.connect(
            lambda checked: self.setting_changed.emit("add_beat_numbers", checked)
        )
        self.add_reversal_symbols_cb.toggled.connect(
            lambda checked: self.setting_changed.emit("add_reversal_symbols", checked)
        )
        self.add_user_info_cb.toggled.connect(
            lambda checked: self.setting_changed.emit("add_user_info", checked)
        )
        self.add_word_cb.toggled.connect(
            lambda checked: self.setting_changed.emit("add_word", checked)
        )
        self.use_last_save_directory_cb.toggled.connect(
            lambda checked: self.setting_changed.emit(
                "use_last_save_directory", checked
            )
        )

        # Format settings
        self.format_combo.currentTextChanged.connect(
            lambda text: self.setting_changed.emit("export_format", text)
        )
        self.quality_input.textChanged.connect(
            lambda text: self.setting_changed.emit("export_quality", text)
        )

        # User settings
        self.user_combo.currentTextChanged.connect(
            lambda text: self.setting_changed.emit("user_name", text)
        )
        self.notes_input.textChanged.connect(
            lambda text: self.setting_changed.emit("custom_note", text)
        )

    def _apply_styling(self):
        """Apply glassmorphism styling without fixed sizes."""
        self.setStyleSheet("""
            QFrame#consolidated_export_settings_card {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                margin: 2px;
            }

            QLabel#main_title {
                color: rgba(255, 255, 255, 0.95);
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 5px;
                background: transparent;
                border: none;
            }

            QFrame#options_section, QFrame#settings_section {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                margin: 2px;
            }

            QLabel#section_title {
                color: rgba(255, 255, 255, 0.9);
                font-size: 13px;
                font-weight: bold;
                margin-bottom: 8px;
                background: transparent;
                border: none;
            }

            QLabel#field_label {
                color: rgba(255, 255, 255, 0.8);
                font-size: 11px;
                margin-top: 3px;
                margin-bottom: 2px;
                background: transparent;
                border: none;
            }

            QCheckBox#export_checkbox {
                color: rgba(255, 255, 255, 0.9);
                font-size: 12px;
                spacing: 6px;
                background: transparent;
                border: none;
                padding: 2px 0px;
            }

            QCheckBox#export_checkbox::indicator {
                width: 14px;
                height: 14px;
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

            QComboBox#setting_combo {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                color: rgba(255, 255, 255, 0.9);
                font-size: 12px;
                padding: 5px 8px;
                min-height: 18px;
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
                width: 18px;
            }

            QComboBox#setting_combo::down-arrow {
                image: none;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-top: 5px solid rgba(255, 255, 255, 0.7);
                margin-right: 6px;
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
                font-size: 12px;
                padding: 5px 8px;
                min-height: 18px;
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

    def get_all_settings(self) -> dict:
        """Get all current settings as a dictionary."""
        return {
            # Export options
            "include_start_position": self.include_start_position_cb.isChecked(),
            "add_beat_numbers": self.add_beat_numbers_cb.isChecked(),
            "add_reversal_symbols": self.add_reversal_symbols_cb.isChecked(),
            "add_user_info": self.add_user_info_cb.isChecked(),
            "add_word": self.add_word_cb.isChecked(),
            "use_last_save_directory": self.use_last_save_directory_cb.isChecked(),
            # Format settings
            "export_format": self.format_combo.currentText(),
            "export_quality": self.quality_input.text(),
            # User settings
            "user_name": self.user_combo.currentText(),
            "custom_note": self.notes_input.text(),
        }

    def set_all_settings(self, settings: dict):
        """Set all settings from a dictionary."""
        # Export options
        if "include_start_position" in settings:
            self.include_start_position_cb.setChecked(
                settings["include_start_position"]
            )
        if "add_beat_numbers" in settings:
            self.add_beat_numbers_cb.setChecked(settings["add_beat_numbers"])
        if "add_reversal_symbols" in settings:
            self.add_reversal_symbols_cb.setChecked(settings["add_reversal_symbols"])
        if "add_user_info" in settings:
            self.add_user_info_cb.setChecked(settings["add_user_info"])
        if "add_word" in settings:
            self.add_word_cb.setChecked(settings["add_word"])
        if "use_last_save_directory" in settings:
            self.use_last_save_directory_cb.setChecked(
                settings["use_last_save_directory"]
            )

        # Format settings
        if "export_format" in settings:
            self.format_combo.setCurrentText(settings["export_format"])
        if "export_quality" in settings:
            self.quality_input.setText(settings["export_quality"])

        # User settings
        if "user_name" in settings:
            self.user_combo.setCurrentText(settings["user_name"])
        if "custom_note" in settings:
            self.notes_input.setText(settings["custom_note"])
