"""
Graph Editor Service Registrar

Handles registration of graph editor services following microservices architecture.
This is a simple registrar with only one service, demonstrating the pattern for
single-responsibility service registration.

Services Registered:
- GraphEditorStateManager: Centralized state management for graph editor
"""

import logging
from typing import TYPE_CHECKING

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class GraphEditorServiceRegistrar(BaseServiceRegistrar):
    """
    Registrar for graph editor services.

    Simple registrar demonstrating the pattern for focused, single-responsibility
    service registration. Handles only graph editor state management services.
    """

    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""
        return "Graph Editor Services"

    def is_critical(self) -> bool:
        """Graph editor services are optional for basic application functionality."""
        return False

    def register_services(self, container: "DIContainer") -> None:
        """Register graph editor services using pure dependency injection."""
        self._update_progress("Registering graph editor services...")

        try:
            from shared.application.services.graph_editor.graph_editor_state_manager import (
                GraphEditorStateManager,
            )

            # Register graph editor state service as singleton for centralized state management
            container.register_singleton(
                GraphEditorStateManager, GraphEditorStateManager
            )
            self._mark_service_available("GraphEditorStateManager")

            self._update_progress("Graph editor services registered successfully")

        except ImportError as e:
            error_msg = f"Failed to register graph editor services: {e}"
            logger.warning(error_msg)
            self._handle_service_unavailable(
                "Graph Editor Services",
                e,
                "Graph editor state management and functionality",
            )
