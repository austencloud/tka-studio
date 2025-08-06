"""
User Settings Card - User information settings component

Handles user name and notes input for export.
Part of the refactored export panel system.
"""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QComboBox, QFrame, QLabel, QLineEdit, QVBoxLayout


class UserSettingsCard(QFrame):
    """
    User settings card containing user information controls.

    Provides controls for:
    - User name selection/input
    - Notes/comments input
    """

    # Signal emitted when user settings change
    user_setting_changed = pyqtSignal(str, str)  # setting_name, value

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("user_settings_card")

        # Control references
        self.user_combo = None
        self.notes_input = None

        self._setup_ui()
        self._setup_connections()
        self._apply_styling()

    def _setup_ui(self):
        """Setup the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("User Settings")
        title.setObjectName("subsection_title")
        title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # User name selection
        user_label = QLabel("User Name:")
        user_label.setObjectName("setting_label")
        layout.addWidget(user_label)

        self.user_combo = QComboBox()
        self.user_combo.setObjectName("setting_combo")
        self.user_combo.setEditable(True)
        self.user_combo.addItems(["Default User", "Admin", "Guest"])
        self.user_combo.setCurrentText("Default User")
        layout.addWidget(self.user_combo)

        # Notes input
        notes_label = QLabel("Notes/Comments:")
        notes_label.setObjectName("setting_label")
        layout.addWidget(notes_label)

        self.notes_input = QLineEdit()
        self.notes_input.setObjectName("setting_input")
        self.notes_input.setPlaceholderText("Optional notes or comments...")
        layout.addWidget(self.notes_input)

    def _setup_connections(self):
        """Setup signal connections."""
        self.user_combo.currentTextChanged.connect(
            lambda text: self.user_setting_changed.emit("user_name", text)
        )
        self.notes_input.textChanged.connect(
            lambda text: self.user_setting_changed.emit("notes", text)
        )

    def _apply_styling(self):
        """Apply glassmorphism styling."""
        self.setStyleSheet("""
            QFrame#user_settings_card {
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

    def get_user_settings(self) -> dict:
        """Get current user settings as a dictionary."""
        return {
            "user_name": self.user_combo.currentText(),
            "notes": self.notes_input.text(),
        }

    def set_user_settings(self, settings: dict):
        """Set user settings from a dictionary."""
        if "user_name" in settings:
            self.user_combo.setCurrentText(settings["user_name"])
        if "notes" in settings:
            self.notes_input.setText(settings["notes"])
