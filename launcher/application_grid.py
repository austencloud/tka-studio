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
from typing import List, Optional

from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QRect,
    QSize,
    Qt,
    QTimer,
    pyqtSignal,
)
from PyQt6.QtGui import QColor, QFont, QPainter, QPalette, QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)

# Import reliable design system components
from ui.components import ReliableApplicationCard
from ui.reliable_effects import get_animation_manager

logger.info("🎨 Reliable UI components loaded successfully")


# Use the reliable application card
ApplicationCard = ReliableApplicationCard


class ApplicationGridWidget(QWidget):
    """
    Responsive grid widget for displaying applications.
    """

    # Signals
    application_launched = pyqtSignal(str, str)  # app_id, app_title

    def __init__(self, tka_integration, parent=None):
        """Initialize the application grid."""
        super().__init__(parent)

        self.tka_integration = tka_integration
        self.applications = []
        self.filtered_applications = []
        # Removed selected_card - using direct launching instead
        self._initial_layout_complete = False

        # Set minimum size to ensure the widget takes up reasonable space
        self.setMinimumSize(400, 300)  # Minimum size to ensure visibility

        # Setup layout
        self._setup_layout()

        # Defer application loading until after initial layout is complete
        # This prevents sizing issues during startup
        QTimer.singleShot(0, self._deferred_initialization)

        logger.info("✅ Application grid initialized")

    def _deferred_initialization(self):
        """Deferred initialization after the widget hierarchy is established."""
        # Force layout calculation to ensure proper sizing
        self.updateGeometry()
        self.scroll_area.updateGeometry()

        # Process any pending layout events
        from PyQt6.QtWidgets import QApplication

        QApplication.processEvents()

        # Load applications after the layout system has had a chance to calculate sizes
        self.refresh_applications()
        self._initial_layout_complete = True

        # Log initial sizing for debugging
        QTimer.singleShot(100, self._log_initial_sizing)

    def _log_initial_sizing(self):
        """Log initial sizing information for debugging."""
        logger.info("🔍 ===== INITIAL SIZING ANALYSIS =====")
        logger.info(
            f"ApplicationGridWidget: {self.size().width()}x{self.size().height()}"
        )
        logger.info(
            f"ScrollArea: {self.scroll_area.size().width()}x{self.scroll_area.size().height()}"
        )
        logger.info(
            f"ScrollArea viewport: {self.scroll_area.viewport().size().width()}x{self.scroll_area.viewport().size().height()}"
        )
        logger.info(
            f"Scroll Widget: {self.scroll_widget.size().width()}x{self.scroll_widget.size().height()}"
        )
        logger.info("🔍 ===== END INITIAL SIZING =====")

    def sizeHint(self):
        """Provide a reasonable size hint for the application grid."""
        # Return a size that works well for 4 cards across with proper spacing
        # This helps Qt's layout system make better initial size calculations
        return QSize(800, 400)  # Width for 4 cards, height for 2-3 rows

    def minimumSizeHint(self):
        """Provide minimum size hint."""
        return QSize(400, 300)  # Minimum for at least 2 cards across

    def _setup_layout(self):
        """Setup the grid layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Ensure this widget expands to fill available space
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create modern scroll area with glassmorphism
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        # Disable all scrollbars since we want everything to fit without scrolling
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Ensure scroll area expands to fill available space
        self.scroll_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Set minimum size for scroll area to help with initial layout
        self.scroll_area.setMinimumSize(400, 300)

        # Apply modern glassmorphism styling (without unsupported CSS properties)
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

        # Create scroll widget with flow layout
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

        # Use a simple grid layout instead of FlowLayout for now
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.grid_layout.setContentsMargins(16, 16, 16, 16)  # 8px grid system
        self.grid_layout.setSpacing(16)  # 8px grid system

        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)

    def refresh_applications(self):
        """Refresh the application list from TKA integration."""
        try:
            logger.info("🔄 Refreshing application list...")

            # Get applications from TKA integration
            self.applications = self.tka_integration.get_applications()
            self.filtered_applications = self.applications.copy()

            # Update the grid display
            self._update_grid()

            logger.info(f"✅ Loaded {len(self.applications)} applications")

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
        logger.info(f"🔍 Filtered to {len(self.filtered_applications)} applications")

    def _update_grid(self):
        """Update the grid display with current applications."""
        # Clear existing cards
        self._clear_grid()

        # Process pending deletion events to ensure clean slate
        from PyQt6.QtWidgets import QApplication

        QApplication.processEvents()

        # Calculate dynamic card width based on actual available width
        available_container_width = self._calculate_available_width()

        # If we still don't have a reliable width, defer the update
        if available_container_width <= 0:
            logger.debug("🔄 Deferring grid update - container width not available yet")
            QTimer.singleShot(50, self._update_grid)
            return

        # Calculate card dimensions for 3-row layout
        card_dimensions = self._calculate_card_dimensions_for_3_rows(
            available_container_width
        )

        # Debug logging
        logger.info(
            f"🎯 3-Row Layout: container_width={available_container_width}, "
            f"card_width={card_dimensions['width']}, card_height={card_dimensions['height']}"
        )

        # Organize applications by category for 3-row layout
        organized_apps = self._organize_apps_by_category()
        cards_created = []

        # Add cards in organized 3-row layout
        for row_index, (_, apps) in enumerate(organized_apps.items()):
            for col_index, app in enumerate(apps):
                card = ReliableApplicationCard(
                    app, card_dimensions["width"], card_dimensions["height"]
                )
                # Direct launching only - no selection needed
                card.launch_requested.connect(self._on_launch_requested)

                # Place in specific row based on category
                self.grid_layout.addWidget(card, row_index, col_index)
                cards_created.append(card)

        # Temporarily disable animations to debug card visibility
        # if ENHANCED_UI_AVAILABLE and cards_created:
        #     self._animate_cards_entrance(cards_created)

        # Update scroll widget size
        self.scroll_widget.updateGeometry()

    def _calculate_available_width(self):
        """Calculate the available width for the grid layout."""
        # Try multiple approaches to get a reliable width

        # Method 1: Use scroll area viewport width (most accurate when available)
        scroll_viewport_width = self.scroll_area.viewport().width()
        if scroll_viewport_width > 0:
            logger.debug(f"📏 Using scroll viewport width: {scroll_viewport_width}")
            return scroll_viewport_width

        # Method 2: Use scroll area width minus scrollbar space
        scroll_area_width = self.scroll_area.width()
        if scroll_area_width > 0:
            # Account for potential vertical scrollbar (typically 16-20px)
            available_width = scroll_area_width - 20
            logger.debug(
                f"📏 Using scroll area width: {available_width} (from {scroll_area_width})"
            )
            return available_width

        # Method 3: Use this widget's width
        widget_width = self.width()
        if widget_width > 0:
            logger.debug(f"📏 Using widget width: {widget_width}")
            return widget_width

        # Method 4: Walk up parent hierarchy
        parent_widget = self.parent()
        while parent_widget and parent_widget.width() <= 0:
            parent_widget = parent_widget.parent()

        if parent_widget and parent_widget.width() > 0:
            # Account for home interface margins (32 left + 32 right = 64)
            available_width = parent_widget.width() - 64
            logger.debug(
                f"📏 Using parent width: {available_width} (from {parent_widget.width()})"
            )
            return available_width

        # Method 5: Use size hint as fallback
        hint_width = self.sizeHint().width()
        logger.debug(f"📏 Using size hint fallback: {hint_width}")
        return hint_width

    def _organize_apps_by_category(self):
        """Organize applications into 3 rows by category."""
        from domain.models import ApplicationCategory

        # Initialize organized structure
        organized = {"Desktop Apps": [], "Web Apps": [], "Development Tools": []}

        # Sort applications by display_order to maintain consistent ordering
        sorted_apps = sorted(
            self.filtered_applications, key=lambda app: app.display_order
        )

        # Categorize applications
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
        # Get available height from scroll area
        available_height = self._calculate_available_height()

        # Calculate margins and spacing
        grid_margins = 32  # 16px top + 16px bottom from grid layout margins
        row_spacing = 32  # 16px spacing between rows * 2 gaps

        # Available height for cards (3 rows)
        available_card_height = available_height - grid_margins - row_spacing
        # Ensure cards fit within available space, with a reasonable minimum
        card_height = max(80, available_card_height // 3)  # Minimum 80px height

        # If calculated height is still too large, reduce it to fit
        total_needed_height = (card_height * 3) + grid_margins + row_spacing
        if total_needed_height > available_height:
            # Recalculate with tighter constraints
            card_height = max(70, (available_height - grid_margins - row_spacing) // 3)
            logger.debug(
                f"📏 Adjusted card height to fit: {card_height}px (available: {available_height}px)"
            )

        logger.debug(
            f"📏 Height calculation: available={available_height}, margins={grid_margins}, spacing={row_spacing}, card_height={card_height}"
        )

        # Calculate width based on container and number of cards per row
        # Find the maximum number of cards in any row
        organized_apps = self._organize_apps_by_category()
        max_cards_per_row = (
            max(len(apps) for apps in organized_apps.values()) if organized_apps else 1
        )

        # Calculate card width with spacing
        grid_side_margins = 32  # 16px left + 16px right
        card_spacing = (max_cards_per_row - 1) * 16 if max_cards_per_row > 1 else 0
        available_card_width = container_width - grid_side_margins - card_spacing
        card_width = max(
            150, available_card_width // max_cards_per_row
        )  # Minimum 150px width

        return {"width": card_width, "height": card_height}

    def _calculate_available_height(self):
        """Calculate the available height for the grid layout."""
        # Try multiple approaches to get a reliable height

        # Method 1: Use scroll area viewport height (most accurate when available)
        scroll_viewport_height = self.scroll_area.viewport().height()
        if scroll_viewport_height > 0:
            logger.debug(f"📏 Using scroll viewport height: {scroll_viewport_height}")
            return scroll_viewport_height

        # Method 2: Use scroll area height
        scroll_area_height = self.scroll_area.height()
        if scroll_area_height > 0:
            logger.debug(f"📏 Using scroll area height: {scroll_area_height}")
            return scroll_area_height

        # Method 3: Use this widget's height
        widget_height = self.height()
        if widget_height > 0:
            logger.debug(f"📏 Using widget height: {widget_height}")
            return widget_height

        # Method 4: Use size hint as fallback
        hint_height = self.sizeHint().height()
        logger.debug(f"📏 Using size hint height fallback: {hint_height}")
        return hint_height

    def _animate_cards_entrance(self, cards):
        """Animate staggered entrance for cards."""
        try:
            animation_manager = get_animation_manager()
            # Animate cards with staggered delay
            for i, card in enumerate(cards):
                # Use reliable entrance animation
                delay = i * 50  # 50ms stagger delay
                QTimer.singleShot(
                    delay, lambda c=card: self._start_entrance_animation(c)
                )

            logger.info("🎬 Started staggered entrance for %d cards", len(cards))
        except Exception as e:
            logger.warning("Could not animate card entrance: %s", e)

    def _start_entrance_animation(self, card):
        """Start entrance animation for a single card."""
        animation_manager = get_animation_manager()
        entrance_anim = animation_manager.smooth_fade(card, fade_in=True)
        entrance_anim.start()

    def _clear_grid(self):
        """Clear all cards from the grid."""
        # Force immediate clearing of all widgets
        items_to_remove = []
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                items_to_remove.append(item.widget())

        # Remove and delete all widgets
        for widget in items_to_remove:
            self.grid_layout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()

        # Clear any remaining items
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child and child.widget():
                child.widget().deleteLater()

        # Removed selection logic - using direct launching instead

    # Removed _on_card_selected - using direct launching instead of selection

    def _on_launch_requested(self, app_id: str):
        """Handle application launch request."""
        self.launch_application(app_id)

    def launch_application(self, app_id: str):
        """Launch an application by ID."""
        try:
            # Find the application
            app = next((app for app in self.applications if app.id == app_id), None)
            if not app:
                logger.error(f"❌ Application not found: {app_id}")
                return

            logger.info(f"🚀 Launching application: {app.title}")

            # Launch through TKA integration
            success = self.tka_integration.launch_application(app_id)

            if success:
                self.application_launched.emit(app_id, app.title)
                logger.info(f"✅ Successfully launched: {app.title}")
            else:
                logger.error(f"❌ Failed to launch: {app.title}")

        except Exception as e:
            logger.error(f"❌ Error launching application {app_id}: {e}")

    # Removed get_selected_application - using direct launching instead

    def cleanup(self):
        """Cleanup resources."""
        logger.info("🧹 Cleaning up application grid...")
        self._clear_grid()

    def resizeEvent(self, event):
        """Handle resize events to update card sizes dynamically."""
        super().resizeEvent(event)
        # Update grid when widget is resized to recalculate card sizes
        if (
            hasattr(self, "filtered_applications")
            and self.filtered_applications
            and self._initial_layout_complete
        ):
            self._update_grid()

    def showEvent(self, event):
        """Handle show event to ensure proper sizing."""
        super().showEvent(event)

        # Only update if initial layout is complete
        if self._initial_layout_complete:
            # Schedule a delayed update to ensure widget is properly sized
            QTimer.singleShot(50, self._update_grid)

        # Schedule size logging after everything is rendered
        QTimer.singleShot(500, self.log_component_sizes)

    def log_component_sizes(self):
        """Log the sizes of all components in the hierarchy to debug width constraints."""
        logger.info("🔍 ===== COMPONENT SIZE ANALYSIS =====")

        # Get main window (walk up the hierarchy)
        main_window = self
        while main_window.parent():
            main_window = main_window.parent()

        logger.info(
            f"1. Main Window: {main_window.size().width()}x{main_window.size().height()}"
        )

        # Find tab widget
        from PyQt6.QtWidgets import QTabWidget

        tab_widget = main_window.findChild(QTabWidget)

        if tab_widget:
            logger.info(
                f"2. Tab Widget: {tab_widget.size().width()}x{tab_widget.size().height()}"
            )

            # Get current widget (home interface)
            home_interface = tab_widget.currentWidget()
            if home_interface:
                logger.info(
                    f"3. Home Interface: {home_interface.size().width()}x{home_interface.size().height()}"
                )

        # ApplicationGridWidget (self)
        logger.info(
            f"4. ApplicationGridWidget: {self.size().width()}x{self.size().height()}"
        )

        # ScrollArea
        if hasattr(self, "scroll_area"):
            logger.info(
                f"5. ScrollArea: {self.scroll_area.size().width()}x{self.scroll_area.size().height()}"
            )
            logger.info(
                f"   ScrollArea viewport: {self.scroll_area.viewport().size().width()}x{self.scroll_area.viewport().size().height()}"
            )

        # Scroll Widget
        if hasattr(self, "scroll_widget"):
            logger.info(
                f"6. Scroll Widget: {self.scroll_widget.size().width()}x{self.scroll_widget.size().height()}"
            )

        # FlowLayout geometry
        if hasattr(self, "flow_layout"):
            rect = self.flow_layout.geometry()
            logger.info(f"7. FlowLayout: {rect.width()}x{rect.height()}")

        # Sample ApplicationCard if any exist
        if hasattr(self, "flow_layout") and self.flow_layout.count() > 0:
            first_card = self.flow_layout.itemAt(0).widget()
            if first_card:
                logger.info(
                    f"8. ApplicationCard (sample): {first_card.size().width()}x{first_card.size().height()}"
                )

        logger.info("🔍 ===== END SIZE ANALYSIS =====")
