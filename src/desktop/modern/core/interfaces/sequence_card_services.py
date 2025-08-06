"""
Sequence Card Services Interfaces

Defines contracts for sequence card functionality following clean architecture.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class CacheLevel(Enum):
    """Cache levels for sequence card data."""

    RAW_IMAGE = "raw_image"
    SCALED_IMAGE = "scaled_image"
    THUMBNAIL = "thumbnail"


@dataclass
class SequenceCardData:
    """Data structure for sequence card information."""

    path: Path
    word: str
    length: int
    metadata: dict[str, Any]
    thumbnail_path: Path | None = None
    high_res_path: Path | None = None
    is_favorite: bool = False
    tags: list[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class CacheStats:
    """Cache performance statistics."""

    raw_cache_hits: int = 0
    raw_cache_misses: int = 0
    scaled_cache_hits: int = 0
    scaled_cache_misses: int = 0
    total_memory_usage: int = 0
    cache_size: int = 0

    @property
    def hit_ratio(self) -> float:
        total_hits = self.raw_cache_hits + self.scaled_cache_hits
        total_requests = total_hits + self.raw_cache_misses + self.scaled_cache_misses
        return total_hits / total_requests if total_requests > 0 else 0.0


@dataclass
class GridDimensions:
    """Grid layout dimensions."""

    columns: int
    rows: int
    total_positions: int


@dataclass
class DisplayState:
    """Current display state."""

    is_loading: bool = False
    current_length: int = 16
    total_sequences: int = 0
    processed_sequences: int = 0
    current_column_count: int = 2
    cache_hit_ratio: float = 0.0


class ISequenceCardDataService(ABC):
    """Service for sequence card data operations."""

    @abstractmethod
    def get_sequences_by_length(
        self, base_path: Path, length: int
    ) -> list[SequenceCardData]:
        """Get all sequences of specified length."""

    @abstractmethod
    def get_all_sequences(self, base_path: Path) -> list[SequenceCardData]:
        """Get all sequences regardless of length."""

    @abstractmethod
    def extract_metadata(self, image_path: Path) -> dict[str, Any]:
        """Extract metadata from sequence image."""

    @abstractmethod
    def watch_directory_changes(
        self, path: Path, callback: Callable[[Path], None]
    ) -> None:
        """Watch for directory changes."""

    @abstractmethod
    def validate_sequence_data(self, data: SequenceCardData) -> tuple[bool, list[str]]:
        """Validate sequence data."""


class ISequenceCardCacheService(ABC):
    """Service for sequence card caching operations."""

    @abstractmethod
    def get_cached_image(self, path: Path, scale: float = 1.0) -> bytes | None:
        """Get cached image data."""

    @abstractmethod
    def cache_image(self, path: Path, image_data: bytes, scale: float = 1.0) -> None:
        """Cache image data."""

    @abstractmethod
    def clear_cache(self, cache_level: CacheLevel | None = None) -> None:
        """Clear cache."""

    @abstractmethod
    def get_cache_stats(self) -> CacheStats:
        """Get cache performance statistics."""

    @abstractmethod
    def optimize_memory_usage(self) -> None:
        """Optimize memory usage."""


class ISequenceCardLayoutService(ABC):
    """Service for sequence card layout calculations."""

    @abstractmethod
    def calculate_grid_dimensions(self, sequence_length: int) -> GridDimensions:
        """Calculate optimal grid dimensions for sequence length."""

    @abstractmethod
    def calculate_page_size(
        self, available_width: int, column_count: int
    ) -> tuple[int, int]:
        """Calculate optimal page size."""

    @abstractmethod
    def calculate_scale_factor(
        self, original_size: tuple[int, int], target_size: tuple[int, int]
    ) -> float:
        """Calculate appropriate scale factor."""


class ISequenceCardDisplayService(ABC):
    """Service for sequence card display coordination."""

    @abstractmethod
    def display_sequences(self, length: int, column_count: int) -> None:
        """Display sequences of specified length."""

    @abstractmethod
    def get_display_state(self) -> DisplayState:
        """Get current display state."""

    @abstractmethod
    def cancel_current_operation(self) -> None:
        """Cancel current loading operation."""

    @abstractmethod
    def set_progress_callback(self, callback: Callable[[int, int], None]) -> None:
        """Set progress update callback."""


class ISequenceCardExportService(ABC):
    """Service for sequence card export operations."""

    @abstractmethod
    def export_all_sequences(self) -> bool:
        """Export all sequence cards."""

    @abstractmethod
    def regenerate_all_images(self) -> bool:
        """Regenerate all sequence card images."""

    @abstractmethod
    def set_export_progress_callback(
        self, callback: Callable[[int, int, str], None]
    ) -> None:
        """Set export progress callback."""


class ISequenceCardSettingsService(ABC):
    """Service for sequence card settings."""

    @abstractmethod
    def get_last_selected_length(self) -> int:
        """Get last selected length."""

    @abstractmethod
    def save_selected_length(self, length: int) -> None:
        """Save selected length."""

    @abstractmethod
    def get_column_count(self) -> int:
        """Get column count setting."""

    @abstractmethod
    def save_column_count(self, count: int) -> None:
        """Save column count setting."""
