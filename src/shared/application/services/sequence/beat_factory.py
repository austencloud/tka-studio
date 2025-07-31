"""
Beat Factory Service

Handles creation of BeatData objects with proper pictograph embedding.
Replaces conversion methods with direct construction.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData


class IBeatFactory(ABC):
    """Interface for beat creation operations."""

    @abstractmethod
    def create_from_pictograph(
        self,
        pictograph_data: PictographData,
        beat_number: int,
        duration: float = 1.0,
        metadata: Optional[dict[str, Any]] = None,
    ) -> BeatData:
        """Create BeatData with embedded pictograph."""

    @abstractmethod
    def create_empty_beat(self, beat_number: int, duration: float = 1.0) -> BeatData:
        """Create empty beat without pictograph."""

    @abstractmethod
    def create_start_position_beat_data(
        self, pictograph_data: PictographData, sequence_start_position: str = "alpha"
    ) -> BeatData:
        """Create a start position beat with pictograph."""


class BeatFactory(IBeatFactory):
    """Factory for creating BeatData objects with consistent patterns."""

    @staticmethod
    def create_from_pictograph(
        pictograph_data: PictographData,
        beat_number: int,
        duration: float = 1.0,
        metadata: Optional[dict[str, Any]] = None,
    ) -> BeatData:
        """
        Create BeatData with embedded pictograph.

        Args:
            pictograph_data: The pictograph to embed
            beat_number: Beat number in sequence
            duration: Beat duration (default 1.0)
            metadata: Additional metadata (optional)

        Returns:
            BeatData with embedded pictograph
        """
        beat_metadata = metadata or {}

        # Add pictograph-derived metadata
        beat_metadata.update(
            {
                "start_position": pictograph_data.start_position,
                "end_position": pictograph_data.end_position,
                "created_from_pictograph": True,
            }
        )

        # Copy relevant pictograph metadata
        if pictograph_data.metadata:
            for key, value in pictograph_data.metadata.items():
                if key not in [
                    "is_start_position"
                ]:  # Don't copy start position flags to regular beats
                    beat_metadata[f"pictograph_{key}"] = value

        return BeatData(
            beat_number=beat_number,
            pictograph_data=pictograph_data,
            duration=duration,
            is_blank=pictograph_data.is_blank,
            metadata=beat_metadata,
        )

    @staticmethod
    def create_empty_beat(beat_number: int, duration: float = 1.0) -> BeatData:
        """Create empty beat without pictograph."""
        return BeatData(
            beat_number=beat_number,
            duration=duration,
            is_blank=True,
            metadata={"type": "empty_beat"},
        )

    @staticmethod
    def create_start_position_beat_data(
        pictograph_data: PictographData, sequence_start_position: str = "alpha"
    ) -> BeatData:
        """Create a start position beat with pictograph."""
        return BeatData(
            beat_number=0,  # Start positions are beat 0
            pictograph_data=pictograph_data,
            duration=1.0,
            metadata={
                "is_start_position": True,
                "sequence_start_position": sequence_start_position,
                "timing": "same",
                "direction": "none",
            },
        )
