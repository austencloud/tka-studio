"""
Export Container Manager Service

Handles dependency injection container management during export operations.
Follows the Single Responsibility Principle by focusing solely on
container lifecycle management.
"""

from __future__ import annotations

import logging

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import (
    register_image_export_services,
)
from desktop.modern.core.interfaces.export_services import IExportContainerManager
from desktop.modern.core.interfaces.image_export_services import ISequenceImageExporter


logger = logging.getLogger(__name__)


class ExportContainerManager(IExportContainerManager):
    """
    Service responsible for managing dependency injection containers during export.

    Responsibilities:
    - Set up and configure export containers
    - Manage global container switching
    - Restore original containers after export
    - Provide access to export services
    """

    def __init__(self):
        """Initialize the container manager."""
        self._original_container: DIContainer | None = None
        self._export_container: DIContainer | None = None
        logger.debug("ExportContainerManager initialized")

    def setup_export_container(self) -> DIContainer:
        """
        Set up and configure a container for export operations.

        Returns:
            Configured DIContainer with export services registered
        """
        try:
            # Create a new container for export operations
            container = DIContainer()

            # Register image export services
            register_image_export_services(container)

            # Store reference to the export container
            self._export_container = container

            logger.debug("Export container set up successfully")
            return container

        except Exception as e:
            logger.exception(f"Failed to set up export container: {e}")
            raise

    def set_as_global_container(self, container: DIContainer) -> None:
        """
        Set the export container as the global container.

        This is necessary for pictograph scenes to access export services.

        Args:
            container: The container to set as global
        """
        try:
            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
                set_container,
            )

            # Store the current global container for restoration
            self._original_container = get_container()

            # Set our export container as the global one
            set_container(container, force=True)

            logger.debug("Export container set as global for pictograph scene access")

        except Exception as e:
            logger.warning(f"Failed to set export container as global: {e}")
            # Don't raise here as this is not critical for basic export functionality

    def restore_original_container(self) -> None:
        """Restore the original global container."""
        try:
            if self._original_container is not None:
                from desktop.modern.core.dependency_injection.di_container import (
                    set_container,
                )

                # Restore the original container
                set_container(self._original_container, force=True)
                self._original_container = None

                logger.debug("Original container restored")

        except Exception as e:
            logger.warning(f"Failed to restore original container: {e}")
            # Don't raise here as this is cleanup code

    def get_image_export_service(
        self, container: DIContainer
    ) -> ISequenceImageExporter:
        """
        Get the image export service from the container.

        Args:
            container: The container to resolve the service from

        Returns:
            The image export service instance
        """
        try:
            return container.resolve(ISequenceImageExporter)
        except Exception as e:
            logger.exception(f"Failed to resolve image export service: {e}")
            raise
