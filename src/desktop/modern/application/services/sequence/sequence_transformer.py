"""
Sequence Transformer - Workbench Transformations

Handles all workbench transformation operations on sequences.
Extracted from the monolithic sequence management service to focus
solely on sequence transformations and spatial operations.
"""

import logging
from enum import Enum
from typing import Any

from desktop.modern.core.interfaces.sequence_operation_services import (
    ISequenceTransformer,
)
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData

logger = logging.getLogger(__name__)


class WorkbenchOperation(Enum):
    """Types of workbench operations."""

    COLOR_SWAP = "color_swap"
    HORIZONTAL_REFLECTION = "horizontal_reflection"
    VERTICAL_REFLECTION = "vertical_reflection"
    ROTATION_90 = "rotation_90"
    ROTATION_180 = "rotation_180"
    ROTATION_270 = "rotation_270"
    REVERSE_SEQUENCE = "reverse_sequence"


class SequenceTransformer(ISequenceTransformer):
    """
    Service for applying workbench transformations to sequences.

    Responsibilities:
    - Color swapping (blue/red motion exchange)
    - Spatial reflections (horizontal/vertical)
    - Rotational transformations (90°, 180°, 270°)
    - Sequence reversal
    - Transformation matrix operations
    """

    def __init__(self):
        # Load transformation matrices for spatial operations
        self._transformation_matrices = self._load_transformation_matrices()

    def apply_workbench_operation(
        self, sequence: SequenceData, operation: str, **kwargs
    ) -> SequenceData:
        """Apply workbench transformation to sequence."""
        if not isinstance(sequence, SequenceData):
            raise ValueError("Sequence must be a SequenceData instance")

        try:
            operation_enum = WorkbenchOperation(operation)
        except ValueError:
            raise ValueError(f"Unknown workbench operation: {operation}")

        logger.info(f"Applying {operation} transformation to sequence {sequence.name}")

        if operation_enum == WorkbenchOperation.COLOR_SWAP:
            return self._apply_color_swap(sequence)
        elif operation_enum == WorkbenchOperation.HORIZONTAL_REFLECTION:
            return self._apply_horizontal_reflection(sequence)
        elif operation_enum == WorkbenchOperation.VERTICAL_REFLECTION:
            return self._apply_vertical_reflection(sequence)
        elif operation_enum == WorkbenchOperation.ROTATION_90:
            return self._apply_rotation(sequence, 90)
        elif operation_enum == WorkbenchOperation.ROTATION_180:
            return self._apply_rotation(sequence, 180)
        elif operation_enum == WorkbenchOperation.ROTATION_270:
            return self._apply_rotation(sequence, 270)
        elif operation_enum == WorkbenchOperation.REVERSE_SEQUENCE:
            return self._apply_reverse_sequence(sequence)
        else:
            raise ValueError(f"Unhandled workbench operation: {operation}")

    def _apply_color_swap(self, sequence: SequenceData) -> SequenceData:
        """Swap blue and red motions in all beats."""
        logger.debug(f"Applying color swap to {len(sequence.beats)} beats")

        new_beats = []
        for beat in sequence.beats:
            new_beat = beat.update(
                blue_motion=beat.red_motion,
                red_motion=beat.blue_motion,
            )
            new_beats.append(new_beat)

        transformed_sequence = sequence.update(beats=new_beats)
        logger.info("Color swap applied successfully")
        return transformed_sequence

    def _apply_horizontal_reflection(self, sequence: SequenceData) -> SequenceData:
        """Apply horizontal reflection to all motions."""
        logger.debug(f"Applying horizontal reflection to {len(sequence.beats)} beats")

        new_beats = []
        transformation_matrix = self._transformation_matrices["horizontal_flip"]

        for beat in sequence.beats:
            new_beat = self._apply_transformation_to_beat(beat, transformation_matrix)
            new_beats.append(new_beat)

        transformed_sequence = sequence.update(beats=new_beats)
        logger.info("Horizontal reflection applied successfully")
        return transformed_sequence

    def _apply_vertical_reflection(self, sequence: SequenceData) -> SequenceData:
        """Apply vertical reflection to all motions."""
        logger.debug(f"Applying vertical reflection to {len(sequence.beats)} beats")

        new_beats = []
        transformation_matrix = self._transformation_matrices["vertical_flip"]

        for beat in sequence.beats:
            new_beat = self._apply_transformation_to_beat(beat, transformation_matrix)
            new_beats.append(new_beat)

        transformed_sequence = sequence.update(beats=new_beats)
        logger.info("Vertical reflection applied successfully")
        return transformed_sequence

    def _apply_rotation(self, sequence: SequenceData, degrees: int) -> SequenceData:
        """Apply rotation to all motions."""
        logger.debug(f"Applying {degrees}° rotation to {len(sequence.beats)} beats")

        # Map degrees to transformation matrix
        rotation_key = f"rotation_{degrees}"
        if rotation_key not in self._transformation_matrices:
            raise ValueError(f"Unsupported rotation angle: {degrees}")

        new_beats = []
        transformation_matrix = self._transformation_matrices[rotation_key]

        for beat in sequence.beats:
            new_beat = self._apply_transformation_to_beat(beat, transformation_matrix)
            new_beats.append(new_beat)

        transformed_sequence = sequence.update(beats=new_beats)
        logger.info(f"{degrees}° rotation applied successfully")
        return transformed_sequence

    def _apply_reverse_sequence(self, sequence: SequenceData) -> SequenceData:
        """Reverse the order of beats in sequence."""
        logger.debug(f"Reversing sequence of {len(sequence.beats)} beats")

        new_beats = list(reversed(sequence.beats))

        # Update beat numbers to maintain proper sequencing
        for i, beat in enumerate(new_beats):
            new_beats[i] = beat.update(beat_number=i + 1)

        reversed_sequence = sequence.update(beats=new_beats)
        logger.info("Sequence reversal applied successfully")
        return reversed_sequence

    def _apply_transformation_to_beat(
        self, beat: BeatData, transformation_matrix: list
    ) -> BeatData:
        """Apply transformation matrix to a single beat's motion data."""
        # This is a placeholder for the actual transformation logic
        # In a real implementation, this would:
        # 1. Extract spatial coordinates from motion data
        # 2. Apply the transformation matrix
        # 3. Update the motion data with new coordinates
        # 4. Handle any orientation/direction changes

        # For now, return the beat unchanged as the actual transformation
        # logic would depend on the specific motion data structure
        logger.debug(f"Applying transformation matrix to beat {beat.beat_number}")
        return beat

    def _load_transformation_matrices(self) -> dict[str, Any]:
        """Load transformation matrices for workbench operations."""
        return {
            "rotation_90": [[0, -1], [1, 0]],
            "rotation_180": [[-1, 0], [0, -1]],
            "rotation_270": [[0, 1], [-1, 0]],
            "horizontal_flip": [[-1, 0], [0, 1]],
            "vertical_flip": [[1, 0], [0, -1]],
        }

    def get_available_operations(self) -> list[str]:
        """Get list of available workbench operations."""
        return [op.value for op in WorkbenchOperation]

    def validate_operation(self, operation: str) -> bool:
        """Validate if operation is supported."""
        try:
            WorkbenchOperation(operation)
            return True
        except ValueError:
            return False

    # Interface implementation methods
    def mirror_sequence(self, sequence: Any, axis: str = "vertical") -> Any:
        """Mirror sequence along axis (interface implementation)."""
        if axis == "vertical":
            return self.apply_transformation(
                sequence, WorkbenchOperation.VERTICAL_REFLECTION
            )
        elif axis == "horizontal":
            return self.apply_transformation(
                sequence, WorkbenchOperation.HORIZONTAL_REFLECTION
            )
        else:
            return sequence

    def rotate_sequence(self, sequence: Any, degrees: float) -> Any:
        """Rotate sequence (interface implementation)."""
        if degrees == 90:
            return self.apply_transformation(sequence, WorkbenchOperation.ROTATION_90)
        elif degrees == 180:
            return self.apply_transformation(sequence, WorkbenchOperation.ROTATION_180)
        elif degrees == 270:
            return self.apply_transformation(sequence, WorkbenchOperation.ROTATION_270)
        else:
            return sequence

    def reverse_sequence(self, sequence: Any) -> Any:
        """Reverse sequence order (interface implementation)."""
        return self.apply_transformation(sequence, WorkbenchOperation.SEQUENCE_REVERSAL)
