"""
File System Service

Pure service for file system operations used by organization services.
Extracted to follow single responsibility principle and enable dependency injection.

This service handles:
- File reading and writing operations
- Python file discovery
- Path validation and safety checks

No business logic, completely testable in isolation.
"""

from __future__ import annotations

import logging
from pathlib import Path

from desktop.modern.core.interfaces.organization_services import IFileSystemService


logger = logging.getLogger(__name__)


class FileSystemService(IFileSystemService):
    """
    Pure service for file system operations.

    Provides safe file system operations with proper error handling
    and validation. No business logic, just infrastructure concerns.
    """

    def __init__(self):
        """Initialize the file system service."""

    def read_file(self, file_path: Path) -> str:
        """
        Read content from a file.

        Args:
            file_path: Path to the file to read

        Returns:
            File content as string

        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read
            UnicodeDecodeError: If file encoding is invalid
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            logger.debug(f"Successfully read file: {file_path}")
            return content

        except FileNotFoundError:
            logger.exception(f"File not found: {file_path}")
            raise
        except PermissionError:
            logger.exception(f"Permission denied reading file: {file_path}")
            raise
        except UnicodeDecodeError as e:
            logger.exception(f"Encoding error reading file {file_path}: {e}")
            raise

    def write_file(self, file_path: Path, content: str) -> None:
        """
        Write content to a file.

        Args:
            file_path: Path to the file to write
            content: Content to write

        Raises:
            PermissionError: If file can't be written
            OSError: If directory doesn't exist or other OS error
        """
        try:
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            logger.debug(f"Successfully wrote file: {file_path}")

        except PermissionError:
            logger.exception(f"Permission denied writing file: {file_path}")
            raise
        except OSError as e:
            logger.exception(f"OS error writing file {file_path}: {e}")
            raise

    def find_python_files(self, root_path: Path) -> list[Path]:
        """
        Find all Python files in a directory tree.

        Args:
            root_path: Root directory to search

        Returns:
            List of Python file paths

        Raises:
            FileNotFoundError: If root path doesn't exist
        """
        if not root_path.exists():
            logger.error(f"Root path does not exist: {root_path}")
            raise FileNotFoundError(f"Root path does not exist: {root_path}")

        if not root_path.is_dir():
            logger.error(f"Root path is not a directory: {root_path}")
            raise ValueError(f"Root path is not a directory: {root_path}")

        try:
            python_files = []

            for file_path in root_path.rglob("*.py"):
                # Skip __pycache__ and other generated files
                if self._should_skip_file(file_path):
                    continue

                python_files.append(file_path)

            logger.debug(f"Found {len(python_files)} Python files in {root_path}")
            return python_files

        except Exception as e:
            logger.exception(f"Error finding Python files in {root_path}: {e}")
            raise

    def _should_skip_file(self, file_path: Path) -> bool:
        """
        Check if a file should be skipped during analysis.

        Args:
            file_path: Path to check

        Returns:
            True if file should be skipped
        """
        skip_patterns = [
            "__pycache__",
            ".pyc",
            ".pyo",
            ".pyd",
            "__init__.py",  # Often just imports
            "test_",  # Test files
            "_test.py",  # Test files
        ]

        file_str = str(file_path)

        return any(pattern in file_str for pattern in skip_patterns)

    def validate_file_path(self, file_path: Path) -> bool:
        """
        Validate that a file path is safe to operate on.

        Args:
            file_path: Path to validate

        Returns:
            True if path is valid and safe
        """
        try:
            # Check if path exists
            if not file_path.exists():
                return False

            # Check if it's a file (not directory)
            if not file_path.is_file():
                return False

            # Check if it's a Python file
            if file_path.suffix != ".py":
                return False

            # Check if path is within reasonable bounds (security check)
            resolved_path = file_path.resolve()
            if len(str(resolved_path)) > 500:  # Arbitrary but reasonable limit
                logger.warning(f"Path too long: {resolved_path}")
                return False

            return True

        except Exception as e:
            logger.exception(f"Error validating file path {file_path}: {e}")
            return False

    def get_file_stats(self, file_path: Path) -> dict:
        """
        Get basic statistics about a file.

        Args:
            file_path: Path to analyze

        Returns:
            Dictionary with file statistics
        """
        try:
            if not file_path.exists():
                return {"error": "File does not exist"}

            stat = file_path.stat()

            return {
                "size_bytes": stat.st_size,
                "modified_time": stat.st_mtime,
                "is_readable": file_path.is_file() and file_path.exists(),
                "extension": file_path.suffix,
                "name": file_path.name,
                "parent": str(file_path.parent),
            }

        except Exception as e:
            logger.exception(f"Error getting file stats for {file_path}: {e}")
            return {"error": str(e)}

    def backup_file(self, file_path: Path) -> Path:
        """
        Create a backup of a file before modification.

        Args:
            file_path: Path to backup

        Returns:
            Path to backup file
        """
        backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")

        try:
            content = self.read_file(file_path)
            self.write_file(backup_path, content)

            logger.info(f"Created backup: {backup_path}")
            return backup_path

        except Exception as e:
            logger.exception(f"Error creating backup for {file_path}: {e}")
            raise
