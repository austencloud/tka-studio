"""
Codex Scroll Area

Scrollable container for the codex pictograph grid with smooth scrolling
and optimized performance.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QWheelEvent
from PyQt6.QtWidgets import QScrollArea, QWidget


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class CodexScrollArea(QScrollArea):
    """
    Scrollable container for codex pictograph grid.

    Provides smooth scrolling and optimized performance for
    displaying the codex pictograph grid.
    """

    def __init__(self, container: DIContainer, parent=None):
        super().__init__(parent)

        self.container = container

        # Set object name for styling
        self.setObjectName("codex_scroll_area")

        # Setup scroll area
        self._setup_scroll_area()

        logger.debug("CodexScrollArea initialized")

    def _setup_scroll_area(self) -> None:
        """Setup the scroll area properties."""
        # Enable widget resizing
        self.setWidgetResizable(True)

        # Set scroll bar policies
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Enable smooth scrolling
        self.viewport().installEventFilter(self)

        # Apply styling - solid background to block animated backgrounds
        self.setStyleSheet("""
            CodexScrollArea {
                border: none;
            }

            CodexScrollArea QScrollBar:vertical {
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }

            CodexScrollArea QScrollBar::handle:vertical {
                border-radius: 6px;
                min-height: 20px;
                margin: 2px;
            }



            CodexScrollArea QScrollBar::add-line:vertical,
            CodexScrollArea QScrollBar::sub-line:vertical {
                height: 0px;
                width: 0px;
            }

            CodexScrollArea QScrollBar::add-page:vertical,

        """)

        # Set frame style
        self.setFrameStyle(QScrollArea.Shape.NoFrame)

    def eventFilter(self, obj: QWidget, event: QEvent) -> bool:
        """
        Event filter for smooth scrolling.

        Intercepts wheel events and makes scrolling smoother.
        """
        if obj is self.viewport() and event.type() == QEvent.Type.Wheel:
            wheel_event = QWheelEvent(event)

            # Get current scroll position
            scroll_bar = self.verticalScrollBar()
            current_value = scroll_bar.value()

            # Calculate smooth scroll amount
            delta = wheel_event.angleDelta().y()
            smooth_delta = delta // 3  # Reduce scroll speed for smoother scrolling

            # Apply smooth scroll
            new_value = current_value - smooth_delta
            scroll_bar.setValue(new_value)

            # Consume the event
            return True

        # Let other events pass through
        return super().eventFilter(obj, event)

    def setWidget(self, widget: QWidget) -> None:
        """
        Set the widget for the scroll area with optimized settings.

        Args:
            widget: The widget to set as the scroll area content
        """
        super().setWidget(widget)

        # Apply optimizations to the widget
        if widget:
            # Set minimal margins for better space usage
            widget.setContentsMargins(5, 10, 5, 10)

            # Enable attribute to improve scrolling performance
            widget.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)

            # Set solid background to block animated backgrounds
            widget.setStyleSheet("""
                background-color: #ffffff;
                border: none;
            """)

    def scroll_to_top(self) -> None:
        """Scroll to the top of the content."""
        self.verticalScrollBar().setValue(0)

    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the content."""
        scroll_bar = self.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def scroll_to_letter(self, letter: str) -> None:
        """
        Scroll to a specific letter in the grid.

        Args:
            letter: The letter to scroll to
        """
        # This would need to be implemented with coordination
        # from the pictograph grid to find the letter's position
        logger.debug(f"Scroll to letter requested: {letter}")

    def get_visible_area_height(self) -> int:
        """
        Get the height of the visible area.

        Returns:
            Height of the visible area in pixels
        """
        return self.viewport().height()

    def get_content_height(self) -> int:
        """
        Get the total height of the content.

        Returns:
            Total content height in pixels
        """
        widget = self.widget()
        if widget:
            return widget.sizeHint().height()
        return 0

    def is_at_top(self) -> bool:
        """
        Check if scrolled to the top.

        Returns:
            True if at the top, False otherwise
        """
        return self.verticalScrollBar().value() == 0

    def is_at_bottom(self) -> bool:
        """
        Check if scrolled to the bottom.

        Returns:
            True if at the bottom, False otherwise
        """
        scroll_bar = self.verticalScrollBar()
        return scroll_bar.value() == scroll_bar.maximum()

    def get_scroll_percentage(self) -> float:
        """
        Get the current scroll position as a percentage.

        Returns:
            Scroll position as percentage (0.0 to 1.0)
        """
        scroll_bar = self.verticalScrollBar()
        if scroll_bar.maximum() == 0:
            return 0.0

        return scroll_bar.value() / scroll_bar.maximum()

    def set_scroll_percentage(self, percentage: float) -> None:
        """
        Set the scroll position by percentage.

        Args:
            percentage: Scroll position as percentage (0.0 to 1.0)
        """
        scroll_bar = self.verticalScrollBar()
        value = int(scroll_bar.maximum() * percentage)
        scroll_bar.setValue(value)
