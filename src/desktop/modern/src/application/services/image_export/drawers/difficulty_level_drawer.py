"""
Difficulty Level Drawer - Legacy-Compatible Difficulty Indicator Rendering
=========================================================================

Renders difficulty level indicators onto exported images using exact legacy
sizing, positioning, and gradient logic.
"""

import logging

from core.interfaces.image_export_services import (
    IDifficultyLevelDrawer,
    ImageExportOptions,
)
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QImage, QLinearGradient, QPainter, QPen

logger = logging.getLogger(__name__)


class DifficultyLevelDrawer(IDifficultyLevelDrawer):
    """
    Drawer for rendering difficulty level indicators with legacy-compatible styling.

    This drawer replicates the exact difficulty level rendering logic from the Legacy system,
    including sizing calculations, gradient colors, and positioning.
    """

    def __init__(self):
        """Initialize the difficulty level drawer."""
        self.border_width = 3
        logger.debug(
            "DifficultyLevelDrawer initialized with legacy-compatible settings"
        )

    def draw_difficulty_level(
        self,
        image: QImage,
        difficulty_level: int,
        options: ImageExportOptions,
    ) -> None:
        """
        Draw difficulty level indicator onto the image using exact legacy logic.

        Args:
            image: Target image
            difficulty_level: Difficulty level to draw (1-5+)
            options: Export options
        """
        if difficulty_level <= 0:
            logger.debug("No difficulty level to draw")
            return

        logger.debug(f"Drawing difficulty level: {difficulty_level}")

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # EXACT LEGACY CALCULATION - use exact legacy formula
        shape_size = int(options.additional_height_top * 0.75)
        inset = options.additional_height_top // 8
        rect = QRect(
            inset + self.border_width,
            inset + self.border_width,
            shape_size,
            shape_size,
        )

        # Set up pen with legacy thickness calculation
        pen = QPen(Qt.GlobalColor.black, max(1, rect.height() // 50))
        painter.setPen(pen)

        # Create gradient based on difficulty level (legacy colors)
        gradient = self._create_difficulty_gradient(rect, difficulty_level)
        painter.setBrush(QBrush(gradient))

        # Draw circle
        painter.drawEllipse(rect)

        # EXACT LEGACY FONT CALCULATION
        font_size = int(rect.height() // 1.75)
        font = QFont("Georgia", font_size, QFont.Weight.Bold)
        painter.setFont(font)

        # Draw difficulty number
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(difficulty_level))

        painter.end()
        logger.debug(f"Difficulty level {difficulty_level} drawn successfully")

    def _create_difficulty_gradient(
        self, rect: QRect, difficulty_level: int
    ) -> QLinearGradient:
        """
        Create gradient for difficulty level indicator using exact legacy colors.

        Args:
            rect: Rectangle to create gradient for
            difficulty_level: Difficulty level (determines colors)

        Returns:
            QLinearGradient with legacy-compatible colors
        """
        gradient = QLinearGradient(
            float(rect.left()),
            float(rect.top()),
            float(rect.right()),
            float(rect.bottom()),
        )

        # EXACT LEGACY DIFFICULTY COLORS
        if difficulty_level == 1:
            gradient.setColorAt(0, QColor(144, 238, 144))  # Light green
            gradient.setColorAt(1, QColor(0, 128, 0))  # Dark green
        elif difficulty_level == 2:
            gradient.setColorAt(0, QColor(255, 255, 0))  # Yellow
            gradient.setColorAt(1, QColor(255, 215, 0))  # Gold
        elif difficulty_level == 3:
            gradient.setColorAt(0, QColor(255, 165, 0))  # Orange
            gradient.setColorAt(1, QColor(255, 140, 0))  # Dark orange
        elif difficulty_level == 4:
            gradient.setColorAt(0, QColor(255, 99, 71))  # Tomato
            gradient.setColorAt(1, QColor(220, 20, 60))  # Crimson
        else:  # difficulty_level >= 5
            gradient.setColorAt(0, QColor(139, 0, 0))  # Dark red
            gradient.setColorAt(1, QColor(75, 0, 130))  # Indigo

        return gradient

    def _calculate_difficulty_rect(
        self, image: QImage, additional_height_top: int
    ) -> QRect:
        """
        Calculate the rectangle for difficulty level indicator using legacy logic.

        Args:
            image: Target image
            additional_height_top: Additional height at top of image

        Returns:
            QRect for difficulty indicator placement
        """
        # EXACT LEGACY CALCULATION
        shape_size = int(additional_height_top * 0.75)
        inset = additional_height_top // 8

        return QRect(
            inset + self.border_width,
            inset + self.border_width,
            shape_size,
            shape_size,
        )

    def _get_difficulty_colors(self, difficulty_level: int) -> tuple[QColor, QColor]:
        """
        Get the gradient colors for a specific difficulty level.

        Args:
            difficulty_level: Difficulty level (1-5+)

        Returns:
            Tuple of (start_color, end_color) for gradient
        """
        color_map = {
            1: (QColor(144, 238, 144), QColor(0, 128, 0)),  # Green
            2: (QColor(255, 255, 0), QColor(255, 215, 0)),  # Yellow/Gold
            3: (QColor(255, 165, 0), QColor(255, 140, 0)),  # Orange
            4: (QColor(255, 99, 71), QColor(220, 20, 60)),  # Red
        }

        # Default for difficulty 5+ (very hard)
        return color_map.get(difficulty_level, (QColor(139, 0, 0), QColor(75, 0, 130)))
