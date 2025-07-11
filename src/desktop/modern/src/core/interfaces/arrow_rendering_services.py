"""
Arrow Rendering Service Interface

Interface for arrow rendering business logic to ensure proper separation
of concerns and enable testing.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Set, Tuple

from domain.models import Location, MotionData
from domain.models.arrow_data import ArrowData
from domain.models.pictograph_data import PictographData


class IArrowRenderingService(ABC):
    """Interface for arrow rendering business operations."""

    # Asset Management
    @abstractmethod
    def get_arrow_svg_path(self, motion_data: MotionData, color: str) -> str:
        """Get the SVG asset path for an arrow."""

    @abstractmethod
    def get_fallback_arrow_svg_path(self, motion_data: MotionData) -> str:
        """Get the fallback SVG asset path for an arrow."""

    @abstractmethod
    def svg_path_exists(self, path: str) -> bool:
        """Check if an SVG path exists."""

    # Caching Operations
    @abstractmethod
    def load_cached_svg_data(self, svg_path: str) -> Optional[str]:
        """Load and cache SVG data from file."""

    @abstractmethod
    def apply_color_transformation(self, svg_data: str, color: str) -> str:
        """Apply color transformation to SVG data."""

    # Position Calculations
    @abstractmethod
    def calculate_arrow_position(
        self,
        arrow_data: ArrowData,
        pictograph_data: Optional[PictographData] = None,
        positioning_orchestrator=None,
        coordinate_system=None,
    ) -> Tuple[float, float, float]:
        """Calculate arrow position using available positioning services."""

    # Cache Management
    @abstractmethod
    def get_cache_statistics(self) -> Dict[str, int]:
        """Get current cache statistics for monitoring."""

    @abstractmethod
    def clear_cache(self) -> None:
        """Clear the SVG file cache and reset statistics."""

    @abstractmethod
    def get_cache_info(self) -> str:
        """Get detailed cache information for debugging."""

    # Validation and Utilities
    @abstractmethod
    def validate_motion_visibility(self, motion_data: MotionData) -> bool:
        """Validate if a motion should be rendered as visible."""

    @abstractmethod
    def get_service_summary(self) -> Dict[str, any]:
        """Get a summary of the service state."""
