from __future__ import annotations
from typing import Union,Optional
from dataclasses import dataclass
from typing import Optional,Optional

from objects.motion.prefloat_state_updater import PrefloatStateUpdater

from data.constants import ANTI, FLOAT, PREFLOAT_MOTION_TYPE, PREFLOAT_PROP_ROT_DIR, PRO


@dataclass
class MotionState:
    color: str | None = None
    motion_type: str | None = None
    turns: int | float | str = 0
    start_loc: str | None = None
    end_loc: str | None = None
    start_ori: str | None = None
    end_ori: str | None = None
    prop_rot_dir: str | None = None
    lead_state: str | None = None
    prefloat_motion_type: str | None = None
    prefloat_prop_rot_dir: str | None = None

    def __post_init__(self):
        self.prefloat_handler = PrefloatStateUpdater(self)

    def update_motion_state(self, motion_data: dict) -> None:
        SHIFT_MOTIONS = [PRO, ANTI, FLOAT]

        for key, value in motion_data.items():
            if value is not None:
                if key in [PREFLOAT_MOTION_TYPE, PREFLOAT_PROP_ROT_DIR]:
                    if self.motion_type in SHIFT_MOTIONS:
                        setattr(self, key, value)
                else:
                    if hasattr(self, key):
                        setattr(self, key, value)

        self.prefloat_handler.update_prefloat_state(motion_data)
