"""
Workbench Export Service Implementation

Refactored to follow Single Responsibility Principle.
Now acts as an orchestrator that coordinates specialized export services
rather than handling all responsibilities itself.
"""

from __future__ import annotations

from datetime import datetime
import logging
from pathlib import Path

from PyQt6.QtCore import QObject

from desktop.modern.core.interfaces.export_services import (
    IExportContainerManager,
    IExportDirectoryService,
    ISequenceDataTransformer,
    ISequenceJsonExporter,
)
from desktop.modern.core.interfaces.image_export_services import ImageExportOptions
from desktop.modern.domain.models.sequence_data import SequenceData

from .export_container_manager import ExportContainerManager

# Import the concrete implementations
from .export_directory_service import ExportDirectoryService
from .sequence_data_transformer import SequenceDataTransformer
from .sequence_json_exporter import SequenceJsonExporter


logger = logging.getLogger(__name__)


class WorkbenchExportService(QObject):
    """
    Refactored Workbench Export Service - Now an Orchestrator

    This service now coordinates specialized export services rather than
    handling all responsibilities itself. Follows Single Responsibility Principle.

    Responsibilities:
    - Orchestrate export operations using specialized services
    - Maintain backward compatibility with existing API
    - Coordinate error handling across services
    - Provide unified interface for export operations
    """

    def __init__(
        self,
        base_export_directory: str | None = None,
        parent=None,
        # Dependency injection for services (optional for backward compatibility)
        directory_service: IExportDirectoryService | None = None,
        data_transformer: ISequenceDataTransformer | None = None,
        json_exporter: ISequenceJsonExporter | None = None,
        container_manager: IExportContainerManager | None = None,
    ):
        """
        Initialize export service with specialized services.

        Args:
            base_export_directory: Base directory for exports, defaults to project exports folder
            parent: Parent QObject for Qt integration
            directory_service: Service for directory operations (optional)
            data_transformer: Service for data transformation (optional)
            json_exporter: Service for JSON export (optional)
            container_manager: Service for container management (optional)
        """
        super().__init__(parent)

        # Initialize specialized services (with defaults for backward compatibility)
        self._directory_service = directory_service or ExportDirectoryService(
            base_export_directory
        )
        self._data_transformer = data_transformer or SequenceDataTransformer()
        self._json_exporter = json_exporter or SequenceJsonExporter(
            self._data_transformer
        )
        self._container_manager = container_manager or ExportContainerManager()

        logger.debug(
            f"WorkbenchExportService initialized with directory: {self._directory_service.get_export_directory()}"
        )

    def export_sequence_image(
        self, sequence: SequenceData, file_path: str | None = None
    ) -> tuple[bool, str]:
        """
        Export sequence as image file using the modern image export service.

        Now orchestrates the export using specialized services.
        """
        try:
            logger.debug(
                f"WorkbenchExportService.export_sequence_image called with sequence={sequence}"
            )

            # Validate input
            if not sequence:
                logger.error("Export failed: No sequence provided")
                return False, "No sequence data to export"
            if sequence.length == 0:
                logger.error(
                    f"Export failed: Empty sequence (length={sequence.length})"
                )
                return False, "No sequence data to export"

            # Use data transformer to convert sequence
            sequence_data = self._data_transformer.to_image_export_format(sequence)
            word = getattr(sequence, "word", "SEQUENCE")

            # Use directory service to get file path
            if not file_path:
                file_path = self._directory_service.generate_file_path(
                    word, sequence.length, ".png"
                )
                logger.debug(f"Generated file path: {file_path}")

            if not file_path:
                logger.info("Export cancelled: No file path provided")
                return False, "Export cancelled by user"

            # Set up export container using container manager
            export_container = self._container_manager.setup_export_container()

            try:
                # Set container as global for pictograph scene access
                self._container_manager.set_as_global_container(export_container)

                # Get image export service from container
                image_export_service = self._container_manager.get_image_export_service(
                    export_container
                )

                # Create export options
                options = self._create_default_export_options()

                # Perform the actual export
                result = image_export_service.export_sequence_image(
                    sequence_data, word, Path(file_path), options
                )

                if result.success:
                    logger.info(f"Sequence image exported to: {file_path}")
                    return True, file_path
                logger.error(f"Image export failed: {result.error_message}")
                return False, result.error_message

            except Exception as e:
                logger.exception(f"Image export failed with exception: {e}")
                return self._create_fallback_placeholder(
                    file_path, word, len(sequence_data), e
                )

            finally:
                # Always restore original container
                self._container_manager.restore_original_container()

        except Exception as e:
            logger.exception(f"Image export failed: {e}")
            return False, f"Image export failed: {e}"

    def get_export_directory(self) -> str:
        """Get the directory where exports are saved."""
        return self._directory_service.get_export_directory()

    def _create_fallback_placeholder(
        self, file_path: str, word: str, beat_count: int, error: Exception
    ) -> tuple[bool, str]:
        """Create a fallback placeholder file when export fails."""
        try:
            with open(file_path, "w") as f:
                f.write("# TKA Sequence Image Export Placeholder\n")
                f.write(f"# Word: {word}\n")
                f.write(f"# Beats: {beat_count}\n")
                f.write(f"# File: {file_path}\n")
                f.write(f"# Export failed with error: {error}\n")
                f.write("# This is a fallback placeholder file\n")

            logger.info(f"Fallback placeholder file created at: {file_path}")
            return False, f"Real export failed: {error}. Placeholder created."

        except Exception as fallback_error:
            logger.exception(f"Failed to create fallback placeholder: {fallback_error}")
            return False, f"Image export failed: {error}"

    def _create_default_export_options(self) -> ImageExportOptions:
        """Create default export options matching legacy behavior."""
        return ImageExportOptions(
            # Enable all visual elements like legacy
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            add_date=True,
            add_note=True,
            add_beat_numbers=True,
            add_reversal_symbols=True,
            include_start_position=True,
            combined_grids=False,
            # User information
            user_name="TKA User",
            export_date=datetime.now().strftime("%m-%d-%Y"),
            notes="Exported from TKA Modern",
            # High quality settings
            png_compression=1,  # Maximum quality
            high_quality=True,
        )

    def _create_default_export_options(self) -> ImageExportOptions:
        """Create default export options matching legacy behavior."""
        return ImageExportOptions(
            # Enable all visual elements like legacy
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            add_date=True,
            add_note=True,
            add_beat_numbers=True,
            add_reversal_symbols=True,
            include_start_position=True,
            combined_grids=False,
            # User information
            user_name="TKA User",
            export_date=datetime.now().strftime("%m-%d-%Y"),
            notes="Exported from TKA Modern",
            # High quality settings
            png_compression=1,  # Maximum quality
            high_quality=True,
        )
