from abc import abstractmethod
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable


@runtime_checkable
class ISequenceDataLoaderSaver(Protocol):
    """Interface for sequence data loading and saving operations."""

    @abstractmethod
    def load_current_sequence(self) -> List[Dict[str, Any]]:
        """Load the current sequence."""
        pass

    @abstractmethod
    def save_current_sequence(self, sequence: List[Dict[str, Any]]) -> None:
        """Save the current sequence."""
        pass


@runtime_checkable
class IJsonManager(Protocol):
    """Interface for the JSON manager."""

    @abstractmethod
    def save_sequence(self, sequence_data: List[Dict[str, Any]]) -> bool:
        """Save the current sequence to the default location."""
        pass

    @abstractmethod
    def load_sequence(self, file_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """Load a sequence from the specified file path or the default location."""
        pass

    @abstractmethod
    def get_updater(self):
        """Get the JSON sequence updater."""
        pass

    @property
    @abstractmethod
    def loader_saver(self) -> ISequenceDataLoaderSaver:
        """Get the sequence data loader/saver."""
        pass
