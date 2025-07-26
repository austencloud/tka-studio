"""
Pictograph Service Registrar

Handles registration of pictograph-related services following microservices architecture.
This registrar manages complex pictograph services including data management,
border management, context detection, and visibility management.

Services Registered:
- PictographDataManager: Pictograph data management operations
- PictographManager: Core pictograph management
- PictographBorderManager: Border management for pictographs
- PictographContextDetector: Context detection services
- PictographVisibilityService: Visibility management
"""

import logging
from typing import TYPE_CHECKING

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

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
        return False  # TEMPORARILY: Make non-critical to test TKA scaling fixes

    def register_services(self, container: "DIContainer") -> None:
        """Register pictograph services using pure dependency injection."""
        self._update_progress("Registering pictograph services...")

        # Register core pictograph services
        self._register_core_pictograph_services(container)

        # Register pictograph rendering service (performance critical)
        self._register_pictograph_rendering_service(container)

        self._update_progress("Pictograph services registered successfully")

    def _register_core_pictograph_services(self, container: "DIContainer") -> None:
        """Register core pictograph management services."""
        try:
            from desktop.modern.core.interfaces.core_services import (
                IPictographBorderManager,
                IPictographContextDetector,
            )
            from desktop.modern.core.interfaces.pictograph_services import (
                IPictographValidator,
            )
            from shared.application.services.data.pictograph_data_manager import (
                IPictographDataManager,
                PictographDataManager,
            )
            from shared.application.services.pictograph.border_manager import (
                PictographBorderManager,
            )
            from shared.application.services.pictograph.context_detection_service import (
                PictographContextDetector,
            )
            from shared.application.services.pictograph.pictograph_csv_manager import (
                PictographCSVManager,
            )
            from shared.application.services.pictograph.pictograph_validator import (
                PictographValidator,
            )

            # PictographScaler removed - direct views handle their own scaling
            from shared.application.services.pictograph.simple_visibility_service import (
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

    def _register_pictograph_rendering_service(self, container: "DIContainer") -> None:
        """Register the pictograph rendering service with microservice dependencies."""
        try:
            # Temporarily ensure shared src is accessible for imports
            import sys
            from pathlib import Path

            # Find shared src path
            current_file = Path(__file__).resolve()
            tka_root = current_file.parents[8]  # Navigate up to TKA root
            shared_src = tka_root / "src"

            # Temporarily move shared src to front of path for imports
            shared_src_str = str(shared_src)
            if shared_src.exists() and shared_src_str in sys.path:
                sys.path.remove(shared_src_str)
                sys.path.insert(0, shared_src_str)

            from desktop.modern.application.services.pictograph.pictograph_rendering_service import (
                PictographRenderingService,
            )
            from desktop.modern.core.interfaces.pictograph_rendering_services import (
                IPictographRenderingService,
            )

            # Register as factory to ensure proper initialization with asset manager
            def create_pictograph_rendering_service():
                from desktop.modern.application.adapters.qt_pictograph_adapter import (
                    create_qt_pictograph_adapter,
                )
                from shared.application.services.core.pictograph_renderer import (
                    create_pictograph_renderer,
                )
                from shared.application.services.pictograph.asset_management.pictograph_asset_manager import (
                    PictographAssetManager,
                )

                # Create asset manager with proper implementation
                asset_manager = PictographAssetManager()

                # Create Qt adapter with asset manager
                qt_adapter = create_qt_pictograph_adapter(asset_manager)

                # Create core renderer with asset manager
                core_renderer = create_pictograph_renderer(asset_manager=asset_manager)

                # Create service with all dependencies
                return PictographRenderingService(
                    asset_manager=asset_manager,
                    core_service=core_renderer,
                    qt_adapter=qt_adapter,
                )

            container.register_factory(
                IPictographRenderingService, create_pictograph_rendering_service
            )
            container.register_factory(
                PictographRenderingService, create_pictograph_rendering_service
            )

            self._mark_service_available("PictographRenderingService")

        except ImportError as e:
            error_msg = f"Failed to import pictograph rendering service: {e}"
            logger.error(error_msg)

            if self.is_critical():
                raise ImportError(
                    f"Critical pictograph rendering service unavailable: {e}"
                ) from e
            else:
                self._handle_service_unavailable(
                    "Pictograph rendering service",
                    e,
                    "Pictograph rendering and visualization",
                )
        except Exception as e:
            error_msg = (
                f"Unexpected error registering pictograph rendering service: {e}"
            )
            logger.error(error_msg)
            raise
