"""
Modern Image Renderer - Refactored with Drawer Pattern
=====================================================

This service orchestrates image rendering using specialized drawer services,
following the Legacy system's drawer pattern but with Modern dependency injection.

The refactored renderer acts as a coordinator that delegates specific rendering
tasks to specialized drawer services, improving maintainability and testability.
"""

import logging
from typing import Any, Dict, List

from core.interfaces.image_export_services import (
    IBeatDrawer,
    IDifficultyLevelDrawer,
    IFontMarginHelper,
    ImageExportOptions,
    ISequenceImageRenderer,
    IUserInfoDrawer,
    IWordDrawer,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QImage, QPainter, QPen

logger = logging.getLogger(__name__)


class SequenceImageRenderer(ISequenceImageRenderer):
    """
    Refactored image renderer using the drawer pattern.

    This renderer coordinates specialized drawer services to render different
    components of the exported image, following the Legacy system's approach
    but with Modern dependency injection and separation of concerns.
    """

    def __init__(self, container=None):
        """
        Initialize the sequence image renderer with drawer services.

        Args:
            container: DI container for accessing services
        """
        self.container = container

        # Resolve drawer services from container
        if container:
            try:
                self.font_margin_helper = container.resolve(IFontMarginHelper)
                self.word_drawer = container.resolve(IWordDrawer)
                self.user_info_drawer = container.resolve(IUserInfoDrawer)
                self.difficulty_drawer = container.resolve(IDifficultyLevelDrawer)
                self.beat_drawer = container.resolve(IBeatDrawer)
                logger.debug("All drawer services resolved successfully")
            except Exception as e:
                logger.warning(f"Failed to resolve drawer services: {e}")
                self._create_fallback_drawers()
        else:
            logger.warning("No container provided, creating fallback drawers")
            self._create_fallback_drawers()

        # Legacy-compatible styling constants
        self.border_width = 3
        self.background_color = QColor(255, 255, 255)  # White background

        logger.debug("SequenceImageRenderer initialized with drawer pattern")

    def _create_fallback_drawers(self):
        """Create fallback drawer instances when container resolution fails."""
        from application.services.image_export.drawers.beat_drawer import BeatDrawer
        from application.services.image_export.drawers.difficulty_level_drawer import (
            DifficultyLevelDrawer,
        )
        from application.services.image_export.drawers.font_margin_helper import (
            FontMarginHelper,
        )
        from application.services.image_export.drawers.user_info_drawer import (
            UserInfoDrawer,
        )
        from application.services.image_export.drawers.word_drawer import WordDrawer

        self.font_margin_helper = FontMarginHelper()
        self.word_drawer = WordDrawer(self.font_margin_helper)
        self.user_info_drawer = UserInfoDrawer(self.font_margin_helper)
        self.difficulty_drawer = DifficultyLevelDrawer()
        self.beat_drawer = BeatDrawer(self.font_margin_helper, self.container)

        logger.debug("Fallback drawer services created")

    def render_sequence_beats(
        self,
        image: QImage,
        sequence_data: List[Dict[str, Any]],
        options: ImageExportOptions,
    ) -> None:
        """Render sequence beats onto the image using beat drawer."""
        logger.debug(f"Rendering {len(sequence_data)} sequence beats")

        if not sequence_data:
            logger.debug("No sequence data to render")
            return

        # Calculate grid layout
        num_beats = len(sequence_data)
        if options.include_start_position:
            base_cols = min(4, num_beats) if num_beats > 0 else 1
            cols = base_cols + 1  # Add column for start position
        else:
            cols = min(4, num_beats) if num_beats > 0 else 1

        rows = (
            num_beats + (cols - 1 if options.include_start_position else cols) - 1
        ) // (cols - 1 if options.include_start_position else cols)

        # Delegate to beat drawer
        self.beat_drawer.draw_beats(image, sequence_data, cols, rows, options)
        logger.debug("Sequence beats rendered")

    def render_word(
        self,
        image: QImage,
        word: str,
        options: ImageExportOptions,
    ) -> None:
        """Render the word text onto the image using word drawer."""
        logger.debug(f"Rendering word: '{word}'")

        # Calculate number of beats for font scaling
        num_filled_beats = getattr(options, "num_filled_beats", 0)

        # Delegate to word drawer
        self.word_drawer.draw_word(image, word, num_filled_beats, options)
        logger.debug(f"Word '{word}' rendered")

    def render_user_info(self, image: QImage, options: ImageExportOptions) -> None:
        """Render user information onto the image using user info drawer."""
        logger.debug("Rendering user info")

        # Calculate number of beats for font scaling
        num_filled_beats = getattr(options, "num_filled_beats", 0)

        # Delegate to user info drawer
        self.user_info_drawer.draw_user_info(image, options, num_filled_beats)
        logger.debug("User info rendered")

    def render_difficulty_level(
        self, image: QImage, difficulty_level: int, options: ImageExportOptions
    ) -> None:
        """Render difficulty level indicator onto the image using difficulty drawer."""
        logger.debug(f"Rendering difficulty level: {difficulty_level}")

        # Delegate to difficulty drawer
        self.difficulty_drawer.draw_difficulty_level(image, difficulty_level, options)
        logger.debug(f"Difficulty level {difficulty_level} rendered")

    def render_sequence_image(
        self,
        image: QImage,
        sequence_data: List[Dict[str, Any]],
        word: str,
        columns: int,
        rows: int,
        options: ImageExportOptions,
    ) -> None:
        """
        Render complete sequence image using drawer services.

        This method orchestrates the rendering process by delegating to
        specialized drawer services in the correct order.

        Args:
            image: Target image to render onto
            sequence_data: Sequence data to render
            word: Word to display
            columns: Number of columns in layout
            rows: Number of rows in layout
            options: Export options
        """
        logger.debug(f"Rendering sequence image: {word} ({len(sequence_data)} beats)")

        try:
            # Step 1: Initialize image with background
            self._initialize_image_background(image)

            # Step 2: Draw beats using BeatDrawer (main content)
            self.beat_drawer.draw_beats(image, sequence_data, columns, rows, options)

            # Step 3: Draw word text using WordDrawer
            if options.add_word and word:
                num_filled_beats = len(sequence_data)
                self.word_drawer.draw_word(image, word, num_filled_beats, options)

            # Step 4: Draw user info using UserInfoDrawer
            if options.add_user_info:
                num_filled_beats = len(sequence_data)
                self.user_info_drawer.draw_user_info(image, options, num_filled_beats)

            # Step 5: Draw difficulty level using DifficultyLevelDrawer
            if options.add_difficulty_level and hasattr(options, "difficulty_level"):
                self.difficulty_drawer.draw_difficulty_level(
                    image, options.difficulty_level, options
                )

            # Step 6: Add border (legacy styling)
            self._add_image_border(image)

            logger.debug("Sequence image rendering completed successfully")

        except Exception as e:
            logger.error(f"Failed to render sequence image: {e}", exc_info=True)
            raise

    def _initialize_image_background(self, image: QImage) -> None:
        """
        Initialize image with background color and basic setup.

        Args:
            image: Target image to initialize
        """
        painter = QPainter(image)
        painter.fillRect(image.rect(), QBrush(self.background_color))
        painter.end()

    def _add_image_border(self, image: QImage) -> None:
        """
        Add border around the image using legacy styling.

        Args:
            image: Target image to add border to
        """
        painter = QPainter(image)
        painter.setPen(QPen(Qt.GlobalColor.black, self.border_width))
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Draw border rectangle
        border_rect = image.rect().adjusted(
            self.border_width // 2,
            self.border_width // 2,
            -self.border_width // 2,
            -self.border_width // 2,
        )
        painter.drawRect(border_rect)
        painter.end()

    def get_beat_size(
        self, image_width: int, image_height: int, columns: int, rows: int
    ) -> int:
        """
        Calculate beat size based on image dimensions and layout.

        Args:
            image_width: Width of the image
            image_height: Height of the image
            columns: Number of columns
            rows: Number of rows

        Returns:
            Calculated beat size in pixels
        """
        # Legacy-compatible beat size calculation
        margin = 10
        available_width = image_width - (columns + 1) * margin
        available_height = image_height - (rows + 1) * margin

        beat_size_width = available_width // columns
        beat_size_height = available_height // rows

        # Use the smaller dimension to ensure beats fit
        beat_size = min(beat_size_width, beat_size_height)

        # Ensure minimum size
        beat_size = max(beat_size, 50)

        logger.debug(f"Calculated beat size: {beat_size} (layout: {columns}x{rows})")
        return beat_size

    def calculate_additional_height(
        self, options: ImageExportOptions
    ) -> tuple[int, int]:
        """
        Calculate additional height needed for text elements.

        Args:
            options: Export options

        Returns:
            Tuple of (top_height, bottom_height)
        """
        top_height = 0
        bottom_height = 0

        # Calculate top height for word text and difficulty level
        if options.add_word or options.add_difficulty_level:
            top_height = 200  # Legacy-compatible height

        # Calculate bottom height for user info
        if options.add_user_info:
            bottom_height = 100  # Legacy-compatible height

        logger.debug(
            f"Additional height calculated: top={top_height}, bottom={bottom_height}"
        )
        return top_height, bottom_height
