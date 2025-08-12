from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.core.interfaces.tab_settings_interfaces import (
    IUserProfileService,
)


class GeneralTab(QWidget):
    setting_changed = pyqtSignal(str, object)

    def __init__(self, user_service: IUserProfileService, parent=None):
        super().__init__(parent)
        self.user_service = user_service
        self._setup_ui()
        self._load_settings()
        self._setup_connections()

    def _setup_ui(self):
        """Setup the enhanced general tab UI with scroll area to prevent expansion."""
        from PyQt6.QtCore import Qt

        # Main layout with minimal margins
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create scroll area to contain content and prevent dialog expansion
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        # Create content widget for the scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(8)

        # Create setting sections using SettingCard approach
        self._create_user_profile_section(content_layout)
        self._create_application_behavior_section(content_layout)

        # Add stretch to push content to top
        content_layout.addStretch()

        # Set content widget to scroll area
        scroll_area.setWidget(content_widget)

        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)

        # Apply styling
        self._apply_styling()

    def _create_user_profile_section(self, parent_layout):
        """Create user profile settings section using SettingCard approach."""
        from ..components.card import SettingCard

        card = SettingCard(
            "User Profile",
            "Configure your user name that appears on exported sequences and shared content.",
        )

        # User Name Input with sophisticated styling
        user_name_layout = QVBoxLayout()
        user_name_label = QLabel("User Name (appears on exported sequences):")
        user_name_label.setFont(QFont("Inter", 11, QFont.Weight.Medium))
        user_name_label.setStyleSheet("color: rgba(255, 255, 255, 0.95);")
        user_name_layout.addWidget(user_name_label)

        # Create modern styled line edit for user name
        user_name_input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter your name...")
        self.user_input.setMaxLength(50)  # Reasonable limit

        # Apply sophisticated styling to match legacy
        self.user_input.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.10));
                border: 1px solid rgba(255, 255, 255, 0.30);
                border-radius: 8px;
                padding: 10px 14px;
                color: white;
                font-size: 14px;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-weight: 500;
                min-height: 32px;
                selection-background-color: rgba(42, 130, 218, 0.3);
            }
            QLineEdit:focus {
                border: 2px solid rgba(42, 130, 218, 0.8);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.22),
                    stop:1 rgba(255, 255, 255, 0.15));
            }
            QLineEdit:hover {
                border-color: rgba(255, 255, 255, 0.45);
            }
        """)

        user_name_input_layout.addWidget(self.user_input)
        user_name_input_layout.addStretch()
        user_name_layout.addLayout(user_name_input_layout)

        card.content_layout.addLayout(user_name_layout)
        parent_layout.addWidget(card)

    def _create_application_behavior_section(self, parent_layout):
        """Create application behavior settings section using SettingCard approach."""
        from ..components.card import ComboCard, ToggleCard

        # Enable fades toggle card
        fades_card = ToggleCard(
            "Smooth Transitions",
            "Enable smooth fade transitions between views for a more polished experience.",
            None,  # No setting key
            True,  # Default value
        )
        fades_card.toggle.toggled.connect(self._on_fades_changed)
        self.enable_fades = fades_card.toggle  # Store reference for loading settings
        parent_layout.addWidget(fades_card)

        # Auto-save toggle card
        auto_save_card = ToggleCard(
            "Auto-save Changes",
            "Automatically save your work without prompting to prevent data loss.",
            None,  # No setting key
            True,  # Default value
        )
        auto_save_card.toggle.toggled.connect(self._on_auto_save_changed)
        self.auto_save = auto_save_card.toggle  # Store reference for loading settings
        parent_layout.addWidget(auto_save_card)

        # Theme selection card
        theme_options = ["Dark", "Light", "Auto"]
        theme_card = ComboCard(
            "Theme",
            "Choose the application theme. Auto follows your system theme preference.",
            None,  # No setting key
            theme_options,
            "Dark",  # Default value
        )
        theme_card.combo.currentTextChanged.connect(self._on_theme_changed)
        self.theme_combo = theme_card.combo  # Store reference for loading settings
        parent_layout.addWidget(theme_card)

    def _apply_styling(self):
        self.setStyleSheet(
            """
            QWidget {
                background: transparent;
                color: white;
            }

            QLabel#section_title {
                color: rgba(255, 255, 255, 0.98);
                font-size: 18px;
                font-weight: bold;
                font-family: "Inter", "Segoe UI", sans-serif;
                letter-spacing: -0.3px;
                margin-bottom: 10px;
            }

            QLabel#subsection_title {
                color: rgba(255, 255, 255, 0.92);
                font-size: 14px;
                font-weight: 600;
                font-family: "Inter", "Segoe UI", sans-serif;
                letter-spacing: 0.2px;
                margin-bottom: 8px;
            }

            QFrame#settings_section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.10));
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 12px;
                padding: 12px;
                margin: 3px 0;
            }

            QFrame#settings_section:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.20),
                    stop:1 rgba(255, 255, 255, 0.14));
                border-color: rgba(255, 255, 255, 0.35);
            }

            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.10));
                border: 1px solid rgba(255, 255, 255, 0.30);
                border-radius: 8px;
                padding: 10px 12px;
                color: white;
                font-size: 13px;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-weight: 500;
            }

            QLineEdit:focus {
                border-color: rgba(42, 130, 218, 0.8);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.20),
                    stop:1 rgba(255, 255, 255, 0.14));
            }

            QCheckBox {
                color: rgba(255, 255, 255, 0.90);
                font-size: 13px;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-weight: 500;
                spacing: 10px;
                padding: 4px 0;
            }

            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 0.40);
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.08));
            }

            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(34, 197, 94, 0.9),
                    stop:1 rgba(34, 197, 94, 0.7));
                border-color: rgba(34, 197, 94, 1.0);
            }

            QCheckBox::indicator:hover {
                border-color: rgba(255, 255, 255, 0.6);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.22),
                    stop:1 rgba(255, 255, 255, 0.12));
            }

            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.10));
                border: 1px solid rgba(255, 255, 255, 0.30);
                border-radius: 8px;
                padding: 10px 12px;
                color: white;
                min-width: 140px;
                font-size: 13px;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-weight: 500;
            }

            QComboBox:focus {
                border-color: rgba(42, 130, 218, 0.8);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.20),
                    stop:1 rgba(255, 255, 255, 0.14));
            }

            QComboBox::drop-down {
                border: none;
                width: 25px;
                background: transparent;
            }

            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid rgba(255, 255, 255, 0.8);
                margin-right: 8px;
            }

            QComboBox:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.20),
                    stop:1 rgba(255, 255, 255, 0.14));
                border-color: rgba(255, 255, 255, 0.45);
            }

            QLabel {
                color: rgba(255, 255, 255, 0.88);
                font-family: "Inter", "Segoe UI", sans-serif;
                font-weight: 500;
            }
        """
        )

    def _load_settings(self):
        current_user = self.user_service.get_current_user()
        self.user_input.setText(current_user)

        # Load other settings with defaults
        self.enable_fades.setChecked(True)
        self.auto_save.setChecked(True)
        self.theme_combo.setCurrentText("Dark")

    def _setup_connections(self):
        """Connect signals to slots."""
        self.user_input.textChanged.connect(self._on_user_changed)
        # Note: Card connections are set up in _create_application_behavior_section

    def _on_user_changed(self, text: str):
        """Handle user name changes."""
        self.user_service.set_current_user(text.strip())
        self.setting_changed.emit("current_user", text.strip())

    def _on_fades_changed(self, enabled: bool):
        """Handle fades setting changes."""
        self.setting_changed.emit("enable_fades", enabled)

    def _on_auto_save_changed(self, enabled: bool):
        """Handle auto-save setting changes."""
        self.setting_changed.emit("auto_save", enabled)

    def _on_theme_changed(self, theme: str):
        """Handle theme setting changes."""
        self.setting_changed.emit("theme", theme)
