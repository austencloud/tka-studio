"""
Export Service Registration

Registers all export-related services with the dependency injection container.
Follows the Single Responsibility Principle by providing focused service registration.
"""

from __future__ import annotations

import logging

from desktop.modern.application.services.workbench.export_container_manager import (
    ExportContainerManager,
)

# Import concrete implementations
from desktop.modern.application.services.workbench.export_directory_service import (
    ExportDirectoryService,
)
from desktop.modern.application.services.workbench.sequence_data_transformer import (
    SequenceDataTransformer,
)
from desktop.modern.application.services.workbench.sequence_json_exporter import (
    SequenceJsonExporter,
)
from desktop.modern.application.services.workbench.workbench_export_service import (
    WorkbenchExportService,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.export_services import (
    IExportContainerManager,
    IExportDirectoryService,
    ISequenceDataTransformer,
    ISequenceJsonExporter,
    IWorkbenchExportOrchestrator,
)


logger = logging.getLogger(__name__)


def register_export_services(
    container: DIContainer, base_export_directory: str | None = None
) -> None:
    """
    Register all export services with the dependency injection container.

    Args:
        container: The DI container to register services with
        base_export_directory: Optional base directory for exports
    """
    try:
        logger.debug("Registering export services...")

        # Register directory service
        directory_service = ExportDirectoryService(base_export_directory)
        container.register_factory(IExportDirectoryService, lambda: directory_service)

        # Register data transformer service
        data_transformer = SequenceDataTransformer()
        container.register_factory(ISequenceDataTransformer, lambda: data_transformer)

        # Register JSON exporter service (depends on data transformer)
        json_exporter = SequenceJsonExporter(data_transformer)
        container.register_factory(ISequenceJsonExporter, lambda: json_exporter)

        # Register container manager service
        container_manager = ExportContainerManager()
        container.register_factory(IExportContainerManager, lambda: container_manager)

        # Register the main orchestrator service (depends on all other services)
        def create_workbench_export_service():
            return WorkbenchExportService(
                base_export_directory=base_export_directory,
                directory_service=directory_service,
                data_transformer=data_transformer,
                json_exporter=json_exporter,
                container_manager=container_manager,
            )

        container.register_factory(
            IWorkbenchExportOrchestrator, create_workbench_export_service
        )

        # Also register under the concrete class for backward compatibility
        container.register_factory(
            WorkbenchExportService, create_workbench_export_service
        )

        logger.debug("Export services registered successfully")

    except Exception as e:
        logger.error(f"Failed to register export services: {e}")
        raise
