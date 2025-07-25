"""
OptionPickerSectionWidgetManager

Handles all widget management and pooling logic for OptionPickerSection including:
- Widget checkout/checkin from pool
- Signal connections and disconnections
- Widget lifecycle management
- Pictograph data updates

Extracted from OptionPickerSection to follow Single Responsibility Principle.
"""

from typing import TYPE_CHECKING, Callable, Dict, List, Optional

from application.services.option_picker.option_pool_service import OptionPoolService
from domain.models.pictograph_data import PictographData
from presentation.components.option_picker.components.option_pictograph import (
    OptionPictograph,
)
from presentation.components.option_picker.types.letter_types import LetterType

if TYPE_CHECKING:
    from presentation.components.option_picker.components.option_picker_scroll import (
        OptionPickerScroll,
    )


class OptionPickerSectionWidgetManager:
    """
    Handles widget management and pooling for OptionPickerSection.

    Responsibilities:
    - Widget checkout/checkin from pool
    - Signal connections and lifecycle
    - Pictograph data updates
    - Widget tracking and cleanup
    """

    def __init__(
        self,
        letter_type: LetterType,
        scroll_area: "OptionPickerScroll",
        option_pool_service: OptionPoolService,
        selection_callback: Callable[[PictographData], None],
    ):
        """Initialize widget manager."""
        self._letter_type = letter_type
        self._scroll_area = scroll_area
        self._option_pool_service = option_pool_service
        self._selection_callback = selection_callback

        # Widget tracking
        self._active_widgets: Dict[str, OptionPictograph] = {}
        self._widget_pool_mapping: Dict[OptionPictograph, int] = {}

    def create_widgets_for_pictographs(
        self, pictographs_for_section: List[PictographData]
    ) -> List[OptionPictograph]:
        """
        Create and setup widgets for the given pictographs.

        Returns:
            List of configured OptionPictograph widgets ready for layout
        """
        widgets = []

        for i, pictograph_data in enumerate(pictographs_for_section):
            widget = self._checkout_and_setup_widget(pictograph_data)
            if widget:
                widgets.append(widget)

        return widgets

    def _checkout_and_setup_widget(
        self, pictograph_data: PictographData
    ) -> Optional[OptionPictograph]:
        """Checkout widget from pool and setup with pictograph data."""
        # Get widget from pool using service
        pool_id = self._option_pool_service.checkout_item()
        if pool_id is None:
            return None

        # Get Qt widget from scroll area's widget pool
        option_frame = self._scroll_area.get_widget_from_pool(pool_id)
        if not option_frame:
            # Return pool ID if widget checkout failed
            self._option_pool_service.checkin_item(pool_id)
            return None

        # Setup Qt widget
        option_frame.update_pictograph(pictograph_data)

        # Setup signal connections
        self._connect_widget_signals(option_frame)

        # Track widget and its pool mapping
        key = f"pictograph_{len(self._active_widgets)}"
        self._active_widgets[key] = option_frame
        self._widget_pool_mapping[option_frame] = pool_id

        # Set the letter type on the pictograph for border coloring
        self._setup_widget_letter_type(option_frame)

        return option_frame

    def _connect_widget_signals(self, widget: OptionPictograph) -> None:
        """Connect widget signals, ensuring no duplicate connections."""
        # CRITICAL: Disconnect any existing connections first to prevent duplicates
        try:
            widget.option_selected.disconnect(self._selection_callback)
        except (TypeError, RuntimeError):
            # No existing connection - this is fine
            pass

        # Connect the signal
        widget.option_selected.connect(self._selection_callback)

    def _disconnect_widget_signals(self, widget: OptionPictograph) -> None:
        """Safely disconnect widget signals."""
        try:
            widget.option_selected.disconnect(self._selection_callback)
        except (TypeError, RuntimeError):
            # Signal was already disconnected or never connected - this is fine
            pass

    def _setup_widget_letter_type(self, widget: OptionPictograph) -> None:
        """Setup letter type on widget for border coloring."""
        if hasattr(widget, "_pictograph_component") and widget._pictograph_component:
            if hasattr(widget._pictograph_component, "set_letter_type"):
                widget._pictograph_component.set_letter_type(self._letter_type)

    def clear_all_widgets(self) -> None:
        """Clear all widgets and return them to pool."""
        for widget in list(self._active_widgets.values()):
            self._cleanup_and_return_widget(widget)

        # Clear tracking dictionaries
        self._active_widgets.clear()
        self._widget_pool_mapping.clear()

    def _cleanup_and_return_widget(self, widget: OptionPictograph) -> None:
        """Clean up widget and return it to pool."""
        if not widget:
            return

        # Remove from layout (handled by layout manager)
        widget.setVisible(False)

        # Disconnect signals
        self._disconnect_widget_signals(widget)

        # Clean up widget content
        widget.clear_pictograph()

        # Return to pool
        pool_id = self._widget_pool_mapping.get(widget)
        if pool_id is not None:
            self._option_pool_service.checkin_item(pool_id)
            del self._widget_pool_mapping[widget]

    def get_active_widgets(self) -> List[OptionPictograph]:
        """Get list of currently active widgets."""
        return list(self._active_widgets.values())

    def get_active_widget_count(self) -> int:
        """Get count of currently active widgets."""
        return len(self._active_widgets)

    def get_widget_by_key(self, key: str) -> Optional[OptionPictograph]:
        """Get widget by tracking key."""
        return self._active_widgets.get(key)

    def has_active_widgets(self) -> bool:
        """Check if there are any active widgets."""
        return len(self._active_widgets) > 0

    def update_widget_pictograph(
        self, widget: OptionPictograph, pictograph_data: PictographData
    ) -> None:
        """Update a widget with new pictograph data."""
        if widget in self._widget_pool_mapping:
            widget.update_pictograph(pictograph_data)
            self._setup_widget_letter_type(widget)

    def get_widgets_dict(self) -> Dict[str, OptionPictograph]:
        """Get the widgets dictionary for compatibility."""
        return self._active_widgets.copy()

    def cleanup(self) -> None:
        """Clean up all resources."""
        self.clear_all_widgets()
