"""
Arrow Rendering Service Interface

Interface for arrow rendering business logic to ensure proper separation
of concerns and enable testing.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from desktop.modern.domain.models import MotionData


class IArrowRenderingService(ABC):
    """Interface for arrow rendering business operations."""

    # Caching Operations
    @abstractmethod
    def load_cached_svg_data(self, svg_path: str) -> Optional[str]:
        """Load and cache SVG data from file."""

    # Validation and Utilities
    @abstractmethod
    def validate_motion_visibility(self, motion_data: MotionData) -> bool:
        """Validate if a motion should be rendered as visible."""
