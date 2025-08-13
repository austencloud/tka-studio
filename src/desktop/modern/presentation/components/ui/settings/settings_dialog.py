from __future__ import annotations

from typing import Any

from PyQt6.QtCore import QRectF, Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QLinearGradient, QPainter, QPainterPath, QRegion
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.application.services.ui.ui_settings_manager import UISettingsManager
from desktop.modern.core.interfaces.core_services import IUIStateManager
from desktop.modern.presentation.components.ui.settings.tabs.background_tab import (
    BackgroundTab,
)
from desktop.modern.presentation.components.ui.settings.tabs.beat_layout_tab import (
    BeatLayoutTab,
)
from desktop.modern.presentation.components.ui.settings.tabs.codex_exporter_tab import (
    CodexExporterTab,
)
from desktop.modern.presentation.components.ui.settings.tabs.general_tab import (
    GeneralTab,
)
from desktop.modern.presentation.components.ui.settings.tabs.image_export_tab import (
    ImageExportTab,
)
from desktop.modern.presentation.components.ui.settings.tabs.prop_type_tab import (
    PropTypeTab,
)
from desktop.modern.presentation.components.ui.settings.visibility.visibility_tab import (
    VisibilityTab,
)

# Import new design system instead of scattered components
from desktop.modern.presentation.styles.mixins import StyleMixin

from .components import (
    SettingsActionButtons,
    SettingsAnimations,
    SettingsContentArea,
    SettingsHeader,
    SettingsSidebar,
)


class SettingsDialog(QDialog, StyleMixin):
    """Modern settings dialog with sidebar navigation and glassmorphism design."""

    settings_changed = pyqtSignal(str, object)

    def __init__(self, ui_state_service: IUIStateManager, parent=None, container=None):
        super().__init__(parent)
        self.ui_state_service = ui_state_service
        self.container = container

        # Initialize drag position for window dragging
        self.drag_position = None

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
        self.current_tab_index = 0

        # Initialize components
        self.services = UISettingsManager(ui_state_service, container)
        self.animations = SettingsAnimations(self)

        self._setup_coordinator()
        self._setup_dialog()
        self._create_ui()
        self._apply_styling()
        self._connect_signals()

    def mousePressEvent(self, event):
        """Handle mouse press for dragging frameless dialog."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if click is on interactive element
            widget_under_mouse = self.childAt(event.pos())
            if self._is_draggable_area(widget_under_mouse):
                # Store the position where the mouse was pressed
                self.drag_position = (
                    event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                )
                event.accept()
                return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging frameless dialog."""
        if (
            event.buttons() == Qt.MouseButton.LeftButton
            and self.drag_position is not None
        ):
            # Move the dialog to the new position
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release to stop dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def _is_draggable_area(self, widget):
        """Check if the clicked widget is in a draggable area (not interactive)."""
        if widget is None:
            return True

        # Allow dragging on non-interactive components
        draggable_types = (QLabel, QFrame, QWidget)
        interactive_types = (QPushButton, QListWidget)

        # Don't drag if clicking on interactive elements
        if isinstance(widget, interactive_types):
            return False

        # Allow dragging on frame containers and labels
        if isinstance(widget, draggable_types):
            return True

        # Check parent widgets for draggable areas
        parent = widget.parent()
        while parent and parent != self:
            if isinstance(parent, interactive_types):
                return False
            if isinstance(parent, draggable_types):
                return True
            parent = parent.parent()

        return True

    def _setup_coordinator(self):
        """Setup the settings coordinator for managing state."""
        from desktop.modern.application.services.settings.settings_coordinator import (
            SettingsCoordinator,
        )
        from desktop.modern.presentation.components.ui.settings.settings_ui_adapter import (
            SettingsUIAdapter,
        )

        # Create the framework-agnostic service
        settings_service = SettingsCoordinator(self.ui_state_service)

        # Create the UI adapter to bridge Qt and the service
        self.coordinator = SettingsUIAdapter(settings_service)
        self.coordinator.settings_changed.connect(self.settings_changed.emit)

    def _setup_dialog(self):
        """Setup basic dialog properties with responsive sizing."""
        self.setWindowTitle("Settings")
        self.setModal(True)

        # Get screen geometry for responsive sizing
        screen = self.screen()
        if screen:
            screen_geometry = screen.availableGeometry()
            # Use more conservative sizing: 60% width, 50% height for better fit
            dialog_width = int(screen_geometry.width() * 0.60)
            dialog_height = int(screen_geometry.height() * 0.50)

            # Set tighter bounds to prevent oversized dialogs
            dialog_width = max(800, min(dialog_width, 1400))  # Min 800px, max 1400px
            dialog_height = max(500, min(dialog_height, 800))  # Min 500px, max 800px
        else:
            # Fallback if screen detection fails
            dialog_width, dialog_height = 1000, 650

        # Use resize instead of setFixedSize to allow content-driven sizing within limits
        self.resize(dialog_width, dialog_height)
        self.setMinimumSize(800, 500)
        self.setMaximumSize(1400, 800)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _create_ui(self):
        """Create the modern UI layout with components."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Main container with glassmorphism effect
        self.container = QFrame()
        self.container.setObjectName("glassmorphism_container")
        main_layout.addWidget(self.container)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(
            16, 16, 16, 16
        )  # Reduced margins for better content fit
        container_layout.setSpacing(12)  # Tighter spacing to fit content better

        # Create header
        self.header = SettingsHeader("Settings")
        container_layout.addWidget(self.header)

        # Content area with sidebar and content
        self._create_content_area(container_layout)

        # Action buttons
        self.action_buttons = SettingsActionButtons()
        container_layout.addWidget(self.action_buttons)

    def _create_content_area(self, parent_layout):
        """Create the content area with sidebar navigation and content."""
        content_layout = QHBoxLayout()
        content_layout.setSpacing(16)  # Reduced spacing for better content fit

        # Create sidebar
        self.sidebar = SettingsSidebar(self.tab_order)
        content_layout.addWidget(self.sidebar)

        # Create content area
        self.content_area = SettingsContentArea()
        content_layout.addWidget(self.content_area, stretch=1)

        # Create all tabs
        self._create_tabs()

        parent_layout.addLayout(content_layout)

    def _create_tabs(self):
        """Create all the tabs and add them to the content area."""
        # General Tab
        general_tab = GeneralTab(self.services.get_user_service())
        general_tab.setting_changed.connect(self.coordinator.update_setting)
        self.content_area.add_tab("General", general_tab)

        # Prop Type Tab
        prop_tab = PropTypeTab(self.services.get_prop_service())
        prop_tab.prop_type_changed.connect(
            lambda prop_type: self.coordinator.update_setting("prop_type", prop_type)
        )
        self.content_area.add_tab("Prop Type", prop_tab)

        # Visibility Tab - using simple visibility service
        visibility_tab = VisibilityTab(self.services.get_visibility_service())
        visibility_tab.visibility_changed.connect(self.coordinator.update_setting)
        self.content_area.add_tab("Visibility", visibility_tab)

        # Beat Layout Tab
        layout_tab = BeatLayoutTab(self.services.get_layout_service())
        layout_tab.layout_changed.connect(
            lambda length, rows, cols: self.coordinator.update_setting(
                "beat_layout", {"length": length, "rows": rows, "cols": cols}
            )
        )
        self.content_area.add_tab("Beat Layout", layout_tab)

        # Image Export Tab
        export_tab = ImageExportTab(self.services.get_export_service())
        export_tab.export_option_changed.connect(self.coordinator.update_setting)
        self.content_area.add_tab("Image Export", export_tab)

        # Background Tab
        background_tab = BackgroundTab(self.services.get_background_service())
        background_tab.background_changed.connect(self.coordinator.update_setting)
        self.content_area.add_tab("Background", background_tab)

        # Codex Exporter Tab
        codex_tab = CodexExporterTab(self.ui_state_service)
        codex_tab.export_requested.connect(self._handle_codex_export)
        self.content_area.add_tab("Codex Exporter", codex_tab)

    def _connect_signals(self):
        """Connect component signals."""
        self.header.close_requested.connect(self.reject)
        self.sidebar.tab_selected.connect(self._on_tab_selected)
        self.action_buttons.reset_requested.connect(self._reset_settings)
        self.action_buttons.apply_requested.connect(self._apply_settings)
        self.action_buttons.ok_requested.connect(self.accept)

    def _handle_codex_export(self, config: dict[str, Any]):
        """Handle codex export request."""
        # For now, just save the configuration
        # In a full implementation, this would trigger the actual export process
        self.coordinator.update_setting("codex_export_config", config)

    def _on_tab_selected(self, index: int, tab_name: str):
        """Handle tab selection from sidebar."""
        self.content_area.select_tab(index)
        self.current_tab_index = index

    def _apply_styling(self):
        """Apply the glassmorphism styling using the centralized design system."""
        self.apply_dialog_style()

    def showEvent(self, event):
        """Override show event to add fade in animation."""
        super().showEvent(event)
        self.animations.fade_in()

    def _apply_settings(self):
        """Apply all current settings."""
        self.coordinator.save_settings()

    def _reset_settings(self):
        """Reset all settings to defaults with confirmation."""
        # TODO: Implement reset confirmation dialog

    def paintEvent(self, event):
        """Custom paint event for glassmorphism background with proper masking."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create rounded rectangle path for the entire dialog
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 24, 24)

        # Set clipping to the rounded path
        painter.setClipPath(path)

        # Create glassmorphism background with enhanced opacity for better visibility
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(8, 12, 20, 250))  # Even more opaque
        gradient.setColorAt(0.3, QColor(12, 16, 24, 245))
        gradient.setColorAt(0.7, QColor(16, 20, 28, 248))
        gradient.setColorAt(1, QColor(10, 14, 22, 252))

        painter.fillRect(self.rect(), QBrush(gradient))

        # Create the window mask for proper rounded edges without black corners
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    # Backward compatibility properties and methods
    @property
    def tabs(self):
        """Get tabs dictionary for backward compatibility."""
        return self.content_area.tabs if self.content_area else {}

    def get_tab(self, tab_name: str):
        """Get a specific tab widget."""
        return self.content_area.get_tab(tab_name) if self.content_area else None

    def refresh_all_tabs(self):
        """Refresh all tab contents."""
        if self.content_area:
            self.content_area.refresh_all_tabs()
