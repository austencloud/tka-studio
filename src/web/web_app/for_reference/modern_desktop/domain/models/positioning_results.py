"""
Positioning Domain Models

Immutable data models for arrow and prop positioning results.
Follows TKA's clean architecture and immutable domain model patterns.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ArrowPositionResult:
    """Immutable result of arrow positioning calculation."""

    x: float
    y: float
    rotation: float
    location: Optional[str] = None

    def update(self, **kwargs) -> ArrowPositionResult:
        """Create updated copy with new values."""
        current_values = {
            "x": self.x,
            "y": self.y,
            "rotation": self.rotation,
            "location": self.location,
        }
        current_values.update(kwargs)
        return ArrowPositionResult(**current_values)


@dataclass(frozen=True)
class PropPositionResult:
    """Immutable result of prop positioning calculation."""

    x: float
    y: float
    rotation: float
    separation_applied: bool = False

    def update(self, **kwargs) -> PropPositionResult:
        """Create updated copy with new values."""
        current_values = {
            "x": self.x,
            "y": self.y,
            "rotation": self.rotation,
            "separation_applied": self.separation_applied,
        }
        current_values.update(kwargs)
        return PropPositionResult(**current_values)
