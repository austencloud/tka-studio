"""
OptionPickerSectionContentLoader

Handles the complex content loading logic for OptionPickerSection including:
- Orchestrating the load_options_from_sequence workflow
- Coordinating between animation, widget, and layout managers
- Managing the transition from old to new content
- Error handling and fallback strategies

Extracted from OptionPickerSection to simplify the main class.
"""

from __future__ import annotations

from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.components.option_picker.components.option_picker_section_animation_handler import (
    OptionPickerSectionAnimationHandler,
)
from desktop.modern.presentation.components.option_picker.components.option_picker_section_layout_manager import (
    OptionPickerSectionLayoutManager,
)
from desktop.modern.presentation.components.option_picker.components.option_picker_section_state_manager import (
    OptionPickerSectionStateManager,
)
from desktop.modern.presentation.components.option_picker.components.option_picker_section_widget_manager import (
    OptionPickerSectionWidgetManager,
)
from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)


class OptionPickerSectionContentLoader:
    """
    Handles content loading orchestration for OptionPickerSection.

    Responsibilities:
    - Orchestrating the complete load_options_from_sequence workflow
    - Coordinating between all manager components
    - Managing state transitions during loading
    - Error handling and fallback strategies
    """

    def __init__(
        self,
        letter_type: LetterType,
        state_manager: OptionPickerSectionStateManager,
        widget_manager: OptionPickerSectionWidgetManager,
        layout_manager: OptionPickerSectionLayoutManager,
        animation_handler: OptionPickerSectionAnimationHandler,
    ):
        """Initialize content loader with manager components."""
        self._letter_type = letter_type
        self._state_manager = state_manager
        self._widget_manager = widget_manager
        self._layout_manager = layout_manager
        self._animation_handler = animation_handler

    def load_options_from_sequence(
        self, pictographs_for_section: list[PictographData]
    ) -> None:
        """
        Load options for this section with animation transitions.

        This is the main entry point that replaces the original 100-line method.
        """
        try:
            # Validate state before starting
            can_load, reason = self._state_manager.validate_state_for_operation(
                "load_options"
            )
            if not can_load:
                print(
                    f"❌ [LOAD] Cannot load options for {self._letter_type}: {reason}"
                )
                return

            # Additional check: ensure layout is initialized
            if not self._layout_manager.is_layout_initialized():
                print(
                    f"❌ [LOAD] Layout not initialized for {self._letter_type}, skipping load"
                )
                return

            # Set loading state
            self._state_manager.set_loading_state(True)

            # Get existing widgets for potential animation
            existing_widgets = self._widget_manager.get_active_widgets()
            print(
                f"🔍 [CONTENT_LOADER] {self._letter_type}: Found {len(existing_widgets)} existing widgets"
            )

            # Decide on loading strategy
            if self._should_use_animation(existing_widgets):
                print(f"🔍 [CONTENT_LOADER] {self._letter_type}: Using animation path")
                self._load_with_animation(pictographs_for_section, existing_widgets)
            else:
                print(f"🔍 [CONTENT_LOADER] {self._letter_type}: Using direct path")
                self._load_directly(pictographs_for_section)

        except Exception as e:
            print(f"❌ [LOAD] Error loading options for {self._letter_type}: {e}")
        finally:
            # Always clear loading state
            self._state_manager.set_loading_state(False)

    def _should_use_animation(self, existing_widgets: list) -> bool:
        """Determine if animation should be used for this load operation."""
        # Use animation if we have existing widgets and animation handler is available
        return len(existing_widgets) > 0 and not self._animation_handler.is_animating()

    def _load_with_animation(
        self, pictographs_for_section: list[PictographData], existing_widgets: list
    ) -> None:
        """Load content with fade animation."""

        # Define callbacks for animation workflow
        def update_content():
            self._update_content_directly(pictographs_for_section)

        def fade_in_new_content():
            new_widgets = self._widget_manager.get_active_widgets()
            self._animation_handler.fade_in_frames(new_widgets)

        # Attempt animation
        animation_started = self._animation_handler.animate_content_update(
            existing_widgets, update_content, fade_in_new_content
        )

        # Fallback to direct loading if animation failed
        if not animation_started:
            self._load_directly(pictographs_for_section)

    def _load_directly(self, pictographs_for_section: list[PictographData]) -> None:
        """Load content directly without animation."""
        self._clear_existing_content()
        self._update_content_directly(pictographs_for_section)

    def _clear_existing_content(self) -> None:
        """Clear existing content from layout and widget manager."""
        # Clear widgets from layout
        self._layout_manager.clear_grid_layout()

        # Clear and return widgets to pool
        self._widget_manager.clear_all_widgets()

    def _update_content_directly(
        self, pictographs_for_section: list[PictographData]
    ) -> None:
        """Update content directly (used by both animated and direct loading)."""
        # NOTE: Cleanup is handled by the caller (_load_directly or animation workflow)
        # Do NOT clear here to avoid double cleanup

        # Create new widgets for pictographs
        new_widgets = self._widget_manager.create_widgets_for_pictographs(
            pictographs_for_section
        )

        # Add widgets to layout
        for i, widget in enumerate(new_widgets):
            self._layout_manager.add_widget_to_grid(widget, i)

    def clear_all_content(self) -> None:
        """Clear all content (public method for external use)."""
        self._clear_existing_content()

    def get_current_widget_count(self) -> int:
        """Get count of currently loaded widgets."""
        return self._widget_manager.get_active_widget_count()

    def has_content(self) -> bool:
        """Check if section has any loaded content."""
        return self._widget_manager.has_active_widgets()

    def cleanup(self) -> None:
        """Clean up content loader resources."""
        self._clear_existing_content()
