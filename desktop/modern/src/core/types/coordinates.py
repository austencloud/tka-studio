"""
Coordinate system types for TKA applications.

Provides coordinate system abstractions for different positioning
systems used in pictograph rendering and layout calculations.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Union

from .geometry import Point


class CoordinateSystem(Enum):
    """Coordinate system types."""
    
    SCENE = "scene"  # Scene coordinates (0,0 at top-left)
    GRID = "grid"    # Grid coordinates (position-based)
    HAND = "hand"    # Hand point coordinates
    LAYER2 = "layer2"  # Layer2 point coordinates


@dataclass(frozen=True)
class Coordinate:
    """
    Framework-agnostic coordinate representation.
    
    Includes coordinate system information for proper transformations.
    """
    
    point: Point
    system: CoordinateSystem
    
    def __post_init__(self):
        """Validate coordinate data."""
        if not isinstance(self.point, Point):
            raise TypeError(f"Coordinate.point must be Point, got {type(self.point)}")
        if not isinstance(self.system, CoordinateSystem):
            raise TypeError(f"Coordinate.system must be CoordinateSystem, got {type(self.system)}")
    
    def to_system(self, target_system: CoordinateSystem) -> Coordinate:
        """
        Convert coordinate to a different coordinate system.
        
        Args:
            target_system: Target coordinate system
            
        Returns:
            New coordinate in the target system
        """
        if self.system == target_system:
            return self
        
        # For now, return the same coordinate with updated system
        # TODO: Implement proper coordinate transformations
        return Coordinate(self.point, target_system)
    
    def translate(self, dx: float, dy: float) -> Coordinate:
        """Create a new coordinate translated by dx, dy."""
        new_point = self.point.translate(dx, dy)
        return Coordinate(new_point, self.system)
    
    def scale(self, factor: float) -> Coordinate:
        """Create a new coordinate scaled by factor."""
        new_point = self.point.scale(factor)
        return Coordinate(new_point, self.system)


@dataclass(frozen=True)
class GridPosition:
    """
    Grid-based position representation.
    
    Represents positions in the TKA grid system (alpha, beta, gamma positions).
    """
    
    position_key: str  # e.g., "alpha1", "beta3", "gamma12"
    coordinate: Coordinate
    
    def __post_init__(self):
        """Validate grid position data."""
        if not isinstance(self.position_key, str):
            raise TypeError(f"GridPosition.position_key must be str, got {type(self.position_key)}")
        if not isinstance(self.coordinate, Coordinate):
            raise TypeError(f"GridPosition.coordinate must be Coordinate, got {type(self.coordinate)}")
    
    @property
    def grid_type(self) -> str:
        """Get the grid type (alpha, beta, gamma)."""
        if self.position_key.startswith("alpha"):
            return "alpha"
        elif self.position_key.startswith("beta"):
            return "beta"
        elif self.position_key.startswith("gamma"):
            return "gamma"
        else:
            return "unknown"
    
    @property
    def grid_number(self) -> int | None:
        """Get the grid number from the position key."""
        try:
            # Extract number from position key (e.g., "alpha1" -> 1)
            for i, char in enumerate(self.position_key):
                if char.isdigit():
                    return int(self.position_key[i:])
            return None
        except (ValueError, IndexError):
            return None


@dataclass(frozen=True)
class LocationCoordinate:
    """
    Location-based coordinate representation.
    
    Represents coordinates for specific locations (N, E, S, W, etc.).
    """
    
    location: str  # e.g., "n", "e", "s", "w", "ne", etc.
    coordinate: Coordinate
    
    def __post_init__(self):
        """Validate location coordinate data."""
        if not isinstance(self.location, str):
            raise TypeError(f"LocationCoordinate.location must be str, got {type(self.location)}")
        if not isinstance(self.coordinate, Coordinate):
            raise TypeError(f"LocationCoordinate.coordinate must be Coordinate, got {type(self.coordinate)}")
    
    @property
    def is_cardinal(self) -> bool:
        """Check if this is a cardinal direction (N, E, S, W)."""
        return self.location.lower() in ["n", "e", "s", "w"]
    
    @property
    def is_diagonal(self) -> bool:
        """Check if this is a diagonal direction (NE, SE, SW, NW)."""
        return self.location.lower() in ["ne", "se", "sw", "nw"]


class CoordinateTransformer:
    """
    Utility class for coordinate system transformations.
    """
    
    def __init__(self, scene_size: tuple[int, int] = (950, 950)):
        """
        Initialize coordinate transformer.
        
        Args:
            scene_size: Size of the scene coordinate system
        """
        self.scene_width, self.scene_height = scene_size
        self.scene_center = Point(self.scene_width / 2, self.scene_height / 2)
    
    def scene_to_grid(self, scene_coord: Coordinate) -> Coordinate:
        """
        Transform scene coordinates to grid coordinates.
        
        Args:
            scene_coord: Coordinate in scene system
            
        Returns:
            Coordinate in grid system
        """
        if scene_coord.system != CoordinateSystem.SCENE:
            raise ValueError("Input coordinate must be in SCENE system")
        
        # For now, return the same point with updated system
        # TODO: Implement proper scene-to-grid transformation
        return Coordinate(scene_coord.point, CoordinateSystem.GRID)
    
    def grid_to_scene(self, grid_coord: Coordinate) -> Coordinate:
        """
        Transform grid coordinates to scene coordinates.
        
        Args:
            grid_coord: Coordinate in grid system
            
        Returns:
            Coordinate in scene system
        """
        if grid_coord.system != CoordinateSystem.GRID:
            raise ValueError("Input coordinate must be in GRID system")
        
        # For now, return the same point with updated system
        # TODO: Implement proper grid-to-scene transformation
        return Coordinate(grid_coord.point, CoordinateSystem.SCENE)
    
    def normalize_to_scene(self, coord: Coordinate) -> Coordinate:
        """
        Normalize any coordinate to scene coordinates.
        
        Args:
            coord: Coordinate in any system
            
        Returns:
            Coordinate in scene system
        """
        if coord.system == CoordinateSystem.SCENE:
            return coord
        elif coord.system == CoordinateSystem.GRID:
            return self.grid_to_scene(coord)
        else:
            # For other systems, assume they're already in scene coordinates
            return Coordinate(coord.point, CoordinateSystem.SCENE)


# Type aliases for convenience
SceneCoordinate = Coordinate
GridCoordinate = Coordinate
HandCoordinate = Coordinate
Layer2Coordinate = Coordinate

# Union type for all coordinate types
AnyCoordinate = Union[Coordinate, GridPosition, LocationCoordinate]
