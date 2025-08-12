from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any
import uuid

from desktop.modern.domain.models.enums import Orientation, PropType, RotationDirection


@dataclass(frozen=True)
class PropData:
    """
    Immutable data for a prop in a pictograph.

    REPLACES: objects.prop.prop.Prop (with UI coupling)
    """

    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prop_type: PropType = PropType.STAFF

    # Visual properties
    color: str = "blue"
    orientation: Orientation = Orientation.IN
    rotation_direction: RotationDirection = RotationDirection.NO_ROTATION

    # Position data (calculated by positioning system)
    location: str | None = None
    position_x: float = 0.0
    position_y: float = 0.0

    # State flags
    is_visible: bool = True
    is_selected: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        # Handle both enum and string values for prop_type
        prop_type_value = (
            self.prop_type.value if hasattr(self.prop_type, "value") else self.prop_type
        )

        return {
            "id": self.id,
            "prop_type": prop_type_value,
            "color": self.color,
            "orientation": self.orientation,
            "rotation_direction": self.rotation_direction,
            "location": self.location,
            "position_x": self.position_x,
            "position_y": self.position_y,
            "is_visible": self.is_visible,
            "is_selected": self.is_selected,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PropData:
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            prop_type=PropType(data.get("prop_type", "staff")),
            color=data.get("color", "blue"),
            orientation=data.get("orientation", "in"),
            rotation_direction=data.get("rotation_direction", "cw"),
            location=data.get("location"),
            position_x=data.get("position_x", 0.0),
            position_y=data.get("position_y", 0.0),
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
    def from_json(cls, json_str: str, camel_case: bool = True) -> PropData:
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json

        if camel_case:
            return domain_model_from_json(json_str, cls)
        data = json.loads(json_str)
        return cls.from_dict(data)
