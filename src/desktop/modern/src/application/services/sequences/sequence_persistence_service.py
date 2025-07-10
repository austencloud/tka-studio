"""
Sequence persistence service - exactly like the legacy version.
Updates current_sequence.json whenever sequence changes occur.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class SequencePersistenceService:
    """Simple sequence persistence that updates current_sequence.json like legacy."""

    def __init__(self):
        # Use same location as legacy
        modern_dir = Path(__file__).parent.parent.parent.parent.parent
        self.current_sequence_json = modern_dir / "current_sequence.json"

        logger.info(f"Sequence persistence initialized: {self.current_sequence_json}")

    def load_current_sequence(self) -> List[Dict[str, Any]]:
        """Load current sequence from JSON file - exactly like legacy."""
        try:
            if not self.current_sequence_json.exists():
                return self.get_default_sequence()

            with open(self.current_sequence_json, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return self.get_default_sequence()

                sequence = json.loads(content)
                if not sequence or not isinstance(sequence, list):
                    return self.get_default_sequence()

            return sequence

        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Failed to load current sequence: {e}")
            # Create default file if it doesn't exist
            default_sequence = self.get_default_sequence()
            self.save_current_sequence(default_sequence)
            return default_sequence

    def save_current_sequence(self, sequence: List[Dict[str, Any]]) -> None:
        """Save current sequence to JSON file - exactly like legacy."""
        # Removed repetitive debug log

        try:
            if not sequence:
                sequence = self.get_default_sequence()
                # Removed repetitive debug log

            # Ensure directory exists
            self.current_sequence_json.parent.mkdir(parents=True, exist_ok=True)
            # Removed repetitive debug log

            with open(self.current_sequence_json, "w", encoding="utf-8") as file:
                json.dump(sequence, file, indent=4, ensure_ascii=False)

            # Removed repetitive debug log
            logger.debug(f"Saved current sequence with {len(sequence)} items")

        except Exception as e:
            print(f"❌ [PERSISTENCE] Failed to save current sequence: {e}")
            logger.error(f"Failed to save current sequence: {e}")
            import traceback

            traceback.print_exc()
            raise

    def clear_current_sequence(self) -> None:
        """Clear the current sequence - exactly like legacy."""
        self.save_current_sequence([])

    def get_default_sequence(self) -> List[Dict[str, Any]]:
        """Return default sequence metadata - exactly like legacy."""
        return [
            {
                "word": "",
                "author": "",
                "level": 0,
                "prop_type": "staff",
                "grid_mode": "diamond",
                "is_circular": False,
                "can_be_CAP": False,
                "is_strict_rotated_CAP": False,
                "is_strict_mirrored_CAP": False,
                "is_strict_swapped_CAP": False,
                "is_mirrored_swapped_CAP": False,
                "is_rotated_swapped_CAP": False,
            }
        ]

    def update_current_sequence_with_beat(self, beat_data: Dict[str, Any]) -> None:
        """Add a beat to the current sequence - exactly like legacy."""
        sequence = self.load_current_sequence()

        # Get metadata and beats
        if sequence and "word" in sequence[0]:
            sequence_metadata = sequence[0]
            sequence_beats = sequence[1:]
        else:
            sequence_metadata = self.get_default_sequence()[0]
            sequence_beats = []

        # Add beat number if not present
        if "beat" not in beat_data:
            beat_data["beat"] = self.get_next_beat_number(sequence_beats)

        sequence_beats.append(beat_data)

        # Sort by beat number
        sequence_beats.sort(key=lambda entry: entry.get("beat", float("inf")))

        # Rebuild sequence
        sequence = [sequence_metadata] + sequence_beats
        self.save_current_sequence(sequence)

    def get_next_beat_number(self, sequence_beats: List[Dict[str, Any]]) -> int:
        """Get the next beat number - exactly like legacy."""
        if not sequence_beats:
            return 1
        return max(beat.get("beat", 0) for beat in sequence_beats) + 1

    def update_sequence_metadata(self, metadata: Dict[str, Any]) -> None:
        """Update sequence metadata - exactly like legacy."""
        sequence = self.load_current_sequence()

        if sequence:
            # Update first item (metadata)
            sequence[0].update(metadata)
        else:
            # Create new sequence with metadata
            sequence = [metadata]

        self.save_current_sequence(sequence)

    def remove_beat_at_index(self, beat_index: int) -> None:
        """Remove a beat from the sequence - exactly like legacy."""
        sequence = self.load_current_sequence()

        if len(sequence) > beat_index + 1:  # +1 because index 0 is metadata
            sequence.pop(beat_index + 1)
            self.save_current_sequence(sequence)

    def clear_all_beats(self) -> None:
        """Remove all beats but keep metadata - exactly like legacy."""
        sequence = self.load_current_sequence()

        if sequence:
            # Keep only metadata (first item)
            sequence = [sequence[0]]
        else:
            sequence = self.get_default_sequence()

        self.save_current_sequence(sequence)

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int) -> None:
        """Update the number of turns for a specific beat - exactly like legacy."""
        sequence = self.load_current_sequence()

        actual_index = beat_index + 1  # +1 because index 0 is metadata
        if len(sequence) > actual_index:
            beat = sequence[actual_index]
            if f"{color}_attributes" in beat:
                beat[f"{color}_attributes"]["turns"] = new_turns
                self.save_current_sequence(sequence)
