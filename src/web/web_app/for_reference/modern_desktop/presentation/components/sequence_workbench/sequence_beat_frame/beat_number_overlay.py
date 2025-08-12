"""
Beat Number Overlay Component for Modern Beat Views

This component adds beat number text overlays directly to beat view widgets,
using the unified text overlay approach that provides reliable visibility and
natural scene integration without visual styling artifacts.

Based on successful testing and unified with StartTextOverlay approach.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QWidget

from .text_overlay_base import (
    TextOverlayBase,
    add_text_overlay_to_view,
)


class BeatNumberOverlay(TextOverlayBase):
    """
    Beat number overlay widget that displays beat numbers on beat views.

    Uses unified text overlay approach for reliable visibility
    and natural integration with the beat frame appearance.
    """

    def __init__(self, beat_number: int, parent_widget: QWidget | None = None):
        # Set beat number specific base size
        self.beat_number = beat_number

        # Initialize with beat number text
        super().__init__(str(beat_number), parent_widget)

        # Beat number uses smaller size than start text
        self._base_size = (25, 25)

    def show_overlay(self):
        """Show the beat number overlay"""
        self._show_overlay_common()

    def hide_overlay(self):
        """Hide the beat number overlay"""
        self._hide_overlay_common()

    def hide_beat_number(self):
        """Hide the beat number overlay (legacy method name)"""
        self.hide_overlay()


def add_beat_number_to_view(
    beat_view: QWidget, beat_number: int
) -> BeatNumberOverlay | None:
    """
    Add beat number overlay to a beat view widget.

    Args:
        beat_view: BeatView widget instance
        beat_number: The beat number to display (1, 2, 3, etc.)

    Returns:
        BeatNumberOverlay instance if successful, None otherwise
    """
    if not beat_view:
        return None

    try:
        # Create the beat number overlay
        beat_number_overlay = BeatNumberOverlay(beat_number, beat_view)

        # Use unified helper function
        return add_text_overlay_to_view(beat_view, beat_number_overlay)

    except Exception as e:
        print(f"Failed to add beat number overlay: {e}")
        return None
