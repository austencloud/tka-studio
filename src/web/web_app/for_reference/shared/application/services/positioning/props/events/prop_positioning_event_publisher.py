"""
Prop Positioning Event Publisher Service

Centralized service for publishing prop positioning events.
Extracted from PropManagementService to follow single responsibility principle.

PROVIDES:
- Centralized event publishing for prop positioning
- Event creation and formatting
- Event bus integration
- Type-safe event publishing
"""

import sys
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional


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

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.enums import PropType
from desktop.modern.domain.models.motion_data import MotionData
from shared.application.services.positioning.props.calculation.direction_calculation_service import (
    SeparationDirection,
)

# Event-driven architecture imports
if TYPE_CHECKING:
    from shared.application.services.core.events import IEventBus

try:
    from shared.application.services.core.events import PropPositionedEvent

    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    # For tests or when event system is not available
    PropPositionedEvent = None
    EVENT_SYSTEM_AVAILABLE = False


class IPropPositioningEventPublisher(ABC):
    """Interface for prop positioning event publishing operations."""

    @abstractmethod
    def publish_overlap_detected(
        self, beat_data: BeatData, blue_motion: MotionData, red_motion: MotionData
    ) -> None:
        """Publish overlap detection event."""

    @abstractmethod
    def publish_beta_positioning_applied(
        self, beat_data: BeatData, positioning_method: str
    ) -> None:
        """Publish beta positioning event."""

    @abstractmethod
    def publish_separation_calculated(
        self,
        beat_data: BeatData,
        blue_direction: SeparationDirection,
        red_direction: SeparationDirection,
        blue_offset: Any,
        red_offset: Any,
        prop_type: PropType,
    ) -> None:
        """Publish separation calculation event."""


class PropPositioningEventPublisher(IPropPositioningEventPublisher):
    """
    Centralized service for prop positioning event publishing.

    Handles all event creation and publishing for prop positioning operations,
    providing consistent event formatting and error handling.
    """

    def __init__(self, event_bus: Optional["IEventBus"] = None):
        """Initialize with event bus dependency."""
        self.event_bus = event_bus

    def publish_overlap_detected(
        self, beat_data: BeatData, blue_motion: MotionData, red_motion: MotionData
    ) -> None:
        """Publish overlap detection event."""
        if not self._can_publish_events():
            return

        event_data = {
            "blue_end_location": blue_motion.end_loc.value,
            "red_end_location": red_motion.end_loc.value,
            "blue_end_orientation": blue_motion.end_ori.value,
            "red_end_orientation": red_motion.end_ori.value,
            "letter": beat_data.letter,
        }

        self._publish_event("overlap_detected", event_data)

    def publish_beta_positioning_applied(
        self, beat_data: BeatData, positioning_method: str
    ) -> None:
        """Publish beta positioning event."""
        if not self._can_publish_events():
            return

        event_data = {
            "letter": beat_data.letter,
            "positioning_method": positioning_method,
            "blue_motion_type": self._get_motion_type_value(beat_data, "blue"),
            "red_motion_type": self._get_motion_type_value(beat_data, "red"),
        }

        self._publish_event("beta_positioning", event_data)

    def publish_separation_calculated(
        self,
        beat_data: BeatData,
        blue_direction: SeparationDirection,
        red_direction: SeparationDirection,
        blue_offset: Any,
        red_offset: Any,
        prop_type: PropType,
    ) -> None:
        """Publish separation calculation event."""
        if not self._can_publish_events():
            return

        event_data = {
            "blue_offset": {"x": blue_offset.x, "y": blue_offset.y},
            "red_offset": {"x": red_offset.x, "y": red_offset.y},
            "blue_direction": blue_direction.value,
            "red_direction": red_direction.value,
            "letter": beat_data.letter,
            "prop_type": prop_type.value,
        }

        self._publish_event("separation", event_data)

    def _can_publish_events(self) -> bool:
        """Check if events can be published."""
        return (
            EVENT_SYSTEM_AVAILABLE
            and self.event_bus is not None
            and PropPositionedEvent is not None
        )

    def _publish_event(
        self, positioning_type: str, position_data: dict[str, Any]
    ) -> None:
        """Publish a prop positioned event."""
        if not self._can_publish_events():
            return

        event = PropPositionedEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            source="PropPositioningEventPublisher",
            positioning_type=positioning_type,
            position_data=position_data,
        )

        self.event_bus.publish(event)

    def _get_motion_type_value(self, beat_data: BeatData, color: str) -> str | None:
        """Get motion type value for specified color."""
        if not beat_data.pictograph_data or not beat_data.pictograph_data.motions:
            return None

        motion = beat_data.pictograph_data.motions.get(color)
        return motion.motion_type.value if motion else None
