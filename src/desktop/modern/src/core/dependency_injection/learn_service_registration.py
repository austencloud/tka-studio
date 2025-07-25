"""
Learn Services Dependency Injection Registration

Registers all learn tab services with the DI container following
the established patterns for service registration.
"""

import logging

from application.services.learn import (
    AnswerValidationService,
    LearnDataService,
    LearnNavigationService,
    LearnUIService,
    LessonConfigurationService,
    LessonProgressService,
    QuestionGenerationService,
    QuizSessionService,
)
from core.dependency_injection.di_container import DIContainer
from core.interfaces.data_builder_services import IPictographDataService
from core.interfaces.learn_services import (
    IAnswerValidationService,
    ILearnDataService,
    ILearnNavigationService,
    ILearnUIService,
    ILessonConfigurationService,
    ILessonProgressService,
    IQuestionGenerationService,
    IQuizSessionService,
)
from core.interfaces.organization_services import IFileSystemService
from infrastructure.file_system.file_system_service import FileSystemService
from presentation.tabs.learn import LearnTab

logger = logging.getLogger(__name__)


def register_learn_services(container: DIContainer) -> None:
    """
    Register all learn tab services with the DI container.

    Args:
        container: DI container to register services with
    """
    try:

        # External dependencies (use real data services)
        # Use the real pictograph service with actual TKA dataset
        from application.services.learn.real_pictograph_data_service import (
            RealPictographDataService,
        )

        # Register the real service for Learn Tab functionality
        container.register_factory(
            IPictographDataService, lambda: RealPictographDataService(container)
        )

        container.register_singleton(IFileSystemService, FileSystemService)

        # Core learn services (singleton pattern for state management)
        container.register_singleton(
            ILessonConfigurationService, LessonConfigurationService
        )
        container.register_singleton(IQuizSessionService, QuizSessionService)
        container.register_singleton(
            IQuestionGenerationService, QuestionGenerationService
        )
        container.register_singleton(IAnswerValidationService, AnswerValidationService)
        container.register_singleton(ILessonProgressService, LessonProgressService)

        # UI and navigation services (singleton for consistency)
        container.register_singleton(ILearnUIService, LearnUIService)
        container.register_singleton(ILearnNavigationService, LearnNavigationService)
        container.register_singleton(ILearnDataService, LearnDataService)

        # Main learn tab (transient to allow multiple instances if needed)
        container.register_transient(LearnTab, LearnTab)

    except Exception as e:
        logger.error(f"Failed to register learn services: {e}")
        raise


def validate_learn_service_registration(container: DIContainer) -> bool:
    """
    Validate that all learn services are properly registered and can be resolved.

    Args:
        container: DI container to validate

    Returns:
        True if all services can be resolved, False otherwise
    """
    try:
        logger.info("Validating learn service registration...")

        # Test core service resolution
        lesson_config_service = container.resolve(ILessonConfigurationService)
        session_service = container.resolve(IQuizSessionService)
        question_service = container.resolve(IQuestionGenerationService)
        validation_service = container.resolve(IAnswerValidationService)
        progress_service = container.resolve(ILessonProgressService)

        # Test UI services
        ui_service = container.resolve(ILearnUIService)
        navigation_service = container.resolve(ILearnNavigationService)
        data_service = container.resolve(ILearnDataService)

        # Test main component (skip in headless environments)
        try:
            learn_tab = container.resolve(LearnTab)
        except Exception as e:
            if "QApplication" in str(e):
                logger.warning("Skipping UI component test in headless environment")
                learn_tab = None
            else:
                raise

        # Verify services have expected interfaces
        services_to_check = [
            (lesson_config_service, ILessonConfigurationService),
            (session_service, IQuizSessionService),
            (question_service, IQuestionGenerationService),
            (validation_service, IAnswerValidationService),
            (progress_service, ILessonProgressService),
            (ui_service, ILearnUIService),
            (navigation_service, ILearnNavigationService),
            (data_service, ILearnDataService),
        ]

        for service, interface in services_to_check:
            if not isinstance(service, interface):
                logger.error(f"Service {service} does not implement {interface}")
                return False

        # Test basic functionality
        lesson_configs = lesson_config_service.get_all_lesson_configs()
        if not lesson_configs:
            logger.error("No lesson configurations found")
            return False

        logger.info("Learn service registration validation completed successfully")
        return True

    except Exception as e:
        logger.error(f"Learn service registration validation failed: {e}")
        return False


def get_learn_service_dependencies() -> dict:
    """
    Get information about learn service dependencies for documentation.

    Returns:
        Dictionary describing service dependencies
    """
    return {
        "core_services": {
            ILessonConfigurationService.__name__: {
                "implementation": LessonConfigurationService.__name__,
                "dependencies": [],
                "description": "Manages lesson configurations and types",
            },
            IQuizSessionService.__name__: {
                "implementation": QuizSessionService.__name__,
                "dependencies": [],
                "description": "Manages quiz sessions and state",
            },
            IQuestionGenerationService.__name__: {
                "implementation": QuestionGenerationService.__name__,
                "dependencies": [
                    IQuizSessionService.__name__,
                    "IPictographDataService",  # External dependency
                ],
                "description": "Generates quiz questions",
            },
            IAnswerValidationService.__name__: {
                "implementation": AnswerValidationService.__name__,
                "dependencies": [IQuizSessionService.__name__],
                "description": "Validates answers and tracks progress",
            },
            ILessonProgressService.__name__: {
                "implementation": LessonProgressService.__name__,
                "dependencies": [
                    IQuizSessionService.__name__,
                    IAnswerValidationService.__name__,
                ],
                "description": "Tracks lesson progress and completion",
            },
        },
        "ui_services": {
            ILearnUIService.__name__: {
                "implementation": LearnUIService.__name__,
                "dependencies": [],
                "description": "Provides UI calculations and styling",
            },
            ILearnNavigationService.__name__: {
                "implementation": LearnNavigationService.__name__,
                "dependencies": [],
                "description": "Manages navigation between views",
            },
            ILearnDataService.__name__: {
                "implementation": LearnDataService.__name__,
                "dependencies": ["IFileSystemService"],  # External dependency
                "description": "Handles data persistence",
            },
        },
        "external_dependencies": [
            "IPictographDataService",  # From existing data services
            "IFileSystemService",  # From existing infrastructure
        ],
    }
