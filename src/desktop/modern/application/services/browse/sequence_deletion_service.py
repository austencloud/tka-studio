"""
Sequence Deletion Service

Modern service for deleting sequence variations and managing file system cleanup.
Provides confirmation dialogs and maintains data integrity after deletion.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
import shutil

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QWidget


logger = logging.getLogger(__name__)


class SequenceDeletionService(QObject):
    """
    Service for handling sequence variation deletion with proper cleanup.

    Features:
    - User confirmation dialogs
    - File system cleanup (remove empty directories)
    - Variation number fixing for sequential numbering
    - Signal emission for UI updates
    """

    # Signals
    variation_deleted = pyqtSignal(str, int)  # word, variation_index
    sequence_deleted = pyqtSignal(str)  # word
    deletion_cancelled = pyqtSignal()

    def __init__(self, sequences_directory: Path, parent: QObject | None = None):
        """
        Initialize the deletion service.

        Args:
            sequences_directory: Root directory containing sequence files
            parent: Parent QObject for signal handling
        """
        super().__init__(parent)
        self.sequences_directory = Path(sequences_directory)
        logger.info(
            f"SequenceDeletionService initialized with directory: {sequences_directory}"
        )

    def delete_variation(
        self,
        word: str,
        thumbnails: list[str],
        variation_index: int,
        parent_widget: QWidget | None = None,
    ) -> bool:
        """
        Delete a specific variation of a sequence.

        Args:
            word: The sequence word/name
            thumbnails: List of thumbnail file paths
            variation_index: Index of variation to delete
            parent_widget: Parent widget for dialogs

        Returns:
            True if deletion was successful, False if cancelled or failed
        """
        try:
            logger.info(f"Attempting to delete variation {variation_index} of '{word}'")

            # Validate inputs
            if (
                not thumbnails
                or variation_index < 0
                or variation_index >= len(thumbnails)
            ):
                logger.error(
                    f"Invalid variation index {variation_index} for word '{word}'"
                )
                return False

            file_path = thumbnails[variation_index]
            if not Path(file_path).exists():
                logger.error(f"File not found: {file_path}")
                return False

            # Show confirmation dialog
            if not self._confirm_deletion(word, variation_index, parent_widget):
                logger.info("Deletion cancelled by user")
                self.deletion_cancelled.emit()
                return False

            # Perform the deletion
            success = self._delete_file(file_path)
            if not success:
                return False

            # Remove from thumbnails list
            remaining_thumbnails = thumbnails.copy()
            remaining_thumbnails.pop(variation_index)

            # Check if this was the last variation
            if not remaining_thumbnails:
                # Delete the entire word directory
                word_directory = Path(file_path).parent
                success = self._delete_word_directory(word_directory)
                if success:
                    logger.info(
                        f"Deleted entire sequence '{word}' (no variations remaining)"
                    )
                    self.sequence_deleted.emit(word)
                return success
            # Clean up empty directories and fix numbering
            self._cleanup_empty_directories()
            self._fix_variation_numbering(word, remaining_thumbnails)

            logger.info(f"Successfully deleted variation {variation_index} of '{word}'")
            self.variation_deleted.emit(word, variation_index)
            return True

        except Exception as e:
            logger.error(f"Error deleting variation: {e}", exc_info=True)
            self._show_error_dialog(f"Failed to delete variation: {e!s}", parent_widget)
            return False

    def delete_entire_sequence(
        self, word: str, parent_widget: QWidget | None = None
    ) -> bool:
        """
        Delete an entire sequence (all variations).

        Args:
            word: The sequence word/name to delete
            parent_widget: Parent widget for dialogs

        Returns:
            True if deletion was successful, False if cancelled or failed
        """
        try:
            logger.info(f"Attempting to delete entire sequence '{word}'")

            word_directory = self.sequences_directory / word
            if not word_directory.exists():
                logger.error(f"Sequence directory not found: {word_directory}")
                return False

            # Show confirmation dialog
            if not self._confirm_sequence_deletion(word, parent_widget):
                logger.info("Sequence deletion cancelled by user")
                self.deletion_cancelled.emit()
                return False

            # Delete the entire directory
            success = self._delete_word_directory(word_directory)
            if success:
                # Clean up any empty parent directories
                self._cleanup_empty_directories()

                logger.info(f"Successfully deleted entire sequence '{word}'")
                self.sequence_deleted.emit(word)
                return True

            return False

        except Exception as e:
            logger.error(f"Error deleting sequence: {e}", exc_info=True)
            self._show_error_dialog(f"Failed to delete sequence: {e!s}", parent_widget)
            return False

    def _confirm_deletion(
        self, word: str, variation_index: int, parent_widget: QWidget | None
    ) -> bool:
        """Show confirmation dialog for variation deletion."""
        reply = QMessageBox.question(
            parent_widget,
            "Confirm Deletion",
            f"Are you sure you want to delete variation {variation_index + 1} of '{word}'?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        return reply == QMessageBox.StandardButton.Yes

    def _confirm_sequence_deletion(
        self, word: str, parent_widget: QWidget | None
    ) -> bool:
        """Show confirmation dialog for entire sequence deletion."""
        reply = QMessageBox.question(
            parent_widget,
            "Confirm Sequence Deletion",
            f"Are you sure you want to delete the entire sequence '{word}' and all its variations?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        return reply == QMessageBox.StandardButton.Yes

    def _delete_file(self, file_path: str) -> bool:
        """Delete a single file with proper error handling."""
        try:
            path = Path(file_path)
            if path.exists():
                # Ensure file is writable
                path.chmod(0o777)
                path.unlink()
                logger.debug(f"Deleted file: {file_path}")
                return True
            logger.warning(f"File not found for deletion: {file_path}")
            return False
        except Exception as e:
            logger.exception(f"Failed to delete file {file_path}: {e}")
            return False

    def _delete_word_directory(self, word_directory: Path) -> bool:
        """Delete an entire word directory with proper permissions handling."""
        try:
            if word_directory.exists():
                # Set permissions recursively
                for root, dirs, files in os.walk(word_directory):
                    for name in files:
                        file_path = Path(root) / name
                        file_path.chmod(0o777)
                    for name in dirs:
                        dir_path = Path(root) / name
                        dir_path.chmod(0o777)

                # Set permissions on the directory itself
                word_directory.chmod(0o777)

                # Remove the directory
                shutil.rmtree(word_directory)
                logger.debug(f"Deleted directory: {word_directory}")
                return True
            logger.warning(f"Directory not found for deletion: {word_directory}")
            return False
        except Exception as e:
            logger.exception(f"Failed to delete directory {word_directory}: {e}")
            return False

    def _cleanup_empty_directories(self):
        """Remove empty directories from the sequences directory."""
        try:
            # Walk the directory tree bottom-up to remove empty directories
            for root, dirs, _files in os.walk(self.sequences_directory, topdown=False):
                for dir_name in dirs:
                    dir_path = Path(root) / dir_name
                    try:
                        if self._is_directory_empty(dir_path):
                            dir_path.chmod(0o777)
                            dir_path.rmdir()
                            logger.debug(f"Removed empty directory: {dir_path}")
                    except OSError:
                        # Directory not empty or permission error - skip
                        continue
        except Exception as e:
            logger.exception(f"Error during directory cleanup: {e}")

    def _is_directory_empty(self, directory: Path) -> bool:
        """Check if a directory is empty."""
        try:
            return not any(directory.iterdir())
        except OSError:
            return False

    def _fix_variation_numbering(self, word: str, remaining_thumbnails: list[str]):
        """
        Fix variation numbering after deletion to ensure sequential numbering.

        This ensures that if variation 2 of 4 is deleted, the remaining variations
        are renumbered as 1, 2, 3 instead of 1, 3, 4.
        """
        try:
            logger.debug(f"Fixing variation numbering for '{word}'")

            # Group thumbnails by their base name (without variation number)
            thumbnail_groups = {}
            for thumbnail_path in remaining_thumbnails:
                path = Path(thumbnail_path)
                # Extract base name (assuming format: word_length_X.png)
                parts = path.stem.split("_")
                if len(parts) >= 3:
                    base_name = "_".join(
                        parts[:-1]
                    )  # Everything except the last number
                    if base_name not in thumbnail_groups:
                        thumbnail_groups[base_name] = []
                    thumbnail_groups[base_name].append(path)

            # Renumber each group
            for base_name, paths in thumbnail_groups.items():
                # Sort by current number
                paths.sort(key=lambda p: self._extract_variation_number(p))

                # Rename to sequential numbers
                for i, old_path in enumerate(paths, 1):
                    new_name = f"{base_name}_{i}{old_path.suffix}"
                    new_path = old_path.parent / new_name

                    if old_path != new_path:
                        try:
                            old_path.rename(new_path)
                            logger.debug(f"Renamed {old_path.name} to {new_path.name}")
                        except OSError as e:
                            logger.warning(
                                f"Failed to rename {old_path} to {new_path}: {e}"
                            )

        except Exception as e:
            logger.exception(f"Error fixing variation numbering: {e}")

    def _extract_variation_number(self, path: Path) -> int:
        """Extract variation number from filename."""
        try:
            parts = path.stem.split("_")
            if parts:
                return int(parts[-1])
        except (ValueError, IndexError):
            pass
        return 0

    def _show_error_dialog(self, message: str, parent_widget: QWidget | None):
        """Show error dialog to user."""
        QMessageBox.critical(
            parent_widget, "Deletion Error", message, QMessageBox.StandardButton.Ok
        )
