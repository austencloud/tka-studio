from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any
import uuid

from desktop.modern.domain.models.arrow_data import ArrowData
from desktop.modern.domain.models.enums import (
    ArrowType,
    Direction,
    GridPosition,
    LetterType,
    Timing,
)
from desktop.modern.domain.models.grid_data import GridData
from desktop.modern.domain.models.prop_data import PropData

from .motion_data import MotionData


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

    # Arrows, props, and motions (consistent dictionary approach)
    arrows: dict[str, ArrowData] = field(default_factory=dict)  # "blue", "red"
    props: dict[str, PropData] = field(default_factory=dict)  # "blue", "red"
    motions: dict[str, MotionData] = field(default_factory=dict)  # "blue", "red"

    # Letter and position data
    letter: str | None = None
    start_position: GridPosition | None = None
    end_position: GridPosition | None = None

    # Letter determination fields
    beat: int = 0
    timing: Timing | None = None  # Timing.SPLIT or Timing.TOG
    direction: Direction | None = None  # Direction.SAME or Direction.OPP
    duration: int | None = None
    letter_type: LetterType | None = None

    # Visual state
    is_blank: bool = False
    is_mirrored: bool = False

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)

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

    def update_arrow(self, color: str, **kwargs) -> PictographData:
        """Create a new pictograph with an updated arrow."""
        if color not in self.arrows:
            raise ValueError(f"Arrow color '{color}' not found")

        current_arrow = self.arrows[color]
        # Use from_dict to properly handle motion_data conversion
        updated_arrow = ArrowData.from_dict({**current_arrow.to_dict(), **kwargs})
        new_arrows = {**self.arrows, color: updated_arrow}

        from dataclasses import replace

        return replace(self, arrows=new_arrows)

    def update_prop(self, color: str, **kwargs) -> PictographData:
        """Create a new pictograph with an updated prop."""
        if color not in self.props:
            raise ValueError(f"Prop color '{color}' not found")

        current_prop = self.props[color]
        # Use from_dict to properly handle field updates
        updated_prop = PropData.from_dict({**current_prop.to_dict(), **kwargs})
        new_props = {**self.props, color: updated_prop}

        from dataclasses import replace

        return replace(self, props=new_props)

    def update(self, **kwargs) -> PictographData:
        """Create a new pictograph with updated fields."""
        from dataclasses import replace

        return replace(self, **kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "grid_data": self.grid_data.to_dict(),
            "arrows": {k: v.to_dict() for k, v in self.arrows.items()},
            "props": {k: v.to_dict() for k, v in self.props.items()},
            "motions": {k: v.to_dict() for k, v in self.motions.items()},
            "letter": self.letter,
            "letter_type": self.letter_type.value if self.letter_type else None,
            "start_position": self.start_position.value
            if self.start_position
            else None,
            "end_position": self.end_position.value if self.end_position else None,
            "is_blank": self.is_blank,
            "is_mirrored": self.is_mirrored,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PictographData:
        """Create from dictionary."""
        grid_data = GridData.from_dict(data.get("grid_data", {}))

        arrows = {}
        for color, arrow_data in data.get("arrows", {}).items():
            arrows[color] = ArrowData.from_dict(arrow_data)

        props = {}
        for color, prop_data in data.get("props", {}).items():
            props[color] = PropData.from_dict(prop_data)

        motions = {}
        for color, motion_data in data.get("motions", {}).items():
            motions[color] = MotionData.from_dict(motion_data)

        # Convert position strings back to enum objects
        start_position = None
        if data.get("start_position"):
            try:
                start_position = GridPosition(data["start_position"])
            except ValueError:
                # If conversion fails, keep as None
                pass

        end_position = None
        if data.get("end_position"):
            try:
                end_position = GridPosition(data["end_position"])
            except ValueError:
                # If conversion fails, keep as None
                pass

        # Handle letter_type conversion
        letter_type = data.get("letter_type")
        if letter_type and hasattr(letter_type, "value"):
            # Already a LetterType enum
            pass
        elif letter_type:
            # Try to convert string to LetterType enum
            try:
                from .enums import LetterType

                if isinstance(letter_type, str):
                    letter_type = getattr(LetterType, letter_type.upper(), None)
            except (AttributeError, ImportError):
                letter_type = None

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            grid_data=grid_data,
            arrows=arrows,
            props=props,
            motions=motions,
            letter=data.get("letter"),
            letter_type=letter_type,
            start_position=start_position,
            end_position=end_position,
            is_blank=data.get("is_blank", False),
            is_mirrored=data.get("is_mirrored", False),
            metadata=data.get("metadata", {}),
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
    def from_json(cls, json_str: str, camel_case: bool = True) -> PictographData:
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json

        if camel_case:
            return domain_model_from_json(json_str, cls)
        data = json.loads(json_str)
        return cls.from_dict(data)
