"""
Generation Service Registration

Registers all generation-related services in the dependency injection container.
Part of the modern TKA application's service registration system.
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


def register_generation_services(container: "DIContainer") -> None:
    """
    Register all generation services in the dependency injection container.
    
    Args:
        container: DI container to register services in
    """
    try:
        # Import service interfaces
        from desktop.modern.core.interfaces.generation_services import (
            IGenerationService,
            ISequenceConfigurationService,
            IGenerationValidationService,
            ITurnIntensityManager,
        )
        
        # Import service implementations
        from .generation_service import GenerationService
        from .sequence_configuration_service import SequenceConfigurationService
        from .generation_validation_service import GenerationValidationService
        from .turn_intensity_manager import ModernTurnIntensityManager  # Use modern wrapper
        
        # Register core generation services
        container.register_singleton(IGenerationService, GenerationService)
        container.register_singleton(ISequenceConfigurationService, SequenceConfigurationService)
        container.register_singleton(IGenerationValidationService, GenerationValidationService)
        container.register_singleton(ITurnIntensityManager, ModernTurnIntensityManager)  # Use modern wrapper
        
        logger.info("✅ Generation services registered successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to register generation services: {str(e)}")
        raise


def register_generation_test_doubles(container: "DIContainer") -> None:
    """
    Register test doubles for generation services.
    
    Args:
        container: DI container to register test doubles in
    """
    try:
        # Import test double implementations
        from .test_doubles.mock_generation_service import MockGenerationService
        from .test_doubles.mock_configuration_service import MockSequenceConfigurationService
        from .test_doubles.mock_validation_service import MockGenerationValidationService
        
        # Import service interfaces
        from desktop.modern.core.interfaces.generation_services import (
            IGenerationService,
            ISequenceConfigurationService,
            IGenerationValidationService,
        )
        
        # Register test doubles
        container.register_singleton(IGenerationService, MockGenerationService)
        container.register_singleton(ISequenceConfigurationService, MockSequenceConfigurationService)
        container.register_singleton(IGenerationValidationService, MockGenerationValidationService)
        
        logger.info("✅ Generation test doubles registered successfully")
        
    except ImportError:
        # Test doubles not available, register actual services
        logger.warning("Test doubles not available, registering actual generation services")
        register_generation_services(container)
    except Exception as e:
        logger.error(f"❌ Failed to register generation test doubles: {str(e)}")
        raise


class GenerationServiceRegistrationHelper:
    """
    Helper class for generation service registration.
    
    Provides utilities for registering generation services and managing
    their dependencies in different application modes.
    """
    
    @staticmethod
    def register_for_production(container: "DIContainer") -> None:
        """Register production generation services."""
        register_generation_services(container)
    
    @staticmethod
    def register_for_testing(container: "DIContainer") -> None:
        """Register test double generation services."""
        register_generation_test_doubles(container)
    
    @staticmethod
    def validate_registration(container: "DIContainer") -> bool:
        """
        Validate that generation services are properly registered.
        
        Args:
            container: DI container to validate
            
        Returns:
            True if all services are registered correctly
        """
        try:
            from desktop.modern.core.interfaces.generation_services import (
                IGenerationService,
                ISequenceConfigurationService,
                IGenerationValidationService,
                ITurnIntensityManager,
            )
            
            # Check that all required services can be resolved
            container.resolve(IGenerationService)
            container.resolve(ISequenceConfigurationService)
            container.resolve(IGenerationValidationService)
            container.resolve(ITurnIntensityManager)
            
            logger.info("✅ Generation service registration validation passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Generation service registration validation failed: {str(e)}")
            return False
