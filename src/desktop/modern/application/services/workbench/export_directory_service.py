"""
Export Directory Service

Handles all directory and file management operations for exports.
Follows the Single Responsibility Principle by focusing solely on
file system operations.
"""

from __future__ import annotations

from datetime import datetime
import logging
import os
from pathlib import Path
from typing import Any

from desktop.modern.core.interfaces.export_services import IExportDirectoryService


logger = logging.getLogger(__name__)


class ExportDirectoryService(IExportDirectoryService):
    """
    Service responsible for managing export directories and file paths.

    Responsibilities:
    - Directory creation and validation
    - File path generation with proper naming
    - File system operations and validation
    - Export statistics and debugging info
    """

    def __init__(self, base_export_directory: str | None = None):
        """
        Initialize the directory service.

        Args:
            base_export_directory: Base directory for exports, defaults to project exports folder
        """
        self._base_directory = (
            base_export_directory or self._get_default_export_directory()
        )
        self.ensure_directory_exists(self._base_directory)

        logger.debug(
            f"ExportDirectoryService initialized with directory: {self._base_directory}"
        )

    def get_export_directory(self) -> str:
        """Get the base export directory path."""
        return self._base_directory

    def ensure_directory_exists(self, directory_path: str) -> None:
        """Ensure the specified directory exists, creating it if necessary."""
        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directory ensured: {directory_path}")
        except Exception as e:
            logger.exception(f"Failed to create directory {directory_path}: {e}")
            raise

    def validate_directory(self, directory_path: str) -> bool:
        """Validate that directory exists and is writable."""
        try:
            export_path = Path(directory_path)

            # Check if directory exists
            if not export_path.exists():
                logger.warning(f"Directory does not exist: {directory_path}")
                return False

            # Check if directory is writable
            if not os.access(directory_path, os.W_OK):
                logger.warning(f"Directory is not writable: {directory_path}")
                return False

            return True

        except Exception as e:
            logger.exception(f"Directory validation failed: {e}")
            return False

    def generate_file_path(
        self,
        word: str,
        beat_count: int,
        file_extension: str = ".png",
        custom_path: str | None = None,
    ) -> str:
        """Generate a file path for export with timestamp and proper naming."""
        try:
            if custom_path:
                return custom_path

            # Generate timestamp-based filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{word}_{beat_count}beats_{timestamp}{file_extension}"

            file_path = str(Path(self._base_directory) / filename)
            logger.debug(f"Generated file path: {file_path}")

            return file_path

        except Exception as e:
            logger.exception(f"Failed to generate file path: {e}")
            # Fallback to simple naming
            fallback_filename = f"export_{timestamp}{file_extension}"
            return str(Path(self._base_directory) / fallback_filename)

    def get_directory_stats(self, directory_path: str) -> dict[str, Any]:
        """Get statistics about the directory for debugging purposes."""
        try:
            export_path = Path(directory_path)

            if not export_path.exists():
                return {
                    "directory": directory_path,
                    "exists": False,
                    "file_count": 0,
                    "writable": False,
                }

            files = list(export_path.glob("*"))

            return {
                "directory": directory_path,
                "exists": True,
                "file_count": len(files),
                "writable": os.access(directory_path, os.W_OK),
                "recent_files": [f.name for f in files[-5:]],  # Last 5 files
            }

        except Exception as e:
            logger.exception(f"Failed to get directory stats: {e}")
            return {"directory": directory_path, "error": str(e)}

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
