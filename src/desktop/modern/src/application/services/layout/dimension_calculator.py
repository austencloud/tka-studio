"""
Dimension Calculator - Pure Calculation Functions
Merged from responsive_sizing_manager.py and dimension_analyzer.py
"""

from typing import Dict, Tuple

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QWidget


class DimensionCalculator:
    """Handles all dimension calculations for option picker layout."""

    def __init__(self):
        # Sizing constraints
        self.min_header_height = 20
        self.max_header_height = 60
        self.min_pictograph_size = 40
        self.max_pictograph_size = 120
        self.section_margins = 5
        self.header_margins = 10

        # Grid parameters
        self.default_pictograph_size = 160
        self.min_pictograph_size = 60
        self.max_pictograph_size = 200
        self.grid_spacing = 8
        self.container_margins = 10

    def calculate_optimal_size(self, option_picker_widget: QWidget) -> QSize:
        """Calculate optimal size based on available screen space."""
        screen = QApplication.primaryScreen()
        if not screen:
            return QSize(800, 600)

        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        if option_picker_widget and option_picker_widget.parent():
            parent = option_picker_widget.parent()
            container_width = min(
                parent.width() if parent.width() > 0 else screen_width // 2,
                screen_width // 2,
            )
            container_height = min(
                parent.height() if parent.height() > 0 else screen_height - 100,
                screen_height - 100,
            )
        else:
            container_width = screen_width // 2
            container_height = screen_height - 100

        return QSize(container_width, container_height)

    def calculate_component_sizing(
        self,
        container_width: int,
        container_height: int,
        section_count: int,
        filter_height: int,
    ) -> Dict:
        """Calculate sizing for all components."""
        total_margins = self.section_margins * 2 * section_count
        header_space_needed = self.header_margins * section_count
        available_height = (
            container_height - filter_height - total_margins - header_space_needed
        )

        header_height = self._calculate_optimal_header_height(
            available_height, section_count
        )
        total_header_height = header_height * section_count
        pictograph_space = available_height - total_header_height
        pictograph_height_per_section = pictograph_space // section_count
        pictograph_size = self._calculate_optimal_pictograph_size(
            container_width, pictograph_height_per_section
        )

        shared_width_sections = max(0, section_count - 3)
        individual_section_width = container_width
        shared_section_width = (
            container_width // 3 if shared_width_sections > 0 else container_width
        )

        return {
            "container_width": container_width,
            "container_height": container_height,
            "header_height": header_height,
            "pictograph_size": pictograph_size,
            "pictograph_space_per_section": pictograph_height_per_section,
            "individual_section_width": individual_section_width,
            "shared_section_width": shared_section_width,
            "section_margins": self.section_margins,
            "filter_height": filter_height,
            "max_rows_per_section": self._calculate_max_rows(
                pictograph_height_per_section, pictograph_size
            ),
            "columns_per_section": 8,
        }

    def _calculate_optimal_header_height(
        self, available_height: int, section_count: int
    ) -> int:
        """Calculate header height that fits proportionally."""
        ideal_header_space = available_height * 0.15
        header_height = int(ideal_header_space / section_count)
        return max(self.min_header_height, min(self.max_header_height, header_height))

    def _calculate_optimal_pictograph_size(
        self, container_width: int, height_per_section: int
    ) -> int:
        """Calculate pictograph size that maximizes space usage."""
        columns = 8
        available_width = container_width - (self.section_margins * 2)
        width_based_size = available_width // columns
        max_rows = 3
        height_based_size = height_per_section // max_rows
        optimal_size = min(width_based_size, height_based_size)
        return max(
            self.min_pictograph_size, min(self.max_pictograph_size, optimal_size)
        )

    def _calculate_max_rows(self, height_per_section: int, pictograph_size: int) -> int:
        """Calculate maximum rows that can fit."""
        if pictograph_size <= 0:
            return 1
        return max(1, height_per_section // pictograph_size)

    def calculate_optimal_pictograph_size_for_width(
        self, available_width: int, column_count: int = 8
    ) -> int:
        """Calculate optimal pictograph size based on available width."""
        total_spacing = self.grid_spacing * (column_count - 1)
        available_for_pictographs = (
            available_width - (2 * self.container_margins) - total_spacing
        )
        optimal_size = available_for_pictographs // column_count
        return max(
            self.min_pictograph_size, min(self.max_pictograph_size, optimal_size)
        )

    def calculate_container_dimensions(
        self, pictograph_count: int, pictograph_size: int, column_count: int = 8
    ) -> Tuple[int, int]:
        """Calculate container dimensions for given pictograph count and size."""
        rows_needed = (pictograph_count - 1) // column_count + 1

        width = (
            (column_count * pictograph_size)
            + (self.grid_spacing * (column_count - 1))
            + (2 * self.container_margins)
        )
        height = (
            (rows_needed * pictograph_size)
            + (self.grid_spacing * (rows_needed - 1))
            + (2 * self.container_margins)
        )

        return width, height

    def analyze_layout_efficiency(
        self, available_width: int, pictograph_count: int
    ) -> dict:
        """Analyze layout efficiency for different configurations."""
        results = {}
        for columns in [6, 7, 8, 9, 10]:
            pictograph_size = self.calculate_optimal_pictograph_size_for_width(
                available_width, columns
            )
            container_width, container_height = self.calculate_container_dimensions(
                pictograph_count, pictograph_size, columns
            )
            used_width = container_width
            width_efficiency = (
                used_width / available_width if available_width > 0 else 0
            )

            results[columns] = {
                "pictograph_size": pictograph_size,
                "container_width": container_width,
                "container_height": container_height,
                "width_efficiency": width_efficiency,
                "rows_needed": (pictograph_count - 1) // columns + 1,
            }
        return results
