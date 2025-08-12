"""
Mock File System Service for Learn Tab Testing

Provides a simple implementation of IFileSystemService for testing
the Learn Tab functionality without requiring the full file system infrastructure.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class MockFileSystemService:
    """
    Mock implementation of IFileSystemService for Learn Tab testing.

    Provides minimal file system functionality to support data persistence
    without requiring actual file operations.
    """

    def __init__(self):
        """Initialize mock service with in-memory storage."""
        self._mock_files: dict[str, Any] = {}
        logger.info("Mock file system service initialized")

    def read_file(self, file_path: str) -> Optional[str]:
        """
        Read file content.

        Args:
            file_path: Path to file

        Returns:
            File content or None if not found
        """
        return self._mock_files.get(file_path)

    def write_file(self, file_path: str, content: str) -> bool:
        """
        Write file content.

        Args:
            file_path: Path to file
            content: Content to write

        Returns:
            True if successful
        """
        self._mock_files[file_path] = content
        return True

    def file_exists(self, file_path: str) -> bool:
        """
        Check if file exists.

        Args:
            file_path: Path to file

        Returns:
            True if file exists
        """
        return file_path in self._mock_files

    def delete_file(self, file_path: str) -> bool:
        """
        Delete file.

        Args:
            file_path: Path to file

        Returns:
            True if deleted successfully
        """
        if file_path in self._mock_files:
            del self._mock_files[file_path]
            return True
        return False

    def create_directory(self, dir_path: str) -> bool:
        """
        Create directory.

        Args:
            dir_path: Path to directory

        Returns:
            True if created successfully
        """
        # Mock implementation - always succeeds
        return True

    def list_files(self, dir_path: str) -> list[str]:
        """
        List files in directory.

        Args:
            dir_path: Path to directory

        Returns:
            List of file names
        """
        # Return files that start with the directory path
        files = []
        for file_path in self._mock_files.keys():
            if file_path.startswith(dir_path):
                relative_path = file_path[len(dir_path) :].lstrip("/")
                if "/" not in relative_path:  # Only direct children
                    files.append(relative_path)
        return files

    def get_file_size(self, file_path: str) -> Optional[int]:
        """
        Get file size.

        Args:
            file_path: Path to file

        Returns:
            File size in bytes or None if not found
        """
        content = self._mock_files.get(file_path)
        if content:
            return len(str(content))
        return None

    def copy_file(self, source_path: str, dest_path: str) -> bool:
        """
        Copy file.

        Args:
            source_path: Source file path
            dest_path: Destination file path

        Returns:
            True if copied successfully
        """
        if source_path in self._mock_files:
            self._mock_files[dest_path] = self._mock_files[source_path]
            return True
        return False

    def move_file(self, source_path: str, dest_path: str) -> bool:
        """
        Move file.

        Args:
            source_path: Source file path
            dest_path: Destination file path

        Returns:
            True if moved successfully
        """
        if source_path in self._mock_files:
            self._mock_files[dest_path] = self._mock_files[source_path]
            del self._mock_files[source_path]
            return True
        return False
