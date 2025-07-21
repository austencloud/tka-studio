"""
Pictograph option frame for displaying real pictographs in option picker.

This frame displays a single pictograph option with proper rendering
and click handling, replacing the placeholder widgets.
"""

import logging
from typing import Optional

from application.services.option_picker.option_picker_size_calculator import (
    OptionPickerSizeCalculator,
)
from domain.models.pictograph_data import PictographData
from presentation.components.pictograph.views import create_option_view
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtWidgets import QFrame, QVBoxLayout

logger = logging.getLogger(__name__)


class OptionPictograph(QFrame):
    """Frame for displaying a single pictograph option."""

    # Signal emitted when this option is clicked
    option_selected = pyqtSignal(object)  # PictographData

    def __init__(self, parent=None, pictograph_component=None, size_calculator=None):
        """
        Initialize the pictograph option frame.

        Args:
            parent: Parent widget
            pictograph_component: DEPRECATED - now creates direct view
            size_calculator: OptionPickerSizeCalculator service for sizing calculations (injected)
        """
        super().__init__(parent)

        self._pictograph_data: Optional[PictographData] = None

        # Create direct pictograph view (no widget wrapper)
        def get_main_window_size():
            main_window = self.window()
            return main_window.size() if main_window else QSize(1000, 800)

        self._pictograph_component = create_option_view(
            parent=self, main_window_size_provider=get_main_window_size
        )

        self._size_calculator: OptionPickerSizeCalculator = size_calculator

        # Debounce mechanism to prevent rapid duplicate selections
        self._last_click_time = 0
        self._debounce_delay = 500  # 500ms debounce delay

        self._setup_ui()
        self._setup_styling()

    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ✅ Use injected pictograph component instead of service location
        if self._pictograph_component is None:
            logger.error(
                "❌ [FRAME] No pictograph component provided - dependency injection failed"
            )
            return

        # Set parent for the injected component
        self._pictograph_component.setParent(self)

        layout.addWidget(self._pictograph_component)

    def _setup_styling(self):
        """Set up the frame styling."""
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Apply baseline styling for proper appearance
        self.setStyleSheet(
            """
            OptionPictograph {
                background: rgba(255, 255, 255, 0.1);
            }
            """
        )

    def update_pictograph(self, pictograph_data: PictographData):
        """Update the displayed pictograph using pool component."""
        self._pictograph_data = pictograph_data

        if self._pictograph_component and pictograph_data:
            try:
                # LEGACY-STYLE SIZING: Calculate size like legacy system
                main_window = self.window()
                main_window_width = main_window.width() if main_window else 1200
                option_picker_width = self.parent().width() if self.parent() else 800

                # Legacy formula: size = max(mw_width // 16, option_picker.width() // 8)
                size_option_1 = main_window_width // 16
                size_option_2 = option_picker_width // 8
                target_size = max(size_option_1, size_option_2)

                # Apply border calculation like legacy
                border_width = max(1, int(target_size * 0.015))
                target_size = target_size - (2 * border_width)
                target_size = max(target_size, 100)  # Minimum size

                # DIRECT VIEW APPROACH: Set size and update option picker width
                self._pictograph_component.set_option_picker_width(
                    self.parent().width() if self.parent() else 800
                )

                # Update pictograph data - direct view handles scaling automatically
                self._pictograph_component.update_from_pictograph_data(pictograph_data)
                logger.debug(
                    f"Updated pictograph option with letter: {pictograph_data.letter}, size: {target_size}x{target_size}"
                )
            except Exception as e:
                logger.error(f"Error updating pictograph option: {e}")

    def clear_pictograph(self):
        """Clear the displayed pictograph."""
        self._pictograph_data = None
        if self._pictograph_component:
            if (
                hasattr(self._pictograph_component, "scene")
                and self._pictograph_component.scene
            ):
                self._pictograph_component.scene.clear()

    def cleanup(self):
        """
        Clean up the frame - pool management handled by lifecycle service.

        Note: Pool management is now handled by WidgetLifecycleService,
        this method only clears the frame's internal state.
        """
        if self._pictograph_component:
            # Clear the pictograph component's content
            if (
                hasattr(self._pictograph_component, "scene")
                and self._pictograph_component.scene
            ):
                self._pictograph_component.scene.clear()

            # Note: Pool checkin is handled by the lifecycle service
            # that created this frame, not by the frame itself

        # Clear internal state
        self._pictograph_data = None

    def get_pictograph_data(self) -> Optional[PictographData]:
        """Get the current pictograph data."""
        return self._pictograph_data

    def mousePressEvent(self, event):
        """Handle mouse press events for selection with debounce protection."""
        if event.button() == Qt.MouseButton.LeftButton and self._pictograph_data:
            import time

            current_time = time.time() * 1000  # Convert to milliseconds

            # Check if enough time has passed since last click
            if current_time - self._last_click_time < self._debounce_delay:
                logger.debug(f"Debounced rapid click on {self._pictograph_data.letter}")
                return

            self._last_click_time = current_time
            logger.debug(f"Pictograph option selected: {self._pictograph_data.letter}")
            self.option_selected.emit(self._pictograph_data)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        """Handle mouse enter - simplified without hover effects."""
        # Keep original functionality without styling changes
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave - simplified without hover effects."""
        # Keep original functionality without styling changes
        super().leaveEvent(event)

    def resize_option_view(self, main_window_size, option_picker_width, spacing=3):
        """Resize using OptionPickerSizeCalculator service - clean architecture."""

        try:
            # ✅ Use injected service for all sizing calculations
            dimensions = self._size_calculator.calculate_frame_dimensions(
                main_window_size, option_picker_width, spacing
            )

            # Update pictograph component size
            component_size = dimensions["component_size"]
            self._pictograph_component.setFixedSize(component_size, component_size)

            # Update frame size
            frame_size = dimensions["frame_size"]
            self.setFixedSize(frame_size, frame_size)

        except Exception as e:
            logger.error(f"Error resizing option view: {e}")
            # Fallback sizing
            fallback_size = 60
            self._pictograph_component.setFixedSize(fallback_size, fallback_size)
            self.setFixedSize(fallback_size + 8, fallback_size + 8)
