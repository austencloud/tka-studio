"""
Option Picker Event Service

Pure service for handling option picker event coordination.
Extracted from OptionPicker to follow single responsibility principle.

This service handles:
- Event handler setup and coordination
- Widget resize event handling
- Filter change event handling
- Click event delegation

No UI dependencies, completely testable in isolation.
"""

import logging
from typing import Any, Callable, Optional

from core.interfaces.option_picker_services import (
    IOptionPickerDataService,
    IOptionPickerDisplayService,
    IOptionPickerEventService,
)
from domain.models.core_models import BeatData
from PyQt6.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class OptionPickerEventService(IOptionPickerEventService):
    """
    Pure service for option picker event handling.

    Coordinates event handling without any UI concerns.
    Provides clean interface for event management.
    """

    def __init__(self):
        """Initialize the event service."""
        self.pool_manager: Optional[Any] = None
        self.filter_widget: Optional[QWidget] = None
        self.beat_click_handler: Optional[Callable[[str], None]] = None
        self.beat_data_click_handler: Optional[Callable[[BeatData], None]] = None
        self.filter_change_handler: Optional[Callable[[str], None]] = None

    def setup_event_handlers(
        self,
        pool_manager: Any,
        filter_widget: QWidget,
        beat_click_handler: Callable[[str], None],
        beat_data_click_handler: Callable[[BeatData], None],
        filter_change_handler: Callable[[str], None],
    ) -> None:
        """
        Setup event handlers for option picker interactions.

        Args:
            pool_manager: Pictograph pool manager
            filter_widget: Filter widget
            beat_click_handler: Handler for beat clicks
            beat_data_click_handler: Handler for beat data clicks
            filter_change_handler: Handler for filter changes
        """
        try:
            self.pool_manager = pool_manager
            self.filter_widget = filter_widget
            self.beat_click_handler = beat_click_handler
            self.beat_data_click_handler = beat_data_click_handler
            self.filter_change_handler = filter_change_handler

            # Setup pool manager click handlers
            if pool_manager:
                if hasattr(pool_manager, "set_click_handler"):
                    pool_manager.set_click_handler(beat_click_handler)
                if hasattr(pool_manager, "set_beat_data_click_handler"):
                    pool_manager.set_beat_data_click_handler(beat_data_click_handler)

            # Setup filter widget connections
            if filter_widget and hasattr(filter_widget, "filter_changed"):
                filter_widget.filter_changed.connect(filter_change_handler)

            logger.debug("Event handlers setup successfully")

        except Exception as e:
            logger.error(f"Error setting up event handlers: {e}")
            raise

    def handle_widget_resize(
        self, pool_manager: Any, display_service: IOptionPickerDisplayService
    ) -> None:
        """
        Handle widget resize events.

        Args:
            pool_manager: Pictograph pool manager
            display_service: Display service for section resizing
        """
        try:
            # Resize pool manager frames
            if pool_manager and hasattr(pool_manager, "resize_all_frames"):
                pool_manager.resize_all_frames()

            # Resize display sections
            if display_service:
                display_service.resize_sections()

            logger.debug("Handled widget resize")

        except Exception as e:
            logger.error(f"Error handling widget resize: {e}")

    def handle_filter_change(
        self,
        filter_text: str,
        data_service: IOptionPickerDataService,
        display_service: IOptionPickerDisplayService,
    ) -> None:
        """
        Handle filter text changes.

        Args:
            filter_text: New filter text
            data_service: Data service for getting options
            display_service: Display service for updating display
        """
        try:
            # Get current beat options (could be filtered in the future)
            beat_options = data_service.get_current_options()

            # For now, just update display with all options
            # TODO: Implement actual filtering logic
            display_service.update_beat_display(beat_options)

            logger.debug(f"Handled filter change: '{filter_text}'")

        except Exception as e:
            logger.error(f"Error handling filter change: {e}")

    def handle_beat_click(self, beat_id: str) -> None:
        """
        Handle beat selection clicks (legacy compatibility).

        Args:
            beat_id: Beat identifier
        """
        try:
            if self.beat_click_handler:
                self.beat_click_handler(beat_id)
                logger.debug(f"Handled beat click: {beat_id}")
            else:
                logger.warning("No beat click handler configured")

        except Exception as e:
            logger.error(f"Error handling beat click: {e}")

    def handle_beat_data_click(self, beat_data: BeatData) -> None:
        """
        Handle beat data selection clicks (modern method).

        Args:
            beat_data: Beat data object
        """
        try:
            if self.beat_data_click_handler:
                self.beat_data_click_handler(beat_data)
                logger.debug(f"Handled beat data click: {beat_data.letter}")
            else:
                logger.warning("No beat data click handler configured")

        except Exception as e:
            logger.error(f"Error handling beat data click: {e}")

    def emit_option_selected(self, option_id: str, signal_emitter: Any) -> None:
        """
        Emit option selected signal.

        Args:
            option_id: Selected option ID
            signal_emitter: Object that can emit signals
        """
        try:
            if signal_emitter and hasattr(signal_emitter, "option_selected"):
                signal_emitter.option_selected.emit(option_id)
                logger.debug(f"Emitted option selected: {option_id}")
            else:
                logger.warning("No signal emitter available for option selected")

        except Exception as e:
            logger.error(f"Error emitting option selected: {e}")

    def emit_beat_data_selected(self, beat_data: BeatData, signal_emitter: Any) -> None:
        """
        Emit beat data selected signal.

        Args:
            beat_data: Selected beat data
            signal_emitter: Object that can emit signals
        """
        try:
            if signal_emitter and hasattr(signal_emitter, "beat_data_selected"):
                signal_emitter.beat_data_selected.emit(beat_data)
                logger.debug(f"Emitted beat data selected: {beat_data.letter}")
            else:
                logger.warning("No signal emitter available for beat data selected")

        except Exception as e:
            logger.error(f"Error emitting beat data selected: {e}")

    def disconnect_all_handlers(self) -> None:
        """Disconnect all event handlers."""
        try:
            # Disconnect filter widget
            if self.filter_widget and hasattr(self.filter_widget, "filter_changed"):
                try:
                    self.filter_widget.filter_changed.disconnect()
                except Exception:
                    pass  # Already disconnected

            # Clear handler references
            self.pool_manager = None
            self.filter_widget = None
            self.beat_click_handler = None
            self.beat_data_click_handler = None
            self.filter_change_handler = None

            logger.debug("Disconnected all event handlers")

        except Exception as e:
            logger.error(f"Error disconnecting handlers: {e}")

    def validate_event_setup(self) -> bool:
        """
        Validate that event handlers are properly setup.

        Returns:
            True if event setup is valid
        """
        try:
            if not self.pool_manager:
                logger.warning("Pool manager not available for events")
                return False

            if not self.filter_widget:
                logger.warning("Filter widget not available for events")
                return False

            if not self.beat_click_handler:
                logger.warning("Beat click handler not configured")
                return False

            if not self.beat_data_click_handler:
                logger.warning("Beat data click handler not configured")
                return False

            if not self.filter_change_handler:
                logger.warning("Filter change handler not configured")
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating event setup: {e}")
            return False

    def get_event_info(self) -> dict:
        """
        Get information about current event configuration.

        Returns:
            Dictionary with event information
        """
        try:
            return {
                "pool_manager_available": self.pool_manager is not None,
                "filter_widget_available": self.filter_widget is not None,
                "beat_click_handler_configured": self.beat_click_handler is not None,
                "beat_data_click_handler_configured": self.beat_data_click_handler
                is not None,
                "filter_change_handler_configured": self.filter_change_handler
                is not None,
                "validation_passed": self.validate_event_setup(),
            }

        except Exception as e:
            logger.error(f"Error getting event info: {e}")
            return {
                "pool_manager_available": False,
                "filter_widget_available": False,
                "beat_click_handler_configured": False,
                "beat_data_click_handler_configured": False,
                "filter_change_handler_configured": False,
                "validation_passed": False,
                "error": str(e),
            }

    def cleanup(self) -> None:
        """Clean up event service resources."""
        try:
            self.disconnect_all_handlers()
            logger.debug("Event service cleaned up")

        except Exception as e:
            logger.error(f"Error during event cleanup: {e}")
