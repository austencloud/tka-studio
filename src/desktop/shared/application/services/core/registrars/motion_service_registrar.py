"""
Motion Service Registrar

Handles registration of motion-related services following microservices architecture.
This is a simple registrar with only one service, demonstrating the pattern for
single-responsibility service registration.

Services Registered:
- OrientationCalculator: Calculates motion orientations
"""

import logging
from typing import TYPE_CHECKING

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class MotionServiceRegistrar(BaseServiceRegistrar):
    """
    Registrar for motion-related services.

    Simple registrar demonstrating the pattern for focused, single-responsibility
    service registration. Handles only motion and orientation calculation services.
    """

    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""
        return "Motion Services"

    def is_critical(self) -> bool:
        """Motion services are critical for application functionality."""
        return True

    def register_services(self, container: "DIContainer") -> None:
        """Register motion services using pure dependency injection."""
        self._update_progress("Registering motion services...")

        try:
            from desktop.modern.application.services.motion.orientation_calculator import (
                IOrientationCalculator,
                OrientationCalculator,
            )

            # Register orientation calculator as singleton
            container.register_singleton(IOrientationCalculator, OrientationCalculator)
            self._mark_service_available("OrientationCalculator")

            self._update_progress("Motion services registered successfully")

        except ImportError as e:
            error_msg = f"Failed to register motion services: {e}"
            logger.error(error_msg)
            self._mark_service_unavailable("OrientationCalculator")

            # Motion services are critical, so re-raise the error
            if self.is_critical():
                raise ImportError(f"Critical motion services unavailable: {e}") from e
            else:
                self._handle_service_unavailable(
                    "Motion Services", e, "Motion orientation calculations"
                )
