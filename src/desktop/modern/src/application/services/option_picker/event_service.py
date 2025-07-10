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
from domain.models.pictograph_models import PictographData
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
        self.option_click_handler: Optional[Callable[[str], None]] = None
        self.pictograph_click_handler: Optional[Callable[[PictographData], None]] = None
        self.filter_change_handler: Optional[Callable[[str], None]] = None

    def setup_event_handlers(
        self,
        pool_manager: Any,
        filter_widget: QWidget,
        option_click_handler: Callable[[str], None],
        pictograph_click_handler: Callable[[PictographData], None],
        filter_change_handler: Callable[[str], None],
    ) -> None:
        """
        Setup event handlers for option picker interactions.

        Args:
            pool_manager: Pictograph pool manager
            filter_widget: Filter widget
            option_click_handler: Handler for option clicks
            pictograph_click_handler: Handler for pictograph data clicks
            filter_change_handler: Handler for filter changes
        """
        try:
            self.pool_manager = pool_manager
            self.filter_widget = filter_widget
            self.option_click_handler = option_click_handler
            self.pictograph_click_handler = pictograph_click_handler
            self.filter_change_handler = filter_change_handler

            # Setup pool manager click handlers
            if pool_manager:
                if hasattr(pool_manager, "set_click_handler"):
                    pool_manager.set_click_handler(option_click_handler)
                if hasattr(pool_manager, "set_pictograph_click_handler"):
                    pool_manager.set_pictograph_click_handler(pictograph_click_handler)

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
            # Get current pictograph options (could be filtered in the future)
            pictograph_options = data_service.get_current_pictographs()

            # For now, just update display with all options
            # TODO: Implement actual filtering logic
            display_service.update_pictograph_display(pictograph_options)

            logger.debug(f"Handled filter change: '{filter_text}'")

        except Exception as e:
            logger.error(f"Error handling filter change: {e}")

    def handle_option_click(self, option_id: str) -> None:
        """
        Handle option selection clicks.

        Args:
            option_id: Option identifier
        """
        try:
            if self.option_click_handler:
                self.option_click_handler(option_id)
                logger.debug(f"Handled option click: {option_id}")
            else:
                logger.warning("No option click handler configured")

        except Exception as e:
            logger.error(f"Error handling option click: {e}")

    def handle_pictograph_click(self, pictograph_data: PictographData) -> None:
        """
        Handle pictograph data selection clicks.

        Args:
            pictograph_data: Pictograph data object
        """
        try:
            if self.pictograph_click_handler:
                self.pictograph_click_handler(pictograph_data)
                logger.debug(f"Handled pictograph click: {pictograph_data.letter}")
            else:
                logger.warning("No pictograph click handler configured")

        except Exception as e:
            logger.error(f"Error handling pictograph click: {e}")

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

    def emit_pictograph_selected(
        self, pictograph_data: PictographData, signal_emitter: Any
    ) -> None:
        """
        Emit pictograph selected signal.

        Args:
            pictograph_data: Selected pictograph data
            signal_emitter: Object that can emit signals
        """
        try:
            if signal_emitter and hasattr(signal_emitter, "pictograph_selected"):
                signal_emitter.pictograph_selected.emit(pictograph_data)
                logger.debug(f"Emitted pictograph selected: {pictograph_data.letter}")
            else:
                logger.warning("No signal emitter available for pictograph selected")

        except Exception as e:
            logger.error(f"Error emitting pictograph selected: {e}")

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
            self.option_click_handler = None
            self.pictograph_click_handler = None
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

            if not self.option_click_handler:
                logger.warning("Option click handler not configured")
                return False

            if not self.pictograph_click_handler:
                logger.warning("Pictograph click handler not configured")
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
                "option_click_handler_configured": self.option_click_handler
                is not None,
                "pictograph_click_handler_configured": self.pictograph_click_handler
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
                "option_click_handler_configured": False,
                "pictograph_click_handler_configured": False,
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
