"""
Generation Services Package

Contains all services related to sequence generation including:
- Main generation orchestration
- Freeform and circular generation algorithms
- Configuration management and validation
- Turn intensity management
- Service registration utilities

This package implements the generation functionality for the modern TKA application,
porting logic from the legacy generation system while maintaining clean architecture.
"""

from .generation_service import GenerationService
from .freeform_generation_service import FreeformGenerationService
from .circular_generation_service import CircularGenerationService
from .generation_validation_service import GenerationValidationService
from .sequence_configuration_service import SequenceConfigurationService
from .turn_intensity_manager import TurnIntensityManager, ModernTurnIntensityManager
from .generation_service_registration import (
    register_generation_services,
    GenerationServiceRegistrationHelper,
)

__all__ = [
    "GenerationService",
    "FreeformGenerationService", 
    "CircularGenerationService",
    "GenerationValidationService",
    "SequenceConfigurationService",
    "TurnIntensityManager",
    "ModernTurnIntensityManager",
    "register_generation_services",
    "GenerationServiceRegistrationHelper",
]
