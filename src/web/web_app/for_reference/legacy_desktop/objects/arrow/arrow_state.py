from __future__ import annotations
from typing import Union,Optional
from dataclasses import dataclass
from typing import Optional,Optional


@dataclass
class ArrowState:
    color: str | None = None
    is_svg_mirrored: bool | None = None
    loc: str | None = None
    motion_type: str | None = None
    turns: int | float | None = None
    initialized: bool = False

    def update_from_dict(self, arrow_data: dict[str, str | int | float]) -> None:
        for key, value in arrow_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
