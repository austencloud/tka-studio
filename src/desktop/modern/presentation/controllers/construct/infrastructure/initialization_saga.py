"""
Saga Pattern Implementation for ConstructTab Initialization

Implements saga pattern using existing command system for transactional
initialization with compensation and rollback capabilities.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
import time
from typing import Any
from uuid import uuid4

from desktop.modern.core.events.domain_events import UIStateChangedEvent
from desktop.modern.core.events.event_bus import IEventBus, get_event_bus


logger = logging.getLogger(__name__)


class SagaStepStatus(Enum):
    """Status of saga step execution."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATED = "compensated"


class SagaStatus(Enum):
    """Overall saga execution status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"


@dataclass
class SagaStepResult:
    """Result of saga step execution."""

    step_id: str
    success: bool
    result: Any | None = None
    error_message: str | None = None
    execution_time_ms: float = 0.0
    compensation_data: dict[str, Any] | None = None


@dataclass
class SagaContext:
    """Context passed to saga steps."""

    saga_id: str
    step_results: dict[str, SagaStepResult] = field(default_factory=dict)
    shared_data: dict[str, Any] = field(default_factory=dict)
    progress_callback: Callable[[int, str], None] | None = None


class SagaStep(ABC):
    """Abstract base class for saga steps."""

    def __init__(self, step_id: str, description: str):
        self.step_id = step_id
        self.description = description
        self.status = SagaStepStatus.PENDING

    @abstractmethod
    async def execute(self, context: SagaContext) -> SagaStepResult:
        """Execute the step."""

    async def compensate(self, context: SagaContext) -> SagaStepResult:
        """Compensate for this step (optional override)."""
        # Default: no compensation needed
        return SagaStepResult(
            step_id=self.step_id, success=True, result="No compensation needed"
        )


class CreateWorkbenchStep(SagaStep):
    """Step to create workbench component."""

    def __init__(self, panel_factory, container):
        super().__init__("create_workbench", "Creating workbench component")
        self.panel_factory = panel_factory
        self.container = container

    async def execute(self, context: SagaContext) -> SagaStepResult:
        """Create workbench panel."""
        start_time = time.time()

        try:
            if context.progress_callback:
                context.progress_callback(10, "Creating workbench...")

            panel, workbench = self.panel_factory.create_workbench_panel()

            # Store results in context
            context.shared_data["workbench_panel"] = panel
            context.shared_data["workbench"] = workbench

            execution_time = (time.time() - start_time) * 1000

            return SagaStepResult(
                step_id=self.step_id,
                success=True,
                result={"workbench": workbench, "panel": panel},
                execution_time_ms=execution_time,
                compensation_data={"workbench_created": True},
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.exception(f"Failed to create workbench: {e}")

            return SagaStepResult(
                step_id=self.step_id,
                success=False,
                error_message=str(e),
                execution_time_ms=execution_time,
            )

    async def compensate(self, context: SagaContext) -> SagaStepResult:
        """Cleanup workbench on failure."""
        try:
            workbench = context.shared_data.get("workbench")
            if workbench and hasattr(workbench, "cleanup"):
                workbench.cleanup()

            # Remove from context
            context.shared_data.pop("workbench", None)
            context.shared_data.pop("workbench_panel", None)

            return SagaStepResult(
                step_id=f"{self.step_id}_compensation",
                success=True,
                result="Workbench cleaned up",
            )
        except Exception as e:
            return SagaStepResult(
                step_id=f"{self.step_id}_compensation",
                success=False,
                error_message=f"Compensation failed: {e}",
            )


class CreatePickersStep(SagaStep):
    """Step to create picker components."""

    def __init__(self, panel_factory):
        super().__init__("create_pickers", "Creating picker components")
        self.panel_factory = panel_factory

    async def execute(self, context: SagaContext) -> SagaStepResult:
        """Create picker components."""
        start_time = time.time()

        try:
            if context.progress_callback:
                context.progress_callback(30, "Creating picker components...")

            # Create start position picker
            start_pos_widget, start_position_picker = (
                self.panel_factory.create_start_position_panel()
            )

            # Create option picker (may be deferred)
            option_widget, option_picker = (
                self.panel_factory.create_option_picker_panel()
            )

            # Store in context
            context.shared_data.update(
                {
                    "start_position_widget": start_pos_widget,
                    "start_position_picker": start_position_picker,
                    "option_widget": option_widget,
                    "option_picker": option_picker,
                }
            )

            execution_time = (time.time() - start_time) * 1000

            return SagaStepResult(
                step_id=self.step_id,
                success=True,
                result={"pickers_created": 2},
                execution_time_ms=execution_time,
                compensation_data={"pickers_created": True},
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.exception(f"Failed to create pickers: {e}")

            return SagaStepResult(
                step_id=self.step_id,
                success=False,
                error_message=str(e),
                execution_time_ms=execution_time,
            )

    async def compensate(self, context: SagaContext) -> SagaStepResult:
        """Cleanup pickers on failure."""
        try:
            # Remove picker references
            context.shared_data.pop("start_position_widget", None)
            context.shared_data.pop("start_position_picker", None)
            context.shared_data.pop("option_widget", None)
            context.shared_data.pop("option_picker", None)

            return SagaStepResult(
                step_id=f"{self.step_id}_compensation",
                success=True,
                result="Pickers cleaned up",
            )
        except Exception as e:
            return SagaStepResult(
                step_id=f"{self.step_id}_compensation",
                success=False,
                error_message=f"Compensation failed: {e}",
            )


class SetupServiceMeshStep(SagaStep):
    """Step to setup service mesh for components."""

    def __init__(self, service_mesh):
        super().__init__("setup_service_mesh", "Setting up service mesh")
        self.service_mesh = service_mesh

    async def execute(self, context: SagaContext) -> SagaStepResult:
        """Setup service mesh for all components."""
        start_time = time.time()

        try:
            if context.progress_callback:
                context.progress_callback(50, "Setting up service mesh...")

            # Get components from context
            components = {
                "workbench": context.shared_data.get("workbench"),
                "start_position_picker": context.shared_data.get(
                    "start_position_picker"
                ),
                "option_picker": context.shared_data.get("option_picker"),
            }

            # Setup service mesh
            proxied_components = self.service_mesh.setup_mesh_for_construct_tab(
                components
            )

            # Store proxied components back in context
            context.shared_data.update(proxied_components)
            context.shared_data["service_mesh"] = self.service_mesh

            execution_time = (time.time() - start_time) * 1000

            return SagaStepResult(
                step_id=self.step_id,
                success=True,
                result={"services_registered": len(proxied_components)},
                execution_time_ms=execution_time,
                compensation_data={"service_mesh_setup": True},
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.exception(f"Failed to setup service mesh: {e}")

            return SagaStepResult(
                step_id=self.step_id,
                success=False,
                error_message=str(e),
                execution_time_ms=execution_time,
            )


class SetupEventIntegrationStep(SagaStep):
    """Step to setup event integration."""

    def __init__(self, event_integration):
        super().__init__("setup_event_integration", "Setting up event integration")
        self.event_integration = event_integration

    async def execute(self, context: SagaContext) -> SagaStepResult:
        """Setup event integration for components."""
        start_time = time.time()

        try:
            if context.progress_callback:
                context.progress_callback(70, "Setting up event integration...")

            # Get components from context
            components = {
                "workbench": context.shared_data.get("workbench"),
                "start_position_picker": context.shared_data.get(
                    "start_position_picker"
                ),
                "option_picker": context.shared_data.get("option_picker"),
                "layout_manager": context.shared_data.get("layout_manager"),
            }

            # Setup event handlers
            self.event_integration.setup_event_handlers(components)

            # Store event integration in context
            context.shared_data["event_integration"] = self.event_integration

            execution_time = (time.time() - start_time) * 1000

            return SagaStepResult(
                step_id=self.step_id,
                success=True,
                result={"event_integration_setup": True},
                execution_time_ms=execution_time,
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.exception(f"Failed to setup event integration: {e}")

            return SagaStepResult(
                step_id=self.step_id,
                success=False,
                error_message=str(e),
                execution_time_ms=execution_time,
            )


class FinalizeInitializationStep(SagaStep):
    """Step to finalize initialization."""

    def __init__(self):
        super().__init__("finalize_initialization", "Finalizing initialization")

    async def execute(self, context: SagaContext) -> SagaStepResult:
        """Finalize initialization process."""
        start_time = time.time()

        try:
            if context.progress_callback:
                context.progress_callback(90, "Finalizing initialization...")

            # Trigger any final setup events
            event_integration = context.shared_data.get("event_integration")
            if event_integration:
                event_integration.publish_ui_state_change(
                    "construct_tab", "initialization_complete", False, True
                )

            if context.progress_callback:
                context.progress_callback(100, "Initialization complete!")

            execution_time = (time.time() - start_time) * 1000

            return SagaStepResult(
                step_id=self.step_id,
                success=True,
                result={"initialization_complete": True},
                execution_time_ms=execution_time,
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.exception(f"Failed to finalize initialization: {e}")

            return SagaStepResult(
                step_id=self.step_id,
                success=False,
                error_message=str(e),
                execution_time_ms=execution_time,
            )


class ConstructTabInitializationSaga:
    """
    Saga for ConstructTab initialization with transactional guarantees.

    Replaces complex timer-based initialization with saga pattern.
    Provides rollback capabilities on failure.
    """

    def __init__(self, event_bus: IEventBus | None = None):
        self.saga_id = str(uuid4())
        self.event_bus = event_bus or get_event_bus()
        self.status = SagaStatus.PENDING
        self.steps: list[SagaStep] = []
        self.executed_steps: list[SagaStep] = []
        self.logger = logging.getLogger(__name__)

    def add_step(self, step: SagaStep):
        """Add step to saga."""
        self.steps.append(step)

    async def execute(self, progress_callback: Callable | None = None) -> bool:
        """Execute saga with rollback on failure."""
        self.status = SagaStatus.IN_PROGRESS
        context = SagaContext(self.saga_id, progress_callback=progress_callback)

        try:
            # Execute all steps
            for step in self.steps:
                self.logger.info(f"Executing step: {step.description}")
                step.status = SagaStepStatus.IN_PROGRESS

                result = await step.execute(context)
                context.step_results[step.step_id] = result

                if result.success:
                    step.status = SagaStepStatus.COMPLETED
                    self.executed_steps.append(step)
                    self._publish_step_completed(step, result)
                else:
                    step.status = SagaStepStatus.FAILED
                    self.logger.error(
                        f"Step {step.step_id} failed: {result.error_message}"
                    )

                    # Rollback executed steps
                    await self._rollback(context)
                    self.status = SagaStatus.FAILED
                    return False

            # All steps completed successfully
            self.status = SagaStatus.COMPLETED
            self._publish_saga_completed(context)
            return True

        except Exception as e:
            self.logger.exception(f"Saga execution failed: {e}")
            await self._rollback(context)
            self.status = SagaStatus.FAILED
            return False

    async def _rollback(self, context: SagaContext):
        """Rollback executed steps in reverse order."""
        self.status = SagaStatus.COMPENSATING

        for step in reversed(self.executed_steps):
            try:
                self.logger.info(f"Compensating step: {step.description}")
                result = await step.compensate(context)

                if result.success:
                    step.status = SagaStepStatus.COMPENSATED
                else:
                    self.logger.error(
                        f"Compensation failed for {step.step_id}: {result.error_message}"
                    )

            except Exception as e:
                self.logger.exception(f"Error during compensation for {step.step_id}: {e}")

        self.status = SagaStatus.COMPENSATED
        self._publish_saga_compensated()

    def _publish_step_completed(self, step: SagaStep, result: SagaStepResult):
        """Publish step completion event."""
        event = UIStateChangedEvent(
            component="saga.construct_tab_initialization",
            state_key="step_completed",
            old_value=None,
            new_value={
                "step_id": step.step_id,
                "description": step.description,
                "execution_time_ms": result.execution_time_ms,
                "success": result.success,
            },
            source="saga",
        )
        self.event_bus.publish(event)

    def _publish_saga_completed(self, context: SagaContext):
        """Publish saga completion event."""
        total_time = sum(r.execution_time_ms for r in context.step_results.values())

        event = UIStateChangedEvent(
            component="saga.construct_tab_initialization",
            state_key="saga_completed",
            old_value=None,
            new_value={
                "saga_id": self.saga_id,
                "total_steps": len(self.steps),
                "total_execution_time_ms": total_time,
                "shared_data_keys": list(context.shared_data.keys()),
            },
            source="saga",
        )
        self.event_bus.publish(event)

    def _publish_saga_compensated(self):
        """Publish saga compensation event."""
        event = UIStateChangedEvent(
            component="saga.construct_tab_initialization",
            state_key="saga_compensated",
            old_value=None,
            new_value={
                "saga_id": self.saga_id,
                "compensated_steps": len(self.executed_steps),
            },
            source="saga",
        )
        self.event_bus.publish(event)


def create_construct_tab_initialization_saga(
    panel_factory, container
) -> ConstructTabInitializationSaga:
    """Factory function to create initialization saga with all steps."""
    saga = ConstructTabInitializationSaga()

    # Add initialization steps in order
    saga.add_step(CreateWorkbenchStep(panel_factory, container))
    saga.add_step(CreatePickersStep(panel_factory))
    saga.add_step(SetupServiceMeshStep(service_mesh))
    saga.add_step(SetupEventIntegrationStep(event_integration))
    saga.add_step(FinalizeInitializationStep())

    return saga
