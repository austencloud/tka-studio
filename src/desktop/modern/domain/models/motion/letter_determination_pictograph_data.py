"""
Extended Pictograph Data for Letter Determination

Extends the existing PictographData model with letter determination
functionality without modifying the core domain model.
"""

from __future__ import annotations

from dataclasses import dataclass

from desktop.modern.domain.models.enums import Direction, GridPosition, Letter, Timing
from desktop.modern.domain.models.pictograph_data import PictographData

from .extended_motion_data import ExtendedMotionData


@dataclass(frozen=True)
class LetterDeterminationPictographData:
    """
    Extended PictographData wrapper for letter determination.

    Provides letter determination specific functionality while
    maintaining compatibility with the existing PictographData model.
    """

    # Core pictograph data
    pictograph_data: PictographData

    # Letter determination specific fields
    beat: int = 0
    letter: Letter | None = None
    timing: Timing | None = None
    direction: Direction | None = None
    duration: int | None = None
    letter_type: str | None = None

    @property
    def blue_motion(self) -> ExtendedMotionData:
        """Get blue motion as ExtendedMotionData."""
        blue_motion_data = self.pictograph_data.motions.get("blue")
        if blue_motion_data:
            return ExtendedMotionData.from_motion_data(blue_motion_data)
        return None

    @property
    def red_motion(self) -> ExtendedMotionData:
        """Get red motion as ExtendedMotionData."""
        red_motion_data = self.pictograph_data.motions.get("red")
        if red_motion_data:
            return ExtendedMotionData.from_motion_data(red_motion_data)
        return None

    @property
    def start_pos(self) -> GridPosition | None:
        """Get start position."""
        return self.pictograph_data.start_position

    @property
    def end_pos(self) -> GridPosition | None:
        """Get end position."""
        return self.pictograph_data.end_position

    @property
    def is_start_position(self) -> bool:
        """Check if this is a start position entry (α position)."""
        return self.letter is None or (
            self.letter and str(self.letter.value).startswith("α")
        )

    @property
    def is_static_motion(self) -> bool:
        """Check if both motions are static."""
        return self.blue_motion.is_static and self.red_motion.is_static

    @property
    def has_float_motion(self) -> bool:
        """Check if either motion is in float state."""
        return self.blue_motion.is_float or self.red_motion.is_float

    @property
    def is_dual_float(self) -> bool:
        """Check if both motions are in float state."""
        return self.blue_motion.is_float and self.red_motion.is_float

    @property
    def is_shift_float_hybrid(self) -> bool:
        """Check if this is a shift-float hybrid motion."""
        blue_is_float = self.blue_motion.is_float
        red_is_float = self.red_motion.is_float
        blue_is_shift = self.blue_motion.is_shift
        red_is_shift = self.red_motion.is_shift

        return (blue_is_float and red_is_shift) or (red_is_float and blue_is_shift)

    def get_float_motion(self) -> ExtendedMotionData | None:
        """Get the float motion if present."""
        if self.blue_motion.is_float:
            return self.blue_motion
        if self.red_motion.is_float:
            return self.red_motion
        return None

    def get_shift_motion(self) -> ExtendedMotionData | None:
        """Get the shift motion if present."""
        if self.blue_motion.is_shift:
            return self.blue_motion
        if self.red_motion.is_shift:
            return self.red_motion
        return None

    def with_beat_number(self, beat: int) -> LetterDeterminationPictographData:
        """Create new instance with different beat number."""
        from dataclasses import replace

        return replace(self, beat=beat)

    def with_letter(self, letter: Letter) -> LetterDeterminationPictographData:
        """Create new instance with different letter."""
        from dataclasses import replace

        return replace(self, letter=letter)

    def with_orientations(
        self,
        blue_start_ori=None,
        blue_end_ori=None,
        red_start_ori=None,
        red_end_ori=None,
    ) -> LetterDeterminationPictographData:
        """Create new instance with updated orientations."""
        from dataclasses import replace

        # Update blue motion if needed
        new_blue_motion = self.blue_motion
        if blue_start_ori is not None or blue_end_ori is not None:
            new_blue_motion = new_blue_motion.update(
                start_ori=blue_start_ori or new_blue_motion.start_ori,
                end_ori=blue_end_ori or new_blue_motion.end_ori,
            )

        # Update red motion if needed
        new_red_motion = self.red_motion
        if red_start_ori is not None or red_end_ori is not None:
            new_red_motion = new_red_motion.update(
                start_ori=red_start_ori or new_red_motion.start_ori,
                end_ori=red_end_ori or new_red_motion.end_ori,
            )

        # Update pictograph data with new motions
        new_pictograph_data = self.pictograph_data.update(
            motions={
                "blue": new_blue_motion.to_motion_data(),
                "red": new_red_motion.to_motion_data(),
            }
        )

        return replace(self, pictograph_data=new_pictograph_data)

    def with_turns(
        self, blue_turns=None, red_turns=None
    ) -> LetterDeterminationPictographData:
        """Create new instance with different turns."""
        from dataclasses import replace

        new_blue_motion = self.blue_motion
        new_red_motion = self.red_motion

        if blue_turns is not None:
            new_blue_motion = new_blue_motion.update(turns=blue_turns)

        if red_turns is not None:
            new_red_motion = new_red_motion.update(turns=red_turns)

        # Update pictograph data with new motions
        new_pictograph_data = self.pictograph_data.update(
            motions={
                "blue": new_blue_motion.to_motion_data(),
                "red": new_red_motion.to_motion_data(),
            }
        )

        return replace(self, pictograph_data=new_pictograph_data)

    def with_prefloat_attributes(
        self, color: str, motion_type, prop_rot_dir
    ) -> LetterDeterminationPictographData:
        """Create new instance with prefloat attributes."""
        from dataclasses import replace

        if color == "blue":
            new_blue_motion = self.blue_motion.with_prefloat_attributes(
                motion_type, prop_rot_dir
            )
            new_pictograph_data = self.pictograph_data.update(
                motions={
                    "blue": new_blue_motion.to_motion_data(),
                    "red": self.red_motion.to_motion_data(),
                }
            )
        else:  # red
            new_red_motion = self.red_motion.with_prefloat_attributes(
                motion_type, prop_rot_dir
            )
            new_pictograph_data = self.pictograph_data.update(
                motions={
                    "blue": self.blue_motion.to_motion_data(),
                    "red": new_red_motion.to_motion_data(),
                }
            )

        return replace(self, pictograph_data=new_pictograph_data)

    def to_legacy_dict(self) -> dict:
        """Convert to legacy dictionary format for compatibility."""
        return {
            "beat": self.beat,
            "letter": str(self.letter.value) if self.letter else "",
            "start_pos": str(self.start_pos.value) if self.start_pos else "",
            "end_pos": str(self.end_pos.value) if self.end_pos else "",
            "timing": str(self.timing.value) if self.timing else "",
            "direction": str(self.direction.value) if self.direction else "",
            "blue_attributes": self._motion_to_legacy_dict(self.blue_motion),
            "red_attributes": self._motion_to_legacy_dict(self.red_motion),
            "duration": self.duration,
            "letter_type": self.letter_type,
        }

    def _motion_to_legacy_dict(self, motion: ExtendedMotionData) -> dict:
        """Convert ExtendedMotionData to legacy dict format."""
        result = {
            "motion_type": str(motion.motion_type.value),
            "start_ori": str(motion.start_ori.value),
            "end_ori": str(motion.end_ori.value),
            "start_loc": str(motion.start_loc.value),
            "end_loc": str(motion.end_loc.value),
            "prop_rot_dir": str(motion.prop_rot_dir.value),
            "turns": motion.turns,
        }

        if motion.prefloat_motion_type:
            result["prefloat_motion_type"] = str(motion.prefloat_motion_type.value)

        if motion.prefloat_prop_rot_dir:
            result["prefloat_prop_rot_dir"] = str(motion.prefloat_prop_rot_dir.value)

        return result

    @classmethod
    def from_legacy_dict(cls, data: dict) -> LetterDeterminationPictographData:
        """Create from legacy dictionary format."""
        from desktop.modern.domain.models.enums import MotionType, RotationDirection
        from desktop.modern.domain.models.motion_data import MotionData

        # Convert motion attributes
        def dict_to_extended_motion(attr_dict: dict) -> ExtendedMotionData:
            base_motion = MotionData.from_dict(attr_dict)

            prefloat_motion_type = None
            if attr_dict.get("prefloat_motion_type"):
                prefloat_motion_type = MotionType(attr_dict["prefloat_motion_type"])

            prefloat_prop_rot_dir = None
            if attr_dict.get("prefloat_prop_rot_dir"):
                prefloat_prop_rot_dir = RotationDirection(
                    attr_dict["prefloat_prop_rot_dir"]
                )

            return ExtendedMotionData.from_motion_data(
                base_motion,
                prefloat_motion_type=prefloat_motion_type,
                prefloat_prop_rot_dir=prefloat_prop_rot_dir,
            )

        blue_motion = dict_to_extended_motion(data["blue_attributes"])
        red_motion = dict_to_extended_motion(data["red_attributes"])

        # Create PictographData
        pictograph_data = PictographData(
            motions={
                "blue": blue_motion.to_motion_data(),
                "red": red_motion.to_motion_data(),
            },
            start_position=GridPosition(data["start_pos"])
            if data.get("start_pos")
            else None,
            end_position=GridPosition(data["end_pos"]) if data.get("end_pos") else None,
            letter=data.get("letter"),
        )

        return cls(
            pictograph_data=pictograph_data,
            beat=data.get("beat", 0),
            letter=Letter(data["letter"]) if data.get("letter") else None,
            timing=Timing(data["timing"]) if data.get("timing") else None,
            direction=Direction(data["direction"]) if data.get("direction") else None,
            duration=data.get("duration"),
            letter_type=data.get("letter_type"),
        )

    @classmethod
    def from_pictograph_data(
        cls, pictograph_data: PictographData, **kwargs
    ) -> LetterDeterminationPictographData:
        """Create from existing PictographData."""
        return cls(pictograph_data=pictograph_data, **kwargs)
