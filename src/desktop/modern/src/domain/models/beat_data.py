"""
Beat Domain Models

Immutable data structures for individual beats in kinetic sequences.
Handles beat data, motion references, and glyph information.
"""

import json
import uuid
from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Any, Dict, Optional, Union

from ._shared_utils import process_field_value
from .glyph_models import GlyphData
from .motion_models import MotionData


@dataclass(frozen=True)
class BeatData:
    """
    REPLACES: Beat class with UI coupling

    Pure business data for a single beat in a sequence.
    No UI dependencies, completely immutable.
    """

    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    beat_number: int = 1

    # Business data
    letter: Optional[str] = None
    duration: float = 1.0

    # Motion data (replaces complex dictionaries)
    blue_motion: Optional[MotionData] = None
    red_motion: Optional[MotionData] = None

    # Glyph data
    glyph_data: Optional[GlyphData] = None

    # State flags
    blue_reversal: bool = False
    red_reversal: bool = False
    is_blank: bool = False

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate beat data."""
        if self.duration < 0:
            raise ValueError("Duration must be positive")
        # Allow beat_number=0 for start positions (legacy compatibility)
        if self.beat_number < 0:
            raise ValueError("Beat number must be non-negative")

    def update(self, **kwargs) -> "BeatData":
        """Create a new BeatData with updated fields."""
        from dataclasses import replace

        return replace(self, **kwargs)

    def is_valid(self) -> bool:
        """Check if beat has valid data for sequence inclusion."""
        if self.is_blank:
            return True
        return (
            self.letter is not None
            and self.blue_motion is not None
            and self.red_motion is not None
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "beat_number": self.beat_number,
            "letter": self.letter,
            "duration": self.duration,
            "blue_motion": self.blue_motion.to_dict() if self.blue_motion else None,
            "red_motion": self.red_motion.to_dict() if self.red_motion else None,
            "glyph_data": self.glyph_data.to_dict() if self.glyph_data else None,
            "blue_reversal": self.blue_reversal,
            "red_reversal": self.red_reversal,
            "is_blank": self.is_blank,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BeatData":
        """Create from dictionary."""
        blue_motion = None
        if data.get("blue_motion"):
            blue_motion = MotionData.from_dict(data["blue_motion"])

        red_motion = None
        if data.get("red_motion"):
            red_motion = MotionData.from_dict(data["red_motion"])

        glyph_data = None
        if data.get("glyph_data"):
            glyph_data = GlyphData.from_dict(data["glyph_data"])

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            beat_number=data.get("beat_number", 1),
            letter=data.get("letter"),
            duration=data.get("duration", 1.0),
            blue_motion=blue_motion,
            red_motion=red_motion,
            glyph_data=glyph_data,
            blue_reversal=data.get("blue_reversal", False),
            red_reversal=data.get("red_reversal", False),
            is_blank=data.get("is_blank", False),
            metadata=data.get("metadata", {}),
        )

    def to_camel_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with camelCase keys for JSON APIs."""
        from ..serialization import dataclass_to_camel_dict

        return dataclass_to_camel_dict(self)

    def to_json(self, camel_case: bool = True, **kwargs) -> str:
        """Serialize to JSON string."""
        from ..serialization import domain_model_to_json

        if camel_case:
            return domain_model_to_json(self, **kwargs)
        else:
            return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_json(cls, json_str: str, camel_case: bool = True) -> "BeatData":
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json

        if camel_case:
            return domain_model_from_json(json_str, cls)
        else:
            data = json.loads(json_str)
            return cls.from_dict(data)

    @classmethod
    def empty(cls) -> "BeatData":
        """Create an empty beat data."""
        return cls(is_blank=True)
