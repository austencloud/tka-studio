"""
Motion Attribute Service Implementation

Handles motion attribute processing, synchronization, and prefloat transformations.
Direct port of legacy attribute management logic.
"""

import logging
from typing import TYPE_CHECKING

from desktop.modern.core.interfaces.letter_determination.letter_determination_services import (
    IMotionAttributeService,
)
from desktop.modern.domain.models.enums import MotionType, PropRotationDirection

if TYPE_CHECKING:
    from desktop.modern.domain.models.motion.motion_attributes import MotionAttributes
    from desktop.modern.domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)


class MotionAttributeService(IMotionAttributeService):
    """
    Handles motion attribute processing and synchronization.

    Direct port of legacy AttributeManager functionality with modern patterns.
    """

    def sync_attributes(self, pictograph_data: "PictographData") -> "PictographData":
        """
        Synchronize and validate motion attributes.

        Direct port of legacy attribute_manager.sync_attributes logic.
        """
        beat_num = pictograph_data.beat
        blue_motion = pictograph_data.motions.get("blue")
        red_motion = pictograph_data.motions.get("red")

        logger.debug(f"Syncing attributes for beat {beat_num}")

        # For now, this is a pass-through as the legacy sync_attributes
        # primarily handled JSON updates which are not needed in the modern system
        # The actual synchronization happens in the comparison service

        # Validate attribute consistency if we have motion data
        if blue_motion and red_motion:
            if not self.validate_motion_consistency(blue_motion, red_motion):
                logger.warning(
                    f"Motion consistency validation failed for beat {beat_num}"
                )

        return pictograph_data

    def validate_motion_consistency(self, blue_motion, red_motion) -> bool:
        """
        Validate consistency between blue and red motions.

        Args:
            blue_motion: Blue motion data
            red_motion: Red motion data

        Returns:
            True if motions are consistent
        """
        try:
            # Basic validation - both motions should have valid motion types
            if not hasattr(blue_motion, "motion_type") or not hasattr(
                red_motion, "motion_type"
            ):
                return False

            # Both should have valid motion types
            if not blue_motion.motion_type or not red_motion.motion_type:
                return False

            return True
        except Exception as e:
            logger.warning(f"Motion consistency validation error: {e}")
            return False

    def apply_prefloat_transformations(
        self, attributes: "MotionAttributes", reference_attributes: "MotionAttributes"
    ) -> "MotionAttributes":
        """
        Apply prefloat motion transformations.

        Updates float motion attributes with prefloat information from reference motion.
        """
        if attributes.motion_type == MotionType.FLOAT:
            from dataclasses import replace

            # Set prefloat attributes from reference motion
            return replace(
                attributes,
                prefloat_motion_type=reference_attributes.motion_type,
                prefloat_prop_rot_dir=reference_attributes.prop_rot_dir,
            )

        return attributes

    def validate_attribute_consistency(
        self, blue_attrs: "MotionAttributes", red_attrs: "MotionAttributes"
    ) -> bool:
        """
        Validate consistency between blue and red attributes.

        Checks for common issues that could cause determination failures.
        """
        try:
            # Check that both attributes have required fields
            required_fields = [
                "motion_type",
                "start_ori",
                "end_ori",
                "start_loc",
                "end_loc",
                "prop_rot_dir",
            ]

            for field in required_fields:
                if getattr(blue_attrs, field) is None:
                    logger.warning(f"Blue attributes missing {field}")
                    return False
                if getattr(red_attrs, field) is None:
                    logger.warning(f"Red attributes missing {field}")
                    return False

            # Validate float state consistency
            if blue_attrs.motion_type == MotionType.FLOAT:
                if not blue_attrs.prefloat_motion_type:
                    logger.warning("Blue float motion missing prefloat_motion_type")
                    return False

            if red_attrs.motion_type == MotionType.FLOAT:
                if not red_attrs.prefloat_motion_type:
                    logger.warning("Red float motion missing prefloat_motion_type")
                    return False

            # Validate turn values
            if not self._validate_turn_value(blue_attrs.turns):
                logger.warning(f"Invalid blue turns value: {blue_attrs.turns}")
                return False

            if not self._validate_turn_value(red_attrs.turns):
                logger.warning(f"Invalid red turns value: {red_attrs.turns}")
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating attribute consistency: {str(e)}")
            return False

    def extract_prefloat_attributes(
        self, pictograph_data: "PictographData"
    ) -> dict[str, "MotionAttributes"]:
        """
        Extract prefloat attributes from pictograph data.

        Returns dictionary mapping color to prefloat attributes if present.
        """
        prefloat_attrs = {}

        # Check blue attributes
        if (
            pictograph_data.blue_attributes.motion_type == MotionType.FLOAT
            and pictograph_data.blue_attributes.prefloat_motion_type
        ):
            from desktop.modern.domain.models.motion.motion_attributes import (
                MotionAttributes,
            )

            prefloat_attrs["blue"] = MotionAttributes(
                motion_type=pictograph_data.blue_attributes.prefloat_motion_type,
                start_ori=pictograph_data.blue_attributes.start_ori,
                end_ori=pictograph_data.blue_attributes.end_ori,
                start_loc=pictograph_data.blue_attributes.start_loc,
                end_loc=pictograph_data.blue_attributes.end_loc,
                prop_rot_dir=pictograph_data.blue_attributes.prefloat_prop_rot_dir
                or PropRotationDirection.NO_ROT,
                turns=pictograph_data.blue_attributes.turns,
            )

        # Check red attributes
        if (
            pictograph_data.red_attributes.motion_type == MotionType.FLOAT
            and pictograph_data.red_attributes.prefloat_motion_type
        ):
            from desktop.modern.domain.models.motion.motion_attributes import (
                MotionAttributes,
            )

            prefloat_attrs["red"] = MotionAttributes(
                motion_type=pictograph_data.red_attributes.prefloat_motion_type,
                start_ori=pictograph_data.red_attributes.start_ori,
                end_ori=pictograph_data.red_attributes.end_ori,
                start_loc=pictograph_data.red_attributes.start_loc,
                end_loc=pictograph_data.red_attributes.end_loc,
                prop_rot_dir=pictograph_data.red_attributes.prefloat_prop_rot_dir
                or PropRotationDirection.NO_ROT,
                turns=pictograph_data.red_attributes.turns,
            )

        return prefloat_attrs

    def _validate_turn_value(self, turns) -> bool:
        """
        Validate that a turn value is valid.

        Turns can be int, float, or the string 'fl' for float transitions.
        """
        if isinstance(turns, (int, float)):
            return turns >= 0
        elif isinstance(turns, str):
            return turns == "fl"
        else:
            return False

    def normalize_float_attributes(
        self, pictograph_data: "PictographData"
    ) -> "PictographData":
        """
        Normalize float attributes to ensure consistency.

        Ensures that float motions have proper prefloat attributes set.
        """
        from dataclasses import replace

        blue_attrs = pictograph_data.blue_attributes
        red_attrs = pictograph_data.red_attributes

        # Normalize blue attributes if float
        if blue_attrs.motion_type == MotionType.FLOAT:
            if not blue_attrs.prefloat_motion_type:
                # Try to infer from red attributes
                if red_attrs.motion_type in [MotionType.PRO, MotionType.ANTI]:
                    blue_attrs = self.apply_prefloat_transformations(
                        blue_attrs, red_attrs
                    )

        # Normalize red attributes if float
        if red_attrs.motion_type == MotionType.FLOAT:
            if not red_attrs.prefloat_motion_type:
                # Try to infer from blue attributes
                if blue_attrs.motion_type in [MotionType.PRO, MotionType.ANTI]:
                    red_attrs = self.apply_prefloat_transformations(
                        red_attrs, blue_attrs
                    )

        return replace(
            pictograph_data, blue_attributes=blue_attrs, red_attributes=red_attrs
        )

    def get_attribute_summary(
        self, pictograph_data: "PictographData"
    ) -> dict[str, any]:
        """
        Get summary of motion attributes for debugging.

        Provides detailed breakdown of all motion attributes.
        """
        return {
            "beat": pictograph_data.beat,
            "letter": str(pictograph_data.letter) if pictograph_data.letter else None,
            "blue": {
                "motion_type": pictograph_data.blue_attributes.motion_type.value,
                "start_ori": pictograph_data.blue_attributes.start_ori.value,
                "end_ori": pictograph_data.blue_attributes.end_ori.value,
                "start_loc": pictograph_data.blue_attributes.start_loc.value,
                "end_loc": pictograph_data.blue_attributes.end_loc.value,
                "prop_rot_dir": pictograph_data.blue_attributes.prop_rot_dir.value,
                "turns": pictograph_data.blue_attributes.turns,
                "prefloat_motion_type": (
                    pictograph_data.blue_attributes.prefloat_motion_type.value
                    if pictograph_data.blue_attributes.prefloat_motion_type
                    else None
                ),
                "prefloat_prop_rot_dir": (
                    pictograph_data.blue_attributes.prefloat_prop_rot_dir.value
                    if pictograph_data.blue_attributes.prefloat_prop_rot_dir
                    else None
                ),
                "is_float": pictograph_data.blue_attributes.is_float,
                "is_shift": pictograph_data.blue_attributes.is_shift,
            },
            "red": {
                "motion_type": pictograph_data.red_attributes.motion_type.value,
                "start_ori": pictograph_data.red_attributes.start_ori.value,
                "end_ori": pictograph_data.red_attributes.end_ori.value,
                "start_loc": pictograph_data.red_attributes.start_loc.value,
                "end_loc": pictograph_data.red_attributes.end_loc.value,
                "prop_rot_dir": pictograph_data.red_attributes.prop_rot_dir.value,
                "turns": pictograph_data.red_attributes.turns,
                "prefloat_motion_type": (
                    pictograph_data.red_attributes.prefloat_motion_type.value
                    if pictograph_data.red_attributes.prefloat_motion_type
                    else None
                ),
                "prefloat_prop_rot_dir": (
                    pictograph_data.red_attributes.prefloat_prop_rot_dir.value
                    if pictograph_data.red_attributes.prefloat_prop_rot_dir
                    else None
                ),
                "is_float": pictograph_data.red_attributes.is_float,
                "is_shift": pictograph_data.red_attributes.is_shift,
            },
            "motion_patterns": {
                "is_static_motion": pictograph_data.is_static_motion,
                "has_float_motion": pictograph_data.has_float_motion,
                "is_dual_float": pictograph_data.is_dual_float,
                "is_shift_float_hybrid": pictograph_data.is_shift_float_hybrid,
            },
        }
