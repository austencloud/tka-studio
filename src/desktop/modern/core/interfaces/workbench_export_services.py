"""
Workbench Export Service Interfaces

Framework-agnostic interfaces for workbench export operations.
These interfaces define contracts for export functionality without
being tied to specific implementations or UI frameworks.
"""

from __future__ import annotations

from typing import Protocol

from desktop.modern.domain.models.sequence_data import SequenceData


class IWorkbenchExportService(Protocol):
    """Interface for workbench export operations."""

    def export_sequence_image(
        self, sequence: SequenceData, file_path: str | None = None
    ) -> tuple[bool, str]:
        """
        Export sequence as image file.

        Args:
            sequence: Sequence to export
            file_path: Optional specific file path, if None uses default naming

        Returns:
            Tuple of (success, message/file_path)
        """
        ...

    def export_sequence_json(self, sequence: SequenceData) -> tuple[bool, str]:
        """
        Export sequence as JSON string.

        Args:
            sequence: Sequence to export

        Returns:
            Tuple of (success, json_string/error_message)
        """
        ...

    def get_export_directory(self) -> str:
        """Get the directory where exports are saved."""
        ...

    def validate_export_directory(self) -> bool:
        """Validate that export directory exists and is writable."""
        ...


class IWorkbenchClipboardService(Protocol):
    """Interface for workbench clipboard operations."""

    def copy_text_to_clipboard(self, text: str) -> tuple[bool, str]:
        """
        Copy text to system clipboard.

        Args:
            text: Text to copy

        Returns:
            Tuple of (success, message)

        Note:
            Web implementation: Uses Navigator.clipboard API, requires user gesture
        """
        ...

    def get_clipboard_text(self) -> tuple[bool, str]:
        """
        Get text from system clipboard.

        Returns:
            Tuple of (success, text/error_message)

        Note:
            Web implementation: Uses Navigator.clipboard API, requires permissions
        """
        ...

    def copy_sequence_json(self, sequence: SequenceData) -> tuple[bool, str]:
        """
        Copy sequence data as JSON to clipboard.

        Args:
            sequence: Sequence data to copy

        Returns:
            Tuple of (success, message)

        Note:
            Web implementation: Serializes to JSON then copies to clipboard
        """
        ...

    def copy_sequence_image_data(self, sequence: SequenceData) -> tuple[bool, str]:
        """
        Copy sequence as image data to clipboard.

        Args:
            sequence: Sequence data to copy as image

        Returns:
            Tuple of (success, message)

        Note:
            Web implementation: Renders to canvas, converts to blob, copies to clipboard
        """
        ...

    def paste_sequence_from_clipboard(self) -> tuple[bool, SequenceData | None, str]:
        """
        Paste sequence data from clipboard.

        Returns:
            Tuple of (success, sequence_data_or_none, message)

        Note:
            Web implementation: Attempts to parse JSON from clipboard
        """
        ...

    def is_clipboard_available(self) -> bool:
        """
        Check if clipboard is available for operations.

        Returns:
            True if clipboard operations are supported

        Note:
            Web implementation: Checks for Navigator.clipboard API availability
        """
        ...

    def get_clipboard_permissions(self) -> dict[str, bool]:
        """
        Get clipboard permissions status.

        Returns:
            Dictionary with permission status for read/write operations

        Note:
            Web implementation: Queries clipboard permissions API
        """
        ...

    def request_clipboard_permissions(self) -> tuple[bool, str]:
        """
        Request clipboard permissions from user.

        Returns:
            Tuple of (success, message)

        Note:
            Web implementation: Requests clipboard permissions, desktop may be no-op
        """
        ...
