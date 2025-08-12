"""
Glyph Domain Models

Data structures for pictograph glyphs (elemental, VTG, TKA, position).
Handles glyph classification and visualization data.
"""

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union
from enum import Enum

from .enums import VTGMode, ElementalType, LetterType


def _process_field_value(value: Any, field_type: Any) -> Any:
    """Process field value based on type for deserialization."""
    # Handle Optional types
    if hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
        args = field_type.__args__
        if len(args) == 2 and type(None) in args:
            actual_type = args[0] if args[1] is type(None) else args[1]
            if value is None:
                return None
            return _process_field_value(value, actual_type)
    
    # Handle dataclasses
    from dataclasses import is_dataclass
    if is_dataclass(field_type) and isinstance(value, dict):
        return field_type.from_dict(value)
    
    # Handle enums
    if isinstance(field_type, type) and issubclass(field_type, Enum):
        return field_type(value)
    
    # Handle lists
    if hasattr(field_type, '__origin__') and field_type.__origin__ is list:
        if isinstance(value, list):
            list_type = field_type.__args__[0]
            return [_process_field_value(item, list_type) for item in value]
    
    return value


@dataclass(frozen=True)
class GlyphData:
    """
    Data for pictograph glyphs (elemental, VTG, TKA, position).
    """

    # VTG glyph data
    vtg_mode: Optional[VTGMode] = None

    # Elemental glyph data
    elemental_type: Optional[ElementalType] = None

    # TKA glyph data
    letter_type: Optional[LetterType] = None
    has_dash: bool = False
    turns_data: Optional[str] = None  # Turns tuple string

    # Start-to-end position glyph data
    start_position: Optional[str] = None
    end_position: Optional[str] = None

    # Visibility flags
    show_elemental: bool = True
    show_vtg: bool = True
    show_tka: bool = True
    show_positions: bool = True

    def update(self, **kwargs) -> "GlyphData":
        """Create a new GlyphData with updated fields."""
        from dataclasses import replace
        return replace(self, **kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "vtg_mode": self.vtg_mode.value if self.vtg_mode else None,
            "elemental_type": (
                self.elemental_type.value if self.elemental_type else None
            ),
            "letter_type": self.letter_type.value if self.letter_type else None,
            "has_dash": self.has_dash,
            "turns_data": self.turns_data,
            "start_position": self.start_position,
            "end_position": self.end_position,
            "show_elemental": self.show_elemental,
            "show_vtg": self.show_vtg,
            "show_tka": self.show_tka,
            "show_positions": self.show_positions,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GlyphData":
        """Create from dictionary."""
        vtg_mode = None
        if data.get("vtg_mode"):
            vtg_mode = VTGMode(data["vtg_mode"])

        elemental_type = None
        if data.get("elemental_type"):
            elemental_type = ElementalType(data["elemental_type"])

        letter_type = None
        if data.get("letter_type"):
            letter_type = LetterType(data["letter_type"])

        return cls(
            vtg_mode=vtg_mode,
            elemental_type=elemental_type,
            letter_type=letter_type,
            has_dash=data.get("has_dash", False),
            turns_data=data.get("turns_data"),
            start_position=data.get("start_position"),
            end_position=data.get("end_position"),
            show_elemental=data.get("show_elemental", True),
            show_vtg=data.get("show_vtg", True),
            show_tka=data.get("show_tka", True),
            show_positions=data.get("show_positions", True),
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
    def from_json(cls, json_str: str, camel_case: bool = True) -> "GlyphData":
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json
        if camel_case:
            return domain_model_from_json(json_str, cls)
        else:
            data = json.loads(json_str)
            return cls.from_dict(data)
