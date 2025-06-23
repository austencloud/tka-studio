"""
Positioning Services - Clean Arrow/Prop Domain Separation

This module provides positioning services organized into two clear domains:
- arrows: All arrow-related positioning, calculation, and key generation
- props: All prop-related positioning, separation, and configuration

The microservices architecture ensures clean separation of concerns and maintainable code.
"""

# Arrow Domain Services
from .arrows.orchestration.arrow_positioning_orchestrator import ArrowPositioningOrchestrator
from .arrows.orchestration.arrow_adjustment_calculator_service import ArrowAdjustmentCalculatorService

from .arrows.calculation.arrow_location_calculator import ArrowLocationCalculator
from .arrows.calculation.arrow_location_calculator_service import ArrowLocationCalculatorService
from .arrows.calculation.arrow_rotation_calculator_service import ArrowRotationCalculatorService
from .arrows.calculation.orientation_calculation_service import OrientationCalculationService
from .arrows.calculation.quadrant_adjustment_service import QuadrantAdjustmentService
from .arrows.calculation.quadrant_index_service import QuadrantIndexService
from .arrows.calculation.directional_tuple_service import DirectionalTupleService

from .arrows.placement.default_placement_service import DefaultPlacementService
from .arrows.placement.special_placement_service import SpecialPlacementService
from .arrows.placement.special_placement_orientation_service import SpecialPlacementOrientationService

from .arrows.coordinate_system.arrow_coordinate_system_service import ArrowCoordinateSystemService

from .arrows.keys.placement_key_generation_service import PlacementKeyGenerationService
from .arrows.keys.placement_key_service import PlacementKeyService
from .arrows.keys.attribute_key_generation_service import AttributeKeyGenerationService
from .arrows.keys.turns_tuple_generation_service import TurnsTupleGenerationService

from .arrows.utilities.dash_location_service import DashLocationService
from .arrows.utilities.position_matching_service import PositionMatchingService

# Prop Domain Services
from .props.orchestration.prop_orchestrator import PropOrchestrator
from .props.orchestration.prop_management_service import PropManagementService

from .props.calculation.direction_calculation_service import DirectionCalculationService
from .props.calculation.offset_calculation_service import OffsetCalculationService
from .props.calculation.prop_classification_service import PropClassificationService

from .props.configuration.json_configuration_service import JsonConfigurationService

# Public API - Main orchestrators for each domain
__all__ = [
    # Arrow Domain - Main orchestrators
    "ArrowPositioningOrchestrator",
    "ArrowAdjustmentCalculatorService",
    
    # Arrow Domain - Calculation services
    "ArrowLocationCalculator",
    "ArrowLocationCalculatorService", 
    "ArrowRotationCalculatorService",
    "OrientationCalculationService",
    "QuadrantAdjustmentService",
    "QuadrantIndexService",
    "DirectionalTupleService",
    
    # Arrow Domain - Placement services
    "DefaultPlacementService",
    "SpecialPlacementService",
    "SpecialPlacementOrientationService",
    
    # Arrow Domain - Coordinate system
    "ArrowCoordinateSystemService",
    
    # Arrow Domain - Key generation
    "PlacementKeyGenerationService",
    "PlacementKeyService",
    "AttributeKeyGenerationService", 
    "TurnsTupleGenerationService",
    
    # Arrow Domain - Utilities
    "DashLocationService",
    "PositionMatchingService",
    
    # Prop Domain - Main orchestrators
    "PropOrchestrator",
    "PropManagementService",
    
    # Prop Domain - Calculation services
    "DirectionCalculationService",
    "OffsetCalculationService",
    "PropClassificationService",
    
    # Prop Domain - Configuration
    "JsonConfigurationService",
]