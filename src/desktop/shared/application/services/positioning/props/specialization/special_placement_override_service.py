"""
Special Placement Override Service

Service for handling manual placement overrides from JSON configuration.
Extracted from PropManagementService to follow single responsibility principle.

PROVIDES:
- Manual swap override detection
- Override key generation
- Override application logic
- JSON configuration integration
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from desktop.modern.domain.models import BeatData

from ..configuration.json_configuration_service import IJSONConfigurator


class ISpecialPlacementOverrideService(ABC):
    """Interface for special placement override operations."""

    @abstractmethod
    def has_swap_override(self, beat_data: BeatData) -> bool:
        """Check if beat has manual override."""

    @abstractmethod
    def apply_swap_override(self, beat_data: BeatData) -> BeatData:
        """Apply manual swap override."""

    @abstractmethod
    def generate_override_key(self, beat_data: BeatData) -> str:
        """Generate key for swap override lookup."""

    @abstractmethod
    def get_override_data(self, beat_data: BeatData) -> dict[str, Any]:
        """Get override data for beat configuration."""


class SpecialPlacementOverrideService(ISpecialPlacementOverrideService):
    """
    Service for handling special placement overrides.

    Manages manual positioning overrides defined in JSON configuration
    for specific letter/motion combinations that require custom positioning.
    """

    def __init__(self, json_configurator: Optional[IJSONConfigurator] = None):
        """Initialize with JSON configurator dependency."""
        self._json_configurator = json_configurator
        if self._json_configurator is None:
            self._json_configurator = self._get_json_configurator()

    def has_swap_override(self, beat_data: BeatData) -> bool:
        """Check if beat has manual swap override in special placements."""
        special_placements = self._get_special_placements()
        if not special_placements:
            return False

        override_key = self.generate_override_key(beat_data)
        return override_key in special_placements

    def apply_swap_override(self, beat_data: BeatData) -> BeatData:
        """
        Apply manual swap override from special placements.

        Loads specific positioning data for this configuration.
        """
        override_data = self.get_override_data(beat_data)

        # Apply override adjustments
        # TODO: Implement specific override application logic
        # This would modify the beat_data with specific positioning overrides
        # For now, return unmodified data as we need renderer integration
        return beat_data

    def generate_override_key(self, beat_data: BeatData) -> str:
        """
        Generate key for swap override lookup.

        Based on validated logic for special placement keys.
        """
        # Get motion data from pictograph_data
        blue_motion = None
        red_motion = None

        if beat_data.pictograph_data and beat_data.pictograph_data.motions:
            blue_motion = beat_data.pictograph_data.motions.get("blue")
            red_motion = beat_data.pictograph_data.motions.get("red")

        if not blue_motion or not red_motion:
            return ""

        blue_type = blue_motion.motion_type.value
        red_type = red_motion.motion_type.value
        letter = beat_data.letter or ""

        # Generate key in standard format
        return f"{letter}_{blue_type}_{red_type}"

    def get_override_data(self, beat_data: BeatData) -> dict[str, Any]:
        """Get override data for beat configuration."""
        override_key = self.generate_override_key(beat_data)
        special_placements = self._get_special_placements()
        return special_placements.get(override_key, {})

    def _get_json_configurator(self) -> IJSONConfigurator:
        """Get JSONConfigurator singleton from DI container."""
        try:
            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
            )

            container = get_container()
            return container.resolve(IJSONConfigurator)
        except Exception as e:
            # Log the DI failure for debugging
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                f"Failed to resolve IJSONConfigurator from DI container: {e}"
            )

            # Fallback to creating new instance if DI fails
            from ..configuration.json_configuration_service import JSONConfigurator

            return JSONConfigurator()

    def _get_special_placements(self) -> dict[str, Any]:
        """Get special placements using JSONConfigurator singleton."""
        return self._json_configurator.load_special_placements()
