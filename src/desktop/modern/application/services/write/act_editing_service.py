"""
Act Editing Service

Service for editing acts including adding/removing sequences,
managing act structure, and updating metadata.
"""

from __future__ import annotations

import logging
from typing import Any

from desktop.modern.core.interfaces.write_services import ActData, IActEditingService


logger = logging.getLogger(__name__)


class ActEditingService(IActEditingService):
    """
    Service for editing acts and managing their sequence content.

    Provides operations for modifying act structure including
    sequence management, metadata updates, and validation.
    """

    def __init__(self):
        """Initialize the act editing service."""
        logger.info("ActEditingService initialized")

    def add_sequence_to_act(
        self, act: ActData, sequence_data: dict[str, Any], position: int = -1
    ) -> bool:
        """
        Add a sequence to an act.

        Args:
            act: The act to add the sequence to
            sequence_data: The sequence data to add
            position: Position to insert at (-1 for end)

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self._validate_sequence_data(sequence_data):
                logger.error("Invalid sequence data provided")
                return False

            # Create a copy of the sequence data to avoid references
            sequence_copy = dict(sequence_data)

            # Add timestamp if not present
            if "added_at" not in sequence_copy:
                import time

                sequence_copy["added_at"] = time.time()

            # Insert at specified position
            if position == -1 or position >= len(act.sequences):
                act.sequences.append(sequence_copy)
                logger.info(
                    f"Added sequence to end of act '{act.name}' (position {len(act.sequences) - 1})"
                )
            else:
                position = max(0, position)  # Ensure non-negative
                act.sequences.insert(position, sequence_copy)
                logger.info(
                    f"Inserted sequence into act '{act.name}' at position {position}"
                )

            # Update act metadata
            self._update_sequence_count_metadata(act)

            return True

        except Exception as e:
            logger.exception(f"Failed to add sequence to act '{act.name}': {e}")
            return False

    def remove_sequence_from_act(self, act: ActData, position: int) -> bool:
        """
        Remove a sequence from an act.

        Args:
            act: The act to remove the sequence from
            position: Position of the sequence to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            if not (0 <= position < len(act.sequences)):
                logger.error(
                    f"Invalid position {position} for act with {len(act.sequences)} sequences"
                )
                return False

            act.sequences.pop(position)
            logger.info(
                f"Removed sequence from position {position} in act '{act.name}'"
            )

            # Update act metadata
            self._update_sequence_count_metadata(act)

            return True

        except Exception as e:
            logger.exception(
                f"Failed to remove sequence at position {position} from act '{act.name}': {e}"
            )
            return False

    def move_sequence_in_act(
        self, act: ActData, from_position: int, to_position: int
    ) -> bool:
        """
        Move a sequence within an act.

        Args:
            act: The act to modify
            from_position: Current position of the sequence
            to_position: New position for the sequence

        Returns:
            True if successful, False otherwise
        """
        try:
            sequence_count = len(act.sequences)

            # Validate positions
            if not (0 <= from_position < sequence_count):
                logger.error(
                    f"Invalid from_position {from_position} for act with {sequence_count} sequences"
                )
                return False

            if not (0 <= to_position < sequence_count):
                logger.error(
                    f"Invalid to_position {to_position} for act with {sequence_count} sequences"
                )
                return False

            if from_position == to_position:
                logger.debug(
                    f"No move needed - from_position equals to_position ({from_position})"
                )
                return True

            # Move the sequence
            sequence = act.sequences.pop(from_position)
            act.sequences.insert(to_position, sequence)

            logger.info(
                f"Moved sequence in act '{act.name}' from position {from_position} to {to_position}"
            )
            return True

        except Exception as e:
            logger.exception(
                f"Failed to move sequence in act '{act.name}' from {from_position} to {to_position}: {e}"
            )
            return False

    def update_act_metadata(self, act: ActData, metadata: dict[str, Any]) -> bool:
        """
        Update act metadata.

        Args:
            act: The act to update
            metadata: New metadata to apply

        Returns:
            True if successful, False otherwise
        """
        try:
            # Update the act's metadata dictionary
            act.metadata.update(metadata)

            # Update last modified time
            import time

            act.metadata["last_modified"] = time.time()

            logger.info(f"Updated metadata for act '{act.name}'")
            return True

        except Exception as e:
            logger.exception(f"Failed to update metadata for act '{act.name}': {e}")
            return False

    def duplicate_sequence_in_act(self, act: ActData, position: int) -> bool:
        """
        Duplicate a sequence in an act.

        Args:
            act: The act to modify
            position: Position of the sequence to duplicate

        Returns:
            True if successful, False otherwise
        """
        try:
            if not (0 <= position < len(act.sequences)):
                logger.error(
                    f"Invalid position {position} for act with {len(act.sequences)} sequences"
                )
                return False

            # Create a copy of the sequence
            original_sequence = act.sequences[position]
            sequence_copy = dict(original_sequence)

            # Update metadata for the copy
            import time

            sequence_copy["added_at"] = time.time()
            if "id" in sequence_copy:
                # Generate new ID for the copy
                sequence_copy["id"] = f"{sequence_copy['id']}_copy_{int(time.time())}"

            # Insert the copy after the original
            act.sequences.insert(position + 1, sequence_copy)

            logger.info(
                f"Duplicated sequence at position {position} in act '{act.name}'"
            )

            # Update act metadata
            self._update_sequence_count_metadata(act)

            return True

        except Exception as e:
            logger.exception(
                f"Failed to duplicate sequence at position {position} in act '{act.name}': {e}"
            )
            return False

    def clear_act_sequences(self, act: ActData) -> bool:
        """
        Remove all sequences from an act.

        Args:
            act: The act to clear

        Returns:
            True if successful, False otherwise
        """
        try:
            sequence_count = len(act.sequences)
            act.sequences.clear()

            # Update act metadata
            self._update_sequence_count_metadata(act)

            logger.info(f"Cleared all {sequence_count} sequences from act '{act.name}'")
            return True

        except Exception as e:
            logger.exception(f"Failed to clear sequences from act '{act.name}': {e}")
            return False

    def _validate_sequence_data(self, sequence_data: dict[str, Any]) -> bool:
        """
        Validate sequence data structure.

        Args:
            sequence_data: The sequence data to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if it's a dictionary
            if not isinstance(sequence_data, dict):
                logger.error("Sequence data must be a dictionary")
                return False

            # Check for required fields (basic validation)
            # These might vary based on your sequence data structure
            required_fields = ["beats"]  # Minimum requirement

            for field in required_fields:
                if field not in sequence_data:
                    logger.error(f"Missing required field in sequence data: {field}")
                    return False

            # Validate beats structure
            beats = sequence_data["beats"]
            if not isinstance(beats, list):
                logger.error("Sequence beats must be a list")
                return False

            logger.debug(f"Sequence data validation passed (beats count: {len(beats)})")
            return True

        except Exception as e:
            logger.exception(f"Error validating sequence data: {e}")
            return False

    def _update_sequence_count_metadata(self, act: ActData) -> None:
        """Update sequence count in act metadata."""
        try:
            act.metadata["sequence_count"] = len(act.sequences)

            # Update total beats count
            total_beats = sum(len(seq.get("beats", [])) for seq in act.sequences)
            act.metadata["total_beats"] = total_beats

            # Update last modified time
            import time

            act.metadata["last_modified"] = time.time()

        except Exception as e:
            logger.exception(f"Failed to update sequence count metadata: {e}")

    def get_act_statistics(self, act: ActData) -> dict[str, Any]:
        """
        Get statistics about an act.

        Args:
            act: The act to analyze

        Returns:
            Dictionary with act statistics
        """
        try:
            total_beats = sum(len(seq.get("beats", [])) for seq in act.sequences)

            # Calculate estimated duration (assuming average beat duration)
            average_beat_duration = 2.0  # seconds - this could be configurable
            estimated_duration = total_beats * average_beat_duration

            stats = {
                "sequence_count": len(act.sequences),
                "total_beats": total_beats,
                "estimated_duration_seconds": estimated_duration,
                "has_music": act.music_file is not None,
                "has_description": bool(act.description.strip()),
                "metadata_count": len(act.metadata),
            }

            return stats

        except Exception as e:
            logger.exception(f"Failed to calculate act statistics for '{act.name}': {e}")
            return {}
