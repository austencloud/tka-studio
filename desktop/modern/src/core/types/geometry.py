"""
Framework-agnostic geometry types for TKA applications.

These types provide a clean abstraction layer between business logic
and UI framework-specific geometry types (like PyQt6's QPoint, QSize, QRect).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Point:
    """Framework-agnostic point representation."""
    
    x: float
    y: float
    
    def __post_init__(self):
        """Ensure coordinates are numeric."""
        if not isinstance(self.x, (int, float)):
            raise TypeError(f"Point.x must be numeric, got {type(self.x)}")
        if not isinstance(self.y, (int, float)):
            raise TypeError(f"Point.y must be numeric, got {type(self.y)}")
    
    def distance_to(self, other: Point) -> float:
        """Calculate distance to another point."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def translate(self, dx: float, dy: float) -> Point:
        """Create a new point translated by dx, dy."""
        return Point(self.x + dx, self.y + dy)
    
    def scale(self, factor: float) -> Point:
        """Create a new point scaled by factor."""
        return Point(self.x * factor, self.y * factor)


@dataclass(frozen=True)
class Size:
    """Framework-agnostic size representation."""
    
    width: int
    height: int
    
    def __post_init__(self):
        """Ensure dimensions are non-negative."""
        if self.width < 0:
            raise ValueError(f"Size.width must be non-negative, got {self.width}")
        if self.height < 0:
            raise ValueError(f"Size.height must be non-negative, got {self.height}")
    
    @property
    def area(self) -> int:
        """Calculate area."""
        return self.width * self.height
    
    def scale(self, factor: float) -> Size:
        """Create a new size scaled by factor."""
        return Size(int(self.width * factor), int(self.height * factor))
    
    def is_empty(self) -> bool:
        """Check if size is empty (zero width or height)."""
        return self.width == 0 or self.height == 0


@dataclass(frozen=True)
class Rect:
    """Framework-agnostic rectangle representation."""
    
    x: int
    y: int
    width: int
    height: int
    
    def __post_init__(self):
        """Ensure dimensions are non-negative."""
        if self.width < 0:
            raise ValueError(f"Rect.width must be non-negative, got {self.width}")
        if self.height < 0:
            raise ValueError(f"Rect.height must be non-negative, got {self.height}")
    
    @property
    def left(self) -> int:
        """Left edge x-coordinate."""
        return self.x
    
    @property
    def top(self) -> int:
        """Top edge y-coordinate."""
        return self.y
    
    @property
    def right(self) -> int:
        """Right edge x-coordinate."""
        return self.x + self.width
    
    @property
    def bottom(self) -> int:
        """Bottom edge y-coordinate."""
        return self.y + self.height
    
    @property
    def center(self) -> Point:
        """Center point of the rectangle."""
        return Point(self.x + self.width / 2, self.y + self.height / 2)
    
    @property
    def size(self) -> Size:
        """Size of the rectangle."""
        return Size(self.width, self.height)
    
    @property
    def top_left(self) -> Point:
        """Top-left corner point."""
        return Point(self.x, self.y)
    
    @property
    def top_right(self) -> Point:
        """Top-right corner point."""
        return Point(self.right, self.y)
    
    @property
    def bottom_left(self) -> Point:
        """Bottom-left corner point."""
        return Point(self.x, self.bottom)
    
    @property
    def bottom_right(self) -> Point:
        """Bottom-right corner point."""
        return Point(self.right, self.bottom)
    
    def contains_point(self, point: Point) -> bool:
        """Check if rectangle contains a point."""
        return (self.x <= point.x <= self.right and 
                self.y <= point.y <= self.bottom)
    
    def intersects(self, other: Rect) -> bool:
        """Check if this rectangle intersects with another."""
        return not (self.right < other.x or 
                   other.right < self.x or 
                   self.bottom < other.y or 
                   other.bottom < self.y)
    
    def translate(self, dx: int, dy: int) -> Rect:
        """Create a new rectangle translated by dx, dy."""
        return Rect(self.x + dx, self.y + dy, self.width, self.height)
    
    def is_empty(self) -> bool:
        """Check if rectangle is empty (zero width or height)."""
        return self.width == 0 or self.height == 0


# Type aliases for compatibility
PointType = Point
SizeType = Size
RectType = Rect
