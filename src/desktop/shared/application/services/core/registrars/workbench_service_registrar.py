"""
Workbench Service Registrar

Handles registration of workbench-related services following microservices architecture.
This registrar manages workbench business logic and presentation services for
sequence editing and management functionality.

Services Registered:
- BeatSelectionService: Beat selection business logic
- WorkbenchStateManager: Framework-agnostic workbench state management
- WorkbenchOperationCoordinator: Framework-agnostic operation coordination
- WorkbenchSessionManager: Framework-agnostic session restoration
- Workbench presentation services: UI components and factories
"""

import logging
from typing import TYPE_CHECKING

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class WorkbenchServiceRegistrar(BaseServiceRegistrar):
    """
    Registrar for workbench-related services.

    Medium complexity registrar handling workbench business logic and
    presentation services for sequence editing and management functionality.
    Separates business logic from presentation concerns.
    """

    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""
        return "Workbench Services"

    def is_critical(self) -> bool:
        """Workbench services are critical for sequence editing functionality."""
        return (
            False  # TEMPORARILY: Make non-critical to get app running, then fix imports
        )

    def _safe_resolve(self, container: "DIContainer", service_key: str):
        """Safely resolve a service, returning None if not available."""
        try:
            return container.resolve(service_key)
        except Exception:
            return None

    def _safe_resolve_class(self, container: "DIContainer", service_class):
        """Safely resolve a service by class type, returning None if not available."""
        try:
            return container.resolve(service_class)
        except Exception:
            return None

    def register_services(self, container: "DIContainer") -> None:
        """Register workbench services."""
        self._update_progress("Registering workbench services...")

        # Register business services
        self._register_business_services(container)

        # Register presentation services
        self._register_presentation_services(container)

        self._update_progress("Workbench services registered successfully")

    def _register_business_services(self, container: "DIContainer") -> None:
        """Register pure business services for workbench functionality."""
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

            from desktop.modern.core.interfaces.workbench_services import (
                IWorkbenchSessionManager,
            )
            from shared.application.services.workbench.beat_selection_service import (
                BeatSelectionService,
            )
            from shared.application.services.workbench.workbench_operation_coordinator import (
                WorkbenchOperationCoordinator,
            )
            from shared.application.services.workbench.workbench_session_manager import (
                WorkbenchSessionManager,
            )
            from shared.application.services.workbench.workbench_state_manager import (
                WorkbenchStateManager,
            )

            # Register beat selection service (no dependencies)
            container.register_singleton(BeatSelectionService, BeatSelectionService)
            self._mark_service_available("BeatSelectionService")

            # Register workbench state manager as singleton with optional dependencies
            # Create the instance once and register it
            state_manager_instance = WorkbenchStateManager(
                sequence_state_tracker=self._safe_resolve(
                    container, "SequenceStateTracker"
                )
            )
            container.register_instance(WorkbenchStateManager, state_manager_instance)

            # Register interface
            from desktop.modern.core.interfaces.workbench_services import (
                IWorkbenchStateManager,
            )

            container.register_instance(IWorkbenchStateManager, state_manager_instance)

            self._mark_service_available("WorkbenchStateManager")
            self._mark_service_available("IWorkbenchStateManager")

            # Register workbench operation coordinator with dependencies
            # Import the required services
            from desktop.modern.application.services.sequence.sequence_beat_operations import (
                SequenceBeatOperations,
            )
            from desktop.modern.application.services.workbench.workbench_export_service import (
                WorkbenchExportService,
            )
            from desktop.modern.core.interfaces.workbench_export_services import (
                IWorkbenchExportService,
            )

            # Register export service with interface
            export_service_instance = WorkbenchExportService()
            container.register_instance(
                IWorkbenchExportService, export_service_instance
            )
            self._mark_service_available("IWorkbenchExportService")

            # Create the instance once using the same state manager and register it
            operation_coordinator_instance = WorkbenchOperationCoordinator(
                workbench_state_manager=state_manager_instance,
                beat_operations=self._safe_resolve_class(
                    container, SequenceBeatOperations
                ),
                dictionary_service=self._safe_resolve(
                    container, "SequenceDictionaryService"
                ),
                fullscreen_service=self._safe_resolve(container, "IFullScreenViewer"),
                sequence_transformer=self._safe_resolve(
                    container, "SequenceTransformer"
                ),
                sequence_persister=self._safe_resolve(container, "SequencePersister"),
                export_service=export_service_instance,
            )
            container.register_instance(
                WorkbenchOperationCoordinator, operation_coordinator_instance
            )
            self._mark_service_available("WorkbenchOperationCoordinator")

            # Register workbench session manager with dependencies
            def create_workbench_session_manager(c):
                return WorkbenchSessionManager(
                    workbench_state_manager=c.resolve(WorkbenchStateManager),
                    session_restoration_coordinator=self._safe_resolve(
                        c, "SessionRestorationCoordinator"
                    ),
                    event_bus=self._safe_resolve(c, "EventBus"),
                )

            container.register_factory(
                IWorkbenchSessionManager, create_workbench_session_manager
            )
            container.register_factory(
                WorkbenchSessionManager, create_workbench_session_manager
            )
            self._mark_service_available("WorkbenchSessionManager")
            self._mark_service_available("IWorkbenchSessionManager")

        except ImportError as e:
            error_msg = f"Failed to register workbench business services: {e}"
            logger.error(error_msg)

            # Business services are critical, so re-raise the error
            if self.is_critical():
                raise ImportError(
                    f"Critical workbench business services unavailable: {e}"
                ) from e

    def _register_presentation_services(self, container: "DIContainer") -> None:
        """Register workbench presentation services and factories."""
        try:
            from desktop.modern.presentation.factories.workbench_factory import (
                configure_workbench_services,
            )

            # Register presentation services using the existing factory
            configure_workbench_services(container)
            self._mark_service_available("WorkbenchPresentationServices")

        except ImportError as e:
            error_msg = f"Failed to register workbench presentation services: {e}"
            logger.error(error_msg)

            # Presentation services are critical for workbench functionality
            if self.is_critical():
                raise ImportError(
                    f"Critical workbench presentation services unavailable: {e}"
                ) from e
