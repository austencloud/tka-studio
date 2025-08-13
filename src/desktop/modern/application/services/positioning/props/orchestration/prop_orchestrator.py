"""
Prop Orchestrator

Orchestrates prop positioning operations using focused services.
Replaces the monolithic PropManagementService with clean architecture.

PROVIDES:
- Complete prop management pipeline coordination
- Service composition and orchestration
- Clean separation of concerns
- Event-driven prop positioning
"""

from __future__ import annotations

import os
from pathlib import Path
import sys
from typing import TYPE_CHECKING
import uuid


# Add project root to path using pathlib (standardized approach)
def _get_project_root() -> Path:
    """Find the TKA project root by looking for pyproject.toml or main.py."""
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / "pyproject.toml").exists() or (parent / "main.py").exists():
            return parent
    # Fallback: assume TKA is 7 levels up from this file
    return current_path.parents[6]


# Add project paths for imports
_project_root = _get_project_root()
sys.path.insert(0, str(_project_root))
sys.path.insert(0, str(_project_root / "src"))
from abc import ABC, abstractmethod
from datetime import datetime
import sys
from typing import Any


# Add project root to path (following established pattern)
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../../../"))

from PyQt6.QtCore import QPointF

from desktop.modern.application.services.positioning.props.calculation.direction_calculation_service import (
    DirectionCalculationService,
    IDirectionCalculationService,
)
from desktop.modern.application.services.positioning.props.calculation.offset_calculation_service import (
    IOffsetCalculationService,
    OffsetCalculationService,
)
from desktop.modern.application.services.positioning.props.calculation.prop_classification_service import (
    IPropClassificationService,
    PropClassificationService,
)
from desktop.modern.application.services.positioning.props.configuration.json_configuration_service import (
    IJSONConfigurator,
    JSONConfigurator,
)
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.enums import PropType


# Event-driven architecture imports
if TYPE_CHECKING:
    from desktop.modern.application.services.core.events import IEventBus

try:
    from desktop.modern.application.services.core.events import (
        EventPriority,
        PropPositionedEvent,
        get_event_bus,
    )

    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    get_event_bus = None
    PropPositionedEvent = None
    EventPriority = None
    EVENT_SYSTEM_AVAILABLE = False


class IPropOrchestrator(ABC):
    """Interface for prop orchestration."""

    @abstractmethod
    def should_apply_beta_positioning(self, beat_data: BeatData) -> bool:
        """Determine if beta positioning should be applied."""

    @abstractmethod
    def apply_beta_positioning(self, beat_data: BeatData) -> BeatData:
        """Apply beta prop positioning if conditions are met."""

    @abstractmethod
    def calculate_separation_offsets(
        self, beat_data: BeatData
    ) -> tuple[QPointF, QPointF]:
        """Calculate separation offsets for blue and red props."""

    @abstractmethod
    def detect_prop_overlap(self, beat_data: BeatData) -> bool:
        """Detect if props overlap based on position and category."""


class PropOrchestrator(IPropOrchestrator):
    """
    Orchestrates prop positioning operations using focused services.

    Coordinates direction calculation, offset calculation, JSON configuration,
    and prop classification services. Returns immutable positioning data.
    """

    def __init__(
        self,
        direction_service: IDirectionCalculationService | None = None,
        offset_service: IOffsetCalculationService | None = None,
        config_service: IJSONConfigurator | None = None,
        classification_service: IPropClassificationService | None = None,
        event_bus: IEventBus | None = None,
    ):
        """Initialize with dependency injection."""
        self.direction_service = direction_service or DirectionCalculationService()
        self.offset_service = offset_service or OffsetCalculationService()

        # Use dependency injection for config service to avoid creating multiple instances
        if config_service is None:
            try:
                from desktop.modern.core.dependency_injection.di_container import (
                    get_container,
                )

                container = get_container()
                self.config_service = container.resolve(IJSONConfigurator)
            except Exception as e:
                # Log the DI failure for debugging
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(
                    f"Failed to resolve IJSONConfigurator from DI container: {e}"
                )

                # Fallback to creating new instance if DI fails
                self.config_service = JSONConfigurator()
        else:
            self.config_service = config_service

        self.classification_service = (
            classification_service or PropClassificationService()
        )

        # Event system integration
        self.event_bus = event_bus or (
            get_event_bus() if EVENT_SYSTEM_AVAILABLE else None
        )
        self._subscription_ids: list[str] = []

    def should_apply_beta_positioning(self, beat_data: BeatData) -> bool:
        """
        Determine if beta positioning should be applied.

        Beta positioning is applied when:
        1. Letter is one that ends at beta positions (G, H, I, J, K, L, Y, Z, Y-, Z-, Ψ, Ψ-, β)
        """
        if not beat_data or not beat_data.letter:
            return False

        return self.classification_service.is_beta_ending_letter(beat_data.letter)

    def apply_beta_positioning(self, beat_data: BeatData) -> BeatData:
        """
        Apply beta prop positioning if conditions are met.

        First checks for manual swap overrides, then applies algorithmic positioning.
        """
        if not self.should_apply_beta_positioning(beat_data):
            return beat_data

        # Check for swap overrides first
        if self.config_service.has_swap_override(beat_data):
            result = self._apply_swap_override(beat_data)
            positioning_method = "swap_override"
        else:
            # Apply algorithmic beta positioning
            result = self._apply_algorithmic_beta_positioning(beat_data)
            positioning_method = "algorithmic"

        # Publish beta positioning event
        self._publish_positioning_event(
            "beta_positioning",
            {
                "letter": beat_data.letter,
                "positioning_method": positioning_method,
                "blue_motion_type": (
                    beat_data.blue_motion.motion_type.value
                    if beat_data.blue_motion
                    else None
                ),
                "red_motion_type": (
                    beat_data.red_motion.motion_type.value
                    if beat_data.red_motion
                    else None
                ),
            },
        )

        return result

    def calculate_separation_offsets(
        self, beat_data: BeatData
    ) -> tuple[QPointF, QPointF]:
        """
        Calculate separation offsets for blue and red props.

        Returns tuple of (blue_offset, red_offset) as QPointF objects.
        """
        if not beat_data.blue_motion or not beat_data.red_motion:
            return QPointF(0, 0), QPointF(0, 0)

        # Calculate separation directions using direction service
        blue_direction = self.direction_service.calculate_separation_direction(
            beat_data.blue_motion, beat_data, "blue"
        )
        red_direction = self.direction_service.calculate_separation_direction(
            beat_data.red_motion, beat_data, "red"
        )

        # Calculate offsets using offset service
        current_prop_type = self._get_current_prop_type()
        blue_offset, red_offset = self.offset_service.calculate_separation_offsets(
            blue_direction, red_direction, current_prop_type
        )

        # Publish separation calculation event
        self._publish_positioning_event(
            "separation",
            {
                "blue_offset": {"x": blue_offset.x, "y": blue_offset.y},
                "red_offset": {"x": red_offset.x, "y": red_offset.y},
                "blue_direction": blue_direction.value,
                "red_direction": red_direction.value,
                "letter": beat_data.letter,
                "prop_type": current_prop_type.value,
            },
        )

        return blue_offset, red_offset

    def detect_prop_overlap(self, beat_data: BeatData) -> bool:
        """
        Detect if props overlap based on their end positions and orientations.
        """
        overlap_detected = self.classification_service.detect_prop_overlap(beat_data)

        # Publish overlap detection event
        if overlap_detected:
            self._publish_positioning_event(
                "overlap_detected",
                {
                    "blue_end_location": (
                        beat_data.blue_motion.end_loc.value
                        if beat_data.blue_motion
                        else None
                    ),
                    "red_end_location": (
                        beat_data.red_motion.end_loc.value
                        if beat_data.red_motion
                        else None
                    ),
                    "letter": beat_data.letter,
                },
            )

        return overlap_detected

    def classify_props_by_size(self, beat_data: BeatData) -> dict[str, list]:
        """Classify props by size categories using classification service."""
        return self.classification_service.classify_props_by_size(beat_data)

    def get_repositioning_strategy(
        self, beat_data: BeatData, prop_classification: dict[str, list]
    ) -> str:
        """Get repositioning strategy using classification service."""
        return self.classification_service.get_repositioning_strategy(
            beat_data, prop_classification
        )

    def calculate_prop_rotation_angle(self, motion_data, start_orientation=None):
        """Calculate prop rotation angle using classification service."""
        return self.classification_service.calculate_prop_rotation_angle(
            motion_data, start_orientation
        )

    def cleanup(self):
        """Clean up event subscriptions when service is destroyed."""
        if self.event_bus:
            for sub_id in self._subscription_ids:
                self.event_bus.unsubscribe(sub_id)
            self._subscription_ids.clear()

    def _apply_swap_override(self, beat_data: BeatData) -> BeatData:
        """Apply manual swap override from special placements."""
        self.config_service.get_swap_override_data(beat_data)

        # TODO: Implement specific override application logic
        # This would modify the beat_data with specific positioning overrides
        return beat_data

    def _apply_algorithmic_beta_positioning(self, beat_data: BeatData) -> BeatData:
        """Apply algorithmic beta prop positioning."""
        if not beat_data.blue_motion or not beat_data.red_motion:
            return beat_data

        # Calculate separation offsets
        blue_offset, red_offset = self.calculate_separation_offsets(beat_data)

        # TODO: Apply offsets to beat_data
        # This would modify the actual positioning data in beat_data
        # For now, return unmodified data as we need renderer integration

        return beat_data

    def _get_current_prop_type(self) -> PropType:
        """Get current prop type from settings."""
        # TODO: Integrate with actual settings system
        return PropType.HAND  # Default to smallest offset

    def _publish_positioning_event(
        self, positioning_type: str, position_data: dict[str, Any]
    ) -> None:
        """Publish positioning event if event system is available."""
        if self.event_bus and PropPositionedEvent:
            self.event_bus.publish(
                PropPositionedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="PropOrchestrator",
                    positioning_type=positioning_type,
                    position_data=position_data,
                )
            )
