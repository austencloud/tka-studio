"""
Workbench Services - Framework-Agnostic Business Logic

This module contains the framework-agnostic business services for workbench functionality.
These services are completely decoupled from Qt and can be used in any presentation layer.

Components:
- WorkbenchStateManager: State management for workbench
- WorkbenchOperationCoordinator: Operation coordination and execution
- WorkbenchSessionManager: Session restoration management
- BeatSelectionService: Beat selection business logic
"""

from __future__ import annotations

from shared.application.services.workbench.beat_selection_service import (
    BeatSelectionService,
)
from shared.application.services.workbench.workbench_operation_coordinator import (
    OperationResult,
    OperationType,
    WorkbenchOperationCoordinator,
)
from shared.application.services.workbench.workbench_session_manager import (
    SessionRestorationPhase,
    SessionRestorationResult,
    WorkbenchSessionManager,
)
from shared.application.services.workbench.workbench_state_manager import (
    StateChangeResult,
    WorkbenchState,
    WorkbenchStateManager,
)


__all__ = [
    # Business Services
    "BeatSelectionService",
    "WorkbenchStateManager",
    "WorkbenchOperationCoordinator",
    "WorkbenchSessionManager",
    # State Management
    "WorkbenchState",
    "StateChangeResult",
    # Operation Coordination
    "OperationType",
    "OperationResult",
    # Session Management
    "SessionRestorationPhase",
    "SessionRestorationResult",
]
