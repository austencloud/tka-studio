"""
Shared type definitions for TKA applications.
Core enums that ensure consistency between desktop and web applications.
"""

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


__all__ = ["MotionType", "RotationDirection", "Location", "PropType", "Color"]
