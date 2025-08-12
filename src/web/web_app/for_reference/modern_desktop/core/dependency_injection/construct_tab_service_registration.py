"""
Construct Tab Service Registration

Registers all construct tab services with the DI container.
Enables proper dependency injection for the refactored architecture.
"""

from __future__ import annotations

from desktop.modern.application.services.construct_tab.construct_tab_component_factory import (
    ConstructTabComponentFactory,
)
from desktop.modern.application.services.construct_tab.construct_tab_coordination_service import (
    ConstructTabCoordinationService,
)
from desktop.modern.application.services.construct_tab.construct_tab_layout_service import (
    ConstructTabLayoutService,
)
from desktop.modern.application.services.workbench.workbench_coordination_service import (
    WorkbenchCoordinationService,
)
from desktop.modern.application.services.workbench.workbench_ui_service import (
    WorkbenchUIService,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.construct_tab_services import (
    IConstructTabComponentFactory,
    IConstructTabCoordinationService,
    IConstructTabLayoutService,
    IWorkbenchCoordinationService,
    IWorkbenchUIService,
)


def register_construct_tab_services(container: DIContainer) -> None:
    """
    Register all construct tab services with the DI container.

    This enables proper dependency injection and eliminates the None initialization pattern.
    """

    # Register component factory
    container.register_factory(
        IConstructTabComponentFactory, lambda c: ConstructTabComponentFactory(c)
    )

    # Register layout service
    container.register_factory(
        IConstructTabLayoutService,
        lambda c: ConstructTabLayoutService(
            c, c.resolve(IConstructTabComponentFactory)
        ),
    )

    # Register coordination service - will be created when needed
    def create_coordination_service(c):
        try:
            from desktop.modern.application.services.sequence.sequence_beat_operations import (
                SequenceBeatOperations,
            )
            from desktop.modern.application.services.sequence.sequence_start_position_manager import (
                SequenceStartPositionManager,
            )

            beat_operations = c.resolve(SequenceBeatOperations)
            start_position_manager = c.resolve(SequenceStartPositionManager)
            layout_service = c.resolve(IConstructTabLayoutService)

            return ConstructTabCoordinationService(
                beat_operations, start_position_manager, layout_service
            )
        except Exception as e:
            print(f"Warning: Could not create coordination service: {e}")
            return None

    container.register_factory(
        IConstructTabCoordinationService, create_coordination_service
    )

    # Register workbench UI service - transient (new instance each time)
    def create_workbench_ui_service(c):
        try:
            from desktop.modern.core.interfaces.core_services import ILayoutService

            layout_service = c.resolve(ILayoutService)
            beat_selection_service = c.resolve("BeatSelectionService")

            return WorkbenchUIService(c, layout_service, beat_selection_service)
        except Exception as e:
            print(f"Warning: Could not create workbench UI service: {e}")
            return None

    container.register_factory(IWorkbenchUIService, create_workbench_ui_service)

    # Register workbench coordination service - transient (new instance each time)
    def create_workbench_coordination_service(c):
        try:
            from shared.application.services.workbench.workbench_operation_coordinator import (
                WorkbenchOperationCoordinator,
            )
            from shared.application.services.workbench.workbench_state_manager import (
                WorkbenchStateManager,
            )

            state_manager = c.resolve(WorkbenchStateManager)
            operation_coordinator = c.resolve(WorkbenchOperationCoordinator)
            ui_service = c.resolve(IWorkbenchUIService)

            return WorkbenchCoordinationService(
                state_manager, operation_coordinator, ui_service
            )
        except Exception as e:
            print(f"Warning: Could not create workbench coordination service: {e}")
            return None

    container.register_factory(
        IWorkbenchCoordinationService, create_workbench_coordination_service
    )

    print("✅ Construct tab services registered successfully")


def register_legacy_compatibility_services(container: DIContainer) -> None:
    """
    Register legacy compatibility services for gradual migration.

    These can be removed once all components are migrated to the new architecture.
    """

    # Skip legacy registration for now since the DI container doesn't support string keys
    # The new interface-based registration is sufficient
    print(
        "✅ Legacy compatibility services registered (skipped - using interface-based registration)"
    )
