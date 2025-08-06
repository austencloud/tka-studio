"""
Write Tab Service Interfaces

Interfaces for write tab functionality including act management,
music player integration, and sequence editing for acts.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import QObject, pyqtSignal


class ActData:
    """Data model for an act."""

    def __init__(
        self,
        name: str = "Untitled Act",
        description: str = "",
        sequences: List[Dict[str, Any]] = None,
        music_file: Optional[Path] = None,
        metadata: Dict[str, Any] = None,
    ):
        self.name = name
        self.description = description
        self.sequences = sequences or []
        self.music_file = music_file
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "sequences": self.sequences,
            "music_file": str(self.music_file) if self.music_file else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ActData:
        """Create from dictionary."""
        return cls(
            name=data.get("name", "Untitled Act"),
            description=data.get("description", ""),
            sequences=data.get("sequences", []),
            music_file=Path(data["music_file"]) if data.get("music_file") else None,
            metadata=data.get("metadata", {}),
        )


class IActDataService(ABC):
    """Service for managing act data and persistence."""

    @abstractmethod
    def save_act(self, act: ActData, file_path: Path) -> bool:
        """Save an act to file."""
        pass

    @abstractmethod
    def load_act(self, file_path: Path) -> Optional[ActData]:
        """Load an act from file."""
        pass

    @abstractmethod
    def get_available_acts(self, acts_directory: Path) -> List[Path]:
        """Get list of available act files."""
        pass

    @abstractmethod
    def delete_act(self, file_path: Path) -> bool:
        """Delete an act file."""
        pass

    @abstractmethod
    def create_act_thumbnail(self, act: ActData) -> Optional[bytes]:
        """Create thumbnail image for an act."""
        pass


class IMusicPlayerService(ABC):
    """Service for music playback functionality."""

    @abstractmethod
    def load_music(self, file_path: Path) -> bool:
        """Load a music file."""
        pass

    @abstractmethod
    def play(self) -> bool:
        """Start playback."""
        pass

    @abstractmethod
    def pause(self) -> bool:
        """Pause playback."""
        pass

    @abstractmethod
    def stop(self) -> bool:
        """Stop playback."""
        pass

    @abstractmethod
    def set_position(self, position_seconds: float) -> bool:
        """Set playback position."""
        pass

    @abstractmethod
    def get_position(self) -> float:
        """Get current playback position in seconds."""
        pass

    @abstractmethod
    def get_duration(self) -> float:
        """Get total duration in seconds."""
        pass

    @abstractmethod
    def is_playing(self) -> bool:
        """Check if music is currently playing."""
        pass


class IActEditingService(ABC):
    """Service for editing acts (adding/removing sequences, etc.)."""

    @abstractmethod
    def add_sequence_to_act(
        self, act: ActData, sequence_data: Dict[str, Any], position: int = -1
    ) -> bool:
        """Add a sequence to an act."""
        pass

    @abstractmethod
    def remove_sequence_from_act(self, act: ActData, position: int) -> bool:
        """Remove a sequence from an act."""
        pass

    @abstractmethod
    def move_sequence_in_act(
        self, act: ActData, from_position: int, to_position: int
    ) -> bool:
        """Move a sequence within an act."""
        pass

    @abstractmethod
    def update_act_metadata(self, act: ActData, metadata: Dict[str, Any]) -> bool:
        """Update act metadata."""
        pass


class IActLayoutService(ABC):
    """Service for calculating act layout and grid positioning."""

    @abstractmethod
    def calculate_grid_dimensions(self, sequence_count: int) -> tuple[int, int]:
        """Calculate optimal grid dimensions for sequences."""
        pass

    @abstractmethod
    def calculate_sequence_size(
        self,
        available_width: int,
        available_height: int,
        grid_cols: int,
        grid_rows: int,
    ) -> tuple[int, int]:
        """Calculate size for individual sequences in the grid."""
        pass

    @abstractmethod
    def get_sequence_position(self, index: int, grid_cols: int) -> tuple[int, int]:
        """Get grid position for a sequence index."""
        pass


class WriteTabSignals(QObject):
    """Signals for write tab communication."""

    act_loaded = pyqtSignal(object)  # ActData
    act_saved = pyqtSignal(str)  # file path
    act_created = pyqtSignal(object)  # ActData
    sequence_added = pyqtSignal(int)  # position
    sequence_removed = pyqtSignal(int)  # position
    music_loaded = pyqtSignal(str)  # file path
    playback_started = pyqtSignal()
    playback_paused = pyqtSignal()
    playback_stopped = pyqtSignal()
    position_changed = pyqtSignal(float)  # position in seconds


class IWriteTabCoordinator(ABC):
    """Coordinator for write tab functionality."""

    @abstractmethod
    def get_signals(self) -> WriteTabSignals:
        """Get the signals object for communication."""
        pass

    @abstractmethod
    def create_new_act(self) -> ActData:
        """Create a new empty act."""
        pass

    @abstractmethod
    def load_act_from_file(self, file_path: Path) -> bool:
        """Load an act from file."""
        pass

    @abstractmethod
    def save_current_act(self, file_path: Optional[Path] = None) -> bool:
        """Save the current act."""
        pass

    @abstractmethod
    def get_current_act(self) -> Optional[ActData]:
        """Get the currently loaded act."""
        pass

    @abstractmethod
    def add_sequence_to_current_act(self, sequence_data: Dict[str, Any]) -> bool:
        """Add a sequence to the current act."""
        pass
