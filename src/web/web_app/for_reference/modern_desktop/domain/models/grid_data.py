from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any

from desktop.modern.domain.models.enums import GridMode


@dataclass(frozen=True)
class GridData:
    """
    Immutable data for the pictograph grid system.

    REPLACES: base_widgets.pictograph.elements.grid.grid_data.GridData
    """

    # Grid configuration
    grid_mode: GridMode = GridMode.DIAMOND
    center_x: float = 0.0
    center_y: float = 0.0
    radius: float = 100.0

    # Grid points (calculated positions)
    grid_points: dict[str, tuple[float, float]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "grid_mode": self.grid_mode.value,
            "center_x": self.center_x,
            "center_y": self.center_y,
            "radius": self.radius,
            "grid_points": self.grid_points,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GridData:
        """Create from dictionary."""
        return cls(
            grid_mode=GridMode(data.get("grid_mode", "diamond")),
            center_x=data.get("center_x", 0.0),
            center_y=data.get("center_y", 0.0),
            radius=data.get("radius", 100.0),
            grid_points=data.get("grid_points", {}),
        )

    def to_camel_dict(self) -> dict[str, Any]:
        """Convert to dictionary with camelCase keys for JSON APIs."""
        from ..serialization import dataclass_to_camel_dict

        return dataclass_to_camel_dict(self)

    def to_json(self, camel_case: bool = True, **kwargs) -> str:
        """Serialize to JSON string."""
        from ..serialization import domain_model_to_json

        if camel_case:
            return domain_model_to_json(self, **kwargs)
        return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_json(cls, json_str: str, camel_case: bool = True) -> GridData:
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json

        if camel_case:
            return domain_model_from_json(json_str, cls)
        data = json.loads(json_str)
        return cls.from_dict(data)
