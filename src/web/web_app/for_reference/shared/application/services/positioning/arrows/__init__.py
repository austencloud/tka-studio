"""
Arrow Positioning Services

Complete arrow positioning service architecture with microservices.
"""

# Import calculation services
from .calculation import (
    ArrowLocationCalculatorService,
    ArrowRotationCalculatorService,
    DashLocationCalculator,
    DirectionalTupleCalculator,
    OrientationCalculator,
    QuadrantIndexCalculator,
)

# Import coordinate system services
from .coordinate_system import ArrowCoordinateSystemService

# Import key generator services
from .key_generators import (
    AttributeKeyGenerator,
    PlacementKeyGenerator,
    TurnsTupleKeyGenerator,
)

# Import orchestration services
from .orchestration import (
    ArrowAdjustmentCalculator,
    DirectionalTupleProcessor,
)

# Import placement services
from .placement import (
    DefaultPlacementService,
    SpecialPlacementOriKeyGenerator,
    SpecialPlacementService,
)

# Import utility services
from .utilities import PictographPositionMatcher

__all__ = [
    # Calculation services
    "ArrowLocationCalculatorService",
    "ArrowRotationCalculatorService",
    "DashLocationCalculator",
    "DirectionalTupleCalculator",
    "OrientationCalculator",
    "QuadrantIndexCalculator",
    # Coordinate system services
    "ArrowCoordinateSystemService",
    # Key generator services
    "AttributeKeyGenerator",
    "PlacementKeyGenerator",
    "TurnsTupleKeyGenerator",
    # Orchestration services
    "ArrowAdjustmentCalculator",
    "DirectionalTupleProcessor",
    # Placement services
    "DefaultPlacementService",
    "SpecialPlacementOriKeyGenerator",
    "SpecialPlacementService",
    # Utility services
    "PictographPositionMatcher",
]
