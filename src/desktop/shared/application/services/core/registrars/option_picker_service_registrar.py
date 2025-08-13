"""
Option Picker Service Registrar

Handles registration of option picker services following microservices architecture.
This is a complex registrar managing option picker business logic, presentation
components, and high-performance object pooling.

Services Registered:
- OptionProvider: Core option providing logic
- PictographPositionMatcher: Position matching for sequence continuity
- SequenceOptionService: Sequence-aware option filtering
- FramePoolService: Frame object pooling for performance
- OptionPoolService: Option object pooling
- OptionConfigurationService: Option configuration management
- OptionLoader: Option loading operations
- OptionPickerSizeCalculator: Size calculation for responsive layout
- OptionPickerScroll: Main option picker component with injected services
"""

import logging
from typing import TYPE_CHECKING

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class OptionPickerServiceRegistrar(BaseServiceRegistrar):
    """
    Registrar for option picker services.

    Complex registrar handling option picker business logic, presentation
    components, and high-performance object pooling. Demonstrates advanced
    dependency injection patterns with factory functions.
    """

    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""
        return "Option Picker Services"

    def is_critical(self) -> bool:
        """Option picker services are optional for basic application functionality."""
        return False

    def register_services(self, container: "DIContainer") -> None:
        """Register option picker services and components."""
        self._update_progress("Registering option picker services...")

        # Register animation services first (required by option picker)
        self._register_animation_services(container)

        # Register core option picker services
        self._register_core_option_services(container)

        # Register microservices
        self._register_option_microservices(container)

        # Register presentation component factories
        self._register_presentation_components(container)

        self._update_progress("Option picker services registered successfully")

    def _register_animation_services(self, container: "DIContainer") -> None:
        """Register modern animation services for option picker fade transitions."""
        # Check if already registered to prevent duplicate registration
        from desktop.modern.core.interfaces.animation_core_interfaces import (
            IAnimationOrchestrator,
        )

        try:
            container.resolve(IAnimationOrchestrator)
            # Already registered, skip
            self._mark_service_available("ModernAnimationServices")
            return
        except:
            # Not registered yet, proceed
            pass

        try:
            from desktop.modern.application.services.ui.animation.modern_service_registration import (
                setup_modern_animation_services,
            )

            setup_modern_animation_services(container)
            self._mark_service_available("ModernAnimationServices")

        except Exception as e:
            # Animation services are optional - option picker will fall back to direct updates
            logger.warning(f"Animation services not available: {e}")

    def _register_core_option_services(self, container: "DIContainer") -> None:
        """Register core option picker services."""
        try:
            from desktop.modern.application.services.option_picker.option_provider import (
                OptionProvider,
            )
            from desktop.modern.application.services.positioning.arrows.utilities.pictograph_position_matcher import (
                PictographPositionMatcher,
            )
            from desktop.modern.core.interfaces.option_picker_interfaces import (
                IOptionProvider,
            )

            # Register core option provider
            container.register_singleton(IOptionProvider, OptionProvider)
            self._mark_service_available("OptionProvider")

            # Register position matcher (safe to register multiple times)
            container.register_singleton(
                PictographPositionMatcher, PictographPositionMatcher
            )
            self._mark_service_available("PictographPositionMatcher")

        except ImportError as e:
            self._handle_service_unavailable(
                "Core option picker services", e, "Basic option picker functionality"
            )

    def _register_option_microservices(self, container: "DIContainer") -> None:
        """Register option picker microservices."""
        try:
            from desktop.modern.application.services.option_picker.frame_pool_service import (
                FramePoolService,
            )
            from desktop.modern.application.services.option_picker.option_configuration_service import (
                OptionConfigurationService,
            )
            from desktop.modern.application.services.option_picker.option_loader import (
                OptionLoader,
            )
            from desktop.modern.application.services.option_picker.option_picker_size_calculator import (
                OptionPickerSizeCalculator,
            )
            from desktop.modern.application.services.option_picker.option_pool_service import (
                OptionPoolService,
            )
            from desktop.modern.application.services.option_picker.sequence_option_service import (
                SequenceOptionService,
            )
            from desktop.modern.application.services.positioning.arrows.utilities.pictograph_position_matcher import (
                PictographPositionMatcher,
            )

            # Register microservices
            container.register_singleton(FramePoolService, FramePoolService)
            self._mark_service_available("FramePoolService")

            container.register_singleton(OptionPoolService, OptionPoolService)
            self._mark_service_available("OptionPoolService")

            container.register_singleton(
                OptionConfigurationService, OptionConfigurationService
            )
            self._mark_service_available("OptionConfigurationService")

            container.register_singleton(
                OptionPickerSizeCalculator, OptionPickerSizeCalculator
            )
            self._mark_service_available("OptionPickerSizeCalculator")

            # Register services with dependencies
            # Try direct singleton registration first to test
            try:
                position_matcher = PictographPositionMatcher()
                sequence_option_service = SequenceOptionService(
                    position_matcher=position_matcher
                )
                container.register_instance(
                    SequenceOptionService, sequence_option_service
                )
            except Exception as e:
                logger.error(f"Failed to create SequenceOptionService instance: {e}")

                # Fallback to factory registration
                def create_sequence_option_service(c):
                    return SequenceOptionService(
                        position_matcher=c.resolve(PictographPositionMatcher)
                    )

                container.register_factory(
                    SequenceOptionService,
                    create_sequence_option_service,
                )
            self._mark_service_available("SequenceOptionService")

            def create_option_loader(c):
                return OptionLoader(frame_pool_service=c.resolve(FramePoolService))

            container.register_factory(
                OptionLoader,
                create_option_loader,
            )
            self._mark_service_available("OptionLoader")

        except ImportError as e:
            self._handle_service_unavailable(
                "Option picker microservices", e, "Advanced option picker functionality"
            )

    def _register_presentation_components(self, container: "DIContainer") -> None:
        """Register option picker presentation component factories."""
        try:
            from desktop.modern.application.services.option_picker.option_configuration_service import (
                OptionConfigurationService,
            )
            from desktop.modern.application.services.option_picker.option_picker_size_calculator import (
                OptionPickerSizeCalculator,
            )
            from desktop.modern.application.services.option_picker.option_pool_service import (
                OptionPoolService,
            )
            from desktop.modern.application.services.option_picker.sequence_option_service import (
                SequenceOptionService,
            )
            from desktop.modern.presentation.components.option_picker.components.option_picker_scroll import (
                OptionPickerScroll,
            )

            # Register OptionPickerScroll factory with injected microservices
            def create_option_picker_scroll(c):
                try:
                    from desktop.modern.core.interfaces.animation_core_interfaces import (
                        IAnimationOrchestrator,
                    )

                    animation_orchestrator = c.resolve(IAnimationOrchestrator)
                except Exception:
                    # Animation system not available - continue without it
                    animation_orchestrator = None

                return OptionPickerScroll(
                    sequence_option_service=c.resolve(SequenceOptionService),
                    option_pool_service=c.resolve(OptionPoolService),
                    option_sizing_service=c.resolve(OptionPickerSizeCalculator),
                    option_config_service=c.resolve(OptionConfigurationService),
                    animation_orchestrator=animation_orchestrator,
                )

            container.register_factory(OptionPickerScroll, create_option_picker_scroll)
            self._mark_service_available("OptionPickerScroll")

        except ImportError as e:
            self._handle_service_unavailable(
                "Option picker components", e, "Option picker UI components"
            )
