from __future__ import annotations

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont, QIcon
from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from desktop.modern.core.interfaces.tab_settings_interfaces import (
    IPropTypeSettingsManager,
    PropType,
)


class PropButton(QPushButton):
    """Modern prop button with visual prop image and glassmorphism styling."""

    def __init__(self, prop_name: str, icon_path: str, parent=None):
        super().__init__(parent)
        self.prop_name = prop_name
        self.icon_path = icon_path
        self.setFixedSize(QSize(100, 100))
        self.setIconSize(QSize(64, 64))
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._is_active = False

        # Load and set icon
        if icon_path:
            self.setIcon(QIcon(icon_path))

        self._apply_styling()

    def set_active(self, active: bool):
        self._is_active = active
        self._apply_styling()

    def _apply_styling(self):
        if self._is_active:
            # Active state - highlighted with primary color
            self.setStyleSheet(
                """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(42, 130, 218, 0.8),
                        stop:1 rgba(42, 130, 218, 0.6));
                    border: 2px solid rgba(42, 130, 218, 1.0);
                    border-radius: 12px;
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                }

                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(42, 130, 218, 1.0),
                        stop:1 rgba(42, 130, 218, 0.8));
                }

                QPushButton:pressed {
                    background: rgba(42, 130, 218, 0.9);
                }
            """
            )
        else:
            # Inactive state - subtle glassmorphism
            self.setStyleSheet(
                """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 255, 255, 0.12),
                        stop:1 rgba(255, 255, 255, 0.08));
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 12px;
                    color: rgba(255, 255, 255, 0.8);
                    padding: 8px;
                }

                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 255, 255, 0.18),
                        stop:1 rgba(255, 255, 255, 0.12));
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    color: rgba(255, 255, 255, 0.9);
                }

                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 255, 255, 0.08),
                        stop:1 rgba(255, 255, 255, 0.06));
                }
            """
            )


class PropTypeTab(QWidget):
    """Modern prop type tab with visual prop buttons like the legacy version."""

    prop_type_changed = pyqtSignal(str)  # Changed to str to match legacy

    def __init__(self, prop_service: IPropTypeSettingsManager, parent=None):
        super().__init__(parent)
        self.prop_service = prop_service
        self.buttons: dict[str, PropButton] = {}
        self._setup_ui()
        self._load_current_prop()
        self._setup_connections()

    def _setup_ui(self):
        """Setup UI with tighter spacing for better content fit."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)  # Reduced for better fit
        main_layout.setSpacing(12)  # Tighter spacing

        # Title with enhanced styling
        title = QLabel("Prop Type")
        title.setObjectName("section_title")
        title.setFont(QFont("Inter", 20, QFont.Weight.Bold))  # Larger title
        main_layout.addWidget(title)

        # Description with better styling
        description = QLabel(
            "Select the prop type for your sequences. This affects the visual appearance and behavior of props in your sequences."
        )
        description.setObjectName("description")
        description.setWordWrap(True)
        description.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        main_layout.addWidget(description)

        # Props container with enhanced glassmorphism styling
        props_container = QWidget()
        props_container.setObjectName("props_container")
        container_layout = QVBoxLayout(props_container)
        container_layout.setContentsMargins(
            12, 12, 12, 12
        )  # Reduced padding for better fit
        container_layout.setSpacing(8)  # Tighter spacing

        # Create grid layout for prop buttons
        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # Define props with their icon paths (absolute paths to modern/images)
        from pathlib import Path
        # Navigate from this file to the modern directory: tabs -> settings -> ui -> components -> presentation -> modern
        modern_dir = Path(__file__).parent.parent.parent.parent.parent.parent
        images_dir = modern_dir / "images"
        props = {
            "Staff": str(images_dir / "props/staff.svg"),
            "Simplestaff": str(images_dir / "props/simple_staff.svg"),
            "Club": str(images_dir / "props/club.svg"),
            "Fan": str(images_dir / "props/fan.svg"),
            "Triad": str(images_dir / "props/triad.svg"),
            "Minihoop": str(images_dir / "props/minihoop.svg"),
            "Buugeng": str(images_dir / "props/buugeng.svg"),
            "Triquetra": str(images_dir / "props/triquetra.svg"),
            "Sword": str(images_dir / "props/sword.svg"),
            "Chicken": str(images_dir / "props/chicken.png"),
            "Hand": str(images_dir / "props/hand.svg"),
            "Guitar": str(images_dir / "props/guitar.svg"),
            "Ukulele": str(images_dir / "props/ukulele.svg"),
        }

        # Create prop buttons in a 4-column grid with cell containers like legacy
        row, col = 0, 0
        for prop, icon_path in props.items():
            # Create prop button with enhanced styling
            button = PropButton(prop, icon_path, self)
            button.clicked.connect(
                lambda checked, p=prop: self._set_current_prop_type(p)
            )
            self.buttons[prop] = button

            # Create label with legacy-style font
            label = QLabel(prop)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFont(QFont("Inter", 11, QFont.Weight.Medium))
            label.setStyleSheet("color: rgba(255, 255, 255, 0.85);")

            # Create cell container like legacy for better organization
            cell_widget = QWidget()
            cell_layout = QVBoxLayout(cell_widget)
            cell_layout.setContentsMargins(6, 6, 6, 6)  # Better padding
            cell_layout.setSpacing(4)  # Spacing between button and label
            cell_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
            cell_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

            grid_layout.addWidget(cell_widget, row, col)

            col += 1
            if col >= 4:  # 4 columns for better layout
                col = 0
                row += 1

        container_layout.addLayout(grid_layout)
        main_layout.addWidget(props_container)
        main_layout.addStretch()
        self._apply_styling()

    def _apply_styling(self):
        self.setStyleSheet(
            """
            QWidget {
                background: transparent;
                color: white;
            }

            QLabel#section_title {
                color: rgba(255, 255, 255, 0.95);
                font-family: "Inter", "Segoe UI", sans-serif;
                font-weight: 700;
                letter-spacing: -0.5px;
            }

            QLabel#description {
                color: rgba(255, 255, 255, 0.8);
                font-family: "Inter", "Segoe UI", sans-serif;
                font-size: 14px;
                letter-spacing: 0.2px;
            }

            QWidget#props_container {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.18),
                    stop:1 rgba(255, 255, 255, 0.12));
                border: 1px solid rgba(255, 255, 255, 0.30);
                border-radius: 18px;
                padding: 12px;
                margin: 8px;
            }
        """
        )

    def _set_current_prop_type(self, prop_type: str):
        """Set the current prop type and update UI."""
        try:
            # Convert string to PropType enum if needed
            if isinstance(prop_type, str):
                # Try to find matching PropType
                for prop_enum in PropType:
                    if prop_enum.value.upper() == prop_type.upper():
                        prop_type_enum = prop_enum
                        break
                else:
                    # Fallback to STAFF if not found
                    prop_type_enum = PropType.STAFF
            else:
                prop_type_enum = prop_type

            # Update the service
            self.prop_service.set_prop_type(prop_type_enum)

            # Update button states
            self._update_active_button(prop_type)

            # Emit signal
            self.prop_type_changed.emit(prop_type)

        except Exception as e:
            print(f"Error setting prop type: {e}")

    def _update_active_button(self, active_prop: str):
        """Update which button appears active."""
        for prop, button in self.buttons.items():
            button.set_active(prop == active_prop)

    def _load_current_prop(self):
        """Load the current prop type from settings."""
        try:
            current_prop = self.prop_service.get_current_prop_type()
            if isinstance(current_prop, str) and current_prop in self.buttons:
                self._update_active_button(current_prop)
            elif hasattr(current_prop, "value") and current_prop.value in self.buttons:
                self._update_active_button(current_prop.value)
        except Exception as e:
            print(f"Error loading current prop: {e}")
            # Default to Staff if there's an error
            if "Staff" in self.buttons:
                self._update_active_button("Staff")

    def _setup_connections(self):
        """Setup signal connections."""
        # Connections are set up in _setup_ui

    def update_active_prop_type_from_settings(self):
        """Update the active prop type from current settings."""
        self._load_current_prop()
