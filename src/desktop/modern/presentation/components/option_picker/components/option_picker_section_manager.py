"""
OptionPickerSectionManager

Manages section lifecycle, updates, and coordination.
Handles section creation, updates, and inter-section communication.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QTimer

from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)


if TYPE_CHECKING:
    from desktop.modern.presentation.components.option_picker.components.option_picker_section import (
        OptionPickerSection,
    )


class OptionPickerSectionManager:
    """
    Manages section lifecycle and coordination.

    Responsibilities:
    - Managing section updates and lifecycle
    - Coordinating between sections
    - Handling section state management
    - Managing section animations
    """

    def __init__(self, sections: dict[LetterType, OptionPickerSection]):
        self._sections = sections
        self._update_in_progress = False
        self._pending_updates: list[tuple] = []

    def update_all_sections_directly(
        self, sequence_data: SequenceData, options_by_type: dict[LetterType, list]
    ) -> None:
        """Update all sections directly without animation."""
        if self._update_in_progress:
            self._pending_updates.append((sequence_data, options_by_type))
            return

        self._update_in_progress = True

        try:
            # Temporarily disable all section animations for performance
            original_orchestrators = {}
            for letter_type, section in self._sections.items():
                original_orchestrators[letter_type] = getattr(
                    section, "_animation_orchestrator", None
                )
                if hasattr(section, "_animation_orchestrator"):
                    section._animation_orchestrator = None

            # PAGINATION FIX: Ensure all sections are properly cleared before loading new options
            # This prevents widget pool exhaustion that causes the pagination issue
            for letter_type, section in self._sections.items():
                section.clear_pictographs()

            # Update all sections quickly
            for letter_type, section in self._sections.items():
                section_options = options_by_type.get(letter_type, [])
                print(
                    f"🔍 [SECTION_MGR] Updating {letter_type} with {len(section_options)} options"
                )
                section.load_options_from_sequence(section_options)
                print(f"🔍 [SECTION_MGR] Section {letter_type} updated successfully")

            # Restore animation orchestrators
            for letter_type, section in self._sections.items():
                if hasattr(section, "_animation_orchestrator"):
                    section._animation_orchestrator = original_orchestrators.get(
                        letter_type
                    )

        except Exception as e:
            print(f"❌ [SECTION_MGR] Error updating sections: {e}")
        finally:
            self._update_in_progress = False
            self._process_pending_updates()

    def _process_pending_updates(self):
        """Process any pending updates that were queued."""
        if self._pending_updates:
            sequence_data, options_by_type = self._pending_updates.pop(0)
            QTimer.singleShot(
                10,
                lambda: self.update_all_sections_directly(
                    sequence_data, options_by_type
                ),
            )

    def clear_all_sections(self) -> None:
        """Clear all pictographs from all sections."""
        for section in self._sections.values():
            if hasattr(section, "clear_pictographs"):
                section.clear_pictographs()

    def get_all_pictograph_frames(self) -> list:
        """Get all pictograph frames from all sections."""
        frames = []
        for section in self._sections.values():
            if hasattr(section, "pictographs") and section.pictographs:
                frames.extend(section.pictographs.values())
        return frames

    def update_all_sections_picker_width(self, picker_width: int) -> None:
        """Update all sections with new picker width."""
        for section in self._sections.values():
            if hasattr(section, "update_option_picker_width"):
                section.update_option_picker_width(picker_width)

    def set_loading_state_for_all_sections(self, loading: bool) -> None:
        """Set loading state for all sections."""
        for section in self._sections.values():
            if hasattr(section, "_loading_options"):
                section._loading_options = loading

    def apply_sizing_to_all_sections(
        self, main_window_size, picker_width: int, layout_config: dict
    ) -> None:
        """Apply sizing to all sections using provided configuration."""
        for section in self._sections.values():
            for frame in getattr(section, "pictographs", {}).values():
                if hasattr(frame, "resize_option_view"):
                    frame.resize_option_view(
                        main_window_size,
                        picker_width,
                        spacing=layout_config.get("spacing", 10),
                    )

    def get_sections_with_content(self) -> list[OptionPickerSection]:
        """Get sections that have pictograph content."""
        return [
            section
            for section in self._sections.values()
            if hasattr(section, "pictographs") and section.pictographs
        ]

    def get_section_by_type(self, letter_type: LetterType) -> OptionPickerSection:
        """Get section by letter type."""
        return self._sections.get(letter_type)

    def get_section_count(self) -> int:
        """Get total number of sections."""
        return len(self._sections)

    def is_update_in_progress(self) -> bool:
        """Check if an update is currently in progress."""
        return self._update_in_progress
