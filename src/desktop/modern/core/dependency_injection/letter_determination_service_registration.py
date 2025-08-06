"""
Letter Determination Services Dependency Injection Registration

Registers all letter determination services with the DI container following
the established patterns for service registration.
"""

from __future__ import annotations

import logging

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.letter_determination.letter_determination_services import (
    ILetterDeterminationService,
    IMotionAttributeService,
    IMotionComparisonService,
    IPictographDatasetProvider,
)


logger = logging.getLogger(__name__)


def register_letter_determination_services(container: DIContainer) -> None:
    """
    Register all letter determination services with the DI container.

    Args:
        container: DI container to register services with
    """
    try:
        logger.info("Registering letter determination services...")

        # Import implementations
        from shared.application.services.data.dataset_query import DatasetQuery
        from shared.application.services.letter_determination.letter_determination_service import (
            LetterDeterminationService,
        )
        from shared.application.services.letter_determination.motion_comparison_service import (
            MotionComparisonService,
        )
        from shared.application.services.letter_determination.pictograph_dataset_provider import (
            PictographDatasetProvider,
        )

        # Import dependencies
        from shared.application.services.pictograph.pictograph_csv_manager import (
            PictographCSVManager,
        )

        # Register dataset provider (singleton for caching)
        container.register_factory(
            IPictographDatasetProvider,
            lambda: PictographDatasetProvider(
                csv_manager=container.resolve(PictographCSVManager),
                dataset_query=container.resolve(DatasetQuery),
            ),
        )
        logger.info("Registered IPictographDatasetProvider")

        # Register motion comparison service (singleton)
        container.register_factory(
            IMotionComparisonService,
            lambda: MotionComparisonService(
                dataset_provider=container.resolve(IPictographDatasetProvider)
            ),
        )
        logger.info("Registered IMotionComparisonService")

        # Register motion attribute service (if it exists)
        try:
            from shared.application.services.letter_determination.motion_attribute_service import (
                MotionAttributeService,
            )

            container.register_singleton(
                IMotionAttributeService, MotionAttributeService
            )
            logger.info("Registered IMotionAttributeService")
        except ImportError:
            logger.warning("MotionAttributeService not found, creating placeholder")
            # Create a simple placeholder implementation

            class PlaceholderMotionAttributeService(IMotionAttributeService):
                def sync_attributes(self, pictograph_data):
                    return pictograph_data

                def validate_attributes(self, pictograph_data):
                    return True

            container.register_singleton(
                IMotionAttributeService, PlaceholderMotionAttributeService
            )
            logger.info("Registered placeholder IMotionAttributeService")

        # Register main letter determination service (singleton)
        container.register_factory(
            ILetterDeterminationService,
            lambda: LetterDeterminationService(
                dataset_provider=container.resolve(IPictographDatasetProvider),
                comparison_service=container.resolve(IMotionComparisonService),
                attribute_service=container.resolve(IMotionAttributeService),
            ),
        )
        logger.info("Registered ILetterDeterminationService")

        logger.info("Letter determination services registration completed successfully")

    except Exception as e:
        logger.error(f"Failed to register letter determination services: {e}")
        raise


def validate_letter_determination_services(container: DIContainer) -> bool:
    """
    Validate that all letter determination services are properly registered.

    Args:
        container: DI container to validate

    Returns:
        True if all services are properly registered
    """
    try:
        logger.info("Validating letter determination services...")

        # Test service resolution
        dataset_provider = container.resolve(IPictographDatasetProvider)
        comparison_service = container.resolve(IMotionComparisonService)
        attribute_service = container.resolve(IMotionAttributeService)
        letter_service = container.resolve(ILetterDeterminationService)

        # Verify services have expected interfaces
        services_to_check = [
            (dataset_provider, IPictographDatasetProvider),
            (comparison_service, IMotionComparisonService),
            (attribute_service, IMotionAttributeService),
            (letter_service, ILetterDeterminationService),
        ]

        for service, interface in services_to_check:
            if not isinstance(service, interface):
                logger.error(f"Service {service} does not implement {interface}")
                return False

        logger.info("All letter determination services validated successfully")
        return True

    except Exception as e:
        logger.error(f"Letter determination services validation failed: {e}")
        return False


def get_letter_determination_service_dependencies() -> dict:
    """
    Get service dependency information for letter determination services.

    Returns:
        Dictionary describing service dependencies
    """
    return {
        "core_services": {
            IPictographDatasetProvider.__name__: {
                "implementation": "PictographDatasetProvider",
                "dependencies": ["PictographCSVManager", "DatasetQuery"],
                "description": "Provides access to pictograph reference datasets",
            },
            IMotionComparisonService.__name__: {
                "implementation": "MotionComparisonService",
                "dependencies": [IPictographDatasetProvider.__name__],
                "description": "Compares motion attributes for letter matching",
            },
            IMotionAttributeService.__name__: {
                "implementation": "MotionAttributeService",
                "dependencies": [],
                "description": "Manages motion attribute synchronization",
            },
            ILetterDeterminationService.__name__: {
                "implementation": "LetterDeterminationService",
                "dependencies": [
                    IPictographDatasetProvider.__name__,
                    IMotionComparisonService.__name__,
                    IMotionAttributeService.__name__,
                ],
                "description": "Main orchestrator for letter determination",
            },
        },
        "external_dependencies": [
            "PictographCSVManager",  # From existing pictograph services
            "DatasetQuery",  # From existing data services
        ],
    }
