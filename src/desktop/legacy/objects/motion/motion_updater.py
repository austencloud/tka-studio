from __future__ import annotations

from typing import TYPE_CHECKING

from data.constants import COLOR, END_ORI, LOC, ORI

if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionUpdater:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion

    def update_motion(self, motion_data: dict = None) -> None:
        if motion_data:
            self.motion.state.update_motion_state(motion_data)
        self.motion.arrow.setup_components()
        self.update_end_ori()
        prop_data = {
            COLOR: self.motion.state.color,
            LOC: self.motion.state.end_loc,
            ORI: self.motion.state.end_ori,
        }
        self.motion.prop.updater.update_prop(prop_data)

    def update_end_ori(self) -> None:
        # Check if motion type is set before trying to calculate end orientation
        if self.motion.state.motion_type is None:
            print(
                f"DEBUG: Skipping end_ori calculation for {self.motion.state.color} motion - motion_type not set yet"
            )
            return

        self.motion.state.end_ori = self.motion.ori_calculator.get_end_ori()
        self.motion.pictograph.state.pictograph_data[
            f"{self.motion.state.color}_attributes"
        ][END_ORI] = self.motion.state.end_ori
