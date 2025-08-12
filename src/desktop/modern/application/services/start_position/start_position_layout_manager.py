"""
Start Position Layout Manager

Handles the actual layout operations for start position picker components.
Contains Qt-specific layout manipulation logic.
"""

from __future__ import annotations

import logging

from PyQt6.QtWidgets import QApplication, QGridLayout, QWidget

from desktop.modern.application.services.start_position.start_position_layout_service import (
    LayoutMode,
    StartPositionLayoutService,
)


logger = logging.getLogger(__name__)


class StartPositionLayoutManager:
    """
    Manager for handling actual layout operations in start position picker.

    Responsibilities:
    - Performing actual Qt layout manipulations
    - Arranging widgets in grid layouts
    - Clearing and resetting layouts
    - Managing layout transitions

    Note: Contains Qt-specific code for layout operations
    """

    def __init__(self, layout_service: StartPositionLayoutService):
        """
        Initialize the layout manager.

        Args:
            layout_service: Service providing layout configuration
        """
        self.layout_service = layout_service
        logger.debug("StartPositionLayoutManager initialized")

    def arrange_positions_in_layout(
        self,
        grid_layout: QGridLayout,
        position_widgets: list[QWidget],
        layout_mode: LayoutMode,
    ) -> bool:
        """
        Arrange position widgets in the grid layout according to the specified mode.

        Args:
            grid_layout: The QGridLayout to arrange widgets in
            position_widgets: List of position option widgets to arrange
            layout_mode: The layout mode to use for arrangement

        Returns:
            True if arrangement was successful, False otherwise
        """
        try:
            # Get layout configuration from service
            config = self.layout_service.get_layout_arrangement_config(
                layout_mode, len(position_widgets)
            )

            if config["type"] == "horizontal":
                return self._arrange_horizontal_layout(
                    grid_layout, position_widgets, config
                )
            if config["type"] == "grid":
                return self._arrange_grid_layout(grid_layout, position_widgets, config)
            logger.warning(f"Unknown layout type: {config['type']}")
            return False

        except Exception as e:
            logger.exception(f"Error arranging positions in layout: {e}")
            return False

    def _arrange_horizontal_layout(
        self, grid_layout: QGridLayout, position_widgets: list[QWidget], config: dict
    ) -> bool:
        """
        Arrange positions horizontally in a single row.

        Args:
            grid_layout: The QGridLayout to arrange widgets in
            position_widgets: List of position widgets to arrange
            config: Layout configuration from service

        Returns:
            True if arrangement was successful
        """
        try:
            # Use arrangement coordinates from service
            for _i, (widget, (row, col)) in enumerate(
                zip(position_widgets, config["arrangement"])
            ):
                grid_layout.addWidget(widget, row, col)
                widget.show()
                widget.setVisible(True)

            # Apply column stretches from configuration
            for col, stretch in config["column_stretches"].items():
                grid_layout.setColumnStretch(col, stretch)

            # Force complete layout recalculation
            self._force_layout_update(grid_layout)

            logger.debug(f"✅ Arranged {len(position_widgets)} positions horizontally")
            return True

        except Exception as e:
            logger.exception(f"Error in horizontal layout arrangement: {e}")
            return False

    def _arrange_grid_layout(
        self, grid_layout: QGridLayout, position_widgets: list[QWidget], config: dict
    ) -> bool:
        """
        Arrange positions in a grid layout.

        Args:
            grid_layout: The QGridLayout to arrange widgets in
            position_widgets: List of position widgets to arrange
            config: Layout configuration from service

        Returns:
            True if arrangement was successful
        """
        try:
            # Use arrangement coordinates from service
            for widget, (row, col) in zip(position_widgets, config["arrangement"]):
                grid_layout.addWidget(widget, row, col)
                widget.show()
                widget.setVisible(True)

            # Force layout update
            self._force_layout_update(grid_layout)

            logger.debug(
                f"✅ Arranged {len(position_widgets)} positions in {config['rows']}x{config['columns']} grid"
            )
            return True

        except Exception as e:
            logger.exception(f"Error in grid layout arrangement: {e}")
            return False

    def clear_grid_layout(self, grid_layout: QGridLayout) -> bool:
        """
        Clear all widgets from grid layout and reset its structure.

        Args:
            grid_layout: The QGridLayout to clear

        Returns:
            True if clearing was successful
        """
        try:
            # Remove all widgets from the layout
            while grid_layout.count():
                item = grid_layout.takeAt(0)
                if item and item.widget():
                    item.widget().setParent(None)

            # Reset column stretches to prevent layout conflicts
            for i in range(10):  # Clear up to 10 columns (more than we'll ever use)
                grid_layout.setColumnStretch(i, 0)

            # Force the grid layout to completely reset its internal structure
            grid_layout.invalidate()

            # Clear any cached geometry information
            if grid_layout.parent():
                grid_layout.parent().updateGeometry()

            logger.debug("Grid layout cleared and structure reset for mode switching")
            return True

        except Exception as e:
            logger.exception(f"Error clearing grid layout: {e}")
            return False

    def _force_layout_update(self, grid_layout: QGridLayout) -> None:
        """
        Force a complete layout update and geometry recalculation.

        Args:
            grid_layout: The layout to update
        """
        try:
            grid_layout.activate()
            grid_layout.update()

            if grid_layout.parent():
                grid_layout.parent().updateGeometry()

            # Process events to ensure changes are applied
            QApplication.processEvents()

            logger.debug("Forced layout update completed")

        except Exception as e:
            logger.exception(f"Error forcing layout update: {e}")

    def validate_layout_arrangement(
        self, grid_layout: QGridLayout, expected_count: int
    ) -> bool:
        """
        Validate that the layout arrangement matches expectations.

        Args:
            grid_layout: The layout to validate
            expected_count: Expected number of widgets in the layout

        Returns:
            True if layout is valid, False otherwise
        """
        try:
            actual_count = grid_layout.count()
            if actual_count != expected_count:
                logger.warning(
                    f"Layout validation failed: expected {expected_count} widgets, "
                    f"found {actual_count}"
                )
                return False

            # Check that all widgets are properly positioned
            for i in range(actual_count):
                item = grid_layout.itemAt(i)
                if not item or not item.widget():
                    logger.warning(
                        f"Layout validation failed: invalid item at position {i}"
                    )
                    return False

            logger.debug(
                f"Layout validation passed: {actual_count} widgets properly arranged"
            )
            return True

        except Exception as e:
            logger.exception(f"Error validating layout arrangement: {e}")
            return False

    def apply_layout_spacing(
        self, grid_layout: QGridLayout, layout_mode: LayoutMode
    ) -> None:
        """
        Apply spacing configuration to the layout.

        Args:
            grid_layout: The layout to apply spacing to
            layout_mode: The layout mode to get spacing for
        """
        try:
            spacing_config = self.layout_service.get_layout_spacing_config(layout_mode)

            grid_layout.setSpacing(spacing_config["grid_spacing"])
            grid_layout.setContentsMargins(
                spacing_config["margins"],
                spacing_config["margins"],
                spacing_config["margins"],
                spacing_config["margins"],
            )

            logger.debug(f"Applied layout spacing for {layout_mode.value} mode")

        except Exception as e:
            logger.exception(f"Error applying layout spacing: {e}")
