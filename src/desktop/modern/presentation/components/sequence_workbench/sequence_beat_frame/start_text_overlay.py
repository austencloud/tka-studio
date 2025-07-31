"""
Start Text Overlay Component for Modern Start Position Views

This component adds "Start" text overlays directly to start position view widgets,
using the unified text overlay approach that provides reliable visibility and
natural scene integration without visual styling artifacts.

Unified with BeatNumberOverlay approach, replacing the problematic QGraphicsTextItem version.
"""

from PyQt6.QtWidgets import QWidget

from .text_overlay_base import (
    TextOverlayBase,
    add_text_overlay_to_view,
    remove_text_overlay_from_view,
)


class StartTextOverlay(TextOverlayBase):
    """
    Start text overlay widget that displays "Start" text on start position views.

    Uses unified text overlay approach for reliable visibility
    and natural integration with the start position appearance.
    """

    def __init__(self, parent_widget: QWidget | None = None):
        # Initialize with "Start" text (not "START" like legacy)
        super().__init__("Start", parent_widget)

        # Start text uses larger size than beat numbers and better positioning
        self._base_size = (50, 25)  # Slightly smaller to prevent cutoff
        self._base_position = (3, 2)  # Further left to prevent cutoff

    def show_overlay(self):
        """Show the start text overlay"""
        self._show_overlay_common()

    def hide_overlay(self):
        """Hide the start text overlay"""
        self._hide_overlay_common()

    def show_start_text(self):
        """Show the start text overlay (legacy method name)"""
        self.show_overlay()

    def hide_start_text(self):
        """Hide the start text overlay (legacy method name)"""
        self.hide_overlay()


def add_start_text_to_view(
    start_position_view: QWidget,
) -> StartTextOverlay | None:
    """
    Add start text overlay to a start position view widget.

    Args:
        start_position_view: StartPositionView widget instance

    Returns:
        StartTextOverlay instance if successful, None otherwise
    """
    if not start_position_view:
        return None

    try:
        # Create the start text overlay
        start_text_overlay = StartTextOverlay(start_position_view)

        # Use unified helper function
        return add_text_overlay_to_view(start_position_view, start_text_overlay)

    except Exception as e:
        print(f"Failed to add start text overlay: {e}")
        return None


def remove_start_text_from_view(
    start_position_view: QWidget, start_text_overlay: StartTextOverlay
):
    """
    Remove start text overlay from a start position view widget.

    Args:
        start_position_view: StartPositionView widget instance
        start_text_overlay: StartTextOverlay instance to remove
    """
    # Use unified helper function
    remove_text_overlay_from_view(start_position_view, start_text_overlay)
