"""
Beat Domain Models

Immutable data structures for individual beats in kinetic sequences.
Handles beat data, motion references, and glyph information.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json

# Forward reference for PictographData to avoid circular imports
from typing import TYPE_CHECKING, Any
import uuid

from .motion_data import MotionData


if TYPE_CHECKING:
    from .pictograph_data import PictographData


@dataclass(frozen=True)
class BeatData:
    """
    REPLACES: Beat class with UI coupling

    Pure business data for a single beat in a sequence.
    No UI dependencies, completely immutable.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    beat_number: int = 1
    duration: float = 1.0
    blue_reversal: bool = False
    red_reversal: bool = False
    is_blank: bool = False

    # NEW: Optional pictograph data
    pictograph_data: PictographData | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate beat data."""
        if self.duration < 0:
            raise ValueError("Duration must be positive")
        if self.beat_number < 0:
            raise ValueError("Beat number must be non-negative")

    def update(self, **kwargs) -> BeatData:
        """Create a new BeatData with updated fields."""
        from dataclasses import replace

        return replace(self, **kwargs)

    def is_valid(self) -> bool:
        """Check if beat has valid data for sequence inclusion."""
        return True

    @property
    def has_pictograph(self) -> bool:
        """Check if this beat has associated pictograph data."""
        return self.pictograph_data is not None

    @property
    def letter(self) -> str | None:
        """Get beat letter from pictograph data if available, fallback to metadata."""
        if self.has_pictograph and self.pictograph_data.letter:
            return self.pictograph_data.letter
        return self.metadata.get("letter")

    @property
    def blue_motion(self) -> MotionData | None:
        """Get blue motion from pictograph data if available."""
        if self.has_pictograph and self.pictograph_data.motions:
            return self.pictograph_data.motions.get("blue")
        return None

    @property
    def red_motion(self) -> MotionData | None:
        """Get red motion from pictograph data if available."""
        if self.has_pictograph and self.pictograph_data.motions:
            return self.pictograph_data.motions.get("red")
        return None

    @classmethod
    def from_pictograph(
        cls, pictograph_data: PictographData, beat_number: int
    ) -> BeatData:
        """Create BeatData from PictographData."""
        return cls(
            beat_number=beat_number,
            pictograph_data=pictograph_data,
            metadata={
                "letter": pictograph_data.letter,
                "created_from_pictograph": True,
            },
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "id": self.id,
            "beat_number": self.beat_number,
            "duration": self.duration,
            "blue_reversal": self.blue_reversal,
            "red_reversal": self.red_reversal,
            "is_blank": self.is_blank,
            "metadata": self.metadata,
        }

        # Add pictograph data if present
        if self.pictograph_data:
            result["pictograph_data"] = self.pictograph_data.to_dict()

        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BeatData:
        """Create from dictionary."""
        # Handle pictograph data
        pictograph_data = None
        if "pictograph_data" in data:
            from .pictograph_data import PictographData

            pictograph_data = PictographData.from_dict(data["pictograph_data"])

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            beat_number=data.get("beat_number", 1),
            duration=data.get("duration", 1.0),
            blue_reversal=data.get("blue_reversal", False),
            red_reversal=data.get("red_reversal", False),
            is_blank=data.get("is_blank", False),
            pictograph_data=pictograph_data,
            metadata=data.get("metadata", {}),
        )

    def to_camel_dict(self) -> dict[str, Any]:
        """Convert to dictionary with camelCase keys for JSON APIs."""
        from ..serialization import dataclass_to_camel_dict

        return dataclass_to_camel_dict(self)

    def to_json(self, camel_case: bool = True, **kwargs) -> str:
        """Serialize to JSON string."""
        from ..serialization import domain_model_to_json

        if camel_case:
            return domain_model_to_json(self, **kwargs)
        return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_json(cls, json_str: str, camel_case: bool = True) -> BeatData:
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json

        if camel_case:
            return domain_model_from_json(json_str, cls)
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def empty(cls) -> BeatData:
        """Create an empty beat data."""
        return cls(is_blank=True)
