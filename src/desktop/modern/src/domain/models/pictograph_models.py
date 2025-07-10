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

import json
import uuid
from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
from typing import Any, Dict, Optional, Tuple, Union

from domain.models.enums import ArrowType, GridMode, PropType
from domain.models.glyph_models import GlyphData

from .motion_models import MotionData


def _process_field_value(value: Any, field_type: Any) -> Any:
    """Process field value based on type for deserialization."""
    # Handle Optional types
    if hasattr(field_type, "__origin__") and field_type.__origin__ is Union:
        args = field_type.__args__
        if len(args) == 2 and type(None) in args:
            actual_type = args[0] if args[1] is type(None) else args[1]
            if value is None:
                return None
            return _process_field_value(value, actual_type)

    # Handle dataclasses
    if is_dataclass(field_type) and isinstance(value, dict):
        return field_type.from_dict(value)

    # Handle enums
    if isinstance(field_type, type) and issubclass(field_type, Enum):
        return field_type(value)

    # Handle lists
    if hasattr(field_type, "__origin__") and field_type.__origin__ is list:
        if isinstance(value, list):
            list_type = field_type.__args__[0]
            return [_process_field_value(item, list_type) for item in value]

    return value


@dataclass(frozen=True)
class ArrowData:
    """
    Immutable data for an arrow in a pictograph.

    REPLACES: objects.arrow.arrow.Arrow (with UI coupling)
    """

    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    arrow_type: ArrowType = ArrowType.BLUE

    # Motion reference
    motion_data: Optional[MotionData] = None

    # Visual properties
    color: str = "blue"
    turns: float = 0.0
    is_mirrored: bool = False

    # Position data (calculated by positioning system)
    location: Optional[str] = None
    position_x: float = 0.0
    position_y: float = 0.0
    rotation_angle: float = 0.0

    # State flags
    is_visible: bool = True
    is_selected: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        # Handle both enum and string values for arrow_type
        arrow_type_value = (
            self.arrow_type.value
            if hasattr(self.arrow_type, "value")
            else self.arrow_type
        )

        # Handle motion_data being either MotionData object or dict
        motion_data_value = None
        if self.motion_data:
            if hasattr(self.motion_data, "to_dict"):
                motion_data_value = self.motion_data.to_dict()
            else:
                motion_data_value = self.motion_data  # Already a dict

        return {
            "id": self.id,
            "arrow_type": arrow_type_value,
            "motion_data": motion_data_value,
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
    def from_dict(cls, data: Dict[str, Any]) -> "ArrowData":
        """Create from dictionary."""
        motion_data = None
        if data.get("motion_data"):
            motion_data = MotionData.from_dict(data["motion_data"])

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            arrow_type=ArrowType(data.get("arrow_type", "blue")),
            motion_data=motion_data,
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

    def to_camel_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with camelCase keys for JSON APIs."""
        from ..serialization import dataclass_to_camel_dict

        return dataclass_to_camel_dict(self)

    def to_json(self, camel_case: bool = True, **kwargs) -> str:
        """Serialize to JSON string."""
        from ..serialization import domain_model_to_json

        if camel_case:
            return domain_model_to_json(self, **kwargs)
        else:
            return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_json(cls, json_str: str, camel_case: bool = True) -> "ArrowData":
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json

        if camel_case:
            return domain_model_from_json(json_str, cls)
        else:
            data = json.loads(json_str)
            return cls.from_dict(data)


@dataclass(frozen=True)
class PropData:
    """
    Immutable data for a prop in a pictograph.

    REPLACES: objects.prop.prop.Prop (with UI coupling)
    """

    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prop_type: PropType = PropType.STAFF

    # Motion reference
    motion_data: Optional[MotionData] = None

    # Visual properties
    color: str = "blue"
    orientation: str = "in"
    rotation_direction: str = "cw"

    # Position data (calculated by positioning system)
    location: Optional[str] = None
    position_x: float = 0.0
    position_y: float = 0.0

    # State flags
    is_visible: bool = True
    is_selected: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        # Handle both enum and string values for prop_type
        prop_type_value = (
            self.prop_type.value if hasattr(self.prop_type, "value") else self.prop_type
        )

        # Handle motion_data being either MotionData object or dict
        motion_data_value = None
        if self.motion_data:
            if hasattr(self.motion_data, "to_dict"):
                motion_data_value = self.motion_data.to_dict()
            else:
                motion_data_value = self.motion_data  # Already a dict

        return {
            "id": self.id,
            "prop_type": prop_type_value,
            "motion_data": motion_data_value,
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
    def from_dict(cls, data: Dict[str, Any]) -> "PropData":
        """Create from dictionary."""
        motion_data = None
        if data.get("motion_data"):
            motion_data = MotionData.from_dict(data["motion_data"])

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            prop_type=PropType(data.get("prop_type", "staff")),
            motion_data=motion_data,
            color=data.get("color", "blue"),
            orientation=data.get("orientation", "in"),
            rotation_direction=data.get("rotation_direction", "cw"),
            location=data.get("location"),
            position_x=data.get("position_x", 0.0),
            position_y=data.get("position_y", 0.0),
            is_visible=data.get("is_visible", True),
            is_selected=data.get("is_selected", False),
        )

    def to_camel_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with camelCase keys for JSON APIs."""
        from ..serialization import dataclass_to_camel_dict

        return dataclass_to_camel_dict(self)

    def to_json(self, camel_case: bool = True, **kwargs) -> str:
        """Serialize to JSON string."""
        from ..serialization import domain_model_to_json

        if camel_case:
            return domain_model_to_json(self, **kwargs)
        else:
            return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_json(cls, json_str: str, camel_case: bool = True) -> "PropData":
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json

        if camel_case:
            return domain_model_from_json(json_str, cls)
        else:
            data = json.loads(json_str)
            return cls.from_dict(data)


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
    grid_points: Dict[str, Tuple[float, float]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "grid_mode": self.grid_mode.value,
            "center_x": self.center_x,
            "center_y": self.center_y,
            "radius": self.radius,
            "grid_points": self.grid_points,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GridData":
        """Create from dictionary."""
        return cls(
            grid_mode=GridMode(data.get("grid_mode", "diamond")),
            center_x=data.get("center_x", 0.0),
            center_y=data.get("center_y", 0.0),
            radius=data.get("radius", 100.0),
            grid_points=data.get("grid_points", {}),
        )

    def to_camel_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with camelCase keys for JSON APIs."""
        from ..serialization import dataclass_to_camel_dict

        return dataclass_to_camel_dict(self)

    def to_json(self, camel_case: bool = True, **kwargs) -> str:
        """Serialize to JSON string."""
        from ..serialization import domain_model_to_json

        if camel_case:
            return domain_model_to_json(self, **kwargs)
        else:
            return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_json(cls, json_str: str, camel_case: bool = True) -> "GridData":
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json

        if camel_case:
            return domain_model_from_json(json_str, cls)
        else:
            data = json.loads(json_str)
            return cls.from_dict(data)


@dataclass(frozen=True)
class PictographData:
    """
    Immutable data for a complete pictograph.

    REPLACES: base_widgets.pictograph.pictograph.Pictograph (QGraphicsScene)

    This is the main pictograph model that contains all the data needed
    to render a pictograph without any UI coupling.
    """

    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # Grid configuration
    grid_data: GridData = field(default_factory=GridData)

    # Arrows and props
    arrows: Dict[str, ArrowData] = field(default_factory=dict)  # "blue", "red"
    props: Dict[str, PropData] = field(default_factory=dict)  # "blue", "red"

    # Letter and position data
    letter: Optional[str] = None
    start_position: Optional[str] = None
    end_position: Optional[str] = None

    # Glyph data for notation rendering
    glyph_data: Optional[GlyphData] = None

    # Visual state
    is_blank: bool = False
    is_mirrored: bool = False

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate pictograph data."""
        # Ensure we have blue and red entries
        if "blue" not in self.arrows:
            object.__setattr__(
                self,
                "arrows",
                {
                    **self.arrows,
                    "blue": ArrowData(arrow_type=ArrowType.BLUE, color="blue"),
                },
            )
        if "red" not in self.arrows:
            object.__setattr__(
                self,
                "arrows",
                {
                    **self.arrows,
                    "red": ArrowData(arrow_type=ArrowType.RED, color="red"),
                },
            )

        if "blue" not in self.props:
            object.__setattr__(
                self, "props", {**self.props, "blue": PropData(color="blue")}
            )
        if "red" not in self.props:
            object.__setattr__(
                self, "props", {**self.props, "red": PropData(color="red")}
            )

    @property
    def blue_arrow(self) -> ArrowData:
        """Get the blue arrow."""
        return self.arrows.get(
            "blue", ArrowData(arrow_type=ArrowType.BLUE, color="blue")
        )

    @property
    def red_arrow(self) -> ArrowData:
        """Get the red arrow."""
        return self.arrows.get("red", ArrowData(arrow_type=ArrowType.RED, color="red"))

    @property
    def blue_prop(self) -> PropData:
        """Get the blue prop."""
        return self.props.get("blue", PropData(color="blue"))

    @property
    def red_prop(self) -> PropData:
        """Get the red prop."""
        return self.props.get("red", PropData(color="red"))

    def update_arrow(self, color: str, **kwargs) -> "PictographData":
        """Create a new pictograph with an updated arrow."""
        if color not in self.arrows:
            raise ValueError(f"Arrow color '{color}' not found")

        current_arrow = self.arrows[color]
        # Use from_dict to properly handle motion_data conversion
        updated_arrow = ArrowData.from_dict({**current_arrow.to_dict(), **kwargs})
        new_arrows = {**self.arrows, color: updated_arrow}

        from dataclasses import replace

        return replace(self, arrows=new_arrows)

    def update_prop(self, color: str, **kwargs) -> "PictographData":
        """Create a new pictograph with an updated prop."""
        if color not in self.props:
            raise ValueError(f"Prop color '{color}' not found")

        current_prop = self.props[color]
        # Use from_dict to properly handle motion_data conversion
        updated_prop = PropData.from_dict({**current_prop.to_dict(), **kwargs})
        new_props = {**self.props, color: updated_prop}

        from dataclasses import replace

        return replace(self, props=new_props)

    def update(self, **kwargs) -> "PictographData":
        """Create a new pictograph with updated fields."""
        from dataclasses import replace

        return replace(self, **kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "grid_data": self.grid_data.to_dict(),
            "arrows": {k: v.to_dict() for k, v in self.arrows.items()},
            "props": {k: v.to_dict() for k, v in self.props.items()},
            "letter": self.letter,
            "start_position": self.start_position,
            "end_position": self.end_position,
            "is_blank": self.is_blank,
            "is_mirrored": self.is_mirrored,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PictographData":
        """Create from dictionary."""
        grid_data = GridData.from_dict(data.get("grid_data", {}))

        arrows = {}
        for color, arrow_data in data.get("arrows", {}).items():
            arrows[color] = ArrowData.from_dict(arrow_data)

        props = {}
        for color, prop_data in data.get("props", {}).items():
            props[color] = PropData.from_dict(prop_data)

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            grid_data=grid_data,
            arrows=arrows,
            props=props,
            letter=data.get("letter"),
            start_position=data.get("start_position"),
            end_position=data.get("end_position"),
            is_blank=data.get("is_blank", False),
            is_mirrored=data.get("is_mirrored", False),
            metadata=data.get("metadata", {}),
        )

    def to_camel_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with camelCase keys for JSON APIs."""
        from ..serialization import dataclass_to_camel_dict

        return dataclass_to_camel_dict(self)

    def to_json(self, camel_case: bool = True, **kwargs) -> str:
        """Serialize to JSON string."""
        from ..serialization import domain_model_to_json

        if camel_case:
            return domain_model_to_json(self, **kwargs)
        else:
            return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_json(cls, json_str: str, camel_case: bool = True) -> "PictographData":
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json

        if camel_case:
            return domain_model_from_json(json_str, cls)
        else:
            data = json.loads(json_str)
            return cls.from_dict(data)
