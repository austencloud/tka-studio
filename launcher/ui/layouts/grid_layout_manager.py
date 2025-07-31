#!/usr/bin/env python3
"""
Grid Layout Manager - Application Grid Layout Logic
==================================================

Handles layout calculations and positioning for the TKA application grid:
- Dynamic card sizing based on container dimensions
- 3-row category-based organization
- Responsive layout calculations
- Grid positioning and spacing

Architecture:
- Extracted from application_grid.py for better separation of concerns
- Pure calculation logic without UI dependencies
- Supports different layout strategies
"""

import logging
from typing import Any

from domain.models import ApplicationCategory, ApplicationData

logger = logging.getLogger(__name__)


class GridLayoutManager:
    """Manages layout calculations for the application grid."""

    def __init__(self):
        """Initialize the layout manager."""
        self.grid_side_margins = 32  # 16px left + 16px right
        self.card_spacing = 16  # Spacing between cards
        self.min_card_width = 150  # Minimum card width
        self.card_height = 120  # Fixed card height for 3-row layout

    def calculate_available_width(self, container_widget) -> int:
        """Calculate available width for the grid container."""
        try:
            # Get the scroll area's viewport width
            if hasattr(container_widget, "scroll_area"):
                viewport_width = container_widget.scroll_area.viewport().width()
                if viewport_width > 0:
                    return viewport_width

            # Fallback to widget width
            widget_width = container_widget.width()
            if widget_width > 0:
                return widget_width

            # Last resort - use parent width if available
            if container_widget.parent():
                parent_width = container_widget.parent().width()
                if parent_width > 0:
                    return parent_width - 40  # Account for margins

            return 0

        except Exception as e:
            logger.warning(f"⚠️ Error calculating available width: {e}")
            return 0

    def calculate_card_dimensions_for_3_rows(
        self, container_width: int, applications: list[ApplicationData]
    ) -> dict[str, int]:
        """Calculate card dimensions optimized for 3-row layout."""
        if container_width <= 0:
            return {"width": self.min_card_width, "height": self.card_height}

        # Organize applications to find max cards per row
        organized_apps = self.organize_apps_by_category(applications)
        max_cards_per_row = (
            max(len(apps) for apps in organized_apps.values()) if organized_apps else 1
        )

        # Calculate card width with spacing
        card_spacing_total = (
            (max_cards_per_row - 1) * self.card_spacing if max_cards_per_row > 1 else 0
        )
        available_card_width = (
            container_width - self.grid_side_margins - card_spacing_total
        )
        card_width = max(self.min_card_width, available_card_width // max_cards_per_row)

        return {"width": card_width, "height": self.card_height}

    def organize_apps_by_category(
        self, applications: list[ApplicationData]
    ) -> dict[str, list[ApplicationData]]:
        """Organize applications into 3 rows by category."""
        # Initialize organized structure
        organized = {"Desktop Apps": [], "Web Apps": [], "Development Tools": []}

        # Sort applications by display_order to maintain consistent ordering
        sorted_apps = sorted(applications, key=lambda app: app.display_order)

        # Categorize applications
        for app in sorted_apps:
            if app.category == ApplicationCategory.DESKTOP:
                organized["Desktop Apps"].append(app)
            elif app.category == ApplicationCategory.WEB:
                organized["Web Apps"].append(app)
            elif app.category == ApplicationCategory.DEVELOPMENT:
                organized["Development Tools"].append(app)

        return organized

    def calculate_grid_positions(
        self, organized_apps: dict[str, list[ApplicationData]]
    ) -> list[tuple[int, int, ApplicationData]]:
        """Calculate grid positions for organized applications."""
        positions = []

        for row_index, (category, apps) in enumerate(organized_apps.items()):
            for col_index, app in enumerate(apps):
                positions.append((row_index, col_index, app))

        return positions

    def get_layout_metrics(
        self, container_width: int, applications: list[ApplicationData]
    ) -> dict[str, Any]:
        """Get comprehensive layout metrics for debugging and optimization."""
        organized_apps = self.organize_apps_by_category(applications)
        card_dimensions = self.calculate_card_dimensions_for_3_rows(
            container_width, applications
        )

        metrics = {
            "container_width": container_width,
            "card_width": card_dimensions["width"],
            "card_height": card_dimensions["height"],
            "total_applications": len(applications),
            "categories": {
                category: len(apps) for category, apps in organized_apps.items()
            },
            "max_cards_per_row": (
                max(len(apps) for apps in organized_apps.values())
                if organized_apps
                else 0
            ),
            "grid_side_margins": self.grid_side_margins,
            "card_spacing": self.card_spacing,
        }

        return metrics

    def validate_layout(
        self, container_width: int, applications: list[ApplicationData]
    ) -> bool:
        """Validate that the layout will work with current parameters."""
        if container_width <= 0:
            return False

        if not applications:
            return True  # Empty grid is valid

        card_dimensions = self.calculate_card_dimensions_for_3_rows(
            container_width, applications
        )

        # Check if card width is reasonable
        if card_dimensions["width"] < self.min_card_width:
            logger.warning(
                f"⚠️ Card width {card_dimensions['width']} below minimum {self.min_card_width}"
            )
            return False

        return True

    def get_responsive_breakpoints(self) -> dict[str, int]:
        """Get responsive breakpoints for different layout modes."""
        return {
            "mobile": 480,
            "tablet": 768,
            "desktop": 1024,
            "large": 1440,
        }

    def suggest_layout_adjustments(
        self, container_width: int, applications: list[ApplicationData]
    ) -> dict[str, Any]:
        """Suggest layout adjustments based on current conditions."""
        suggestions = {"adjustments": [], "warnings": [], "optimizations": []}

        organized_apps = self.organize_apps_by_category(applications)
        max_cards_per_row = (
            max(len(apps) for apps in organized_apps.values()) if organized_apps else 0
        )

        # Check for uneven distribution
        category_counts = [len(apps) for apps in organized_apps.values()]
        if max(category_counts) - min(category_counts) > 3:
            suggestions["warnings"].append(
                "Uneven category distribution may cause layout imbalance"
            )

        # Check container width
        breakpoints = self.get_responsive_breakpoints()
        if container_width < breakpoints["tablet"]:
            suggestions["adjustments"].append(
                "Consider reducing card spacing for narrow containers"
            )

        # Check card density
        if max_cards_per_row > 8:
            suggestions["optimizations"].append(
                "Consider pagination or scrolling for large card counts"
            )

        return suggestions
