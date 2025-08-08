from __future__ import annotations

"""
Thumbnail Size Calculator - Handles size calculations for different view modes.

Extracted from ThumbnailImageLabel to follow Single Responsibility Principle.
"""

import logging
from typing import TYPE_CHECKING

from PyQt6.QtCore import QSize

if TYPE_CHECKING:
    from ..thumbnail_box import ThumbnailBox


class ThumbnailSizeCalculator:
    """
    Calculates thumbnail sizes for different view modes and contexts.

    Responsibilities:
    - Calculate target sizes based on view mode
    - Handle sequence viewer vs browse mode sizing
    - Manage aspect ratio considerations
    - Provide consistent sizing logic
    """

    # No hard-coded size constants - all sizing calculated dynamically

    def __init__(self, thumbnail_box: ThumbnailBox):
        self.thumbnail_box = thumbnail_box
        self.logger = logging.getLogger(__name__)

    def calculate_target_size(self, is_sequence_viewer: bool) -> QSize:
        """
        Calculate the target size for thumbnail processing.

        Args:
            is_sequence_viewer: Whether in sequence viewer mode

        Returns:
            Target QSize for thumbnail processing
        """
        try:
            if is_sequence_viewer:
                return self._calculate_sequence_viewer_size()
            else:
                return self._calculate_browse_mode_size()

        except Exception as e:
            self.logger.warning(f"Error calculating target size: {e}")
            # Emergency fallback
            return QSize(140, 140)

    def _calculate_sequence_viewer_size(self) -> QSize:
        """
        Calculate size for sequence viewer mode - use full width with height constraints.

        Returns:
            QSize optimized for sequence viewer that uses full width
        """
        try:
            # Get the sequence viewer's available space
            sequence_viewer = self.thumbnail_box.browse_tab.sequence_viewer

            # Calculate available width (use most of sequence viewer width)
            padding = 20  # Small padding for aesthetics
            available_width = max(200, sequence_viewer.width() - padding)

            # Calculate maximum height to prevent window expansion
            main_widget_height = self.thumbnail_box.main_widget.height()
            max_height_ratio = 0.6  # Use up to 60% of main widget height
            max_height = max(200, int(main_widget_height * max_height_ratio))

            # For sequence viewer, prioritize using full width
            # Height is constrained to prevent window expansion
            image_width = available_width
            image_height = min(
                available_width, max_height
            )  # Maintain reasonable aspect ratio

            calculated_size = QSize(int(image_width), int(image_height))
            self.logger.debug(
                f"Calculated sequence viewer size: {calculated_size} "
                f"(width={available_width}, max_height={max_height})"
            )

            return calculated_size

        except Exception as e:
            self.logger.error(f"Error calculating sequence viewer size: {e}")
            # Emergency fallback - use reasonable minimum
            return QSize(300, 300)

    def _calculate_browse_mode_size(self) -> QSize:
        """
        Calculate size for browse mode using container's actual current width.
        Image should fill the full width of its thumbnail box container.

        Returns:
            QSize that fills the thumbnail box container width
        """
        try:
            # CRITICAL FIX: Use the thumbnail box's actual current size
            container_size = self.thumbnail_box.size()

            # If container is not ready, fall back to parent or scroll widget calculation
            if container_size.width() <= 1 or container_size.height() <= 1:
                # Fall back to scroll widget calculation for initial sizing
                scroll_widget = self.thumbnail_box.sequence_picker.scroll_widget
                available_width = scroll_widget.width()

                scrollbar_width = scroll_widget.calculate_scrollbar_width()
                content_margins = 40
                grid_margins = 30
                usable_width = (
                    available_width - scrollbar_width - content_margins - grid_margins
                )
                grid_spacing = 15 * 2
                width_per_column = (usable_width - grid_spacing) // 3
                container_width = max(150, width_per_column)

                self.logger.debug(
                    f"Using calculated container width: {container_width}"
                )
            else:
                # Use the actual container width
                container_width = container_size.width()
                self.logger.debug(f"Using actual container width: {container_width}")

            # Image should fit within the actual available space inside the thumbnail box
            # Account for thumbnail box margins (applied in layout) and small internal padding
            thumbnail_box_margins = (
                self.thumbnail_box.margin * 2
            )  # Left + right margins
            internal_padding = 4  # Small internal padding for the image
            available_width = container_width - thumbnail_box_margins - internal_padding

            image_width = max(50, available_width)

            # For browse mode, use square aspect ratio
            image_height = image_width

            calculated_size = QSize(int(image_width), int(image_height))

            self.logger.debug(f"Browse mode calculated size: {calculated_size}")
            return calculated_size

        except Exception as e:
            self.logger.error(f"Error calculating browse mode size: {e}")
            # Emergency fallback - use reasonable minimum
            return QSize(140, 140)

    def calculate_display_size(
        self, target_size: QSize, available_size: QSize
    ) -> QSize:
        """
        Calculate the actual display size within available space.

        Args:
            target_size: Desired target size
            available_size: Available space for display

        Returns:
            Actual display size that fits within available space
        """
        try:
            # Ensure thumbnail fits within available space
            scale_w = available_size.width() / target_size.width()
            scale_h = available_size.height() / target_size.height()
            scale = min(scale_w, scale_h, 1.0)  # Don't scale up

            display_size = QSize(
                int(target_size.width() * scale), int(target_size.height() * scale)
            )

            return self._clamp_size(display_size)

        except Exception as e:
            self.logger.warning(f"Error calculating display size: {e}")
            return target_size

    def calculate_aspect_ratio_size(
        self, original_size: QSize, target_size: QSize
    ) -> QSize:
        """
        Calculate size maintaining aspect ratio within target bounds.

        Args:
            original_size: Original image size
            target_size: Target bounds

        Returns:
            Size that maintains aspect ratio within target bounds
        """
        try:
            if original_size.width() == 0 or original_size.height() == 0:
                return target_size

            aspect_ratio = original_size.width() / original_size.height()
            target_aspect = target_size.width() / target_size.height()

            if aspect_ratio > target_aspect:
                # Image is wider - fit to width
                new_width = target_size.width()
                new_height = int(target_size.width() / aspect_ratio)
            else:
                # Image is taller - fit to height
                new_height = target_size.height()
                new_width = int(target_size.height() * aspect_ratio)

            return self._clamp_size(QSize(new_width, new_height))

        except Exception as e:
            self.logger.warning(f"Error calculating aspect ratio size: {e}")
            return target_size

    def get_grid_cell_size(
        self, container_width: int, columns: int, spacing: int = 10
    ) -> QSize:
        """
        Calculate cell size for grid layout.

        Args:
            container_width: Width of the container
            columns: Number of columns in grid
            spacing: Spacing between items

        Returns:
            Size for each grid cell
        """
        try:
            if columns <= 0:
                columns = 1

            # Calculate available width per column
            total_spacing = spacing * (columns - 1)
            available_width = container_width - total_spacing
            cell_width = max(available_width // columns, self.MINIMUM_SIZE.width())

            # Use square cells for thumbnails
            cell_height = cell_width

            return self._clamp_size(QSize(cell_width, cell_height))

        except Exception as e:
            self.logger.warning(f"Error calculating grid cell size: {e}")
            return self.BROWSE_MODE_SIZE

    def _clamp_size(self, size: QSize) -> QSize:
        """
        Clamp size to minimum and maximum bounds.

        Args:
            size: Size to clamp

        Returns:
            Clamped size within bounds
        """
        width = max(
            self.MINIMUM_SIZE.width(), min(size.width(), self.MAXIMUM_SIZE.width())
        )
        height = max(
            self.MINIMUM_SIZE.height(), min(size.height(), self.MAXIMUM_SIZE.height())
        )

        return QSize(width, height)
