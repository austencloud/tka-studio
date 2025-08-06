"""
Start Position Orchestrator Service

Coordinates start position operations between multiple services.
Handles complex workflows and service interactions.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from desktop.modern.core.interfaces.start_position_services import (
    IStartPositionDataService,
    IStartPositionOrchestrator,
    IStartPositionSelectionService,
    IStartPositionUIService,
)

# Command processor removed - using Qt signals instead
from desktop.modern.domain.models.pictograph_data import PictographData


try:
    from PyQt6.QtCore import QSize
except ImportError:
    # Mock QSize for environments without PyQt6
    class QSize:
        def __init__(self, width=0, height=0):
            self._width = width
            self._height = height

        def width(self):
            return self._width

        def height(self):
            return self._height


logger = logging.getLogger(__name__)


class StartPositionOrchestrator(IStartPositionOrchestrator):
    """
    Orchestrator service for coordinating start position operations.

    Responsibilities:
    - Coordinating between data, selection, and UI services
    - Handling complete workflows for position selection
    - Managing service interactions and error handling
    - Providing high-level operations for presentation layer
    """

    def __init__(
        self,
        data_service: IStartPositionDataService,
        selection_service: IStartPositionSelectionService,
        ui_service: IStartPositionUIService,
    ):
        """
        Initialize the orchestrator with injected dependencies.

        Args:
            data_service: Service for data operations
            selection_service: Service for selection logic
            ui_service: Service for UI operations
        """
        self.data_service = data_service
        self.selection_service = selection_service
        self.ui_service = ui_service
        logger.debug("StartPositionOrchestrator initialized")

    def handle_position_selection(self, position_key: str) -> bool:
        """
        Handle the complete workflow of position selection.

        Args:
            position_key: Position key selected by user

        Returns:
            True if selection was successful, False otherwise
        """
        try:
            logger.info(f"Handling position selection: {position_key}")

            # Step 1: Validate the selection
            if not self.selection_service.validate_selection(position_key):
                logger.warning(f"Position selection validation failed: {position_key}")
                return False

            # Step 2: Create the selection command
            try:
                command = self.selection_service.create_selection_command(position_key)
            except Exception as e:
                logger.error(f"Failed to create selection command: {e}")
                return False

            # Step 3: Execute the command directly (command processor removed)
            try:
                command.execute()
                logger.info(
                    f"✅ Position selection completed successfully: {position_key}"
                )
                return True
            except Exception as e:
                logger.error(f"❌ Command execution failed: {e}")
                return False

        except Exception as e:
            logger.error(f"❌ Error in position selection workflow: {e}")
            return False

    def get_position_data_for_display(
        self, position_key: str, grid_mode: str
    ) -> Optional[PictographData]:
        """
        Get position data optimized for display in the UI.

        Args:
            position_key: Position key to get data for
            grid_mode: Grid mode ("diamond" or "box")

        Returns:
            PictographData optimized for display, None if not available
        """
        try:
            logger.debug(
                f"Getting position data for display: {position_key} ({grid_mode})"
            )

            # Retrieve data from data service
            pictograph_data = self.data_service.get_position_data(
                position_key, grid_mode
            )

            if pictograph_data:
                logger.debug(
                    f"Successfully retrieved position data for display: {position_key}"
                )
                # TODO: Apply any display-specific optimizations here
                # For now, return the data as-is
                return pictograph_data
            logger.warning(f"No position data available for display: {position_key}")
            return None

        except Exception as e:
            logger.error(f"Error getting position data for display: {e}")
            return None

    def calculate_responsive_layout(
        self, container_size: QSize, position_count: int
    ) -> dict[str, Any]:
        """
        Calculate responsive layout parameters for position options.

        Args:
            container_size: Size of the container widget
            position_count: Number of positions to display

        Returns:
            Dictionary with layout parameters (rows, cols, spacing, etc.)
        """
        try:
            logger.debug(
                f"Calculating responsive layout for {position_count} positions in {container_size}"
            )

            # Delegate to UI service
            layout_params = self.ui_service.calculate_responsive_layout(
                container_size, position_count
            )

            logger.debug(f"Calculated layout parameters: {layout_params}")
            return layout_params

        except Exception as e:
            logger.error(f"Error calculating responsive layout: {e}")
            # Return safe fallback
            return {
                "rows": 1,
                "cols": min(position_count, 3),
                "option_size": 100,
                "spacing": 15,
                "margin": 12,
                "position_count": position_count,
            }

    def get_positions_and_layout_for_mode(
        self, grid_mode: str, is_advanced: bool, container_size: QSize
    ) -> dict[str, Any]:
        """
        Get both position list and layout configuration for a specific mode.

        Args:
            grid_mode: Grid mode ("diamond" or "box")
            is_advanced: True for advanced picker, False for basic
            container_size: Size of the container widget

        Returns:
            Dictionary containing positions list and layout configuration
        """
        try:
            logger.debug(
                f"Getting positions and layout for {grid_mode} mode (advanced={is_advanced})"
            )

            # Get positions from UI service
            positions = self.ui_service.get_positions_for_mode(grid_mode, is_advanced)

            # Get layout configuration
            layout_config = self.ui_service.get_grid_layout_config(
                grid_mode, is_advanced
            )

            # Calculate responsive layout
            responsive_layout = self.calculate_responsive_layout(
                container_size, len(positions)
            )

            # Get style configuration
            style_config = self.ui_service.get_layout_style_config(is_advanced)

            result = {
                "positions": positions,
                "layout_config": layout_config,
                "responsive_layout": responsive_layout,
                "style_config": style_config,
                "grid_mode": grid_mode,
                "is_advanced": is_advanced,
                "position_count": len(positions),
            }

            logger.debug(f"Generated complete configuration for {grid_mode} mode")
            return result

        except Exception as e:
            logger.error(f"Error getting positions and layout for mode: {e}")
            # Safe fallback
            return {
                "positions": ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"],
                "layout_config": {"rows": 1, "cols": 3, "spacing": 15},
                "responsive_layout": {"rows": 1, "cols": 3, "option_size": 100},
                "style_config": {"container_style": "", "scroll_style": ""},
                "grid_mode": grid_mode,
                "is_advanced": is_advanced,
                "position_count": 3,
            }

    def validate_and_normalize_position(self, position_key: str) -> Optional[str]:
        """
        Validate and normalize a position key for consistency.

        Args:
            position_key: Position key to validate and normalize

        Returns:
            Normalized position key if valid, None if invalid
        """
        try:
            # Validate using selection service
            if not self.selection_service.validate_selection(position_key):
                logger.warning(f"Position validation failed: {position_key}")
                return None

            # Normalize using selection service
            normalized_key = self.selection_service.normalize_position_key(position_key)

            logger.debug(
                f"Validated and normalized position: {position_key} -> {normalized_key}"
            )
            return normalized_key

        except Exception as e:
            logger.error(f"Error validating and normalizing position: {e}")
            return None

    def preload_position_data(self, grid_mode: str, is_advanced: bool = False) -> int:
        """
        Preload position data for better performance.

        Args:
            grid_mode: Grid mode ("diamond" or "box")
            is_advanced: True for advanced picker, False for basic

        Returns:
            Number of positions successfully preloaded
        """
        try:
            logger.debug(
                f"Preloading position data for {grid_mode} mode (advanced={is_advanced})"
            )

            # Get positions for the mode
            positions = self.ui_service.get_positions_for_mode(grid_mode, is_advanced)

            loaded_count = 0
            for position_key in positions:
                try:
                    # Attempt to load each position
                    data = self.data_service.get_position_data(position_key, grid_mode)
                    if data:
                        loaded_count += 1
                except Exception as e:
                    logger.warning(f"Failed to preload position {position_key}: {e}")
                    continue

            logger.info(
                f"Preloaded {loaded_count}/{len(positions)} positions for {grid_mode} mode"
            )
            return loaded_count

        except Exception as e:
            logger.error(f"Error preloading position data: {e}")
            return 0
