"""
Act Data Service

Service for managing act data persistence, loading, and saving.
Handles JSON serialization and file management for acts.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from desktop.modern.core.interfaces.write_services import ActData, IActDataService


logger = logging.getLogger(__name__)


class ActDataService(IActDataService):
    """
    Service for managing act data and persistence.

    Handles saving/loading acts as JSON files and provides
    thumbnail generation and file management capabilities.
    """

    def __init__(self, acts_directory: Path | None = None):
        """
        Initialize the act data service.

        Args:
            acts_directory: Directory where acts are stored (default: data/acts)
        """
        if acts_directory is None:
            # Default to TKA data/acts directory
            from pathlib import Path

            desktop_root = Path(__file__).parent.parent.parent.parent.parent
            acts_directory = desktop_root / "data" / "acts"

        self.acts_directory = Path(acts_directory)
        self.acts_directory.mkdir(parents=True, exist_ok=True)

        logger.info(f"ActDataService initialized with directory: {self.acts_directory}")

    def save_act(self, act: ActData, file_path: Path) -> bool:
        """
        Save an act to a JSON file.

        Args:
            act: The act data to save
            file_path: Path to save the act to

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure the file has .json extension
            if not file_path.suffix or file_path.suffix.lower() != ".json":
                file_path = file_path.with_suffix(".json")

            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Convert act to dictionary and save as JSON
            act_dict = act.to_dict()

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(act_dict, f, indent=2, ensure_ascii=False)

            logger.info(f"Successfully saved act '{act.name}' to {file_path}")
            return True

        except Exception as e:
            logger.exception(f"Failed to save act '{act.name}' to {file_path}: {e}")
            return False

    def load_act(self, file_path: Path) -> ActData | None:
        """
        Load an act from a JSON file.

        Args:
            file_path: Path to the act file

        Returns:
            ActData if successful, None otherwise
        """
        try:
            if not file_path.exists():
                logger.error(f"Act file does not exist: {file_path}")
                return None

            with open(file_path, encoding="utf-8") as f:
                act_dict = json.load(f)

            act = ActData.from_dict(act_dict)
            logger.info(f"Successfully loaded act '{act.name}' from {file_path}")
            return act

        except Exception as e:
            logger.exception(f"Failed to load act from {file_path}: {e}")
            return None

    def get_available_acts(self, acts_directory: Path | None = None) -> list[Path]:
        """
        Get list of available act files in a directory.

        Args:
            acts_directory: Directory to search (defaults to self.acts_directory)

        Returns:
            List of paths to act files
        """
        if acts_directory is None:
            acts_directory = self.acts_directory

        try:
            if not acts_directory.exists():
                logger.warning(f"Acts directory does not exist: {acts_directory}")
                return []

            # Find all JSON files in the directory
            act_files = list(acts_directory.glob("*.json"))

            # Sort by modification time (newest first)
            act_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

            logger.info(f"Found {len(act_files)} act files in {acts_directory}")
            return act_files

        except Exception as e:
            logger.exception(f"Failed to get available acts from {acts_directory}: {e}")
            return []

    def delete_act(self, file_path: Path) -> bool:
        """
        Delete an act file.

        Args:
            file_path: Path to the act file to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            if not file_path.exists():
                logger.warning(f"Act file does not exist, cannot delete: {file_path}")
                return False

            file_path.unlink()
            logger.info(f"Successfully deleted act file: {file_path}")
            return True

        except Exception as e:
            logger.exception(f"Failed to delete act file {file_path}: {e}")
            return False

    def create_act_thumbnail(self, act: ActData) -> bytes | None:
        """
        Create a thumbnail image for an act.

        Args:
            act: The act to create a thumbnail for

        Returns:
            Thumbnail image as bytes, or None if failed
        """
        try:
            # For now, return None - thumbnail generation would require
            # rendering the first few sequences of the act
            # This could be implemented later using the existing pictograph rendering system
            logger.debug(f"Thumbnail generation not implemented for act: {act.name}")
            return None

        except Exception as e:
            logger.exception(f"Failed to create thumbnail for act '{act.name}': {e}")
            return None

    def get_acts_directory(self) -> Path:
        """Get the acts directory path."""
        return self.acts_directory

    def set_acts_directory(self, directory: Path) -> None:
        """Set the acts directory path."""
        self.acts_directory = Path(directory)
        self.acts_directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Acts directory changed to: {self.acts_directory}")

    def get_act_info(self, file_path: Path) -> dict[str, Any] | None:
        """
        Get basic info about an act without fully loading it.

        Args:
            file_path: Path to the act file

        Returns:
            Dictionary with act info (name, description, sequence_count, etc.)
        """
        try:
            if not file_path.exists():
                return None

            with open(file_path, encoding="utf-8") as f:
                act_dict = json.load(f)

            return {
                "name": act_dict.get("name", "Untitled Act"),
                "description": act_dict.get("description", ""),
                "sequence_count": len(act_dict.get("sequences", [])),
                "has_music": bool(act_dict.get("music_file")),
                "file_size": file_path.stat().st_size,
                "modified_time": file_path.stat().st_mtime,
            }

        except Exception as e:
            logger.exception(f"Failed to get act info from {file_path}: {e}")
            return None
