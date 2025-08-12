"""
Sequence Domain Models

Immutable data structures for complete kinetic sequences.
Handles sequence composition, beat management, and validation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any
import uuid

from .beat_data import BeatData


@dataclass(frozen=True)
class SequenceData:
    """
    REPLACES: Complex sequence management with UI coupling

    Pure business data for a complete kinetic sequence.
    No UI dependencies, completely immutable.
    """

    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    word: str = ""  # Generated word from sequence

    # Business data
    beats: list[BeatData] = field(default_factory=list)
    start_position: BeatData | None = None

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate sequence data."""
        # Validate beat numbers are sequential (allowing beat_number=0 for start positions)
        for i, beat in enumerate(self.beats):
            # Check if this is a start position beat
            is_start_position = beat.metadata.get("is_start_position", False)

            if is_start_position:
                # Start position should be beat_number=0 and should be first in array
                if beat.beat_number != 0:
                    raise ValueError(
                        f"Start position beat has number {beat.beat_number}, expected 0"
                    )
                if i != 0:
                    raise ValueError(
                        f"Start position beat is at index {i}, should be at index 0"
                    )
            else:
                # Regular beats should be numbered sequentially starting from 1
                # Account for start position offset
                start_position_offset = (
                    1
                    if (
                        self.beats
                        and self.beats[0].metadata.get("is_start_position", False)
                    )
                    else 0
                )
                expected_beat_number = i + 1 - start_position_offset

                if beat.beat_number != expected_beat_number:
                    raise ValueError(
                        f"Beat {i} has number {beat.beat_number}, expected {expected_beat_number}"
                    )

    @property
    def length(self) -> int:
        """Get the number of beats in the sequence."""
        return len(self.beats)

    @property
    def total_duration(self) -> float:
        """Get the total duration of the sequence."""
        return sum(beat.duration for beat in self.beats)

    @property
    def is_empty(self) -> bool:
        """Check if sequence has no beats."""
        return len(self.beats) == 0

    @property
    def is_valid(self) -> bool:
        """Check if sequence is valid."""
        if self.is_empty:
            return False
        return all(beat.is_valid() for beat in self.beats)

    def get_beat(self, beat_number: int) -> BeatData | None:
        """Get a beat by its number."""
        for beat in self.beats:
            if beat.beat_number == beat_number:
                return beat
        return None

    def add_beat(self, beat_data: BeatData) -> SequenceData:
        """Create a new sequence with an additional beat."""
        # Calculate the correct beat number (excluding start position beat)
        non_start_beats = [
            b for b in self.beats if not b.metadata.get("is_start_position", False)
        ]
        next_beat_number = len(non_start_beats) + 1

        new_beat = beat_data.update(beat_number=next_beat_number)
        new_beats = [*list(self.beats), new_beat]

        from dataclasses import replace

        return replace(self, beats=new_beats)

    def remove_beat(self, beat_number: int) -> SequenceData:
        """Create a new sequence with a beat removed."""
        new_beats = []
        for beat in self.beats:
            if beat.beat_number != beat_number:
                # Renumber remaining beats Call
                new_beat_number = len(new_beats) + 1
                new_beats.append(beat.update(beat_number=new_beat_number))

        from dataclasses import replace

        return replace(self, beats=new_beats)

    def update_beat(self, beat_number: int, **kwargs) -> SequenceData:
        """Create a new sequence with an updated beat."""
        new_beats = []
        for beat in self.beats:
            if beat.beat_number == beat_number:
                new_beats.append(beat.update(**kwargs))
            else:
                new_beats.append(beat)

        from dataclasses import replace

        return replace(self, beats=new_beats)

    def update(self, **kwargs) -> SequenceData:
        """Create a new sequence with updated fields."""
        from dataclasses import replace

        return replace(self, **kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "word": self.word,
            "beats": [beat.to_dict() for beat in self.beats],
            "start_position": (
                self.start_position.to_dict() if self.start_position else None
            ),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SequenceData:
        """Create from dictionary."""
        beats = [BeatData.from_dict(beat_data) for beat_data in data.get("beats", [])]

        start_position = None
        if data.get("start_position"):
            start_position = BeatData.from_dict(data["start_position"])

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            word=data.get("word", ""),
            beats=beats,
            start_position=start_position,
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
    def from_json(cls, json_str: str, camel_case: bool = True) -> SequenceData:
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json

        if camel_case:
            return domain_model_from_json(json_str, cls)
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def empty(cls) -> SequenceData:
        """Create an empty sequence."""
        return cls(name="", beats=[])
