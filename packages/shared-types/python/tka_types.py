"""
Shared type definitions for TKA applications.
These types ensure consistency between desktop and web applications.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum


class MotionType(Enum):
    """Motion types for kinetic sequences."""

    PRO = "pro"
    ANTI = "anti"
    FLOAT = "float"
    DASH = "dash"
    STATIC = "static"


class RotationDirection(Enum):
    """Rotation directions for motion."""

    CLOCKWISE = "cw"
    COUNTER_CLOCKWISE = "ccw"
    NO_ROTATION = "no_rot"


class Location(Enum):
    """Location positions for motion."""

    NORTH = "n"
    EAST = "e"
    SOUTH = "s"
    WEST = "w"
    NORTHEAST = "ne"
    SOUTHEAST = "se"
    SOUTHWEST = "sw"
    NORTHWEST = "nw"


class PropType(Enum):
    """Prop types for kinetic sequences."""

    STAFF = "staff"
    CLUB = "club"
    BUUGENG = "buugeng"
    FAN = "fan"
    TRIAD = "triad"
    MINIHOOP = "minihoop"
    BIGBALL = "bigball"
    FRACTALS = "fractals"


class Color(Enum):
    """Colors for motion elements."""

    BLUE = "blue"
    RED = "red"


@dataclass
class SharedSequenceType:
    """Shared sequence type definition for API consistency."""

    id: str
    name: str
    word: str
    beats: List[Dict[str, Any]]
    length: int
    total_duration: float
    start_position: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SharedBeatType:
    """Shared beat type definition."""

    id: str
    beat_number: int
    letter: Optional[str]
    duration: float
    blue_motion: Optional[Dict[str, Any]] = None
    red_motion: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SharedMotionType:
    """Shared motion type definition."""

    motion_type: MotionType
    prop_type: PropType
    color: Color
    start_location: Location
    end_location: Location
    rotation_direction: RotationDirection
    turns: float = 0.0
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SharedSettingsType:
    """Shared settings type definition."""

    background_type: str
    theme: str
    window_geometry: Optional[Dict[str, int]] = None
    last_sequence_id: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


# Export for code generation
__all__ = [
    "MotionType",
    "RotationDirection",
    "Location",
    "PropType",
    "Color",
    "SharedSequenceType",
    "SharedBeatType",
    "SharedMotionType",
    "SharedSettingsType",
]
