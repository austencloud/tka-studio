"""
Event System Registrar

Handles registration of event system services following microservices architecture.
This registrar manages event bus and command processing infrastructure with
graceful degradation for backward compatibility.

Services Registered:
- EventBus: Inter-component communication
- CommandProcessor: Command processing infrastructure
"""

import logging
from typing import TYPE_CHECKING

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class EventSystemRegistrar(BaseServiceRegistrar):
    """
    Registrar for event system services.

    Simple registrar handling event bus and command processing infrastructure.
    Uses graceful degradation to maintain backward compatibility when event
    system is not available.
    """

    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""
        return "Event System"

    def is_critical(self) -> bool:
        """Event system is optional for backward compatibility."""
        return False

    def register_services(self, container: "DIContainer") -> None:
        """Register event system and command infrastructure."""
        self._update_progress("Registering event system...")

        try:
            from core.commands import CommandProcessor
            from core.events import IEventBus, get_event_bus

            # Get or create event bus
            event_bus = get_event_bus()
            container.register_instance(IEventBus, event_bus)
            self._mark_service_available("EventBus")

            # Register command processor
            command_processor = CommandProcessor(event_bus)
            container.register_instance(CommandProcessor, command_processor)
            self._mark_service_available("CommandProcessor")

            self._update_progress("Event system registered successfully")

        except ImportError as e:
            self._handle_service_unavailable(
                "Event system",
                e,
                "Inter-component communication and command processing",
            )
