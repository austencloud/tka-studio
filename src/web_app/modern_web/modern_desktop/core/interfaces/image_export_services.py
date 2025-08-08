"""
Core interfaces for image export services.

This module defines the interfaces for image export functionality in the modern TKA system.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from PyQt6.QtCore import QRect
from PyQt6.QtGui import QFont, QImage, QPainter

from desktop.modern.domain.models.pictograph_data import PictographData


@dataclass
class ImageExportOptions:
    """Configuration options for image export."""

    # Visual elements to include
    add_word: bool = True
    add_user_info: bool = True
    add_difficulty_level: bool = True
    add_date: bool = True
    add_note: bool = True
    add_beat_numbers: bool = True
    add_reversal_symbols: bool = True
    include_start_position: bool = True
    combined_grids: bool = False

    # User information
    user_name: str = "Unknown"
    export_date: str = ""
    notes: str = "Created using The Kinetic Alphabet"

    # Image quality settings
    png_compression: int = 1  # 0-9, lower is better quality
    high_quality: bool = True

    # Additional height for text elements
    additional_height_top: int = 0
    additional_height_bottom: int = 0


@dataclass
class ExportResult:
    """Result of an image export operation."""

    success: bool
    output_path: Optional[Path] = None
    error_message: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


@dataclass
class ExportProgress:
    """Progress information for export operations."""

    current: int
    total: int
    message: str
    percentage: float = 0.0

    def __post_init__(self):
        if self.total > 0:
            self.percentage = (self.current / self.total) * 100


class ISequenceImageExporter(ABC):
    """Interface for image export services."""

    @abstractmethod
    def export_sequence_image(
        self,
        sequence_data: list[dict[str, Any]],
        word: str,
        output_path: Path,
        options: ImageExportOptions,
    ) -> ExportResult:
        """
        Export a single sequence as an image.

        Args:
            sequence_data: The sequence data to export
            word: The word associated with the sequence
            output_path: Where to save the exported image
            options: Export configuration options

        Returns:
            ExportResult with success status and details
        """

    @abstractmethod
    def export_all_sequences(
        self,
        source_directory: Path,
        export_directory: Path,
        options: ImageExportOptions,
        progress_callback: Optional[callable] = None,
    ) -> dict[str, Any]:
        """
        Export all sequences from a directory.

        Args:
            source_directory: Directory containing sequence files
            export_directory: Directory to export images to
            options: Export configuration options
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with export statistics and results
        """

    @abstractmethod
    def create_sequence_image(
        self,
        sequence_data: list[dict[str, Any]],
        word: str,
        options: ImageExportOptions,
    ) -> QImage:
        """
        Create a QImage from sequence data.

        Args:
            sequence_data: The sequence data to render
            word: The word associated with the sequence
            options: Export configuration options

        Returns:
            QImage containing the rendered sequence
        """


class ISequenceImageRenderer(ABC):
    """Interface for image rendering components."""

    @abstractmethod
    def render_sequence_beats(
        self,
        image: QImage,
        sequence_data: list[dict[str, Any]],
        options: ImageExportOptions,
    ) -> None:
        """Render sequence beats onto the image."""

    @abstractmethod
    def render_word(
        self, image: QImage, word: str, options: ImageExportOptions
    ) -> None:
        """Render the word text onto the image."""

    @abstractmethod
    def render_user_info(self, image: QImage, options: ImageExportOptions) -> None:
        """Render user information onto the image."""

    @abstractmethod
    def render_difficulty_level(
        self, image: QImage, difficulty_level: int, options: ImageExportOptions
    ) -> None:
        """Render difficulty level indicator onto the image."""


class ISequenceMetadataExtractor(ABC):
    """Interface for extracting metadata from sequence files."""

    @abstractmethod
    def extract_sequence_data(self, file_path: Path) -> Optional[list[dict[str, Any]]]:
        """Extract sequence data from a file."""

    @abstractmethod
    def extract_metadata(self, file_path: Path) -> Optional[dict[str, Any]]:
        """Extract metadata from a sequence file."""

    @abstractmethod
    def get_difficulty_level(self, sequence_data: list[dict[str, Any]]) -> int:
        """Calculate difficulty level for a sequence."""


class ISequenceImageLayoutCalculator(ABC):
    """Interface for calculating image layout dimensions."""

    @abstractmethod
    def calculate_layout(
        self, num_beats: int, include_start_position: bool
    ) -> tuple[int, int]:
        """
        Calculate optimal layout (columns, rows) for the given number of beats.

        Args:
            num_beats: Number of beats in the sequence
            include_start_position: Whether to include start position

        Returns:
            Tuple of (columns, rows)
        """

    @abstractmethod
    def calculate_image_dimensions(
        self, columns: int, rows: int, beat_size: int, additional_height: int = 0
    ) -> tuple[int, int]:
        """
        Calculate image dimensions based on layout.

        Args:
            columns: Number of columns
            rows: Number of rows
            beat_size: Size of each beat in pixels
            additional_height: Additional height for text elements

        Returns:
            Tuple of (width, height)
        """


class IWordDrawer(ABC):
    """Interface for drawing word text on images."""

    @abstractmethod
    def draw_word(
        self,
        image: QImage,
        word: str,
        num_filled_beats: int,
        options: ImageExportOptions,
    ) -> None:
        """
        Draw word text onto the image.

        Args:
            image: Target image
            word: Word to draw
            num_filled_beats: Number of beats in sequence (affects font size)
            options: Export options
        """


class IUserInfoDrawer(ABC):
    """Interface for drawing user information on images."""

    @abstractmethod
    def draw_user_info(
        self,
        image: QImage,
        options: ImageExportOptions,
        num_filled_beats: int,
    ) -> None:
        """
        Draw user information onto the image.

        Args:
            image: Target image
            options: Export options containing user info
            num_filled_beats: Number of beats in sequence (affects font size)
        """


class IDifficultyLevelDrawer(ABC):
    """Interface for drawing difficulty level indicators on images."""

    @abstractmethod
    def draw_difficulty_level(
        self,
        image: QImage,
        difficulty_level: int,
        options: ImageExportOptions,
    ) -> None:
        """
        Draw difficulty level indicator onto the image.

        Args:
            image: Target image
            difficulty_level: Difficulty level to draw
            options: Export options
        """


class IBeatDrawer(ABC):
    """Interface for drawing beats and pictographs on images."""

    @abstractmethod
    def draw_beats(
        self,
        image: QImage,
        sequence_data: list[dict[str, Any]],
        columns: int,
        rows: int,
        options: ImageExportOptions,
        beat_size: int = None,
    ) -> None:
        """
        Draw sequence beats onto the image.

        Args:
            image: Target image
            sequence_data: Sequence data to draw
            columns: Number of columns in layout
            rows: Number of rows in layout
            options: Export options
            beat_size: Size of each beat (optional)
        """


class IFontMarginHelper(ABC):
    """Interface for font and margin calculations following legacy logic."""

    @abstractmethod
    def adjust_font_and_margin(
        self,
        base_font: QFont,
        num_filled_beats: int,
        base_margin: int,
        beat_scale: float = 1.0,
    ) -> tuple[QFont, int]:
        """
        Adjust font and margin based on number of beats using exact legacy logic.

        Args:
            base_font: Base font to adjust
            num_filled_beats: Number of beats in sequence
            base_margin: Base margin to adjust
            beat_scale: Scale factor to apply

        Returns:
            Tuple of (adjusted_font, adjusted_margin)
        """

    @abstractmethod
    def calculate_beat_scale(self, beat_size: int, reference_size: int = 280) -> float:
        """
        Calculate beat scale factor based on beat size.

        Args:
            beat_size: Actual beat size in pixels
            reference_size: Reference beat size for scaling

        Returns:
            Scale factor for fonts and elements
        """


class IImageFontManager(ABC):
    """Interface for managing fonts and scaling in image export."""

    @abstractmethod
    def calculate_beat_scale(self, beat_size: int, reference_size: int = 280) -> float:
        """
        Calculate beat scale factor based on beat size.

        Args:
            beat_size: Actual beat size in pixels
            reference_size: Reference beat size for scaling

        Returns:
            Scale factor for fonts and elements
        """

    @abstractmethod
    def adjust_font_for_beats(
        self, base_font: QFont, num_beats: int, beat_scale: float = 1.0
    ) -> QFont:
        """
        Adjust font size based on number of beats using legacy logic.

        Args:
            base_font: Base font to adjust
            num_beats: Number of beats in sequence
            beat_scale: Scale factor to apply

        Returns:
            Adjusted font
        """

    @abstractmethod
    def adjust_margin_for_beats(
        self, base_margin: int, num_beats: int, beat_scale: float = 1.0
    ) -> int:
        """
        Adjust margin based on number of beats using legacy logic.

        Args:
            base_margin: Base margin to adjust
            num_beats: Number of beats in sequence
            beat_scale: Scale factor to apply

        Returns:
            Adjusted margin
        """


class IImageTextRenderer(ABC):
    """Interface for rendering text elements on images."""

    @abstractmethod
    def render_word_text(
        self,
        image: QImage,
        word: str,
        font: QFont,
        options: ImageExportOptions,
    ) -> None:
        """
        Render word text onto the image.

        Args:
            image: Target image
            word: Word to render
            font: Font to use
            options: Export options
        """

    @abstractmethod
    def render_user_info_text(
        self,
        image: QImage,
        options: ImageExportOptions,
        fonts: dict[str, QFont],
    ) -> None:
        """
        Render user information text onto the image.

        Args:
            image: Target image
            options: Export options containing user info
            fonts: Dictionary of fonts for different text elements
        """

    @abstractmethod
    def render_difficulty_indicator(
        self,
        image: QImage,
        difficulty_level: int,
        options: ImageExportOptions,
    ) -> None:
        """
        Render difficulty level indicator onto the image.

        Args:
            image: Target image
            difficulty_level: Difficulty level to render
            options: Export options
        """


class IBeatRenderer(ABC):
    """Interface for rendering individual beats and pictographs."""

    @abstractmethod
    def render_beat_at_position(
        self,
        painter: QPainter,
        beat_data: dict[str, Any],
        x: int,
        y: int,
        size: int,
        beat_number: int,
        options: ImageExportOptions,
    ) -> None:
        """
        Render a single beat at the specified position.

        Args:
            painter: QPainter to draw with
            beat_data: Beat data to render
            x: X position
            y: Y position
            size: Size of the beat
            beat_number: Beat number for display
            options: Export options
        """

    @abstractmethod
    def render_start_position(
        self,
        painter: QPainter,
        x: int,
        y: int,
        size: int,
        options: ImageExportOptions,
    ) -> None:
        """
        Render the start position at the specified location.

        Args:
            painter: QPainter to draw with
            x: X position
            y: Y position
            size: Size of the start position
            options: Export options
        """


class IVisualElementRenderer(ABC):
    """Interface for rendering visual elements like grids, props, and arrows."""

    @abstractmethod
    def render_pictograph_elements(
        self,
        painter: QPainter,
        pictograph_data: PictographData,
        rect: QRect,
        options: ImageExportOptions,
    ) -> None:
        """
        Render pictograph visual elements (grids, props, arrows).

        Args:
            painter: QPainter to draw with
            pictograph_data: Pictograph data containing element information
            rect: Rectangle to render within
            options: Export options
        """

    @abstractmethod
    def add_text_overlay(
        self,
        painter: QPainter,
        text: str,
        x: int,
        y: int,
        size: int,
    ) -> None:
        """
        Add text overlay to a pictograph.

        Args:
            painter: QPainter to draw with
            text: Text to overlay
            x: X position
            y: Y position
            size: Size of the area
        """
