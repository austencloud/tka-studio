"""
Sequence Card Layout Service Implementation

Handles layout calculations and responsive design.
Replicates legacy system's exact page sizing and grid layout specifications.
"""

from __future__ import annotations

from enum import Enum
import logging

from PyQt6.QtCore import QRect, QSize

from desktop.modern.core.interfaces.sequence_card_services import (
    GridDimensions,
    ISequenceCardLayoutService,
)


logger = logging.getLogger(__name__)


class PaperSize(Enum):
    """Standard paper sizes in points (1/72 inch) - exact legacy replication."""

    A4 = (595, 842)  # 210mm x 297mm at 72 DPI
    LETTER = (612, 792)  # 8.5" x 11" at 72 DPI
    LEGAL = (612, 1008)  # 8.5" x 14" at 72 DPI
    TABLOID = (792, 1224)  # 11" x 17" at 72 DPI


class PaperOrientation(Enum):
    """Paper orientation options - exact legacy replication."""

    PORTRAIT = 0
    LANDSCAPE = 1


class PrintablePageLayout:
    """
    Manages layout calculations for printable pages with standard paper sizes.
    Exact replication of legacy system's PrintablePageLayout class.
    """

    # Default margins in points (1/72 inch) - exact legacy values
    DEFAULT_MARGINS = (18, 36, 18, 36)  # left, top, right, bottom

    # Default DPI for screen display - exact legacy values
    SCREEN_DPI = 96
    PRINT_DPI = 300

    def __init__(
        self,
        paper_size: PaperSize = PaperSize.LETTER,  # Legacy uses LETTER by default
        orientation: PaperOrientation = PaperOrientation.PORTRAIT,
        margins: tuple[int, int, int, int] = DEFAULT_MARGINS,
        screen_dpi: int = SCREEN_DPI,
        print_dpi: int = PRINT_DPI,
    ):
        self.paper_size = paper_size
        self.orientation = orientation
        self.margins = margins
        self.screen_dpi = screen_dpi
        self.print_dpi = print_dpi

        # Calculate page dimensions
        self._calculate_dimensions()

    def _calculate_dimensions(self):
        """Calculate page dimensions based on paper size and orientation."""
        width, height = self.paper_size.value

        # Swap dimensions for landscape orientation
        if self.orientation == PaperOrientation.LANDSCAPE:
            width, height = height, width

        self.page_width_pts = width
        self.page_height_pts = height

        # Calculate content area (excluding margins)
        left, top, right, bottom = self.margins
        self.content_width_pts = width - left - right
        self.content_height_pts = height - top - bottom

        # Calculate screen dimensions (for display)
        scale_factor = self.screen_dpi / 72  # Convert from points to pixels
        self.page_width_px = int(width * scale_factor)
        self.page_height_px = int(height * scale_factor)
        self.content_width_px = int(self.content_width_pts * scale_factor)
        self.content_height_px = int(self.content_height_pts * scale_factor)

    def get_page_size_px(self) -> QSize:
        """Get the page size in pixels for screen display."""
        return QSize(self.page_width_px, self.page_height_px)

    def get_content_rect_px(self) -> QRect:
        """Get the content rectangle in pixels for screen display."""
        left, top, _, _ = self.margins
        left_px = int(left * self.screen_dpi / 72)
        top_px = int(top * self.screen_dpi / 72)
        return QRect(left_px, top_px, self.content_width_px, self.content_height_px)


class SequenceCardLayoutService(ISequenceCardLayoutService):
    """Implementation of sequence card layout calculations."""

    # Grid mappings from legacy system - EXACT replication
    # CRITICAL FIX: Use correct legacy grid mappings (cols, rows) - REVERSED!
    GRID_MAPPINGS = {
        2: (2, 3),  # 2 columns, 3 rows (legacy: (3, 2) reversed)
        3: (2, 3),  # 2 columns, 3 rows (legacy: (3, 2) reversed)
        4: (2, 10),  # 2 columns, 10 rows (legacy: (10, 2) reversed)
        5: (3, 2),  # 3 columns, 2 rows (legacy: (2, 3) reversed)
        6: (3, 2),  # 3 columns, 2 rows (legacy: (2, 3) reversed)
        8: (2, 5),  # 2 columns, 5 rows (legacy: (5, 2) reversed)
        10: (3, 4),  # 3 columns, 4 rows (legacy: (4, 3) reversed)
        12: (3, 4),  # 3 columns, 4 rows (legacy: (4, 3) reversed)
        16: (2, 3),  # 2 columns, 3 rows (legacy: (3, 2) reversed) - FIXED!
    }

    def __init__(self):
        """Initialize with letter-sized page layout matching legacy system."""
        self.page_layout = PrintablePageLayout(
            paper_size=PaperSize.LETTER, orientation=PaperOrientation.PORTRAIT
        )

    def calculate_grid_dimensions(self, sequence_length: int) -> GridDimensions:
        """Calculate optimal grid dimensions for sequence length."""
        if sequence_length in self.GRID_MAPPINGS:
            cols, rows = self.GRID_MAPPINGS[sequence_length]
            return GridDimensions(columns=cols, rows=rows, total_positions=cols * rows)
        # Default fallback for unknown lengths
        logger.warning(f"Unknown sequence length {sequence_length}, using default grid")
        return GridDimensions(columns=4, rows=4, total_positions=16)

    def calculate_page_size(
        self, available_width: int, column_count: int
    ) -> tuple[int, int]:
        """Calculate optimal page size based on letter-sized pages and available width."""
        # Get the base letter-sized page dimensions
        base_page_size = self.page_layout.get_page_size_px()
        base_width = base_page_size.width()
        base_height = base_page_size.height()

        # Calculate scaling to fit available width with proper spacing
        # MINIMAL MARGINS: Almost no side margins to maximize available width (legacy behavior)
        side_margins = 0  # Exact legacy value
        page_spacing = 10  # Default spacing between page previews
        column_spacing = page_spacing * (column_count - 1)
        available_for_pages = available_width - side_margins - column_spacing

        # Calculate the maximum width for each page with minimum size to prevent too small pages
        max_page_width = max(
            300, available_for_pages // column_count
        )  # Legacy minimum: 300

        # Calculate scale factor to maintain letter-sized aspect ratio
        scale_factor = max_page_width / base_width
        scaled_height = int(base_height * scale_factor)

        return max_page_width, scaled_height

    def get_letter_page_size_px(self) -> QSize:
        """Get the base letter-sized page dimensions in pixels."""
        return self.page_layout.get_page_size_px()

    def get_content_rect_px(self) -> QRect:
        """Get the content rectangle for letter-sized pages in pixels."""
        return self.page_layout.get_content_rect_px()

    def calculate_scale_factor(
        self, original_size: tuple[int, int], target_size: tuple[int, int]
    ) -> float:
        """Calculate appropriate scale factor."""
        orig_width, orig_height = original_size
        target_width, target_height = target_size

        if orig_width <= 0 or orig_height <= 0:
            return 1.0

        # Calculate scale factors for both dimensions
        width_scale = target_width / orig_width
        height_scale = target_height / orig_height

        # Use the smaller scale to ensure image fits
        scale_factor = min(width_scale, height_scale)

        # Ensure scale factor is reasonable (not too small or too large)
        return max(0.1, min(scale_factor, 5.0))
