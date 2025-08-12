"""
Codex Operations Service

Handles transformation operations on pictograph data for the codex,
including rotate, mirror, and color swap operations.
"""

from __future__ import annotations

import logging

from legacy.data.constants import (
    ALPHA1,
    ALPHA3,
    ALPHA5,
    ALPHA7,
    BETA1,
    BETA3,
    BETA5,
    BETA7,
    BLUE,
    END_POS,
    GAMMA1,
    GAMMA3,
    GAMMA5,
    GAMMA7,
    GAMMA11,
    GAMMA13,
    GAMMA15,
    MOTION_TYPE,
    RED,
    START_POS,
)

from desktop.modern.domain.models.pictograph_data import PictographData


logger = logging.getLogger(__name__)


class CodexOperationsService:
    """
    Service for performing operations on codex pictograph data.

    Handles rotate, mirror, and color swap transformations
    while maintaining data integrity.
    """

    # Position mappings for mirroring (vertical mirror)
    VERTICAL_MIRROR_POSITIONS = {
        ALPHA1: ALPHA3,
        ALPHA3: ALPHA1,
        ALPHA5: ALPHA7,
        ALPHA7: ALPHA5,
        BETA1: BETA3,
        BETA3: BETA1,
        BETA5: BETA7,
        BETA7: BETA5,
        GAMMA1: GAMMA15,
        GAMMA3: GAMMA13,
        GAMMA5: GAMMA11,
        GAMMA7: GAMMA11,  # This might need adjustment based on actual layout
        GAMMA11: GAMMA5,
        GAMMA13: GAMMA3,
        GAMMA15: GAMMA1,
    }

    def __init__(self):
        pass

    def rotate_pictograph_data(self, pictograph_data: PictographData) -> PictographData:
        """
        Rotate a pictograph by 90 degrees clockwise.

        Args:
            pictograph_data: The pictograph data to rotate

        Returns:
            New PictographData with rotated positions
        """
        try:
            # Get the current data as dict
            data_dict = pictograph_data.to_dict()

            # Apply rotation to start and end positions
            data_dict[START_POS] = self._rotate_position(data_dict[START_POS])
            data_dict[END_POS] = self._rotate_position(data_dict[END_POS])

            # Create new PictographData with rotated positions
            return PictographData.from_dict(data_dict)

        except Exception as e:
            logger.exception(f"Failed to rotate pictograph data: {e}")
            return pictograph_data  # Return original on error

    def mirror_pictograph_data(self, pictograph_data: PictographData) -> PictographData:
        """
        Mirror a pictograph vertically.

        Args:
            pictograph_data: The pictograph data to mirror

        Returns:
            New PictographData with mirrored positions
        """
        try:
            # Get the current data as dict
            data_dict = pictograph_data.to_dict()

            # Apply mirroring to start and end positions
            data_dict[START_POS] = self._mirror_position(data_dict[START_POS])
            data_dict[END_POS] = self._mirror_position(data_dict[END_POS])

            # Create new PictographData with mirrored positions
            return PictographData.from_dict(data_dict)

        except Exception as e:
            logger.exception(f"Failed to mirror pictograph data: {e}")
            return pictograph_data  # Return original on error

    def swap_colors_pictograph_data(
        self, pictograph_data: PictographData
    ) -> PictographData:
        """
        Swap red and blue motion types in a pictograph.

        Args:
            pictograph_data: The pictograph data to color swap

        Returns:
            New PictographData with swapped colors
        """
        try:
            # Get the current data as dict
            data_dict = pictograph_data.to_dict()

            # Swap blue and red motion types
            blue_motion = data_dict.get(f"{BLUE}_{MOTION_TYPE}")
            red_motion = data_dict.get(f"{RED}_{MOTION_TYPE}")

            if blue_motion is not None and red_motion is not None:
                data_dict[f"{BLUE}_{MOTION_TYPE}"] = red_motion
                data_dict[f"{RED}_{MOTION_TYPE}"] = blue_motion

            # Create new PictographData with swapped colors
            return PictographData.from_dict(data_dict)

        except Exception as e:
            logger.exception(f"Failed to swap colors in pictograph data: {e}")
            return pictograph_data  # Return original on error

    def _rotate_position(self, position: str) -> str:
        """
        Rotate a position by 90 degrees clockwise.

        This is a simplified rotation - in a real implementation,
        you'd need the actual position layout to do proper rotation.
        """
        # For now, return the same position
        # This would need to be implemented based on the actual grid layout
        return position

    def _mirror_position(self, position: str) -> str:
        """
        Mirror a position vertically.

        Args:
            position: The position to mirror

        Returns:
            The mirrored position
        """
        return self.VERTICAL_MIRROR_POSITIONS.get(position, position)

    def apply_operation_to_all(
        self, pictograph_data_dict: dict[str, PictographData | None], operation: str
    ) -> dict[str, PictographData | None]:
        """
        Apply an operation to all pictographs in a dictionary.

        Args:
            pictograph_data_dict: Dictionary of letter -> PictographData
            operation: Operation to apply ('rotate', 'mirror', 'color_swap')

        Returns:
            New dictionary with transformed pictograph data
        """
        result = {}

        for letter, pictograph_data in pictograph_data_dict.items():
            if pictograph_data is None:
                result[letter] = None
                continue

            try:
                if operation == "rotate":
                    result[letter] = self.rotate_pictograph_data(pictograph_data)
                elif operation == "mirror":
                    result[letter] = self.mirror_pictograph_data(pictograph_data)
                elif operation == "color_swap":
                    result[letter] = self.swap_colors_pictograph_data(pictograph_data)
                else:
                    logger.warning(f"Unknown operation: {operation}")
                    result[letter] = pictograph_data

            except Exception as e:
                logger.exception(f"Failed to apply {operation} to letter {letter}: {e}")
                result[letter] = pictograph_data  # Keep original on error

        return result
