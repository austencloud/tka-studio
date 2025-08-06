"""
Browse Action Handler - Handles all user actions for Browse Tab

This class is responsible for:
- Processing edit, save, delete, and fullscreen actions
- Managing user confirmations and dialogs
- Coordinating with services for action execution
- Providing feedback to users on action results
"""

from __future__ import annotations

import logging
from pathlib import Path

from PyQt6.QtWidgets import QFileDialog, QMessageBox, QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.browse_services import ISequenceDeletionService
from desktop.modern.core.interfaces.image_export_services import (
    ImageExportOptions,
    ISequenceImageExporter,
    ISequenceMetadataExtractor,
)
from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.components.ui.full_screen.full_screen_overlay import (
    FullScreenOverlay,
)


logger = logging.getLogger(__name__)


class BrowseActionHandler:
    """
    Handles all user actions for the Browse tab.

    Processes edit, save, delete, and fullscreen actions with proper
    error handling and user feedback.
    """

    def __init__(
        self,
        container: DIContainer,
        sequences_dir: Path,
        parent_widget: QWidget,
    ):
        """
        Initialize the browse action handler.

        Args:
            container: Dependency injection container
            sequences_dir: Directory containing sequence files
            parent_widget: Parent widget for dialogs
        """
        self.sequences_dir = sequences_dir
        self.parent_widget = parent_widget

        # Initialize services from DI container
        try:
            self.image_export_service = container.resolve(ISequenceImageExporter)
            self.metadata_extractor = container.resolve(ISequenceMetadataExtractor)
            self.deletion_service = container.resolve(ISequenceDeletionService)
        except Exception as e:
            logger.error(f"❌ Failed to initialize services from DI container: {e}")
            self._initialize_fallback_services()

    def handle_edit_sequence(self, sequence_id: str) -> str:
        """
        Handle edit sequence action.

        Args:
            sequence_id: ID of the sequence to edit

        Returns:
            The sequence_id to emit for opening in construct tab
        """
        return sequence_id

    def handle_save_image(
        self,
        sequence_data: SequenceData,
        current_variation_index: int,
    ) -> bool:
        """
        Handle save image action using the modern image export service.

        Args:
            sequence_data: The sequence data to save
            current_variation_index: Index of the current variation

        Returns:
            True if save was successful, False otherwise
        """
        try:
            if not self.image_export_service:
                QMessageBox.warning(
                    self.parent_widget,
                    "Service Unavailable",
                    "Image export service is not available.",
                )
                return False

            if not sequence_data:
                QMessageBox.warning(
                    self.parent_widget, "No Sequence", "Please select a sequence first."
                )
                return False

            # Get the thumbnail path for the current variation
            if (
                not sequence_data.thumbnails
                or current_variation_index < 0
                or current_variation_index >= len(sequence_data.thumbnails)
            ):
                QMessageBox.warning(
                    self.parent_widget,
                    "No Image",
                    "No image available for the selected variation.",
                )
                return False

            current_thumbnail_path = Path(
                sequence_data.thumbnails[current_variation_index]
            )

            # Extract sequence JSON from thumbnail metadata
            sequence_json_data = self.metadata_extractor.extract_metadata(
                current_thumbnail_path
            )
            if not sequence_json_data:
                QMessageBox.warning(
                    self.parent_widget,
                    "No Metadata",
                    "Could not extract sequence data from the selected image.",
                )
                return False

            # Create export options (using default settings for now)
            export_options = ImageExportOptions(
                add_word=True,
                add_user_info=True,
                add_difficulty_level=True,
                include_start_position=True,
            )

            # Use file dialog to get save location
            suggested_name = f"{sequence_data.word}_exported.png"
            file_path, _ = QFileDialog.getSaveFileName(
                self.parent_widget,
                "Save Sequence Image",
                suggested_name,
                "PNG Images (*.png);;All Files (*)",
            )

            if file_path:
                output_path = Path(file_path)

                # Extract sequence beats from metadata
                sequence_beats = sequence_json_data.get("sequence", [])

                # Export the image
                result = self.image_export_service.export_sequence_image(
                    sequence_beats, sequence_data.word, output_path, export_options
                )

                if result.success:
                    QMessageBox.information(
                        self.parent_widget,
                        "Export Successful",
                        f"Image saved successfully to:\n{output_path}",
                    )
                    return True
                QMessageBox.critical(
                    self.parent_widget,
                    "Export Failed",
                    f"Failed to export image:\n{result.error_message}",
                )
                logger.error(f"❌ Failed to export image: {result.error_message}")
                return False

            return False  # User cancelled dialog

        except Exception as e:
            logger.error(f"Error during image save: {e}", exc_info=True)
            QMessageBox.critical(
                self.parent_widget,
                "Export Error",
                f"An error occurred while saving the image:\n{e!s}",
            )
            return False

    def handle_delete_variation(
        self,
        sequence_data: SequenceData,
        current_variation_index: int,
    ) -> bool:
        """
        Handle delete variation action using the deletion service.

        Args:
            sequence_data: The sequence data containing the variation to delete
            current_variation_index: Index of the variation to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            if not sequence_data:
                QMessageBox.warning(
                    self.parent_widget, "No Sequence", "Please select a sequence first."
                )
                return False

            if not sequence_data.thumbnails:
                QMessageBox.warning(
                    self.parent_widget,
                    "No Variations",
                    "No variations available to delete.",
                )
                return False

            # Perform deletion using the service
            success = self.deletion_service.delete_variation(
                sequence_data.word,
                sequence_data.thumbnails,
                current_variation_index,
                self.parent_widget,  # parent widget for dialogs
            )

            return success

        except Exception as e:
            logger.error(f"Error during variation deletion: {e}", exc_info=True)
            QMessageBox.critical(
                self.parent_widget,
                "Deletion Error",
                f"An error occurred while deleting the variation:\n{e!s}",
            )
            return False

    def handle_fullscreen_view(
        self,
        current_thumbnails: list,
        current_index: int,
    ) -> bool:
        """
        Handle fullscreen view action using the full screen overlay.

        Args:
            current_thumbnails: List of thumbnail paths
            current_index: Index of the current thumbnail

        Returns:
            True if fullscreen was opened successfully, False otherwise
        """
        try:
            if (
                not current_thumbnails
                or current_index < 0
                or current_index >= len(current_thumbnails)
            ):
                QMessageBox.warning(
                    self.parent_widget,
                    "No Image",
                    "No image available for fullscreen view.",
                )
                return False

            current_thumbnail_path = Path(current_thumbnails[current_index])

            if not current_thumbnail_path.exists():
                QMessageBox.warning(
                    self.parent_widget,
                    "Image Not Found",
                    f"Image file not found:\n{current_thumbnail_path}",
                )
                return False

            # Create and show full screen overlay
            overlay = FullScreenOverlay(self.parent_widget)
            overlay.show_image(current_thumbnail_path)
            return True

        except Exception as e:
            logger.error(f"Error during fullscreen view: {e}", exc_info=True)
            QMessageBox.critical(
                self.parent_widget,
                "Fullscreen Error",
                f"An error occurred while opening fullscreen view:\n{e!s}",
            )
            return False

    def _initialize_fallback_services(self):
        """Initialize fallback services if DI container services are not available."""
        logger.warning("Initializing fallback services")

        # Create basic fallback implementations
        from shared.application.services.image_export.sequence_metadata_extractor import (
            SequenceMetadataExtractor,
        )

        from desktop.modern.application.services.browse.sequence_deletion_service import (
            SequenceDeletionService,
        )

        self.metadata_extractor = SequenceMetadataExtractor()
        self.deletion_service = SequenceDeletionService(self.sequences_dir)
        self.image_export_service = None  # Will show error if used
