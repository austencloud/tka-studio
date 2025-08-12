"""
Start Position Data Service

Handles data retrieval and caching for start position operations.
Extracts data access logic from presentation components.
"""

import logging
from functools import lru_cache

from desktop.modern.core.interfaces.start_position_services import (
    IStartPositionDataService,
)
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from shared.application.services.data.dataset_query import DatasetQuery, IDatasetQuery

logger = logging.getLogger(__name__)


class StartPositionDataService(IStartPositionDataService):
    """
    Service for retrieving start position data from the dataset.

    Responsibilities:
    - Abstracting dataset access for start positions
    - Caching frequently accessed position data
    - Providing clean interface for position data retrieval
    - Error handling for data access operations
    """

    def __init__(self, dataset_service: IDatasetQuery | None = None):
        """
        Initialize the start position data service.

        Args:
            dataset_service: Optional dataset service for dependency injection
        """
        if dataset_service:
            self.dataset_service = dataset_service
        else:
            # Create DataManager and DatasetQuery
            from desktop.modern.core.config.data_config import create_data_config
            from shared.application.services.data.data_service import DataManager

            data_manager = DataManager(create_data_config())
            self.dataset_service = DatasetQuery(data_manager)
        logger.debug("StartPositionDataService initialized")

    def get_position_data(
        self, position_key: str, grid_mode: str = "diamond"
    ) -> PictographData | None:
        """
        Get pictograph data for a start position.

        Args:
            position_key: Position key like "alpha1_alpha1"
            grid_mode: Grid mode ("diamond" or "box")

        Returns:
            PictographData if found, None otherwise
        """
        try:
            logger.debug(
                f"Retrieving position data for {position_key} in {grid_mode} mode"
            )

            # Use the existing dataset service method
            pictograph_data = self.dataset_service.get_start_position_pictograph_data(
                position_key, grid_mode
            )

            if pictograph_data:
                logger.debug(f"Successfully retrieved position data for {position_key}")
                return pictograph_data
            else:
                logger.warning(
                    f"No position data found for {position_key} in {grid_mode} mode"
                )
                return None

        except Exception as e:
            logger.error(f"Error retrieving position data for {position_key}: {e}")
            return None

    def get_available_positions(self, grid_mode: str = "diamond") -> list[str]:
        """
        Get all available start positions for a grid mode.

        Args:
            grid_mode: Grid mode ("diamond" or "box")

        Returns:
            List of available position keys
        """
        try:
            logger.debug(f"Retrieving available positions for {grid_mode} mode")

            # Get available positions from dataset service
            positions_dict = self.dataset_service.get_available_positions(grid_mode)
            start_positions = positions_dict.get("start_positions", [])

            # Filter for start position format (position_position)
            start_position_keys = []
            for pos in start_positions:
                if pos and "_" not in pos:
                    # Create start position key format (position_position for start positions)
                    start_position_keys.append(f"{pos}_{pos}")

            logger.debug(f"Found {len(start_position_keys)} available start positions")
            return start_position_keys

        except Exception as e:
            logger.error(f"Error retrieving available positions for {grid_mode}: {e}")
            return []

    def get_position_beat_data(
        self, position_key: str, grid_mode: str = "diamond"
    ) -> BeatData | None:
        """
        Get complete beat data for a start position.

        Args:
            position_key: Position key like "alpha1_alpha1"
            grid_mode: Grid mode ("diamond" or "box")

        Returns:
            BeatData with embedded pictograph if found, None otherwise
        """
        try:
            logger.debug(f"Retrieving beat data for {position_key} in {grid_mode} mode")

            # Use the existing dataset service method
            beat_data = self.dataset_service.get_start_position_pictograph(
                position_key, grid_mode
            )

            if beat_data:
                logger.debug(f"Successfully retrieved beat data for {position_key}")
                return beat_data
            else:
                logger.warning(
                    f"No beat data found for {position_key} in {grid_mode} mode"
                )
                return None

        except Exception as e:
            logger.error(f"Error retrieving beat data for {position_key}: {e}")
            return None

    @lru_cache(maxsize=128)
    def _get_cached_position_data(
        self, position_key: str, grid_mode: str
    ) -> PictographData | None:
        """
        Internal cached method for frequently accessed position data.

        Args:
            position_key: Position key to retrieve
            grid_mode: Grid mode

        Returns:
            Cached PictographData if available, None otherwise
        """
        return self.get_position_data(position_key, grid_mode)

    def clear_cache(self):
        """Clear the internal cache for position data."""
        self._get_cached_position_data.cache_clear()
        logger.debug("StartPositionDataService cache cleared")
