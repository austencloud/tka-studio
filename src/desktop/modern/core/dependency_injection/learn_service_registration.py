"""
Learn Services Dependency Injection Registration

Registers all learn tab services with the DI container following
the established patterns for service registration.
"""

from __future__ import annotations

import logging

from desktop.modern.application.services.data.dataset_query import IDatasetQuery
from desktop.modern.application.services.learn import (
    AnswerValidationService,
    LearnDataService,
    LearnNavigationService,
    LearnUIService,
    LessonConfigurationService,
    LessonProgressService,
    QuizSessionService,
)
from desktop.modern.application.services.learn.question_generation_service import (
    QuestionGenerationService,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.learn_services import (
    IAnswerValidationService,
    ILearnDataService,
    ILearnNavigationService,
    ILearnUIService,
    ILessonConfigurationService,
    ILessonProgressService,
    IQuestionGenerationService,
    IQuizSessionService,
)
from desktop.modern.core.interfaces.organization_services import IFileSystemService
from desktop.modern.core.interfaces.pictograph_services import IPictographDataManager
from desktop.modern.infrastructure.file_system.file_system_service import (
    FileSystemService,
)
from desktop.modern.presentation.views.learn import LearnTab


logger = logging.getLogger(__name__)


def register_learn_services(container: DIContainer) -> None:
    """
    Register all learn tab services with the DI container.

    Args:
        container: DI container to register services with
    """
    try:
        # First register IDatasetQuery dependency
        from desktop.modern.application.services.data.dataset_query import DatasetQuery

        container.register_singleton(IDatasetQuery, DatasetQuery)

        # External dependencies (use real data services)
        # Use the real pictograph service with actual TKA dataset
        from desktop.modern.application.services.data.pictograph_data_manager import (
            PictographDataManager,
        )

        # Register the real service for Learn Tab functionality
        # PictographDataManager now has all the methods needed for Learn Tab
        container.register_factory(
            IPictographDataManager,
            lambda: PictographDataManager(
                cache_manager=None, dataset_query=container.resolve(IDatasetQuery)
            ),
        )

        container.register_singleton(IFileSystemService, FileSystemService)

        # Core learn services (singleton pattern for state management)
        container.register_singleton(
            ILessonConfigurationService, LessonConfigurationService
        )
        container.register_singleton(IQuizSessionService, QuizSessionService)
        container.register_factory(
            IQuestionGenerationService,
            lambda: QuestionGenerationService(
                session_service=container.resolve(IQuizSessionService),
                pictograph_data_service=container.resolve(IPictographDataManager),
            ),
        )
        container.register_singleton(IAnswerValidationService, AnswerValidationService)
        container.register_singleton(ILessonProgressService, LessonProgressService)

        # UI and navigation services (singleton for consistency)
        container.register_singleton(ILearnUIService, LearnUIService)
        container.register_singleton(ILearnNavigationService, LearnNavigationService)
        container.register_singleton(ILearnDataService, LearnDataService)

        # Codex services (singleton for state management)
        from desktop.modern.application.services.generation.core.data_and_filtering import (
            PictographDataManager as CodexPictographDataManager,
        )
        from desktop.modern.domain.services.codex import (
            CodexDataService,
            CodexOperationsService,
        )

        # Register PictographDataManager for codex data loading
        container.register_singleton(
            CodexPictographDataManager, CodexPictographDataManager
        )

        # Register CodexDataService with proper pictograph data service injection
        container.register_factory(
            CodexDataService,
            lambda container: CodexDataService(
                pictograph_data_service=container.resolve(CodexPictographDataManager)
            ),
        )
        container.register_singleton(CodexOperationsService, CodexOperationsService)

        # Main learn tab (factory to inject container)
        container.register_factory(LearnTab, lambda: LearnTab(container))

    except Exception as e:
        logger.exception(f"Failed to register learn services: {e}")
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
            container.resolve(LearnTab)
        except Exception as e:
            if "QApplication" in str(e):
                logger.warning("Skipping UI component test in headless environment")
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
        logger.exception(f"Learn service registration validation failed: {e}")
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
                    IPictographDataManager.__name__,  # Now using unified pictograph manager
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
