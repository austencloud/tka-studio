"""
Pictograph Domain Models for Kinetic Constructor

These models represent the pure business logic for pictograph rendering and positioning.
They integrate with the existing modern architecture and eliminate UI coupling from the
original pictograph implementation.

REPLACES:
- base_widgets.pictograph.pictograph.Pictograph (QGraphicsScene)
- base_widgets.pictograph.elements.pictograph_elements.PictographElements
- base_widgets.pictograph.state.pictograph_state.PictographState
- Complex UI-coupled pictograph classes

PROVIDES:
- Immutable pictograph data structures
- Pure business logic for arrow and prop positioning
- Clean separation between data and rendering
- Easy testing and serialization
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any
import uuid

from desktop.modern.domain.models.enums import ArrowType


@dataclass(frozen=True)
class ArrowData:
    """
    Immutable data for an arrow in a pictograph.

    REPLACES: objects.arrow.arrow.Arrow (with UI coupling)
    """

    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    arrow_type: ArrowType = ArrowType.BLUE

    # Visual properties
    color: str = "blue"
    turns: float = 0.0
    is_mirrored: bool = False

    # Position data (calculated by positioning system)
    location: str | None = None
    position_x: float = 0.0
    position_y: float = 0.0
    rotation_angle: float = 0.0

    # State flags
    is_visible: bool = True
    is_selected: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        # Handle both enum and string values for arrow_type
        arrow_type_value = (
            self.arrow_type.value
            if hasattr(self.arrow_type, "value")
            else self.arrow_type
        )

        # Note: motion_data is deprecated - motion data now lives in PictographData.motions
        return {
            "id": self.id,
            "arrow_type": arrow_type_value,
            "color": self.color,
            "turns": self.turns,
            "is_mirrored": self.is_mirrored,
            "location": self.location,
            "position_x": self.position_x,
            "position_y": self.position_y,
            "rotation_angle": self.rotation_angle,
            "is_visible": self.is_visible,
            "is_selected": self.is_selected,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ArrowData:
        """Create from dictionary."""
        # Note: motion_data is deprecated - motion data now lives in PictographData.motions

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            arrow_type=ArrowType(data.get("arrow_type", "blue")),
            color=data.get("color", "blue"),
            turns=data.get("turns", 0.0),
            is_mirrored=data.get("is_mirrored", False),
            location=data.get("location"),
            position_x=data.get("position_x", 0.0),
            position_y=data.get("position_y", 0.0),
            rotation_angle=data.get("rotation_angle", 0.0),
            is_visible=data.get("is_visible", True),
            is_selected=data.get("is_selected", False),
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
    def from_json(cls, json_str: str, camel_case: bool = True) -> ArrowData:
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json

        if camel_case:
            return domain_model_from_json(json_str, cls)
        data = json.loads(json_str)
        return cls.from_dict(data)
