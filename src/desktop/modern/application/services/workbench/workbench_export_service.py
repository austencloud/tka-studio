"""
Workbench Export Service Implementation

Framework-agnostic implementation of workbench export operations.
Handles image and JSON export functionality for sequences.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import (
    register_image_export_services,
)
from desktop.modern.core.interfaces.image_export_services import (
    ImageExportOptions,
    ISequenceImageExporter,
)
from desktop.modern.domain.models.sequence_data import SequenceData
from PyQt6.QtCore import QObject

logger = logging.getLogger(__name__)


class WorkbenchExportService(QObject):
    """
    Framework-agnostic implementation of workbench export operations.

    Responsibilities:
    - Export sequences as images (via existing services)
    - Export sequences as JSON with proper formatting
    - Manage export directories and file naming
    - Provide validation and error handling
    """

    def __init__(self, base_export_directory: Optional[str] = None, parent=None):
        """
        Initialize export service.

        Args:
            base_export_directory: Base directory for exports, defaults to project exports folder
            parent: Parent QObject for Qt integration
        """
        super().__init__(parent)
        self._base_directory = (
            base_export_directory or self._get_default_export_directory()
        )
        self._ensure_export_directory_exists()

        # Initialize the actual image export service using DI container
        self._container = DIContainer()
        register_image_export_services(self._container)
        self._image_export_service = self._container.resolve(ISequenceImageExporter)

        # Store reference to original global container for restoration
        self._original_container = None

        logger.debug(
            f"WorkbenchExportService initialized with directory: {self._base_directory}"
        )

    def _get_default_export_directory(self) -> str:
        """Get default export directory based on project structure."""
        try:
            # Navigate to project root and create exports directory
            current_dir = Path(__file__).parent
            project_root = current_dir

            # Find project root by looking for known files
            while project_root.parent != project_root:
                if (project_root / "main.py").exists() or (
                    project_root / "pyproject.toml"
                ).exists():
                    break
                project_root = project_root.parent

            exports_dir = project_root / "exports" / "workbench"
            return str(exports_dir)

        except Exception as e:
            logger.warning(
                f"Could not determine project root, using temp directory: {e}"
            )
            return str(Path.home() / "TKA_Exports")

    def _ensure_export_directory_exists(self) -> None:
        """Ensure export directory exists."""
        try:
            Path(self._base_directory).mkdir(parents=True, exist_ok=True)
            logger.debug(f"Export directory ensured: {self._base_directory}")
        except Exception as e:
            logger.error(
                f"Failed to create export directory {self._base_directory}: {e}"
            )
            raise

    def export_sequence_image(
        self, sequence: SequenceData, file_path: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Export sequence as image file using the modern image export service.
        """
        try:
            logger.debug(
                f"WorkbenchExportService.export_sequence_image called with sequence={sequence}"
            )
            if not sequence:
                logger.error("Export failed: No sequence provided")
                return False, "No sequence data to export"
            if sequence.length == 0:
                logger.error(
                    f"Export failed: Empty sequence (length={sequence.length})"
                )
                return False, "No sequence data to export"

            # Convert SequenceData to the format expected by the image export service
            sequence_data = self._convert_sequence_to_export_format(sequence)

            # Get the current word (for now, use a default or extract from sequence)
            word = getattr(sequence, "word", "SEQUENCE")

            # Show file dialog to get save location
            if not file_path:
                logger.debug(
                    f"Showing file dialog for word='{word}', length={sequence.length}"
                )
                try:
                    file_path = self._get_save_file_path(word, sequence.length)
                    logger.debug(f"File dialog result: file_path='{file_path}'")
                except Exception as e:
                    logger.error(f"File dialog failed: {e}")
                    # Fallback to automatic file path if dialog fails
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    default_filename = f"{word}_{sequence.length}beats_{timestamp}.png"
                    file_path = str(Path(self._base_directory) / default_filename)
                    logger.info(f"Using fallback file path: {file_path}")

                if not file_path:
                    logger.info("Export cancelled: User cancelled file dialog")
                    return False, "Export cancelled by user"

            # Create export options with default settings
            options = self._create_default_export_options()

            # Try actual image rendering with proper error handling
            logger.info("Attempting real image export with error handling...")

            try:
                # CRITICAL FIX: Set export container as global so pictograph scenes can access services
                self._set_export_container_as_global()

                # Use the modern image export service
                result = self._image_export_service.export_sequence_image(
                    sequence_data, word, Path(file_path), options
                )

                if result.success:
                    logger.info(f"Sequence image exported to: {file_path}")
                    # Don't auto-open file - let the test handle display
                    return True, file_path
                else:
                    logger.error(f"Image export failed: {result.error_message}")
                    return False, result.error_message

            except Exception as e:
                logger.error(f"Image export failed with exception: {e}")

                # Fallback to placeholder if real export fails
                logger.info("Falling back to placeholder file due to export error...")
                try:
                    with open(file_path, "w") as f:
                        f.write(f"# TKA Sequence Image Export Placeholder\n")
                        f.write(f"# Word: {word}\n")
                        f.write(f"# Beats: {len(sequence_data)}\n")
                        f.write(f"# File: {file_path}\n")
                        f.write(f"# Export failed with error: {e}\n")
                        f.write(f"# This is a fallback placeholder file\n")

                    logger.info(f"Fallback placeholder file created at: {file_path}")
                    return False, f"Real export failed: {e}. Placeholder created."

                except Exception as fallback_error:
                    logger.error(
                        f"Failed to create fallback placeholder: {fallback_error}"
                    )
                    return False, f"Image export failed: {e}"

            finally:
                # CRITICAL: Always restore original container
                self._restore_original_container()

        except Exception as e:
            logger.error(f"Image export failed: {e}")
            return False, f"Image export failed: {e}"

    def export_sequence_json(self, sequence: SequenceData) -> Tuple[bool, str]:
        """
        Export sequence as JSON string.
        """
        try:
            if not sequence:
                return False, "No sequence data to export"

            # Create comprehensive JSON representation
            export_data = {
                "metadata": {
                    "export_timestamp": datetime.now().isoformat(),
                    "export_version": "1.0",
                    "sequence_length": sequence.length,
                },
                "sequence": {"length": sequence.length, "beats": []},
            }

            # Add beat data
            for i, beat in enumerate(sequence.beats):
                beat_data = {
                    "index": i,
                    "letter": getattr(beat, "letter", f"Beat_{i}"),
                    # Add more beat properties as needed
                    "data": str(beat) if hasattr(beat, "__dict__") else repr(beat),
                }
                export_data["sequence"]["beats"].append(beat_data)

            # Convert to formatted JSON
            json_string = json.dumps(export_data, indent=2, ensure_ascii=False)

            logger.info(f"Sequence JSON exported: {len(json_string)} characters")
            return True, json_string

        except Exception as e:
            logger.error(f"JSON export failed: {e}")
            return False, f"JSON export failed: {e}"

    def get_export_directory(self) -> str:
        """Get the directory where exports are saved."""
        return self._base_directory

    def validate_export_directory(self) -> bool:
        """Validate that export directory exists and is writable."""
        try:
            export_path = Path(self._base_directory)

            # Check if directory exists
            if not export_path.exists():
                logger.warning(
                    f"Export directory does not exist: {self._base_directory}"
                )
                return False

            # Check if directory is writable
            if not os.access(self._base_directory, os.W_OK):
                logger.warning(
                    f"Export directory is not writable: {self._base_directory}"
                )
                return False

            return True

        except Exception as e:
            logger.error(f"Export directory validation failed: {e}")
            return False

    def get_export_stats(self) -> dict:
        """Get statistics about exports for debugging."""
        try:
            export_path = Path(self._base_directory)

            if not export_path.exists():
                return {
                    "directory": self._base_directory,
                    "exists": False,
                    "file_count": 0,
                    "writable": False,
                }

            files = list(export_path.glob("*"))

            return {
                "directory": self._base_directory,
                "exists": True,
                "file_count": len(files),
                "writable": os.access(self._base_directory, os.W_OK),
                "recent_files": [f.name for f in files[-5:]],  # Last 5 files
            }

        except Exception as e:
            logger.error(f"Failed to get export stats: {e}")
            return {"directory": self._base_directory, "error": str(e)}

    def _convert_sequence_to_export_format(
        self, sequence: SequenceData
    ) -> List[Dict[str, Any]]:
        """Convert SequenceData to the format expected by the image export service."""
        sequence_data = []

        for i, beat in enumerate(sequence.beats):
            # Convert beat to dictionary format expected by image export
            beat_data = {
                "beat_number": beat.beat_number,
                "letter": self._extract_letter_from_beat(beat),
                "start_pos": self._extract_start_position_from_beat(beat),
                "end_pos": self._extract_end_position_from_beat(beat),
                "blue_attributes": self._extract_motion_attributes(beat, "blue"),
                "red_attributes": self._extract_motion_attributes(beat, "red"),
                "pictograph_data": (
                    beat.pictograph_data.to_dict() if beat.pictograph_data else None
                ),
                "is_blank": beat.is_blank,
                "blue_reversal": beat.blue_reversal,
                "red_reversal": beat.red_reversal,
            }
            sequence_data.append(beat_data)

        return sequence_data

    def _get_save_file_path(self, word: str, beat_count: int) -> Optional[str]:
        """Show file dialog to get save location for the image."""
        try:
            # Create default filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"{word}_{beat_count}beats_{timestamp}.png"

            # TEMPORARY: Skip file dialog for testing - use automatic path
            # TODO: Re-enable file dialog once Qt integration is working properly
            auto_path = str(Path(self._base_directory) / default_filename)
            logger.info(f"Using automatic file path (dialog bypassed): {auto_path}")
            return auto_path

            # Show save dialog (commented out for testing)
            # file_path, _ = QFileDialog.getSaveFileName(
            #     None,  # parent
            #     "Save Sequence Image",
            #     str(Path(self._base_directory) / default_filename),
            #     "PNG Images (*.png);;All Files (*)",
            # )
            #
            # return file_path if file_path else None

        except Exception as e:
            logger.error(f"Failed to show save dialog: {e}")
            return None

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

    def _extract_letter_from_beat(self, beat: "BeatData") -> str:
        """Extract letter from beat data."""
        # Try to get letter from pictograph data first
        if beat.pictograph_data and hasattr(beat.pictograph_data, "letter"):
            return beat.pictograph_data.letter

        # Fallback to metadata or default
        return beat.metadata.get("letter", "A")

    def _extract_start_position_from_beat(self, beat: "BeatData") -> str:
        """Extract start position from beat data."""
        if beat.pictograph_data and hasattr(beat.pictograph_data, "start_position"):
            return beat.pictograph_data.start_position

        return beat.metadata.get("start_pos", "alpha")

    def _extract_end_position_from_beat(self, beat: "BeatData") -> str:
        """Extract end position from beat data."""
        if beat.pictograph_data and hasattr(beat.pictograph_data, "end_position"):
            return beat.pictograph_data.end_position

        return beat.metadata.get("end_pos", "beta")

    def _extract_motion_attributes(
        self, beat: "BeatData", color: str
    ) -> Dict[str, Any]:
        """Extract motion attributes for a specific color from beat data."""
        attributes = {}

        if beat.pictograph_data and hasattr(beat.pictograph_data, "motions"):
            motion = beat.pictograph_data.motions.get(color)
            if motion:
                attributes = {
                    "motion_type": getattr(motion, "motion_type", ""),
                    "prop_rot_dir": getattr(motion, "prop_rot_dir", ""),
                    "turns": getattr(motion, "turns", 0),
                    "start_ori": getattr(motion, "start_ori", ""),
                    "end_ori": getattr(motion, "end_ori", ""),
                }

        # Add reversal information
        if color == "blue":
            attributes["reversal"] = beat.blue_reversal
        elif color == "red":
            attributes["reversal"] = beat.red_reversal

        return attributes

    def _set_export_container_as_global(self) -> None:
        """Set the export container as the global container for pictograph scene access."""
        try:
            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
                set_container,
            )

            # Store the current global container
            self._original_container = get_container()

            # Set our export container as the global one
            set_container(self._container, force=True)

            logger.debug("Export container set as global for pictograph scene access")

        except Exception as e:
            logger.warning(f"Failed to set export container as global: {e}")

    def _restore_original_container(self) -> None:
        """Restore the original global container."""
        try:
            if self._original_container is not None:
                from desktop.modern.core.dependency_injection.di_container import set_container

                # Restore the original container
                set_container(self._original_container, force=True)
                self._original_container = None

                logger.debug("Original container restored")

        except Exception as e:
            logger.warning(f"Failed to restore original container: {e}")
