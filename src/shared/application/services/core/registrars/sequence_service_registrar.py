"""
Sequence Service Registrar

Handles registration of sequence-related services following microservices architecture.
This registrar manages services for sequence operations, validation, persistence,
and management.

Services Registered:
- BeatFactory: Factory for creating beat objects
- SequencePersister: Sequence persistence operations
- SequenceRepository: Sequence data repository
- SequenceValidator: Sequence validation logic
- SequenceLoader: Sequence loading operations
- SequenceBeatOperations: Beat manipulation operations
- SequenceStartPositionManager: Start position management
"""

import logging
from typing import TYPE_CHECKING

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class SequenceServiceRegistrar(BaseServiceRegistrar):
    """
    Registrar for sequence-related services.

    Medium complexity registrar handling sequence operations, validation,
    persistence, and management services. These services are critical for
    sequence functionality in the application.
    """

    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""
        return "Sequence Services"

    def is_critical(self) -> bool:
        """Sequence services are critical for application functionality."""
        return True

    def register_services(self, container: "DIContainer") -> None:
        """Register sequence services with interface bindings."""
        self._update_progress("Registering sequence services...")

        try:
            # Import sequence service interfaces and implementations
            from desktop.modern.core.interfaces.sequence_data_services import (
                ISequenceLoader,
                ISequenceStartPositionManager,
            )
            from shared.application.services.sequence.beat_factory import (
                BeatFactory,
                IBeatFactory,
            )
            from shared.application.services.sequence.sequence_beat_operations_service import (
                SequenceBeatOperationsService,
            )
            from shared.application.services.sequence.sequence_loader_service import (
                SequenceLoaderService,
            )
            from shared.application.services.sequence.sequence_persister import (
                ISequencePersister,
                SequencePersister,
            )
            from shared.application.services.sequence.sequence_repository import (
                ISequenceRepository,
                SequenceRepository,
            )
            from shared.application.services.sequence.sequence_start_position_service import (
                SequenceStartPositionService,
            )
            from shared.application.services.sequence.sequence_validator import (
                ISequenceValidator,
                SequenceValidator,
            )

            # Register sequence services with interfaces
            container.register_singleton(IBeatFactory, BeatFactory)
            self._mark_service_available("BeatFactory")

            container.register_singleton(ISequencePersister, SequencePersister)
            self._mark_service_available("SequencePersister")

            container.register_singleton(ISequenceRepository, SequenceRepository)
            self._mark_service_available("SequenceRepository")

            container.register_singleton(ISequenceValidator, SequenceValidator)
            self._mark_service_available("SequenceValidator")

            # Register pure sequence services with interfaces
            container.register_singleton(ISequenceLoader, SequenceLoaderService)
            self._mark_service_available("SequenceLoaderService")

            container.register_singleton(
                ISequenceStartPositionManager, SequenceStartPositionService
            )
            self._mark_service_available("SequenceStartPositionService")

            # Register pure beat operations service (no interface yet)
            container.register_singleton(
                SequenceBeatOperationsService, SequenceBeatOperationsService
            )
            self._mark_service_available("SequenceBeatOperationsService")

            # Register sequence state tracker service
            # Note: This needs event_bus and command_processor dependencies
            # For now, we'll register it as a factory that gets resolved later
            from desktop.modern.presentation.adapters.qt.sequence_state_tracker_adapter import (
                QtSequenceStateTrackerAdapter,
            )

            # We need to register the Qt adapter since that's what the system expects
            # The adapter will create the pure service internally
            container.register_factory(
                QtSequenceStateTrackerAdapter,
                lambda: self._create_sequence_state_tracker_adapter(),
            )
            # String-based registration removed - use class-based registration above
            self._mark_service_available("SequenceStateTracker")

            self._update_progress("Sequence services registered successfully")

        except ImportError as e:
            error_msg = f"Failed to register sequence services: {e}"
            logger.error(error_msg)

            # Sequence services are critical, so re-raise the error
            if self.is_critical():
                raise ImportError(f"Critical sequence services unavailable: {e}") from e

    def _create_sequence_state_tracker_adapter(self):
        """Create a sequence state tracker adapter with required dependencies."""
        try:
            from desktop.modern.presentation.adapters.qt.sequence_state_tracker_adapter import (
                QtSequenceStateTrackerAdapter,
            )

            # Create adapter without event bus dependencies for now
            # TODO: Add proper Qt signal coordination later
            return QtSequenceStateTrackerAdapter(event_bus=None, command_processor=None)
        except Exception as e:
            logger.error(f"Failed to create sequence state tracker adapter: {e}")
            return None
