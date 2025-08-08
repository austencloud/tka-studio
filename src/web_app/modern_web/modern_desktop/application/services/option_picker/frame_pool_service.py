"""
FramePoolService - Microservice for PictographOptionFrame object pool management.

This service extracts object lifecycle management from presentation components to handle:
- Frame pool initialization and management
- Checkout/checkin operations for frame reuse
- Frame lifecycle and cleanup
- Pool size optimization

Replaces object management logic previously embedded in OptionFactory.
"""

from __future__ import annotations

import logging
from typing import Optional

from PyQt6.QtWidgets import QWidget

from desktop.modern.presentation.components.option_picker.components.option_pictograph import (
    OptionPictograph,
)


logger = logging.getLogger(__name__)


class FramePoolService:
    """
    Microservice for managing PictographOptionFrame object pool.

    Handles all object lifecycle concerns:
    - Pool initialization with configurable size
    - Frame checkout/checkin for reuse
    - Frame cleanup and reset operations
    - Pool statistics and monitoring
    """

    def __init__(self, max_frames: int = 36):
        """
        Initialize frame pool service.

        Args:
            max_frames: Maximum number of frames in pool (default 36 for 6 sections × 6 frames)
        """
        self._max_frames = max_frames
        self._pool: list[OptionPictograph] = []
        self._parent_widget: Optional[QWidget] = None
        self._initialized = False

        # Pool statistics
        self._checkout_count = 0
        self._checkin_count = 0

    def initialize_pool(self, parent_widget: QWidget) -> None:
        """
        Initialize frame pool with parent widget.

        Must be called before using checkout operations.
        Creates all frames upfront for optimal performance.

        Args:
            parent_widget: Parent widget for frame creation
        """
        if self._initialized:
            logger.warning("Frame pool already initialized")
            return

        self._parent_widget = parent_widget

        try:
            # Import here to avoid circular dependencies
            from desktop.modern.presentation.components.option_picker.components.option_pictograph import (
                OptionPictograph,
            )

            # Create all frames upfront with direct view approach
            self._pool = []
            for i in range(self._max_frames):
                frame = OptionPictograph(
                    parent=parent_widget,
                    pictograph_component=None,  # DEPRECATED - creates own direct view
                    size_calculator=None,  # Will be set when needed
                )
                frame.hide()  # Start hidden
                self._pool.append(frame)

            self._initialized = True
            logger.debug(f"Initialized frame pool with {self._max_frames} frames")

        except Exception as e:
            logger.error(f"Failed to initialize frame pool: {e}")
            self._pool = []

    def checkin_frame(self, frame: OptionPictograph) -> None:
        """
        Return frame to pool.

        Hides frame and clears its content for reuse.

        Args:
            frame: Frame to return to pool
        """
        if not frame:
            return

        try:
            # Hide frame and clear content
            frame.hide()
            frame.setVisible(False)

            # Clear pictograph content if method exists
            if hasattr(frame, "clear_pictograph"):
                frame.clear_pictograph()

            # Disconnect any signals to prevent memory leaks
            if hasattr(frame, "option_selected"):
                frame.option_selected.disconnect()

            self._checkin_count += 1
            logger.debug(f"Checked in frame (total checkins: {self._checkin_count})")

        except Exception as e:
            logger.error(f"Error checking in frame: {e}")

    def reset_all_frames(self) -> None:
        """
        Reset all frames in pool to hidden state.

        Useful for clearing all options at once.
        """
        try:
            for frame in self._pool:
                self.checkin_frame(frame)

            logger.debug(f"Reset all {len(self._pool)} frames in pool")

        except Exception as e:
            logger.error(f"Error resetting frames: {e}")

    def cleanup(self) -> None:
        """
        Cleanup pool resources.

        Should be called when shutting down to properly cleanup frames.
        """
        try:
            # Reset all frames first
            self.reset_all_frames()

            # Clear pool
            self._pool.clear()
            self._initialized = False
            self._parent_widget = None

            logger.debug("Frame pool cleanup completed")

        except Exception as e:
            logger.error(f"Error during frame pool cleanup: {e}")

    def __len__(self) -> int:
        """Return pool size."""
        return len(self._pool)

    def __bool__(self) -> bool:
        """Return True if pool is initialized and has frames."""
        return self._initialized and len(self._pool) > 0
