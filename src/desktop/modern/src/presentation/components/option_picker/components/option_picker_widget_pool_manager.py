"""
OptionPickerWidgetPoolManager

Manages widget pool lifecycle and coordination with services.
Handles widget creation, pooling, and cleanup.
"""

from typing import TYPE_CHECKING, Dict, Optional

from presentation.components.option_picker.components.option_pictograph import (
    OptionPictograph,
)
from PyQt6.QtWidgets import QWidget

if TYPE_CHECKING:
    from application.services.option_picker.option_picker_size_calculator import (
        OptionPickerSizeCalculator,
    )
    from application.services.option_picker.option_pool_service import OptionPoolService
    from application.services.pictograph_pool_manager import PictographPoolManager


class OptionPickerWidgetPoolManager:
    """
    Manages widget pool for option picker.

    Responsibilities:
    - Creating and managing widget pool
    - Coordinating with service-level pool
    - Managing widget lifecycle
    - Handling widget cleanup
    """

    def __init__(
        self,
        parent: QWidget,
        option_pool_service: "OptionPoolService",
        pictograph_pool_manager: "PictographPoolManager",
        size_calculator: "OptionPickerSizeCalculator",
        max_widgets: int,
    ):
        self._parent = parent
        self._option_pool_service = option_pool_service
        self._pictograph_pool_manager = pictograph_pool_manager
        self._size_calculator = size_calculator
        self._max_widgets = max_widgets

        # Qt widget pool
        self._widget_pool: Dict[int, OptionPictograph] = {}

        self._initialize_widget_pool()

    def _initialize_widget_pool(self) -> None:
        """Initialize Qt widget pool with proper dependency injection."""
        print(
            f"🏗️ [WIDGET_POOL] Initializing widget pool with {self._max_widgets} widgets"
        )

        # Create Qt widgets with direct view approach (no pictograph pool needed)
        for i in range(self._max_widgets):
            try:
                # Create frame with direct view (no pictograph component injection needed)
                frame = OptionPictograph(
                    parent=self._parent,
                    pictograph_component=None,  # DEPRECATED - creates own direct view
                    size_calculator=self._size_calculator,
                )
                frame.hide()  # Hide initially to prevent random display
                self._widget_pool[i] = frame

            except Exception as e:
                print(f"❌ [WIDGET_POOL] Error creating widget {i}: {e}")
                import traceback

                traceback.print_exc()

        # Initialize service pool with same IDs
        self._option_pool_service.reset_pool()

        print(
            f"✅ [WIDGET_POOL] Widget pool initialized with {len(self._widget_pool)} widgets"
        )

    def get_widget_by_id(self, pool_id: int) -> Optional[OptionPictograph]:
        """Get Qt widget from pool by service-provided ID."""
        return self._widget_pool.get(pool_id)

    def get_widget_count(self) -> int:
        """Get total number of widgets in pool."""
        return len(self._widget_pool)

    def get_available_widget_count(self) -> int:
        """Get number of available (hidden) widgets."""
        return sum(1 for widget in self._widget_pool.values() if not widget.isVisible())

    def get_active_widget_count(self) -> int:
        """Get number of active (visible) widgets."""
        return sum(1 for widget in self._widget_pool.values() if widget.isVisible())

    def reset_pool(self) -> None:
        """Reset the widget pool to initial state."""
        print("🔄 [WIDGET_POOL] Resetting widget pool")

        # Hide all widgets
        for widget in self._widget_pool.values():
            widget.hide()

        # Reset service pool
        self._option_pool_service.reset_pool()

        print("✅ [WIDGET_POOL] Widget pool reset complete")

    def cleanup_widget_pool(self) -> None:
        """Clean up widget pool resources."""
        print("🧹 [WIDGET_POOL] Cleaning up widget pool")

        # Hide and cleanup all widgets
        for widget in self._widget_pool.values():
            widget.hide()
            if hasattr(widget, "cleanup"):
                widget.cleanup()

        # Clear the pool
        self._widget_pool.clear()

        print("✅ [WIDGET_POOL] Widget pool cleanup complete")

    def get_widget_pool_status(self) -> Dict[str, int]:
        """Get status information about the widget pool."""
        return {
            "total_widgets": self.get_widget_count(),
            "active_widgets": self.get_active_widget_count(),
            "available_widgets": self.get_available_widget_count(),
        }

    def validate_widget_pool_integrity(self) -> bool:
        """Validate that widget pool is in a consistent state."""
        try:
            # Check that all expected widgets exist
            for i in range(self._max_widgets):
                if i not in self._widget_pool:
                    print(f"❌ [WIDGET_POOL] Missing widget with ID {i}")
                    return False

                widget = self._widget_pool[i]
                if not isinstance(widget, OptionPictograph):
                    print(f"❌ [WIDGET_POOL] Widget {i} is not OptionPictograph")
                    return False

            # Check that no extra widgets exist
            if len(self._widget_pool) != self._max_widgets:
                print(
                    f"❌ [WIDGET_POOL] Expected {self._max_widgets} widgets, found {len(self._widget_pool)}"
                )
                return False

            return True

        except Exception as e:
            print(f"❌ [WIDGET_POOL] Error validating widget pool: {e}")
            return False
