"""
Option Picker Section Coordination Service

Platform-agnostic service for managing section updates and coordination.
Contains pure business logic extracted from OptionPickerSectionManager.
"""

import copy
from typing import TYPE_CHECKING, Any

from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)

if TYPE_CHECKING:
    pass


class OptionPickerSectionCoordinationService:
    """
    Platform-agnostic service for section coordination and updates.

    Responsibilities:
    - Managing section update coordination
    - Handling section state management
    - Coordinating between sections
    - Managing update queues and priorities
    """

    def __init__(self):
        self._update_in_progress = False
        self._pending_updates: list[tuple] = []
        self._section_state_cache: dict[LetterType, dict[str, Any]] = {}

    def can_start_update(self) -> bool:
        """Check if a section update can be started."""
        return not self._update_in_progress

    def start_update(self) -> None:
        """Mark update as in progress."""
        self._update_in_progress = True

    def finish_update(self) -> None:
        """Mark update as finished and process pending updates."""
        self._update_in_progress = False

        if self._pending_updates:
            # Process next pending update
            next_update = self._pending_updates.pop(0)
            return next_update

        return None

    def queue_update(
        self, sequence_data: SequenceData, options_by_type: dict[LetterType, list]
    ) -> None:
        """Queue an update for later processing."""
        self._pending_updates.append((sequence_data, options_by_type))

    def get_pending_update_count(self) -> int:
        """Get number of pending updates."""
        return len(self._pending_updates)

    def clear_pending_updates(self) -> None:
        """Clear all pending updates."""
        self._pending_updates.clear()

    def cache_section_state(
        self, letter_type: LetterType, state: dict[str, Any]
    ) -> None:
        """Cache section state for coordination."""
        self._section_state_cache[letter_type] = copy.deepcopy(state)

    def get_cached_section_state(self, letter_type: LetterType) -> dict[str, Any]:
        """Get cached section state."""
        return self._section_state_cache.get(letter_type, {})

    def clear_section_state_cache(self) -> None:
        """Clear all cached section states."""
        self._section_state_cache.clear()

    def get_update_strategy(self, sequence_data: SequenceData) -> dict[str, Any]:
        """Get update strategy based on sequence data."""
        return {
            "use_animation": len(sequence_data.beats)
            < 10,  # Animate for small sequences
            "batch_size": 5,  # Process sections in batches
            "priority_order": [
                LetterType.TYPE1,
                LetterType.TYPE2,
                LetterType.TYPE3,
                LetterType.TYPE4,
            ],
            "defer_heavy_operations": len(sequence_data.beats) > 20,
        }

    def should_disable_animations(
        self, options_by_type: dict[LetterType, list]
    ) -> bool:
        """Determine if animations should be disabled for performance."""
        total_options = sum(len(options) for options in options_by_type.values())
        return total_options > 50  # Disable animations for large datasets

    def get_section_priorities(self) -> list[LetterType]:
        """Get section update priorities."""
        return [
            LetterType.TYPE1,  # Highest priority
            LetterType.TYPE2,
            LetterType.TYPE3,
            LetterType.TYPE4,  # Lowest priority
        ]

    def validate_section_data(
        self, options_by_type: dict[LetterType, list]
    ) -> dict[str, Any]:
        """Validate section data and return validation results."""
        validation_results = {"valid": True, "errors": [], "warnings": [], "stats": {}}

        try:
            total_options = 0
            for letter_type, options in options_by_type.items():
                option_count = len(options)
                total_options += option_count

                # Check for reasonable option counts
                if option_count > 100:
                    validation_results["warnings"].append(
                        f"High option count for {letter_type}: {option_count}"
                    )
                elif option_count == 0:
                    validation_results["warnings"].append(
                        f"No options for {letter_type}"
                    )

                validation_results["stats"][letter_type] = {
                    "count": option_count,
                    "valid": True,
                }

            validation_results["stats"]["total_options"] = total_options

            # Check for overall data health
            if total_options > 500:
                validation_results["warnings"].append(
                    f"Very large dataset: {total_options} total options"
                )
            elif total_options == 0:
                validation_results["errors"].append("No options provided")
                validation_results["valid"] = False

        except Exception as e:
            validation_results["errors"].append(f"Validation error: {e}")
            validation_results["valid"] = False

        return validation_results
