"""
Pictograph option frame for displaying real pictographs in option picker.

This frame displays a single pictograph option with proper rendering
and click handling, replacing the placeholder widgets.
"""

import logging
from typing import Optional

from application.services.pictograph_pool_manager import get_pictograph_pool
from domain.models.pictograph_data import PictographData
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QVBoxLayout

logger = logging.getLogger(__name__)


class PictographOptionFrame(QFrame):
    """Frame for displaying a single pictograph option."""

    # Signal emitted when this option is clicked
    option_selected = pyqtSignal(object)  # PictographData

    def __init__(self, parent=None):
        """Initialize the pictograph option frame."""
        super().__init__(parent)

        self._pictograph_data: Optional[PictographData] = None
        self._pictograph_component = None

        self._setup_ui()
        self._setup_styling()

    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)

        # Get pictograph component from pool for high performance
        pool = get_pictograph_pool()
        self._pictograph_component = pool.checkout_pictograph(parent=self)

        if self._pictograph_component is None:
            logger.error("❌ [FRAME] Failed to get pictograph from pool")
            return

        # Use Legacy sizing strategy - will be set in resize_option_view()
        self._pictograph_component.setFixedSize(
            100, 100
        )  # Default size, will be updated

        # Make the frame itself square to match the pictograph
        self.setFixedSize(108, 108)  # Default size + padding, will be updated

        layout.addWidget(self._pictograph_component)

    def _setup_styling(self):
        """Set up the frame styling."""
        self.setStyleSheet(
            """
            PictographOptionFrame {
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.1);
            }
            PictographOptionFrame:hover {
                border: 2px solid rgba(255, 255, 255, 0.6);
                background: rgba(255, 255, 255, 0.2);
            }
        """
        )

        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)

        # Make clickable
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def update_pictograph(self, pictograph_data: PictographData):
        """Update the displayed pictograph using pool component."""
        self._pictograph_data = pictograph_data

        if self._pictograph_component and pictograph_data:
            try:
                # Use the real pictograph component from pool
                self._pictograph_component.update_from_pictograph_data(pictograph_data)
                logger.debug(
                    f"Updated pictograph option with letter: {pictograph_data.letter}"
                )
            except Exception as e:
                logger.error(f"Error updating pictograph option: {e}")

    def clear_pictograph(self):
        """Clear the displayed pictograph."""
        self._pictograph_data = None
        if self._pictograph_component:
            # Clear the pictograph component
            if (
                hasattr(self._pictograph_component, "scene")
                and self._pictograph_component.scene
            ):
                self._pictograph_component.scene.clear()

    def cleanup(self):
        """Return the pictograph component to the pool."""
        if self._pictograph_component:
            pool = get_pictograph_pool()
            pool.checkin_pictograph(self._pictograph_component)
            self._pictograph_component = None

    def get_pictograph_data(self) -> Optional[PictographData]:
        """Get the current pictograph data."""
        return self._pictograph_data

    def mousePressEvent(self, event):
        """Handle mouse press events for selection."""
        if event.button() == Qt.MouseButton.LeftButton and self._pictograph_data:
            logger.debug(f"Pictograph option selected: {self._pictograph_data.letter}")
            self.option_selected.emit(self._pictograph_data)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        """Handle mouse enter for hover effects."""
        self.setStyleSheet(
            """
            PictographOptionFrame {
                border: 2px solid rgba(255, 255, 255, 0.6);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.2);
            }
        """
        )
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave to restore normal styling."""
        self.setStyleSheet(
            """
            PictographOptionFrame {
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.1);
            }
        """
        )
        super().leaveEvent(event)

    def resize_option_view(self, main_window_size, option_picker_width, spacing=3):
        """Resize using Legacy sizing strategy."""
        # Legacy formula: max(main_window_width // 16, option_picker_width // 8)
        size_option_1 = main_window_size.width() // 16
        size_option_2 = option_picker_width // 8
        size = max(size_option_1, size_option_2)

        # Calculate border width (Legacy: max(1, int(size * 0.015)))
        border_width = max(1, int(size * 0.015))

        # Adjust for border and spacing (Legacy: size -= 2 * bw + spacing)
        adjusted_size = size - (2 * border_width) - spacing
        adjusted_size = max(adjusted_size, 60)  # Minimum size

        # Update pictograph component size
        self._pictograph_component.setFixedSize(adjusted_size, adjusted_size)

        # Update frame size (add padding)
        frame_size = adjusted_size + 8  # +8 for frame padding
        self.setFixedSize(frame_size, frame_size)

        print(
            f"🔧 [FRAME_SIZING] Resized to {adjusted_size}px (frame: {frame_size}px) - MW: {main_window_size.width()}, OP: {option_picker_width}"
        )
