from __future__ import annotations
from abc import abstractmethod
from typing import Any, Optional, Protocol, runtime_checkable,Optional


@runtime_checkable
class ISequenceDataLoaderSaver(Protocol):
    """Interface for sequence data loading and saving operations."""

    @abstractmethod
    def load_current_sequence(self) -> list[dict[str, Any]]:
        """Load the current sequence."""

    @abstractmethod
    def save_current_sequence(self, sequence: list[dict[str, Any]]) -> None:
        """Save the current sequence."""


@runtime_checkable
class IJsonManager(Protocol):
    """Interface for the JSON manager."""

    @abstractmethod
    def save_sequence(self, sequence_data: list[dict[str, Any]]) -> bool:
        """Save the current sequence to the default location."""

    @abstractmethod
    def load_sequence(self, file_path: str | None = None) -> list[dict[str, Any]]:
        """Load a sequence from the specified file path or the default location."""

    @abstractmethod
    def get_updater(self):
        """Get the JSON sequence updater."""

    @property
    @abstractmethod
    def loader_saver(self) -> ISequenceDataLoaderSaver:
        """Get the sequence data loader/saver."""
