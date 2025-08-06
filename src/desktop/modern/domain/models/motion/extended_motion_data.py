"""
Extended Motion Data for Letter Determination

Extends the existing MotionData model with prefloat attributes needed
for letter determination without modifying the core domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from desktop.modern.domain.models.enums import MotionType, RotationDirection
from desktop.modern.domain.models.motion_data import MotionData


@dataclass(frozen=True)
class ExtendedMotionData(MotionData):
    """
    Extended MotionData with prefloat attributes for letter determination.

    Extends the existing MotionData model to include prefloat state
    information needed for complex letter determination logic.
    """

    # Prefloat attributes for handling float state transitions
    prefloat_motion_type: Optional[MotionType] = None
    prefloat_prop_rot_dir: Optional[RotationDirection] = None

    @property
    def is_float(self) -> bool:
        """Check if this motion is in a float state."""
        return self.motion_type == MotionType.FLOAT

    @property
    def is_shift(self) -> bool:
        """Check if this motion is a shift (pro or anti)."""
        return self.motion_type in [MotionType.PRO, MotionType.ANTI]

    @property
    def effective_motion_type(self) -> MotionType:
        """Get the effective motion type, considering prefloat states."""
        if self.is_float and self.prefloat_motion_type:
            return self.prefloat_motion_type
        return self.motion_type

    @property
    def effective_prop_rot_dir(self) -> RotationDirection:
        """Get the effective prop rotation direction, considering prefloat states."""
        if self.is_float and self.prefloat_prop_rot_dir:
            return self.prefloat_prop_rot_dir
        return self.prop_rot_dir

    def to_float_state(
        self, prefloat_motion_type: MotionType, prefloat_prop_rot_dir: RotationDirection
    ) -> ExtendedMotionData:
        """Convert this motion to float state with prefloat attributes."""
        from dataclasses import replace

        return replace(
            self,
            motion_type=MotionType.FLOAT,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            turns="fl",
            prefloat_motion_type=prefloat_motion_type,
            prefloat_prop_rot_dir=prefloat_prop_rot_dir,
        )

    def with_prefloat_attributes(
        self, motion_type: MotionType, prop_rot_dir: RotationDirection
    ) -> ExtendedMotionData:
        """Create new instance with prefloat attributes."""
        from dataclasses import replace

        return replace(
            self, prefloat_motion_type=motion_type, prefloat_prop_rot_dir=prop_rot_dir
        )

    @classmethod
    def from_motion_data(
        cls,
        motion_data: MotionData,
        prefloat_motion_type: Optional[MotionType] = None,
        prefloat_prop_rot_dir: Optional[RotationDirection] = None,
    ) -> ExtendedMotionData:
        """Create ExtendedMotionData from existing MotionData."""
        return cls(
            motion_type=motion_data.motion_type,
            prop_rot_dir=motion_data.prop_rot_dir,
            start_loc=motion_data.start_loc,
            end_loc=motion_data.end_loc,
            turns=motion_data.turns,
            start_ori=motion_data.start_ori,
            end_ori=motion_data.end_ori,
            is_visible=motion_data.is_visible,
            prefloat_motion_type=prefloat_motion_type,
            prefloat_prop_rot_dir=prefloat_prop_rot_dir,
        )

    def to_motion_data(self) -> MotionData:
        """Convert back to base MotionData (strips prefloat attributes)."""
        return MotionData(
            motion_type=self.motion_type,
            prop_rot_dir=self.prop_rot_dir,
            start_loc=self.start_loc,
            end_loc=self.end_loc,
            turns=self.turns,
            start_ori=self.start_ori,
            end_ori=self.end_ori,
            is_visible=self.is_visible,
        )

    def to_dict(self) -> dict:
        """Convert to dictionary including prefloat attributes."""
        base_dict = super().to_dict()
        base_dict.update(
            {
                "prefloat_motion_type": self.prefloat_motion_type.value
                if self.prefloat_motion_type
                else None,
                "prefloat_prop_rot_dir": self.prefloat_prop_rot_dir.value
                if self.prefloat_prop_rot_dir
                else None,
            }
        )
        return base_dict

    @classmethod
    def from_dict(cls, data: dict) -> ExtendedMotionData:
        """Create from dictionary including prefloat attributes."""
        prefloat_motion_type = None
        if data.get("prefloat_motion_type"):
            prefloat_motion_type = MotionType(data["prefloat_motion_type"])

        prefloat_prop_rot_dir = None
        if data.get("prefloat_prop_rot_dir"):
            prefloat_prop_rot_dir = RotationDirection(data["prefloat_prop_rot_dir"])

        # Create base MotionData first
        base_data = {
            k: v
            for k, v in data.items()
            if k not in ["prefloat_motion_type", "prefloat_prop_rot_dir"]
        }
        base_motion = MotionData.from_dict(base_data)

        return cls.from_motion_data(
            base_motion,
            prefloat_motion_type=prefloat_motion_type,
            prefloat_prop_rot_dir=prefloat_prop_rot_dir,
        )
