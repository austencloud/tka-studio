"""
Learn Service Registrar

Specialized registrar for Learn Tab services following the microservices
registration architecture pattern.
"""

import logging
from typing import TYPE_CHECKING, Optional

from ..service_registration_manager import IServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class LearnServiceRegistrar(IServiceRegistrar):
    """
    Registrar for Learn Tab services.

    Handles registration of all learn-related services including:
    - Lesson configuration services
    - Quiz session management
    - Question generation
    - Answer validation
    - Progress tracking
    - UI and navigation services
    - Data persistence
    """

    def __init__(self, progress_callback: Optional[callable] = None):
        """Initialize Learn service registrar."""
        self.progress_callback = progress_callback

    def register_services(self, container: "DIContainer") -> None:
        """Register all Learn Tab services."""
        try:
            self._update_progress("Registering Learn Tab services...")

            # Import and register Learn services
            from desktop.modern.core.dependency_injection.learn_service_registration import (
                register_learn_services,
            )

            register_learn_services(container)

            self._update_progress("Learn Tab services registered successfully")

        except Exception as e:
            logger.error(f"Failed to register Learn Tab services: {e}")
            raise

    def get_domain_name(self) -> str:
        """Get the domain name for this registrar."""
        return "Learn Tab Services"

    def get_registered_services(self) -> list[str]:
        """Get list of service names registered by this registrar."""
        return [
            "ILessonConfigurationService",
            "IQuizSessionService",
            "IQuestionGenerationService",
            "IAnswerValidationService",
            "ILessonProgressService",
            "ILearnUIService",
            "ILearnNavigationService",
            "ILearnDataService",
            "ModernLearnTab",
        ]

    def is_critical(self) -> bool:
        """
        Determine if Learn Tab services are critical.

        Returns:
            False - Learn Tab is optional functionality
        """
        return False

    def get_service_dependencies(self) -> list[str]:
        """
        Get list of service domains this registrar depends on.

        Returns:
            List of dependency domain names
        """
        return [
            "Data Services",  # For file system services
            "Core Services",  # For basic infrastructure
        ]

    def _update_progress(self, message: str) -> None:
        """Update progress if callback is available."""
        if self.progress_callback:
            self.progress_callback(message)
        logger.debug(message)
