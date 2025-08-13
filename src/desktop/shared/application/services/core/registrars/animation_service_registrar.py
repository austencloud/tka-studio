"""
Animation Service Registrar

Specialized registrar for animation services following the microservices architecture.
Registers the modern animation system with the DI container.
"""

import logging

from ..service_registration_manager import BaseServiceRegistrar

logger = logging.getLogger(__name__)


class AnimationServiceRegistrar(BaseServiceRegistrar):
    """
    Registrar for animation services.

    Registers the modern animation system including:
    - IAnimationOrchestrator (main interface)
    - LegacyFadeManagerWrapper (for migration)
    - Animation engine and adapters
    """

    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""
        return "Animation Services"

    def is_critical(self) -> bool:
        """Animation services are optional - application can run without them."""
        return False

    def register_services(self, container) -> None:
        """Register animation services with the DI container."""
        # Check if already registered to prevent spam
        from desktop.modern.core.interfaces.animation_core_interfaces import (
            IAnimationOrchestrator,
        )

        try:
            container.resolve(IAnimationOrchestrator)
            # Already registered, skip
            return
        except:
            # Not registered yet, proceed
            pass

        try:
            self._update_progress("Registering modern animation system...")

            # Import and register modern animation services
            from desktop.modern.application.services.ui.animation.modern_service_registration import (
                setup_modern_animation_services,
            )

            setup_modern_animation_services(container)

            # Mark services as available
            self._mark_service_available("animation_orchestrator")
            self._mark_service_available("legacy_fade_wrapper")

            self._update_progress("Modern animation system registered successfully")
            logger.info("✅ Modern animation system registered successfully")

        except Exception as e:
            logger.warning(f"Failed to register animation services: {e}")
            self._mark_service_unavailable("animation_orchestrator")
            self._mark_service_unavailable("legacy_fade_wrapper")

            # Don't raise - animation services are optional
            self._handle_service_unavailable(
                "Animation Services", e, "Widget fade transitions will not be available"
            )

    def get_registered_services(self) -> list[str]:
        """Get list of service names registered by this registrar."""
        return [
            "IAnimationOrchestrator",
            "LegacyFadeManagerWrapper",
            "AnimationEngine",
            "QtAnimationAdapters",
        ]
