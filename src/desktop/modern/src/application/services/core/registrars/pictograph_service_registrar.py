"""
Pictograph Service Registrar

Handles registration of pictograph-related services following microservices architecture.
This registrar manages complex pictograph services including data management,
border management, context detection, visibility management, and object pooling.

Services Registered:
- PictographDataManager: Pictograph data management operations
- PictographManager: Core pictograph management
- PictographBorderManager: Border management for pictographs
- PictographContextDetector: Context detection services
- PictographVisibilityService: Visibility management
- PictographPoolManager: High-performance object pooling
"""

import logging
from typing import TYPE_CHECKING

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class PictographServiceRegistrar(BaseServiceRegistrar):
    """
    Registrar for pictograph-related services.

    Complex registrar handling multiple pictograph services including data management,
    border management, context detection, visibility management, and high-performance
    object pooling for optimal performance.
    """

    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""
        return "Pictograph Services"

    def is_critical(self) -> bool:
        """Pictograph services are critical for application functionality."""
        return True

    def register_services(self, container: "DIContainer") -> None:
        """Register pictograph services using pure dependency injection."""
        self._update_progress("Registering pictograph services...")

        # Register core pictograph services
        self._register_core_pictograph_services(container)

        # Register pictograph pool manager (performance critical)
        self._register_pictograph_pool_manager(container)

        # Register pictograph rendering service (performance critical)
        self._register_pictograph_rendering_service(container)

        self._update_progress("Pictograph services registered successfully")

    def _register_core_pictograph_services(self, container: "DIContainer") -> None:
        """Register core pictograph management services."""
        try:
            from core.interfaces.core_services import (
                IPictographBorderManager,
                IPictographContextDetector,
            )
            from core.interfaces.pictograph_services import IPictographValidator

            from application.services.data.pictograph_data_service import (
                IPictographDataManager,
                PictographDataManager,
            )
            from application.services.pictograph.border_manager import (
                PictographBorderManager,
            )
            from application.services.pictograph.context_detection_service import (
                PictographContextDetector,
            )
            from application.services.pictograph.pictograph_position_matcher import (
                PictographCSVManager,
            )
            from application.services.pictograph.pictograph_validator import (
                PictographValidator,
            )

            # PictographScaler removed - direct views handle their own scaling
            from application.services.pictograph.simple_visibility_service import (
                PictographVisibilityService,
            )

            # Register pictograph data manager
            container.register_singleton(IPictographDataManager, PictographDataManager)
            self._mark_service_available("PictographDataManager")

            # Register core pictograph manager
            container.register_singleton(PictographCSVManager, PictographCSVManager)
            self._mark_service_available("PictographManager")

            # Register border manager
            container.register_singleton(
                IPictographBorderManager, PictographBorderManager
            )
            self._mark_service_available("PictographBorderManager")

            # Register context detector
            container.register_singleton(
                IPictographContextDetector, PictographContextDetector
            )
            self._mark_service_available("PictographContextDetector")

            # Register visibility service as singleton to ensure all components use the same instance
            container.register_singleton(
                PictographVisibilityService, PictographVisibilityService
            )
            self._mark_service_available("PictographVisibilityService")

            # Register pictograph validator
            container.register_factory(IPictographValidator, PictographValidator)
            self._mark_service_available("PictographValidator")

            # PictographScaler registration removed - direct views handle their own scaling

        except ImportError as e:
            error_msg = f"Failed to register core pictograph services: {e}"
            logger.error(error_msg)

            # Pictograph services are critical, so re-raise the error
            if self.is_critical():
                raise ImportError(
                    f"Critical pictograph services unavailable: {e}"
                ) from e

    def _register_pictograph_pool_manager(self, container: "DIContainer") -> None:
        """Register pictograph pool manager for high-performance option picker."""
        try:
            from application.services.pictograph_pool_manager import (
                PictographPoolManager,
            )

            # Register pictograph pool manager as singleton for high-performance option picker
            # CRITICAL: Must be singleton so all components use the same initialized pool
            # Use factory registration but ensure singleton behavior by storing instance
            _pool_manager_instance = PictographPoolManager(container=container)
            container.register_instance(PictographPoolManager, _pool_manager_instance)
            self._mark_service_available("PictographPoolManager")

        except ImportError as e:
            error_msg = f"Failed to register pictograph pool manager: {e}"
            logger.error(error_msg)

            # Pool manager is critical for performance, so re-raise the error
            if self.is_critical():
                raise ImportError(
                    f"Critical pictograph pool manager unavailable: {e}"
                ) from e

    def _register_pictograph_rendering_service(self, container: "DIContainer") -> None:
        """Register the pictograph rendering service with microservice dependencies."""
        # TEMPORARILY DISABLED - Import path issues need to be resolved
        self._handle_service_unavailable(
            "Pictograph rendering service",
            ImportError("Temporarily disabled for prop service testing"),
            "Pictograph rendering and visualization",
        )
        return

        try:
            from core.interfaces.pictograph_rendering_services import (
                IPictographRenderingService,
            )

            from application.services.pictograph.pictograph_rendering_service import (
                PictographRenderingService,
            )

            # Register as singleton to ensure only one instance is ever created
            container.register_singleton(
                IPictographRenderingService, PictographRenderingService
            )
            container.register_singleton(
                PictographRenderingService, PictographRenderingService
            )

            self._mark_service_available("PictographRenderingService")

        except ImportError as e:
            error_msg = f"Failed to import pictograph rendering service: {e}"
            logger.error(error_msg)

            if self.is_critical():
                raise ImportError(
                    f"Critical pictograph rendering service unavailable: {e}"
                ) from e
        except Exception as e:
            error_msg = (
                f"Unexpected error registering pictograph rendering service: {e}"
            )
            logger.error(error_msg)
            raise
