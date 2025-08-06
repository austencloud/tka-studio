"""
Simplified Sequence Workbench

Dramatically reduced workbench component that delegates to focused services.
This replaces the 469-line workbench with a clean, focused component.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget
from shared.application.services.workbench.workbench_operation_coordinator import (
    WorkbenchOperationCoordinator,
)
from shared.application.services.workbench.workbench_session_manager import (
    WorkbenchSessionManager,
)
from shared.application.services.workbench.workbench_state_manager import (
    WorkbenchStateManager,
)

from desktop.modern.application.services.workbench.workbench_coordination_service import (
    WorkbenchCoordinationService,
)
from desktop.modern.application.services.workbench.workbench_ui_service import (
    WorkbenchUIService,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.core_services import ILayoutService
from desktop.modern.domain.models import BeatData, SequenceData
from desktop.modern.presentation.components.component_base import ViewableComponentBase


if TYPE_CHECKING:
    from shared.application.services.workbench.beat_selection_service import (
        BeatSelectionService,
    )


class SimplifiedSequenceWorkbench(ViewableComponentBase):
    """
    Simplified sequence workbench using service-based architecture.

    Responsibilities (ONLY):
    - Service coordination
    - Signal forwarding
    - Component lifecycle management

    All business logic and UI management delegated to services.
    """

    # Qt signals for parent coordination (forwarded from services)
    sequence_modified = pyqtSignal(object)
    operation_completed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    beat_selected = pyqtSignal(int)

    def __init__(
        self,
        container: DIContainer,
        layout_service: ILayoutService,
        beat_selection_service: BeatSelectionService,
        parent: QWidget | None = None,
    ):
        """Initialize workbench with injected services."""
        super().__init__(container, parent)

        # Resolve business services
        self._state_manager: WorkbenchStateManager = container.resolve(
            WorkbenchStateManager
        )
        self._operation_coordinator: WorkbenchOperationCoordinator = container.resolve(
            WorkbenchOperationCoordinator
        )
        self._session_manager: WorkbenchSessionManager = container.resolve(
            WorkbenchSessionManager
        )

        # Create focused services
        self._ui_service = WorkbenchUIService(
            container, layout_service, beat_selection_service
        )
        self._coordination_service = WorkbenchCoordinationService(
            self._state_manager, self._operation_coordinator, self._ui_service
        )

        # Session restoration tracking
        self._subscription_ids: list[str] = []

    def initialize(self) -> None:
        """Initialize the workbench component."""
        try:
            # Setup session subscriptions
            self._setup_session_subscriptions()

            # Setup UI through service
            self._widget = self._ui_service.setup_workbench_ui(self.parent())

            # Setup coordination through service
            self._coordination_service.setup_workbench_signals(self)

            # Connect service signals to our signals (forwarding)
            self._connect_service_signals()

            # Mark as initialized
            self._initialized = True
            self.component_ready.emit()

        except Exception as e:
            self.emit_error(f"Failed to initialize workbench: {e}", e)
            raise

    def get_widget(self) -> QWidget:
        """Get the main widget for this component."""
        if not self._widget:
            raise RuntimeError("Workbench not initialized - call initialize() first")
        return self._widget

    def _connect_service_signals(self):
        """Connect service signals to our public signals."""
        self._coordination_service.sequence_modified.connect(
            self.sequence_modified.emit
        )
        self._coordination_service.operation_completed.connect(
            self.operation_completed.emit
        )
        self._coordination_service.error_occurred.connect(self.error_occurred.emit)
        self._coordination_service.beat_selected.connect(self.beat_selected.emit)

    def _setup_session_subscriptions(self):
        """Setup session restoration subscriptions."""
        if self._session_manager:
            # Subscribe to session events for restoration
            subscription_id = self._session_manager.subscribe_to_restoration_events(
                self._on_session_restored
            )
            if subscription_id:
                self._subscription_ids.append(subscription_id)

    def _on_session_restored(self, session_data):
        """Handle session restoration."""
        try:
            if "sequence" in session_data:
                sequence = session_data["sequence"]
                self._coordination_service.update_workbench_state(sequence)
        except Exception as e:
            self.emit_error(f"Session restoration failed: {e}", e)

    # Public API methods (delegate to services)

    def set_sequence(self, sequence: SequenceData) -> None:
        """Set the current sequence."""
        self._coordination_service.update_workbench_state(sequence)

    def get_sequence(self) -> SequenceData | None:
        """Get the current sequence."""
        return self._state_manager.get_current_sequence()

    def set_start_position(
        self,
        start_position_data: BeatData,
        from_restoration: bool = False,
    ) -> None:
        """Set the start position."""
        result = self._state_manager.set_start_position(
            start_position_data, from_restoration
        )
        if result.success:
            self._ui_service.update_sequence_display(
                self._state_manager.get_current_sequence()
            )

    def get_start_position_data(self) -> BeatData | None:
        """Get the current start position."""
        return self._state_manager.get_start_position()

    def execute_operation(self, operation_type: str, **kwargs) -> None:
        """Execute a workbench operation."""
        self._coordination_service.handle_workbench_operation(operation_type, **kwargs)

    def cleanup(self) -> None:
        """Clean up workbench resources."""
        try:
            # Clean up session subscriptions
            if self._session_manager and self._subscription_ids:
                self._session_manager.cleanup_event_subscriptions(
                    self._subscription_ids
                )
                self._subscription_ids.clear()

            # Call parent cleanup
            super().cleanup()

        except Exception as e:
            self.emit_error(f"Error during cleanup: {e}", e)
