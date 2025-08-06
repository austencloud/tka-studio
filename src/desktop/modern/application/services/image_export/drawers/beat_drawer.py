"""
Beat Drawer - Legacy-Compatible Beat and Pictograph Rendering
============================================================

Renders sequence beats and pictographs onto exported images using the modern
pictograph system while maintaining exact legacy positioning and layout logic.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional

from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QBrush, QFont, QImage, QPainter, QPen
from shared.application.services.data.pictograph_factory import PictographFactory

from desktop.modern.core.interfaces.image_export_services import (
    IBeatDrawer,
    ImageExportOptions,
)
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.components.pictograph.pictograph_scene import (
    PictographScene,
)


if TYPE_CHECKING:
    from .font_margin_helper import FontMarginHelper

logger = logging.getLogger(__name__)


class BeatDrawer(IBeatDrawer):
    """
    Drawer for rendering beats and pictographs with legacy-compatible layout.

    This drawer handles the rendering of sequence beats using the modern pictograph
    system while maintaining exact legacy positioning and layout calculations.
    """

    def __init__(self, font_margin_helper: FontMarginHelper, container=None):
        """
        Initialize the beat drawer.

        Args:
            font_margin_helper: Helper for font and margin calculations
            container: DI container for accessing pictograph services
        """
        self.font_margin_helper = font_margin_helper
        self.container = container
        self.pictograph_factory = PictographFactory()
        self.pictograph_size = 280  # Default pictograph size

        logger.debug("BeatDrawer initialized with modern pictograph system")

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
        Draw sequence beats onto the image using legacy layout logic.

        Args:
            image: Target image
            sequence_data: Sequence data to draw
            columns: Number of columns in layout
            rows: Number of rows in layout
            options: Export options
            beat_size: Size of each beat (optional)
        """
        if not sequence_data:
            logger.debug("No sequence data to draw")
            return

        logger.debug(f"Drawing {len(sequence_data)} beats in {columns}x{rows} layout")

        # Use provided beat_size or fall back to default
        if beat_size is None:
            beat_size = self.pictograph_size

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        margin = 10

        # LEGACY LOGIC: Render start position if enabled
        if options.include_start_position:
            self._render_start_position(
                painter,
                margin,
                options.additional_height_top,
                beat_size,
                options,
            )

        # LEGACY LOGIC: Render each beat with CORRECT LEGACY POSITIONING
        for i, beat_data in enumerate(sequence_data):
            # LEGACY LOGIC: When start position is visible, beats start at column 2
            if options.include_start_position:
                beats_per_row = columns - 1  # One less column for beats
                row = i // beats_per_row
                col = (i % beats_per_row) + 1  # +1 to skip column 0 (start position)
            else:
                # Standard layout without start position
                row = i // columns
                col = i % columns

            x = margin + col * (beat_size + margin)
            y = options.additional_height_top + row * beat_size

            # Render the beat at calculated position
            self._render_single_beat(
                painter, beat_data, x, y, beat_size, i + 1, options
            )

        painter.end()
        logger.debug("Beats drawn successfully")

    def _render_start_position(
        self,
        painter: QPainter,
        x: int,
        y: int,
        size: int,
        options: ImageExportOptions,
    ) -> None:
        """
        Render the start position pictograph.

        Args:
            painter: QPainter to draw with
            x: X position
            y: Y position
            size: Size of the start position
            options: Export options
        """
        try:
            # Create a simple start position entry
            start_entry = {
                "letter": "α",  # Alpha symbol for start
                "start_pos": "alpha",
                "end_pos": "alpha",
                "blue_attributes": {"motion": "static"},
                "red_attributes": {"motion": "static"},
            }

            # Convert to pictograph data
            start_pictograph_data = self._convert_beat_data_to_pictograph(start_entry)

            if start_pictograph_data:
                # Render the pictograph
                self._render_pictograph_to_painter(
                    painter, start_pictograph_data, x, y, size
                )

            # Add "START" text overlay if beat numbers are enabled
            if options.add_beat_numbers:
                self._add_text_overlay(painter, "START", x, y, size)

        except Exception as e:
            logger.warning(f"Error rendering start position: {e}")
            # Fallback: draw a simple placeholder
            self._draw_placeholder_beat(painter, x, y, size, "START")

    def _render_single_beat(
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
        Render a single beat pictograph.

        Args:
            painter: QPainter to draw with
            beat_data: Beat data to render
            x: X position
            y: Y position
            size: Size of the beat
            beat_number: Beat number for display
            options: Export options
        """
        try:
            # Convert beat data to pictograph data
            pictograph_data = self._convert_beat_data_to_pictograph(beat_data)

            if pictograph_data:
                # Render the actual pictograph
                self._render_pictograph_to_painter(painter, pictograph_data, x, y, size)

                # Add beat number if enabled
                if options.add_beat_numbers:
                    self._add_text_overlay(painter, str(beat_number), x, y, size)
            else:
                # Fallback: draw placeholder
                self._draw_placeholder_beat(painter, x, y, size, str(beat_number))

        except Exception as e:
            logger.warning(f"Error rendering beat {beat_number}: {e}")
            # Fallback: draw placeholder
            self._draw_placeholder_beat(painter, x, y, size, str(beat_number))

    def _convert_beat_data_to_pictograph(
        self, beat_data: dict[str, Any]
    ) -> Optional[PictographData]:
        """
        Convert sequence beat data to PictographData.

        Args:
            beat_data: Beat data dictionary

        Returns:
            PictographData object or None if conversion fails
        """
        try:
            # Create entry format expected by pictograph factory
            entry = {
                "letter": beat_data.get("letter", "?"),
                "start_pos": beat_data.get(
                    "start_pos", beat_data.get("start_position", "")
                ),
                "end_pos": beat_data.get("end_pos", beat_data.get("end_position", "")),
                "blue_attributes": beat_data.get("blue_attributes", {}),
                "red_attributes": beat_data.get("red_attributes", {}),
            }

            # Use pictograph factory to create pictograph data
            return self.pictograph_factory.create_pictograph_data_from_entry(
                entry, "diamond"
            )

        except Exception as e:
            logger.warning(f"Error converting beat data to pictograph: {e}")
            return None

    def _render_pictograph_to_painter(
        self,
        painter: QPainter,
        pictograph_data: PictographData,
        x: int,
        y: int,
        size: int,
    ) -> None:
        """
        Render a pictograph to the painter at the specified position.

        Args:
            painter: QPainter to draw with
            pictograph_data: Pictograph data to render
            x: X position
            y: Y position
            size: Size of the pictograph
        """
        try:
            # Try to render the REAL pictograph using the modern pictograph system
            if self._render_real_pictograph(painter, pictograph_data, x, y, size):
                return

            # Fallback to simplified if real rendering fails
            logger.debug("Falling back to simplified pictograph rendering")
            self._render_simplified_pictograph(painter, pictograph_data, x, y, size)

        except Exception as e:
            logger.warning(f"Error rendering pictograph to painter: {e}")
            # Final fallback: draw placeholder
            self._draw_placeholder_beat(painter, x, y, size, "?")

    def _render_real_pictograph(
        self,
        painter: QPainter,
        pictograph_data: PictographData,
        x: int,
        y: int,
        size: int,
    ) -> bool:
        """
        Render a REAL pictograph using the modern pictograph system.

        Args:
            painter: QPainter to draw with
            pictograph_data: Pictograph data to render
            x: X position
            y: Y position
            size: Size of the pictograph

        Returns:
            True if rendering was successful, False otherwise
        """
        try:
            # Ensure the global container is set so PictographScene can access services
            if self.container:
                from desktop.modern.core.dependency_injection.di_container import (
                    set_container,
                )

                set_container(self.container)

            # Create a pictograph scene with the real rendering system
            scene = PictographScene()
            scene.setSceneRect(0, 0, 950, 950)  # Standard pictograph size

            # Render the pictograph data to the scene using the REAL system
            scene.render_pictograph(pictograph_data)

            # Create a QImage from the scene
            scene_image = QImage(950, 950, QImage.Format.Format_ARGB32)
            scene_image.fill(Qt.GlobalColor.white)

            # Render the scene to the image
            scene_painter = QPainter(scene_image)
            scene_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            scene_painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

            # Render the scene
            scene.render(scene_painter)
            scene_painter.end()

            # Scale and draw the image to the target position
            target_rect = QRect(x, y, size, size)
            painter.drawImage(target_rect, scene_image)

            logger.debug(f"Successfully rendered REAL pictograph at ({x}, {y})")
            return True

        except Exception as e:
            logger.debug(f"Failed to render real pictograph: {e}")
            return False

    def _render_simplified_pictograph(
        self,
        painter: QPainter,
        pictograph_data: PictographData,
        x: int,
        y: int,
        size: int,
    ) -> None:
        """
        Render a simplified pictograph representation.

        Args:
            painter: QPainter to draw with
            pictograph_data: Pictograph data to render
            x: X position
            y: Y position
            size: Size of the pictograph
        """
        # Draw a simple representation with letter and basic info
        rect = QRect(x, y, size, size)

        # Draw border
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.setBrush(QBrush(Qt.GlobalColor.white))
        painter.drawRect(rect)

        # Draw letter in center
        font = QFont("Arial", size // 8, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, pictograph_data.letter)

    def _draw_placeholder_beat(
        self, painter: QPainter, x: int, y: int, size: int, text: str
    ) -> None:
        """
        Draw a placeholder beat when pictograph rendering fails.

        Args:
            painter: QPainter to draw with
            x: X position
            y: Y position
            size: Size of the beat
            text: Text to display in placeholder
        """
        rect = QRect(x, y, size, size)

        # Draw placeholder rectangle
        painter.setPen(QPen(Qt.GlobalColor.gray, 2))
        painter.setBrush(QBrush(Qt.GlobalColor.lightGray))
        painter.drawRect(rect)

        # Draw text
        font = QFont("Arial", size // 10, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

    def _add_text_overlay(
        self, painter: QPainter, text: str, x: int, y: int, size: int
    ) -> None:
        """
        Add text overlay to a pictograph (for beat numbers or labels).

        Args:
            painter: QPainter to draw with
            text: Text to overlay
            x: X position
            y: Y position
            size: Size of the area
        """
        # Calculate beat scale for font sizing
        beat_scale = self.font_margin_helper.calculate_beat_scale(size)

        # Use legacy font size calculation
        base_font = QFont("Arial", 12, QFont.Weight.Bold)
        font, _ = self.font_margin_helper.adjust_font_and_margin(
            base_font,
            1,
            0,
            beat_scale,  # Use 1 beat for overlay text
        )

        painter.setFont(font)

        # Position text in top-left corner with small offset
        text_x = x + size // 20
        text_y = y + font.pointSize() + size // 20

        # Draw text with white background for visibility
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(text_x + 1, text_y + 1, text)  # Shadow
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(text_x, text_y, text)  # Main text
