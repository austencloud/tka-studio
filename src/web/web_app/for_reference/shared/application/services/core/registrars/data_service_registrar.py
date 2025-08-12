"""
Data Service Registrar

Handles registration of data management services following microservices architecture.
This registrar manages multiple related services for data operations, conversion,
and management.

Services Registered:
- CSVReader: CSV file reading operations
- JSONConfigurator: JSON configuration management
- DataManager: Core data management operations
- DatasetQuery: Dataset querying operations
- PictographDataManager: Pictograph-specific data management
- LegacyToModernConverter: Legacy data format conversion
- ModernToLegacyConverter: Modern to legacy data format conversion
"""

import logging
from typing import TYPE_CHECKING

from desktop.modern.core.interfaces.core_services import IDataServiceRegistrar

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class DataServiceRegistrar(BaseServiceRegistrar, IDataServiceRegistrar):
    """
    Registrar for data management services.

    Medium complexity registrar handling multiple related services for data operations,
    conversion, and management. Demonstrates the pattern for registering service groups
    with shared functionality.
    """

    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""
        return "Data Services"

    def is_critical(self) -> bool:
        """Data services are critical for application functionality."""
        return True

    def register_services(self, container: "DIContainer") -> None:
        """Register data management services using pure dependency injection."""
        self._update_progress("Registering data services...")

        # Register core data services
        self._register_core_data_services(container)

        # Register data conversion services
        self._register_conversion_services(container)

        self._update_progress("Data services registered successfully")

    def _register_core_data_services(self, container: "DIContainer") -> None:
        """Register core data management services."""
        try:
            from desktop.modern.core.interfaces.data_services import IDataCacheManager
            from shared.application.services.data.cache_manager import DataCacheManager
            from shared.application.services.data.csv_reader import (
                CSVReader,
                ICSVReader,
            )
            from shared.application.services.data.data_service import (
                DataManager,
                IDataManager,
            )
            from shared.application.services.data.dataset_query import (
                DatasetQuery,
                IDatasetQuery,
            )
            from shared.application.services.data.pictograph_data_manager import (
                IPictographDataManager,
                PictographDataManager,
            )
            from shared.application.services.positioning.props.configuration.json_configuration_service import (
                IJSONConfigurator,
                JSONConfigurator,
            )

            # Register cache manager
            container.register_singleton(DataCacheManager, DataCacheManager)
            container.register_singleton(IDataCacheManager, DataCacheManager)
            self._mark_service_available("DataCacheManager")
            self._mark_service_available("IDataCacheManager")

            # Register core data services
            container.register_singleton(ICSVReader, CSVReader)
            self._mark_service_available("CSVReader")

            container.register_singleton(IJSONConfigurator, JSONConfigurator)
            self._mark_service_available("JSONConfigurator")

            container.register_singleton(IDataManager, DataManager)
            self._mark_service_available("DataManager")

            container.register_singleton(IDatasetQuery, DatasetQuery)
            self._mark_service_available("DatasetQuery")

            container.register_singleton(IPictographDataManager, PictographDataManager)
            self._mark_service_available("PictographDataManager")

        except ImportError as e:
            error_msg = f"Failed to register core data services: {e}"
            logger.error(error_msg)

            # Data services are critical, so re-raise the error
            if self.is_critical():
                raise ImportError(f"Critical data services unavailable: {e}") from e

    def _register_conversion_services(self, container: "DIContainer") -> None:
        """Register data conversion services."""
        try:
            from desktop.modern.core.interfaces.data_services import (
                ILegacyToModernConverter,
                IModernToLegacyConverter,
            )
            from shared.application.services.data.legacy_to_modern_converter import (
                LegacyToModernConverter,
            )
            from shared.application.services.data.modern_to_legacy_converter import (
                ModernToLegacyConverter,
            )

            # Register microservices directly instead of facades
            container.register_singleton(
                LegacyToModernConverter, LegacyToModernConverter
            )
            container.register_singleton(
                ILegacyToModernConverter, LegacyToModernConverter
            )
            self._mark_service_available("LegacyToModernConverter")
            self._mark_service_available("ILegacyToModernConverter")

            container.register_singleton(
                ModernToLegacyConverter, ModernToLegacyConverter
            )
            container.register_singleton(
                IModernToLegacyConverter, ModernToLegacyConverter
            )
            self._mark_service_available("ModernToLegacyConverter")
            self._mark_service_available("IModernToLegacyConverter")

        except ImportError as e:
            error_msg = f"Failed to register conversion services: {e}"
            logger.error(error_msg)

            # Conversion services are critical, so re-raise the error
            if self.is_critical():
                raise ImportError(
                    f"Critical conversion services unavailable: {e}"
                ) from e
