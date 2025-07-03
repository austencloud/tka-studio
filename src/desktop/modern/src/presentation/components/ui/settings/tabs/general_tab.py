from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QComboBox,
    QFrame,
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont

from core.interfaces.tab_settings_interfaces import (
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
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)  # Reduced from 30
        main_layout.setSpacing(12)  # Reduced from 20

        title = QLabel("General Settings")
        title.setObjectName("section_title")
        title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # User Profile Section
        user_section = self._create_user_section()
        main_layout.addWidget(user_section)

        # Application Behavior Section
        behavior_section = self._create_behavior_section()
        main_layout.addWidget(behavior_section)

        main_layout.addStretch()
        self._apply_styling()

    def _create_user_section(self):
        section = QFrame()
        section.setObjectName("settings_section")
        layout = QVBoxLayout(section)
        layout.setContentsMargins(16, 12, 16, 12)  # Reduced padding
        layout.setSpacing(10)  # Reduced spacing

        title = QLabel("User Profile")
        title.setObjectName("subsection_title")
        layout.addWidget(title)

        # Current User
        user_layout = QHBoxLayout()
        user_layout.setSpacing(8)  # Reduced spacing
        user_layout.addWidget(QLabel("Current User:"))
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter your name")
        user_layout.addWidget(self.user_input)
        layout.addLayout(user_layout)

        return section

    def _create_behavior_section(self):
        section = QFrame()
        section.setObjectName("settings_section")
        layout = QVBoxLayout(section)
        layout.setContentsMargins(16, 12, 16, 12)  # Reduced padding
        layout.setSpacing(10)  # Reduced spacing

        title = QLabel("Application Behavior")
        title.setObjectName("subsection_title")
        layout.addWidget(title)

        # Enable fades
        self.enable_fades = QCheckBox("Enable smooth transitions")
        self.enable_fades.setToolTip("Enable smooth fade transitions between views")
        layout.addWidget(self.enable_fades)

        # Auto-save
        self.auto_save = QCheckBox("Auto-save changes")
        self.auto_save.setToolTip("Automatically save changes without prompting")
        layout.addWidget(self.auto_save)

        # Theme selection
        theme_layout = QHBoxLayout()
        theme_layout.setSpacing(8)  # Reduced spacing
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Auto"])
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        return section

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
        self.user_input.textChanged.connect(self._on_user_changed)
        self.enable_fades.toggled.connect(
            lambda x: self.setting_changed.emit("enable_fades", x)
        )
        self.auto_save.toggled.connect(
            lambda x: self.setting_changed.emit("auto_save", x)
        )
        self.theme_combo.currentTextChanged.connect(
            lambda x: self.setting_changed.emit("theme", x)
        )

    def _on_user_changed(self, text: str):
        self.user_service.set_current_user(text.strip())
        self.setting_changed.emit("current_user", text.strip())
