"""
Export Service Interfaces

Defines clean interfaces for the decomposed export services following
the Single Responsibility Principle.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.domain.models.sequence_data import SequenceData


class IExportDirectoryService(ABC):
    """Interface for export directory and file management operations."""

    @abstractmethod
    def get_export_directory(self) -> str:
        """Get the base export directory path."""
        ...

    @abstractmethod
    def ensure_directory_exists(self, directory_path: str) -> None:
        """Ensure the specified directory exists, creating it if necessary."""
        ...

    @abstractmethod
    def validate_directory(self, directory_path: str) -> bool:
        """Validate that directory exists and is writable."""
        ...

    @abstractmethod
    def generate_file_path(
        self,
        word: str,
        beat_count: int,
        file_extension: str = ".png",
        custom_path: Optional[str] = None,
    ) -> str:
        """Generate a file path for export with timestamp and proper naming."""
        ...

    @abstractmethod
    def get_directory_stats(self, directory_path: str) -> Dict[str, Any]:
        """Get statistics about the directory for debugging purposes."""
        ...


class ISequenceDataTransformer(ABC):
    """Interface for transforming sequence data between different formats."""

    @abstractmethod
    def to_image_export_format(self, sequence: SequenceData) -> List[Dict[str, Any]]:
        """Convert SequenceData to format expected by image export services."""
        ...

    @abstractmethod
    def to_legacy_json_format(self, sequence: SequenceData) -> List[Dict[str, Any]]:
        """Convert SequenceData to legacy-compatible JSON format."""
        ...


class ISequenceJsonExporter(ABC):
    """Interface for JSON export operations."""

    @abstractmethod
    def export_to_json_string(self, sequence: SequenceData) -> Tuple[bool, str]:
        """Export sequence as JSON string in legacy-compatible format."""
        ...


class IExportContainerManager(ABC):
    """Interface for managing dependency injection containers during export."""

    @abstractmethod
    def setup_export_container(self) -> DIContainer:
        """Set up and configure a container for export operations."""
        ...

    @abstractmethod
    def set_as_global_container(self, container: DIContainer) -> None:
        """Set the export container as the global container."""
        ...

    @abstractmethod
    def restore_original_container(self) -> None:
        """Restore the original global container."""
        ...

    @abstractmethod
    def get_image_export_service(self, container: DIContainer) -> Any:
        """Get the image export service from the container."""
        ...


class IWorkbenchExportOrchestrator(ABC):
    """Interface for the main export orchestration service."""

    @abstractmethod
    def export_sequence_image(
        self, sequence: SequenceData, file_path: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Export sequence as image file."""
        ...

    @abstractmethod
    def export_sequence_json(self, sequence: SequenceData) -> Tuple[bool, str]:
        """Export sequence as JSON string."""
        ...

    @abstractmethod
    def get_export_directory(self) -> str:
        """Get the directory where exports are saved."""
        ...

    @abstractmethod
    def validate_export_directory(self) -> bool:
        """Validate that export directory exists and is writable."""
        ...

    @abstractmethod
    def get_export_stats(self) -> Dict[str, Any]:
        """Get statistics about exports for debugging."""
        ...
