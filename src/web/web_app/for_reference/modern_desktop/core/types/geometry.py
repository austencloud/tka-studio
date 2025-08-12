"""
Framework-agnostic geometry types for the core layer.

These types replace PyQt6 geometry types in the core interfaces,
allowing the core layer to remain UI framework independent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Size:
    """Framework-agnostic size representation."""

    width: int
    height: int

    def __iter__(self):
        """Allow tuple unpacking."""
        yield self.width
        yield self.height

    def is_valid(self) -> bool:
        """Check if size is valid (positive dimensions)."""
        return self.width > 0 and self.height > 0

    def scaled(self, factor: float) -> Size:
        """Return a new Size scaled by the given factor."""
        return Size(width=int(self.width * factor), height=int(self.height * factor))

    def __add__(self, other: Size) -> Size:
        """Add two sizes together."""
        return Size(width=self.width + other.width, height=self.height + other.height)

    def __sub__(self, other: Size) -> Size:
        """Subtract one size from another."""
        return Size(width=self.width - other.width, height=self.height - other.height)

    def __mul__(self, factor: float) -> Size:
        """Multiply size by a scalar."""
        return Size(width=int(self.width * factor), height=int(self.height * factor))

    def __truediv__(self, factor: float) -> Size:
        """Divide size by a scalar."""
        return Size(width=int(self.width / factor), height=int(self.height / factor))


@dataclass(frozen=True)
class Point:
    """Framework-agnostic point representation."""

    x: float
    y: float

    def __iter__(self):
        """Allow tuple unpacking."""
        yield self.x
        yield self.y

    def scaled(self, factor: float) -> Point:
        """Return a new Point scaled by the given factor."""
        return Point(x=self.x * factor, y=self.y * factor)


@dataclass(frozen=True)
class Rect:
    """Framework-agnostic rectangle representation."""

    x: int
    y: int
    width: int
    height: int

    @property
    def left(self) -> int:
        return self.x

    @property
    def top(self) -> int:
        return self.y

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def bottom(self) -> int:
        return self.y + self.height

    @property
    def center(self) -> Point:
        return Point(x=self.x + self.width / 2, y=self.y + self.height / 2)

    @property
    def size(self) -> Size:
        return Size(width=self.width, height=self.height)


@dataclass
class Widget:
    """Framework-agnostic widget representation for interface definitions."""

    element_id: str
    visible: bool = True
    opacity: float = 1.0


# Type aliases for common use cases
SizeType = Union[Size, tuple[int, int]]
PointType = Union[Point, tuple[float, float]]
RectType = Union[Rect, tuple[int, int, int, int]]
WidgetType = Union[Widget, str]  # Widget object or element ID
