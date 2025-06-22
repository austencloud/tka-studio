"""
Production-ready settings dialog - drop-in replacement for ModernSettingsDialog.

This is the enhanced settings dialog that combines the beautiful glassmorphism design
from the legacy system with the modern architecture. It's designed to be a complete
replacement for the existing ModernSettingsDialog.

Features:
- Glassmorphism design with translucent backgrounds and blur effects
- Enhanced component architecture with reusable SettingCard, Toggle, ComboBox
- Settings coordinator for centralized state management
- Smooth animations and modern visual hierarchy
- All essential tabs: General, Prop Types, Visibility, Beat Layout, Image Export, Background
- Backward compatible service integration

This dialog automatically creates and manages all required services internally,
making it a true drop-in replacement that requires minimal integration effort.

Usage:
    Replace any instance of ModernSettingsDialog with SettingsDialog:

    # Old way:
    dialog = ModernSettingsDialog(ui_state_service, parent)

    # New way:
    dialog = SettingsDialog(ui_state_service, parent)

The new dialog provides the same interface while delivering a significantly
enhanced user experience with modern visual design.

Note: Import errors in IDE are expected due to relative imports - all services
and tabs exist and will resolve correctly at runtime.
"""

from typing import Any, Dict, Optional

from core.interfaces.core_services import IUIStateManagementService
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QCursor, QFont, QLinearGradient, QPainter
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .coordinator import SettingsCoordinator
from .tabs.background_tab import BackgroundTab
from .tabs.beat_layout_tab import BeatLayoutTab
from .tabs.codex_exporter_tab import CodexExporterTab
from .tabs.general_tab import GeneralTab
from .tabs.image_export_tab import ImageExportTab
from .tabs.prop_type_tab import PropTypeTab
from .tabs.visibility_tab import VisibilityTab


class SettingsDialog(QDialog):
    """Modern settings dialog with sidebar navigation and glassmorphism design."""

    settings_changed = pyqtSignal(str, object)

    def __init__(self, ui_state_service: IUIStateManagementService, parent=None):
        super().__init__(parent)
        self.ui_state_service = ui_state_service

        # Initialize tab structure
        self.tab_order = [
            "General",
            "Prop Type",
            "Visibility",
            "Beat Layout",
            "Image Export",
            "Background",
            "Codex Exporter",
        ]
        self.tabs: Dict[str, QWidget] = {}
        self.current_tab_index = 0

        self._setup_coordinator()
        self._initialize_services()
        self._setup_dialog()
        self._create_ui()
        self._apply_styling()
        self._setup_animations()

    def _setup_coordinator(self):
        """Setup the settings coordinator for managing state."""
        from application.services.settings.settings_service import SettingsService

        settings_service = SettingsService(self.ui_state_service)
        self.coordinator = SettingsCoordinator(settings_service)
        self.coordinator.settings_changed.connect(self.settings_changed.emit)

    def _initialize_services(self):
        """Initialize all the tab-specific services."""
        from application.services.settings.background_service import BackgroundService
        from application.services.settings.beat_layout_service import BeatLayoutService
        from application.services.settings.image_export_service import (
            ImageExportService,
        )
        from application.services.settings.prop_type_service import PropTypeService
        from application.services.settings.user_profile_service import (
            UserProfileService,
        )
        from application.services.settings.visibility_service import VisibilityService

        self.user_service = UserProfileService(self.ui_state_service)
        self.prop_service = PropTypeService(self.ui_state_service)
        self.visibility_service = VisibilityService(self.ui_state_service)
        self.layout_service = BeatLayoutService(self.ui_state_service)
        self.export_service = ImageExportService(self.ui_state_service)
        self.background_service = BackgroundService(self.ui_state_service)

    def _setup_dialog(self):
        """Setup basic dialog properties."""
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setFixedSize(1200, 800)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _create_ui(self):
        """Create the modern UI layout with sidebar navigation."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Main container with glassmorphism effect
        self.container = QFrame()
        self.container.setObjectName("glassmorphism_container")
        main_layout.addWidget(self.container)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(25, 25, 25, 25)
        container_layout.setSpacing(20)

        # Enhanced header
        self._create_header(container_layout)

        # Content area with sidebar and stacked widget
        self._create_content_area(container_layout)

        # Enhanced action buttons
        self._create_action_buttons(container_layout)

    def _create_header(self, parent_layout):
        """Create the enhanced header with glassmorphism styling."""
        header_frame = QFrame()
        header_frame.setObjectName("header_frame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 15, 15, 15)

        # Title with enhanced styling
        title = QLabel("Settings")
        title.setObjectName("dialog_title")
        title.setFont(QFont("Inter", 28, QFont.Weight.Bold))

        # Close button with hover effects
        self.close_button = QPushButton("×")
        self.close_button.setObjectName("close_button")
        self.close_button.setFixedSize(45, 45)
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.clicked.connect(self.close)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.close_button)

        parent_layout.addWidget(header_frame)

    def _create_content_area(self, parent_layout):
        """Create the content area with sidebar navigation and stacked widget."""
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Create sidebar
        self._create_sidebar()
        content_layout.addWidget(self.sidebar)

        # Create stacked widget for tab content
        self.content_area = QStackedWidget()
        self.content_area.setMinimumWidth(500)
        content_layout.addWidget(self.content_area, stretch=1)

        # Create all tabs
        self._create_tabs()

        parent_layout.addLayout(content_layout)

    def _create_sidebar(self):
        """Create the settings dialog sidebar."""
        self.sidebar = QListWidget()
        self.sidebar.setObjectName("settings_sidebar")
        self.sidebar.setFixedWidth(240)
        self.sidebar.setSpacing(6)
        self.sidebar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.sidebar.setIconSize(QSize(24, 24))
        self.sidebar.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.sidebar.setMouseTracking(True)

        # Add tab items to sidebar
        for tab_name in self.tab_order:
            item = QListWidgetItem(tab_name)
            self.sidebar.addItem(item)

        # Connect selection change
        self.sidebar.currentRowChanged.connect(self._on_tab_selected)
        self.sidebar.setCurrentRow(0)  # Select first tab by default

    def _create_tabs(self):
        """Create all the tabs and add them to the stacked widget."""
        # General Tab
        general_tab = GeneralTab(self.user_service)
        general_tab.setting_changed.connect(self.coordinator.update_setting)
        self.tabs["General"] = general_tab
        self.content_area.addWidget(general_tab)

        # Prop Type Tab
        prop_tab = PropTypeTab(self.prop_service)
        prop_tab.prop_type_changed.connect(
            lambda prop_type: self.coordinator.update_setting("prop_type", prop_type)
        )
        self.tabs["Prop Type"] = prop_tab
        self.content_area.addWidget(prop_tab)

        # Visibility Tab
        visibility_tab = VisibilityTab(self.visibility_service)
        visibility_tab.visibility_changed.connect(self.coordinator.update_setting)
        self.tabs["Visibility"] = visibility_tab
        self.content_area.addWidget(visibility_tab)

        # Beat Layout Tab
        layout_tab = BeatLayoutTab(self.layout_service)
        layout_tab.layout_changed.connect(
            lambda length, rows, cols: self.coordinator.update_setting(
                "beat_layout", {"length": length, "rows": rows, "cols": cols}
            )
        )
        self.tabs["Beat Layout"] = layout_tab
        self.content_area.addWidget(layout_tab)

        # Image Export Tab
        export_tab = ImageExportTab(self.export_service)
        export_tab.export_option_changed.connect(self.coordinator.update_setting)
        self.tabs["Image Export"] = export_tab
        self.content_area.addWidget(export_tab)

        # Background Tab
        background_tab = BackgroundTab(self.background_service)
        background_tab.background_changed.connect(self.coordinator.update_setting)
        self.tabs["Background"] = background_tab
        self.content_area.addWidget(background_tab)

        # Codex Exporter Tab
        codex_tab = CodexExporterTab(self.ui_state_service)
        codex_tab.export_requested.connect(self._handle_codex_export)
        self.tabs["Codex Exporter"] = codex_tab
        self.content_area.addWidget(codex_tab)

    def _handle_codex_export(self, config: Dict[str, Any]):
        """Handle codex export request."""
        # For now, just save the configuration
        # In a full implementation, this would trigger the actual export process
        self.coordinator.update_setting("codex_export_config", config)

    def _on_tab_selected(self, index: int):
        """Handle tab selection from sidebar."""
        if hasattr(self, "content_area") and 0 <= index < self.content_area.count():
            self.content_area.setCurrentIndex(index)
            self.current_tab_index = index

    def _create_action_buttons(self, parent_layout):
        """Create enhanced action buttons."""
        button_frame = QFrame()
        button_frame.setObjectName("button_frame")
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(15, 15, 15, 15)
        button_layout.addStretch()

        # Reset button
        self.reset_button = QPushButton("Reset to Defaults")
        self.reset_button.setObjectName("secondary_button")
        self.reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_button.clicked.connect(self._reset_settings)

        # Apply button
        self.apply_button = QPushButton("Apply")
        self.apply_button.setObjectName("secondary_button")
        self.apply_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_button.clicked.connect(self._apply_settings)

        # OK button (primary)
        self.ok_button = QPushButton("OK")
        self.ok_button.setObjectName("primary_button")
        self.ok_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ok_button.clicked.connect(self.accept)

        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.ok_button)

        parent_layout.addWidget(button_frame)

    def _setup_animations(self):
        """Setup smooth animations for UI interactions."""
        # Fade in animation for dialog
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(250)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def showEvent(self, event):
        """Override show event to add fade in animation."""
        super().showEvent(event)
        self.setWindowOpacity(0)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()

    def _apply_settings(self):
        """Apply all current settings."""
        self.coordinator.save_settings()

    def _reset_settings(self):
        """Reset all settings to defaults with confirmation."""
        from PyQt6.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to their default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.coordinator.reset_to_defaults()

    def paintEvent(self, event):
        """Custom paint event for glassmorphism background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create glassmorphism background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(20, 25, 35, 180))
        gradient.setColorAt(0.5, QColor(25, 30, 40, 160))
        gradient.setColorAt(1, QColor(30, 35, 45, 180))

        painter.fillRect(self.rect(), QBrush(gradient))

    def _apply_styling(self):
        """Apply the enhanced glassmorphism styling."""
        self.setStyleSheet(
            """
            QDialog {
                background: transparent;
            }
            
            #glassmorphism_container {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12),
                    stop:0.5 rgba(255, 255, 255, 0.08),
                    stop:1 rgba(255, 255, 255, 0.06));
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 24px;
                backdrop-filter: blur(20px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }

            #header_frame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.08),
                    stop:1 rgba(255, 255, 255, 0.04));
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 16px;
                margin-bottom: 16px;
                padding: 8px;
            }

            #dialog_title {
                color: rgba(255, 255, 255, 0.98);
                background: transparent;
                padding: 8px;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-weight: 700;
                letter-spacing: -0.5px;
            }
            
            #close_button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 22px;
                color: rgba(255, 255, 255, 0.85);
                font-size: 18px;
                font-weight: 600;
                font-family: "Inter", sans-serif;
            }

            #close_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 100, 100, 0.4),
                    stop:1 rgba(255, 80, 80, 0.3));
                border-color: rgba(255, 150, 150, 0.6);
                color: white;
                transform: scale(1.05);
            }

            #close_button:pressed {
                background: rgba(255, 60, 60, 0.5);
                transform: scale(0.95);
            }
            
            #settings_sidebar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.08),
                    stop:1 rgba(255, 255, 255, 0.04));
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 16px;
                outline: none;
                selection-background-color: transparent;
                padding: 8px;
            }

            #settings_sidebar::item {
                background: transparent;
                border: none;
                padding: 16px 20px;
                margin: 4px 0px;
                border-radius: 12px;
                color: rgba(255, 255, 255, 0.75);
                font-weight: 500;
                font-size: 14px;
                font-family: "Inter", "Segoe UI", sans-serif;
                letter-spacing: 0.2px;
            }

            #settings_sidebar::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(42, 130, 218, 0.4),
                    stop:1 rgba(42, 130, 218, 0.25));
                border: 1px solid rgba(42, 130, 218, 0.6);
                color: white;
                font-weight: 600;
                box-shadow: 0 2px 8px rgba(42, 130, 218, 0.2);
            }

            #settings_sidebar::item:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.08));
                color: rgba(255, 255, 255, 0.95);
                transform: translateX(2px);
            }

            QStackedWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.08),
                    stop:1 rgba(255, 255, 255, 0.04));
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 16px;
                padding: 8px;
            }

            #button_frame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.08),
                    stop:1 rgba(255, 255, 255, 0.04));
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 16px;
                margin-top: 16px;
                padding: 8px;
            }
            
            #primary_button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(42, 130, 218, 0.9),
                    stop:0.5 rgba(42, 130, 218, 0.8),
                    stop:1 rgba(42, 130, 218, 0.7));
                border: 1px solid rgba(42, 130, 218, 1.0);
                border-radius: 14px;
                color: white;
                font-weight: 600;
                padding: 14px 28px;
                font-size: 14px;
                font-family: "Inter", "Segoe UI", sans-serif;
                letter-spacing: 0.3px;
                box-shadow: 0 4px 16px rgba(42, 130, 218, 0.3);
            }

            #primary_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(42, 130, 218, 1.0),
                    stop:0.5 rgba(42, 130, 218, 0.9),
                    stop:1 rgba(42, 130, 218, 0.8));
                box-shadow: 0 6px 20px rgba(42, 130, 218, 0.4);
                transform: translateY(-1px);
            }

            #primary_button:pressed {
                background: rgba(42, 130, 218, 0.95);
                transform: translateY(0px);
                box-shadow: 0 2px 8px rgba(42, 130, 218, 0.3);
            }
            
            #secondary_button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 14px;
                color: rgba(255, 255, 255, 0.85);
                font-weight: 500;
                padding: 14px 24px;
                font-size: 14px;
                font-family: "Inter", "Segoe UI", sans-serif;
                letter-spacing: 0.2px;
                margin-right: 12px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }

            #secondary_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.2),
                    stop:1 rgba(255, 255, 255, 0.12));
                color: white;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                transform: translateY(-1px);
            }

            #secondary_button:pressed {
                background: rgba(255, 255, 255, 0.1);
                transform: translateY(0px);
                box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
            }

            /* Settings group styling */
            QGroupBox {
                font-weight: 600;
                color: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 12px;
                margin-top: 16px;
                padding-top: 16px;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-size: 15px;
                letter-spacing: 0.3px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 4px 12px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
            }

            /* Setting controls styling */
            QLabel[objectName="setting_label"] {
                color: rgba(255, 255, 255, 0.85);
                font-weight: 500;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-size: 14px;
                letter-spacing: 0.2px;
            }

            QSpinBox, QDoubleSpinBox, QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12),
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 10px;
                padding: 10px 14px;
                color: white;
                font-size: 14px;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-weight: 500;
            }

            QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border-color: rgba(42, 130, 218, 0.8);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.18),
                    stop:1 rgba(255, 255, 255, 0.12));
                box-shadow: 0 0 0 2px rgba(42, 130, 218, 0.2);
            }

            QCheckBox {
                color: rgba(255, 255, 255, 0.85);
                font-weight: 500;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-size: 14px;
                letter-spacing: 0.2px;
            }

            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 0.35);
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12),
                    stop:1 rgba(255, 255, 255, 0.06));
            }

            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(42, 130, 218, 0.8),
                    stop:1 rgba(42, 130, 218, 0.6));
                border-color: rgba(42, 130, 218, 1.0);
                box-shadow: 0 2px 8px rgba(42, 130, 218, 0.3);
            }

            QCheckBox::indicator:hover {
                border-color: rgba(255, 255, 255, 0.5);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.18),
                    stop:1 rgba(255, 255, 255, 0.10));
            }
        """
        )
