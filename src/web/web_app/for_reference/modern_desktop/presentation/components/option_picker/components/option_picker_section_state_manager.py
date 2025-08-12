"""
OptionPickerSectionStateManager

Handles all state management for OptionPickerSection including:
- Loading states and transitions
- UI initialization tracking
- Scroll area readiness detection
- State validation and coordination

Extracted from OptionPickerSection to follow Single Responsibility Principle.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from shared.application.services.option_picker.option_configuration_service import (
    OptionConfigurationService,
)

from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)


if TYPE_CHECKING:
    from desktop.modern.presentation.components.option_picker.components.option_picker_scroll import (
        OptionPickerScroll,
    )


class OptionPickerSectionStateManager:
    """
    Handles state management for OptionPickerSection.

    Responsibilities:
    - Loading state management
    - UI initialization tracking
    - Scroll area readiness detection
    - State transitions and validation
    """

    def __init__(
        self,
        letter_type: LetterType,
        scroll_area: OptionPickerScroll,
        option_config_service: OptionConfigurationService,
    ):
        """Initialize state manager."""
        self._letter_type = letter_type
        self._scroll_area = scroll_area
        self._option_config_service = option_config_service

        # State tracking
        self._loading_options = False
        self._ui_initialized = False
        self._scroll_area_ready = False

        # Configuration state
        self._option_picker_width: Optional[int] = None
        self._is_groupable: Optional[bool] = None

    def set_loading_state(self, loading: bool) -> None:
        """Set the loading state."""
        self._loading_options = loading

    def is_loading(self) -> bool:
        """Check if currently loading options."""
        return self._loading_options

    def set_ui_initialized(self, initialized: bool) -> None:
        """Set UI initialization state."""
        self._ui_initialized = initialized

    def is_ui_initialized(self) -> bool:
        """Check if UI is initialized."""
        return self._ui_initialized

    def set_scroll_area_ready(self, ready: bool) -> None:
        """Set scroll area readiness state."""
        self._scroll_area_ready = ready

    def is_scroll_area_ready(self) -> bool:
        """Check if scroll area is ready."""
        return self._scroll_area_ready

    def update_option_picker_width(self, width: int) -> None:
        """Update option picker width and related state."""
        self._option_picker_width = width

        # Update groupable state based on configuration
        self._is_groupable = self._option_config_service.is_groupable_type(
            self._letter_type
        )

    def get_option_picker_width(self) -> Optional[int]:
        """Get current option picker width."""
        return self._option_picker_width

    def is_groupable(self) -> Optional[bool]:
        """Check if this section type is groupable."""
        return self._is_groupable

    def check_scroll_area_readiness(self) -> bool:
        """
        Check if scroll area has valid dimensions and update readiness state.

        Returns:
            True if scroll area is ready, False otherwise
        """
        if not self._ui_initialized:
            return False

        if not self._scroll_area:
            return False

        scroll_width = self._scroll_area.width()
        parent_width = (
            self._scroll_area.parent().width() if self._scroll_area.parent() else 0
        )

        # More robust validation - check if we have a reasonable width
        is_reasonable_width = (
            scroll_width > 800
        )  # Should be much larger than 640px default
        is_not_default = scroll_width != 640  # Avoid the default fallback value
        has_parent_width = parent_width > 800  # Parent should also be properly sized

        ready = is_reasonable_width and is_not_default and has_parent_width

        if ready != self._scroll_area_ready:
            self._scroll_area_ready = ready
            return True  # State changed

        return ready

    def can_handle_resize(self) -> bool:
        """Check if resize events can be handled in current state."""
        # Skip resizing during option loading
        if self._loading_options:
            return False

        # Only proceed if UI is properly initialized and scroll area is ready
        if not self._ui_initialized:
            return False

        if not self._scroll_area_ready:
            return False

        return True

    def can_load_options(self) -> bool:
        """Check if options can be loaded in current state."""
        # Can load if UI is initialized (scroll area readiness is checked separately)
        return self._ui_initialized

    def get_state_summary(self) -> dict:
        """Get a summary of current state for debugging."""
        return {
            "letter_type": self._letter_type.value if self._letter_type else None,
            "loading_options": self._loading_options,
            "ui_initialized": self._ui_initialized,
            "scroll_area_ready": self._scroll_area_ready,
            "option_picker_width": self._option_picker_width,
            "is_groupable": self._is_groupable,
            "scroll_area_width": self._scroll_area.width()
            if self._scroll_area
            else None,
            "scroll_area_parent_width": (
                self._scroll_area.parent().width()
                if self._scroll_area and self._scroll_area.parent()
                else None
            ),
        }

    def validate_state_for_operation(self, operation: str) -> tuple[bool, str]:
        """
        Validate state for a specific operation.

        Args:
            operation: The operation to validate ('resize', 'load_options', 'clear')

        Returns:
            Tuple of (is_valid, reason_if_invalid)
        """
        if operation == "resize":
            if not self.can_handle_resize():
                if self._loading_options:
                    return False, "Cannot resize while loading options"
                if not self._ui_initialized:
                    return False, "UI not initialized"
                if not self._scroll_area_ready:
                    return False, "Scroll area not ready"
            return True, ""

        if operation == "load_options":
            if not self.can_load_options():
                return False, "UI not initialized"
            return True, ""

        if operation == "clear":
            # Clear can always be performed
            return True, ""

        return False, f"Unknown operation: {operation}"

    def reset_state(self) -> None:
        """Reset all state to initial values."""
        self._loading_options = False
        self._ui_initialized = False
        self._scroll_area_ready = False
        self._option_picker_width = None
        self._is_groupable = None

    def cleanup(self) -> None:
        """Clean up state manager resources."""
        self.reset_state()
