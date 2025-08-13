"""
Prop Positioning Orchestrator

Main orchestrator for prop positioning operations using focused microservices.
Replaces the monolithic PropManagementService with clean, modular architecture.

PROVIDES:
- Complete prop management pipeline coordination
- Service composition and orchestration
- Clean separation of concerns
- Backward compatibility with existing interfaces
- Event-driven prop positioning
"""

import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Optional


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

from desktop.modern.core.types import Point
from desktop.modern.domain.models import BeatData
from desktop.modern.domain.models.enums import PropType
from desktop.modern.domain.models.pictograph_data import PictographData

from ..calculation import (
    DirectionCalculationService,
    IDirectionCalculationService,
    IOffsetCalculationService,
    IPropClassificationService,
    IPropRotationCalculator,
    OffsetCalculationService,
    PropClassificationService,
    PropRotationCalculator,
)
from ..detection import (
    BetaPositioningDetector,
    IBetaPositioningDetector,
    IPropOverlapDetector,
    PropOverlapDetector,
)
from ..events import IPropPositioningEventPublisher, PropPositioningEventPublisher
from ..specialization import (
    ILetterIPositioningService,
    ISpecialPlacementOverrideService,
    LetterIPositioningService,
    SpecialPlacementOverrideService,
)

# Event-driven architecture imports
if TYPE_CHECKING:
    from desktop.modern.application.services.core.events import IEventBus

try:
    from desktop.modern.core.events import get_event_bus

    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    get_event_bus = None
    EVENT_SYSTEM_AVAILABLE = False


class IPropPositioningOrchestrator(ABC):
    """Interface for prop positioning orchestration."""

    @abstractmethod
    def should_apply_beta_positioning(self, beat_data: BeatData) -> bool:
        """Determine if beta positioning should be applied."""

    @abstractmethod
    def apply_beta_positioning(self, beat_data: BeatData) -> BeatData:
        """Apply beta prop positioning if conditions are met."""

    @abstractmethod
    def calculate_separation_offsets(
        self, pictograph_data: PictographData
    ) -> tuple[Point, Point]:
        """Calculate separation offsets for blue and red props."""

    @abstractmethod
    def detect_prop_overlap(self, beat_data: BeatData) -> bool:
        """Detect if props overlap based on position and category."""


class PropPositioningOrchestrator(IPropPositioningOrchestrator):
    """
    Main orchestrator for prop positioning operations.

    Coordinates all prop positioning services to provide the same external
    interface as the original PropManagementService while using clean,
    modular architecture internally.
    """

    def __init__(
        self,
        beta_detector: IBetaPositioningDetector | None = None,
        overlap_detector: IPropOverlapDetector | None = None,
        direction_service: IDirectionCalculationService | None = None,
        letter_i_service: ILetterIPositioningService | None = None,
        offset_calculator: IOffsetCalculationService | None = None,
        classification_service: IPropClassificationService | None = None,
        rotation_calculator: IPropRotationCalculator | None = None,
        override_service: ISpecialPlacementOverrideService | None = None,
        event_publisher: IPropPositioningEventPublisher | None = None,
        event_bus: Optional["IEventBus"] = None,
    ):
        """Initialize with dependency injection of all services."""
        # Core detection services
        self.beta_detector = beta_detector or BetaPositioningDetector()
        self.overlap_detector = overlap_detector or PropOverlapDetector()

        # Calculation services
        self.direction_service = direction_service or DirectionCalculationService()
        self.letter_i_service = letter_i_service or LetterIPositioningService()
        self.offset_calculator = offset_calculator or OffsetCalculationService()
        self.rotation_calculator = rotation_calculator or PropRotationCalculator()

        # Configuration and specialization services
        self.classification_service = (
            classification_service or PropClassificationService()
        )
        self.override_service = override_service or SpecialPlacementOverrideService()

        # Event management
        event_bus = event_bus or (get_event_bus() if EVENT_SYSTEM_AVAILABLE else None)
        self.event_publisher = event_publisher or PropPositioningEventPublisher(
            event_bus
        )

    def should_apply_beta_positioning(self, beat_data: BeatData) -> bool:
        """Determine if beta positioning should be applied."""
        return self.beta_detector.should_apply_beta_positioning(beat_data)

    def apply_beta_positioning(self, beat_data: BeatData) -> BeatData:
        """
        Apply beta prop positioning if conditions are met.

        First checks for manual swap overrides, then applies algorithmic positioning.
        """
        if not self.should_apply_beta_positioning(beat_data):
            return beat_data

        # Check for swap overrides first
        if self.override_service.has_swap_override(beat_data):
            result = self.override_service.apply_swap_override(beat_data)
            positioning_method = "swap_override"
        else:
            # Apply algorithmic beta positioning
            result = self._apply_algorithmic_beta_positioning(beat_data)
            positioning_method = "algorithmic"

        # Publish beta positioning event
        self.event_publisher.publish_beta_positioning_applied(
            beat_data, positioning_method
        )

        return result

    def calculate_separation_offsets(
        self, pictograph_data: PictographData
    ) -> tuple[Point, Point]:
        """
        Calculate separation offsets for blue and red props.

        Returns tuple of (blue_offset, red_offset) as Point objects.
        """
        # Get motion data from pictograph_data
        blue_motion = None
        red_motion = None

        if pictograph_data and pictograph_data.motions:
            blue_motion = pictograph_data.motions.get("blue")
            red_motion = pictograph_data.motions.get("red")

        if not blue_motion or not red_motion:
            return Point(0, 0), Point(0, 0)

        # SPECIAL CASE: Letter I positioning coordination
        if pictograph_data.letter == "I":
            blue_direction, red_direction = (
                self.letter_i_service.calculate_letter_i_directions(
                    blue_motion, red_motion
                )
            )
        else:
            # Calculate separation directions based on motion types and letter
            beat_data = BeatData(
                letter=pictograph_data.letter, pictograph_data=pictograph_data
            )
            blue_direction = self.direction_service.calculate_separation_direction(
                blue_motion, beat_data, "blue"
            )
            red_direction = self.direction_service.calculate_separation_direction(
                red_motion, beat_data, "red"
            )

        # Calculate offsets based on directions and prop types
        current_prop_type = self._get_current_prop_type()
        blue_offset = self.offset_calculator.calculate_directional_offset(
            blue_direction, current_prop_type
        )
        red_offset = self.offset_calculator.calculate_directional_offset(
            red_direction, current_prop_type
        )

        # Publish separation calculation event
        beat_data = BeatData(
            letter=pictograph_data.letter, pictograph_data=pictograph_data
        )
        self.event_publisher.publish_separation_calculated(
            beat_data,
            blue_direction,
            red_direction,
            blue_offset,
            red_offset,
            current_prop_type,
        )

        return blue_offset, red_offset

    def detect_prop_overlap(self, beat_data: BeatData) -> bool:
        """
        Detect if props overlap based on their end positions and orientations.
        """
        overlap_detected = self.overlap_detector.detect_prop_overlap(beat_data)

        # Publish overlap detection event if overlap found
        if overlap_detected and beat_data.pictograph_data:
            blue_motion = beat_data.pictograph_data.motions.get("blue")
            red_motion = beat_data.pictograph_data.motions.get("red")
            if blue_motion and red_motion:
                self.event_publisher.publish_overlap_detected(
                    beat_data, blue_motion, red_motion
                )

        return overlap_detected

    def _apply_algorithmic_beta_positioning(self, beat_data: BeatData) -> BeatData:
        """
        Apply algorithmic beta prop positioning.

        Uses classification and repositioning logic.
        """
        # Get motion data from pictograph_data
        if not beat_data.pictograph_data:
            return beat_data

        # Calculate separation offsets
        blue_offset, red_offset = self.calculate_separation_offsets(
            beat_data.pictograph_data
        )

        # TODO: Apply offsets to beat_data
        # This would modify the actual positioning data in beat_data
        # For now, return unmodified data as we need renderer integration

        return beat_data

    def _get_current_prop_type(self) -> PropType:
        """
        Get current prop type from settings.

        For now returns a default, but should integrate with settings system.
        """
        # TODO: Integrate with actual settings system
        return PropType.HAND  # Default to smallest offset
