#!/usr/bin/env python3
"""
Application Grid Widget - Premium 2025 Application Display
=========================================================

A responsive grid widget for displaying TKA applications with:
- Premium 2025 glassmorphism card design
- Advanced micro-interactions and animations
- Staggered entrance effects
- Search filtering with modern UI
- Category organization
- Launch functionality with spring physics

Architecture:
- Enhanced ModernApplicationCard with premium animations
- Staggered entrance animations
- Integrated design system
- Performance-optimized rendering
- Pure PyQt6 implementation
"""

import logging

from PyQt6.QtCore import (
    QSize,
    Qt,
    QTimer,
    pyqtSignal,
)
from PyQt6.QtWidgets import (
    QGridLayout,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)

from ..components import ReliableApplicationCard
from ..reliable_effects import get_animation_manager

ApplicationCard = ReliableApplicationCard


class ApplicationGridWidget(QWidget):
    """
    Responsive grid widget for displaying applications.
    """

    application_launched = pyqtSignal(str, str)  # app_id, app_title

    def __init__(self, tka_integration, parent=None):
        """Initialize the application grid."""
        super().__init__(parent)
        self.tka_integration = tka_integration
        self.applications = []
        self.filtered_applications = []
        self._initial_layout_complete = False
        self.setMinimumSize(400, 300)
        self._setup_layout()
        QTimer.singleShot(0, self._deferred_initialization)
        # Application grid initialized - log removed to reduce startup noise

    def _deferred_initialization(self):
        """Deferred initialization after the widget hierarchy is established."""
        self.updateGeometry()
        self.scroll_area.updateGeometry()
        from PyQt6.QtWidgets import QApplication

        QApplication.processEvents()
        self.refresh_applications()
        self._initial_layout_complete = True
        QTimer.singleShot(100, self._log_initial_sizing)

    def _log_initial_sizing(self):
        """Log initial sizing information for debugging."""
        # Sizing analysis removed to reduce startup noise

    def sizeHint(self):
        """Provide a reasonable size hint for the application grid."""
        return QSize(800, 400)

    def minimumSizeHint(self):
        """Provide minimum size hint."""
        return QSize(400, 300)

    def _setup_layout(self):
        """Setup the grid layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.scroll_area.setMinimumSize(400, 300)
        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.05);
                width: 8px;
                border-radius: 4px;
                margin: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                min-height: 24px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """
        )
        self.scroll_widget = QWidget()
        self.scroll_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.scroll_widget.setStyleSheet(
            """
            QWidget {
                background-color: transparent;
            }
        """
        )
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.grid_layout.setContentsMargins(16, 16, 16, 16)
        self.grid_layout.setSpacing(16)
        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)

    def refresh_applications(self):
        """Refresh the application list from TKA integration."""
        try:
            self.applications = self.tka_integration.get_applications()
            self.filtered_applications = self.applications.copy()
            self._update_grid()
        except Exception as e:
            logger.error(f"❌ Failed to refresh applications: {e}")
            self.applications = []
            self.filtered_applications = []
            self._update_grid()

    def filter_applications(self, search_text: str):
        """Filter applications based on search text."""
        if not search_text:
            self.filtered_applications = self.applications.copy()
        else:
            search_lower = search_text.lower()
            self.filtered_applications = [
                app
                for app in self.applications
                if (
                    search_lower in app.title.lower()
                    or search_lower in app.description.lower()
                    or search_lower in app.category.value.lower()
                )
            ]
        self._update_grid()

    def _update_grid(self):
        """Update the grid display with current applications."""
        self._clear_grid()
        from PyQt6.QtWidgets import QApplication

        QApplication.processEvents()
        available_container_width = self._calculate_available_width()
        if available_container_width <= 0:
            QTimer.singleShot(50, self._update_grid)
            return
        card_dimensions = self._calculate_card_dimensions_for_3_rows(
            available_container_width
        )
        organized_apps = self._organize_apps_by_category()
        cards_created = []
        for row_index, (_, apps) in enumerate(organized_apps.items()):
            for col_index, app in enumerate(apps):
                card = ReliableApplicationCard(
                    app, card_dimensions["width"], card_dimensions["height"]
                )
                card.launch_requested.connect(self._on_launch_requested)
                self.grid_layout.addWidget(card, row_index, col_index)
                cards_created.append(card)
        self.scroll_widget.updateGeometry()

    def _calculate_available_width(self):
        """Calculate the available width for the grid layout."""
        scroll_viewport_width = self.scroll_area.viewport().width()
        if scroll_viewport_width > 0:
            return scroll_viewport_width
        scroll_area_width = self.scroll_area.width()
        if scroll_area_width > 0:
            return scroll_area_width - 20
        widget_width = self.width()
        if widget_width > 0:
            return widget_width
        parent_widget = self.parent()
        while parent_widget and parent_widget.width() <= 0:
            parent_widget = parent_widget.parent()
        if parent_widget and parent_widget.width() > 0:
            return parent_widget.width() - 64
        hint_width = self.sizeHint().width()
        return hint_width

    def _organize_apps_by_category(self):
        """Organize applications into 3 rows by category."""
        from domain.models import ApplicationCategory

        organized = {"Desktop Apps": [], "Web Apps": [], "Development Tools": []}
        sorted_apps = sorted(
            self.filtered_applications, key=lambda app: app.display_order
        )
        for app in sorted_apps:
            if app.category == ApplicationCategory.DESKTOP:
                organized["Desktop Apps"].append(app)
            elif app.category == ApplicationCategory.WEB:
                organized["Web Apps"].append(app)
            elif app.category == ApplicationCategory.DEVELOPMENT:
                organized["Development Tools"].append(app)
        return organized

    def _calculate_card_dimensions_for_3_rows(self, container_width):
        """Calculate card dimensions that fit exactly in 3 rows without scrolling."""
        available_height = self._calculate_available_height()
        grid_margins = 32
        row_spacing = 32
        available_card_height = available_height - grid_margins - row_spacing
        card_height = max(80, available_card_height // 3)
        total_needed_height = (card_height * 3) + grid_margins + row_spacing
        if total_needed_height > available_height:
            card_height = max(70, (available_height - grid_margins - row_spacing) // 3)
        organized_apps = self._organize_apps_by_category()
        max_cards_per_row = (
            max(len(apps) for apps in organized_apps.values()) if organized_apps else 1
        )
        # Ensure max_cards_per_row is at least 1 to prevent division by zero
        max_cards_per_row = max(1, max_cards_per_row)

        grid_side_margins = 32
        card_spacing = (max_cards_per_row - 1) * 16 if max_cards_per_row > 1 else 0
        available_card_width = container_width - grid_side_margins - card_spacing
        card_width = max(150, available_card_width // max_cards_per_row)
        return {"width": card_width, "height": card_height}

    def _calculate_available_height(self):
        """Calculate the available height for the grid layout."""
        scroll_viewport_height = self.scroll_area.viewport().height()
        if scroll_viewport_height > 0:
            return scroll_viewport_height
        scroll_area_height = self.scroll_area.height()
        if scroll_area_height > 0:
            return scroll_area_height
        widget_height = self.height()
        if widget_height > 0:
            return widget_height
        hint_height = self.sizeHint().height()
        return hint_height

    def _animate_cards_entrance(self, cards):
        """Animate staggered entrance for cards."""
        try:
            animation_manager = get_animation_manager()
            for i, card in enumerate(cards):
                delay = i * 50
                QTimer.singleShot(
                    delay, lambda c=card: self._start_entrance_animation(c)
                )
        except Exception as e:
            logger.warning("Could not animate card entrance: %s", e)

    def _start_entrance_animation(self, card):
        """Start entrance animation for a single card."""
        animation_manager = get_animation_manager()
        entrance_anim = animation_manager.smooth_fade(card, fade_in=True)
        entrance_anim.start()

    def _clear_grid(self):
        """Clear all cards from the grid."""
        items_to_remove = []
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                items_to_remove.append(item.widget())
        for widget in items_to_remove:
            self.grid_layout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child and child.widget():
                child.widget().deleteLater()

    def _on_launch_requested(self, app_id: str):
        """Handle application launch request."""
        self.launch_application(app_id)

    def launch_application(self, app_id: str):
        """Launch an application by ID."""
        try:
            app = next((app for app in self.applications if app.id == app_id), None)
            if not app:
                logger.error(f"❌ Application not found: {app_id}")
                return
            logger.info(f"🚀 Launching application: {app.title}")
            success = self.tka_integration.launch_application(app_id)
            if success:
                self.application_launched.emit(app_id, app.title)
            else:
                logger.error(f"❌ Failed to launch: {app.title}")
        except Exception as e:
            logger.error(f"❌ Error launching application {app_id}: {e}")

    def cleanup(self):
        """Cleanup resources."""
        logger.info("🧹 Cleaning up application grid...")
        self._clear_grid()

    def resizeEvent(self, event):
        """Handle resize events to update card sizes dynamically."""
        super().resizeEvent(event)
        if (
            hasattr(self, "filtered_applications")
            and self.filtered_applications
            and self._initial_layout_complete
        ):
            self._update_grid()

    def showEvent(self, event):
        """Handle show event to ensure proper sizing."""
        super().showEvent(event)
        if self._initial_layout_complete:
            QTimer.singleShot(50, self._update_grid)
        QTimer.singleShot(500, self.log_component_sizes)

    def log_component_sizes(self):
        """Log the sizes of all components in the hierarchy to debug width constraints."""
        logger.info("🔍 ===== COMPONENT SIZE ANALYSIS =====")
        main_window = self
        while main_window.parent():
            main_window = main_window.parent()
        logger.info(
            f"1. Main Window: {main_window.size().width()}x{main_window.size().height()}"
        )
        from PyQt6.QtWidgets import QTabWidget

        tab_widget = main_window.findChild(QTabWidget)
        if tab_widget:
            logger.info(
                f"2. Tab Widget: {tab_widget.size().width()}x{tab_widget.size().height()}"
            )
            home_interface = tab_widget.currentWidget()
            if home_interface:
                logger.info(
                    f"3. Home Interface: {home_interface.size().width()}x{home_interface.size().height()}"
                )
        logger.info(
            f"4. ApplicationGridWidget: {self.size().width()}x{self.size().height()}"
        )
        if hasattr(self, "scroll_area"):
            logger.info(
                f"5. ScrollArea: {self.scroll_area.size().width()}x{self.scroll_area.size().height()}"
            )
            logger.info(
                f"   ScrollArea viewport: {self.scroll_area.viewport().size().width()}x{self.scroll_area.viewport().size().height()}"
            )
        if hasattr(self, "scroll_widget"):
            logger.info(
                f"6. Scroll Widget: {self.scroll_widget.size().width()}x{self.scroll_widget.size().height()}"
            )
        if hasattr(self, "flow_layout"):
            rect = self.flow_layout.geometry()
            logger.info(f"7. FlowLayout: {rect.width()}x{rect.height()}")
        if hasattr(self, "flow_layout") and self.flow_layout.count() > 0:
            first_card = self.flow_layout.itemAt(0).widget()
            if first_card:
                logger.info(
                    f"8. ApplicationCard (sample): {first_card.size().width()}x{first_card.size().height()}"
                )
        logger.info("🔍 ===== END SIZE ANALYSIS =====")
