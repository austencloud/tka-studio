"""
Framework-agnostic geometry types for the core layer.

These types replace PyQt6 geometry types in the core interfaces,
allowing the core layer to remain UI framework independent.
"""

from dataclasses import dataclass
from typing import Tuple, Union


@dataclass(frozen=True)
class Size:
    """Framework-agnostic size representation."""

    width: int
    height: int

    def to_tuple(self) -> Tuple[int, int]:
        """Convert to tuple format."""
        return (self.width, self.height)

    @classmethod
    def from_tuple(cls, size_tuple: Tuple[int, int]) -> "Size":
        """Create from tuple format."""
        return cls(width=size_tuple[0], height=size_tuple[1])

    def __iter__(self):
        """Allow tuple unpacking."""
        yield self.width
        yield self.height

    def is_valid(self) -> bool:
        """Check if size is valid (positive dimensions)."""
        return self.width > 0 and self.height > 0

    def scaled(self, factor: float) -> "Size":
        """Return a new Size scaled by the given factor."""
        return Size(width=int(self.width * factor), height=int(self.height * factor))

    def with_max_dimension(self, max_size: int) -> "Size":
        """Return a new Size scaled to fit within max dimension."""
        if max(self.width, self.height) <= max_size:
            return self

        scale = max_size / max(self.width, self.height)
        return self.scaled(scale)

    def __add__(self, other: "Size") -> "Size":
        """Add two sizes together."""
        return Size(width=self.width + other.width, height=self.height + other.height)

    def __sub__(self, other: "Size") -> "Size":
        """Subtract one size from another."""
        return Size(width=self.width - other.width, height=self.height - other.height)

    def __mul__(self, factor: float) -> "Size":
        """Multiply size by a scalar."""
        return Size(width=int(self.width * factor), height=int(self.height * factor))

    def __truediv__(self, factor: float) -> "Size":
        """Divide size by a scalar."""
        return Size(width=int(self.width / factor), height=int(self.height / factor))


@dataclass(frozen=True)
class Point:
    """Framework-agnostic point representation."""

    x: float
    y: float

    def to_tuple(self) -> Tuple[float, float]:
        """Convert to tuple format."""
        return (self.x, self.y)

    @classmethod
    def from_tuple(cls, point_tuple: Tuple[float, float]) -> "Point":
        """Create from tuple format."""
        return cls(x=point_tuple[0], y=point_tuple[1])

    def __iter__(self):
        """Allow tuple unpacking."""
        yield self.x
        yield self.y

    def distance_to(self, other: "Point") -> float:
        """Calculate distance to another point."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def translated(self, dx: float, dy: float) -> "Point":
        """Return a new Point translated by the giv Hey there en offset."""
        return Point(x=self.x + dx, y=self.y + dy)

    def scaled(self, factor: float) -> "Point":
        """Return a new Point scaled by the given factor."""
        return Point(x=self.x * factor, y=self.y * factor)

    def __add__(self, other: "Point") -> "Point":
        """Add two points together."""
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        """Subtract one point from another."""
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __mul__(self, factor: float) -> "Point":
        """Multiply point by a scalar."""
        return Point(x=self.x * factor, y=self.y * factor)

    def __truediv__(self, factor: float) -> "Point":
        """Divide point by a scalar."""
        return Point(x=self.x / factor, y=self.y / factor)

    def __neg__(self) -> "Point":
        """Negate the point."""
        return Point(x=-self.x, y=-self.y)


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

    def contains_point(self, point: Point) -> bool:
        """Check if the rectangle contains the given point."""
        return self.left <= point.x <= self.right and self.top <= point.y <= self.bottom

    def intersects(self, other: "Rect") -> bool:
        """Check if this rectangle intersects with another."""
        return not (
            self.right < other.left
            or self.left > other.right
            or self.bottom < other.top
            or self.top > other.bottom
        )


@dataclass
class Widget:
    """Framework-agnostic widget representation for interface definitions."""

    element_id: str
    visible: bool = True
    opacity: float = 1.0

    def set_visible(self, visible: bool) -> None:
        """Set widget visibility."""
        self.visible = visible

    def set_opacity(self, opacity: float) -> None:
        """Set widget opacity."""
        self.opacity = opacity

    def is_visible(self) -> bool:
        """Check if widget is visible."""
        return self.visible


# Type aliases for common use cases
SizeType = Union[Size, Tuple[int, int]]
PointType = Union[Point, Tuple[float, float]]
RectType = Union[Rect, Tuple[int, int, int, int]]
WidgetType = Union[Widget, str]  # Widget object or element ID
