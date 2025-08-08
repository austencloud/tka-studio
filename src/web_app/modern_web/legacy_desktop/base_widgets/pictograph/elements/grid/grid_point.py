from __future__ import annotations
from typing import Optional,Optional

from PyQt6.QtCore import QPointF


class GridPoint:
    def __init__(self, name: str, coordinates: QPointF | None) -> None:
        self.name = name
        self.coordinates = coordinates
