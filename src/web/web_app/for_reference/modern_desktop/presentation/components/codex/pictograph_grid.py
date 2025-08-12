"""
Codex Pictograph Grid

Grid layout component that organizes pictographs in rows/sections
like the legacy codex system.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.services.codex import CodexDataService
from desktop.modern.presentation.components.codex.views import CodexPictographView


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class CodexPictographGrid(QWidget):
    """
    Grid component for organizing codex pictographs.

    Organizes pictographs in rows/sections following the legacy
    codex layout with proper spacing and alignment.
    """

    def __init__(self, container: DIContainer, parent=None):
        super().__init__(parent)

        self.container = container
        self.pictograph_views: dict[str, CodexPictographView] = {}
        self.pictograph_size = 80  # Default size

        # Get services
        self.data_service = container.resolve(CodexDataService)

        # Set object name for styling
        self.setObjectName("codex_pictograph_grid")

        # Setup UI
        self._setup_ui()

        # Load pictographs
        self._load_pictographs()

        logger.debug("CodexPictographGrid initialized")

    def _setup_ui(self) -> None:
        """Setup the grid UI structure."""
        # Main layout for the grid
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)  # Space between rows

        # Apply grid styling
        self.setStyleSheet("""
            CodexPictographGrid {
                background-color: transparent;
            }
        """)

    def _load_pictographs(self) -> None:
        """Load and display pictographs in grid layout."""
        try:
            # Get the row organization from the data service
            rows = self.data_service.get_letters_by_row()

            # Create each row
            for row_letters in rows:
                self._create_row(row_letters)

            # Add stretch at the end to push content to top
            self.main_layout.addStretch()

            logger.debug(f"Loaded {len(self.pictograph_views)} pictographs in grid")

        except Exception as e:
            logger.error(f"Failed to load pictographs: {e}")

    def _create_row(self, letters: list[str]) -> None:
        """
        Create a row of pictographs.

        Args:
            letters: List of letters for this row
        """
        # Create row container
        row_widget = QWidget()
        row_widget.setStyleSheet("QWidget { background-color: transparent; }")
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(10)  # Space between pictographs
        row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add pictographs to row
        for letter in letters:
            try:
                pictograph_data = self.data_service.get_pictograph_data(letter)
                logger.debug(
                    f"Got pictograph data for {letter}: {type(pictograph_data)}"
                )

                if pictograph_data:
                    # Debug the pictograph data structure
                    logger.debug(
                        f"Pictograph data for {letter}: start_pos={pictograph_data.start_position}, end_pos={pictograph_data.end_position}"
                    )
                    logger.debug(f"Motions: {list(pictograph_data.motions.keys())}")

                    # Create pictograph view
                    view = CodexPictographView(row_widget)
                    view.set_codex_size(self.pictograph_size)

                    # Update with pictograph data
                    view.update_from_pictograph_data(pictograph_data)

                    # Store reference
                    self.pictograph_views[letter] = view

                    # Add to row layout
                    row_layout.addWidget(view)

                    logger.debug(f"Added pictograph for letter: {letter}")
                else:
                    # Add placeholder for missing pictographs
                    placeholder = self._create_placeholder(letter)
                    row_layout.addWidget(placeholder)
                    logger.debug(f"Added placeholder for letter: {letter}")
            except Exception as e:
                import traceback

                logger.error(f"Error creating pictograph for {letter}: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                # Add placeholder on error
                placeholder = self._create_placeholder(letter)
                row_layout.addWidget(placeholder)

        # Add row to main layout
        self.main_layout.addWidget(row_widget)

    def _create_placeholder(self, letter: str) -> QWidget:
        """
        Create a placeholder for missing pictographs.

        Args:
            letter: The letter for the placeholder

        Returns:
            Placeholder widget
        """
        placeholder = QLabel(letter)
        placeholder.setFixedSize(self.pictograph_size, self.pictograph_size)
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("""
            QLabel {
                border: 1px dashed #ccc;
                background-color: #f8f9fa;
                color: #6c757d;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        return placeholder

    def update_pictograph_data(
        self, letter: str, pictograph_data: PictographData
    ) -> None:
        """
        Update a specific pictograph's data.

        Args:
            letter: The letter to update
            pictograph_data: New pictograph data
        """
        if letter in self.pictograph_views:
            view = self.pictograph_views[letter]
            view.update_from_pictograph_data(pictograph_data)
            logger.debug(f"Updated pictograph data for letter: {letter}")

    def update_all_pictographs(
        self, pictograph_data_dict: dict[str, PictographData | None]
    ) -> None:
        """
        Update all pictographs with new data.

        Args:
            pictograph_data_dict: Dictionary of letter -> PictographData
        """
        for letter, pictograph_data in pictograph_data_dict.items():
            if pictograph_data and letter in self.pictograph_views:
                self.update_pictograph_data(letter, pictograph_data)

        logger.debug("Updated all pictographs with new data")

    def set_pictograph_size(self, size: int) -> None:
        """
        Set the size for all pictograph views.

        Args:
            size: New size in pixels
        """
        self.pictograph_size = size

        # Update all existing views
        for view in self.pictograph_views.values():
            view.set_codex_size(size)

        logger.debug(f"Set pictograph size to: {size}")

    def calculate_optimal_size(self, container_width: int) -> int:
        """
        Calculate optimal pictograph size based on container width.

        Args:
            container_width: Width of the container

        Returns:
            Optimal size for pictographs
        """
        # Get the maximum number of columns from any row
        rows = self.data_service.get_letters_by_row()
        max_columns = max(len(row) for row in rows) if rows else 6

        # Calculate size with margins and spacing
        margins = 20  # Left and right margins
        spacing = 10 * (max_columns - 1)  # Space between items
        available_width = container_width - margins - spacing

        size = available_width // max_columns

        # Ensure reasonable bounds
        size = max(60, min(size, 120))

        return size

    def refresh_grid(self) -> None:
        """Refresh the entire grid with current data."""
        try:
            # Clear existing views
            self.pictograph_views.clear()

            # Clear layout
            while self.main_layout.count():
                child = self.main_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Reload pictographs
            self._load_pictographs()

            logger.debug("Grid refreshed successfully")

        except Exception as e:
            logger.error(f"Failed to refresh grid: {e}")

    def get_pictograph_view(self, letter: str) -> CodexPictographView | None:
        """
        Get the pictograph view for a specific letter.

        Args:
            letter: The letter to get the view for

        Returns:
            The pictograph view or None if not found
        """
        return self.pictograph_views.get(letter)
