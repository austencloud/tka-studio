"""
Dataset Query Service

Handles querying and searching operations on pictograph datasets.
Focused solely on data retrieval and filtering logic.
"""

import logging
from abc import ABC, abstractmethod

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData

from .data_service import IDataManager
from .pictograph_factory import PictographFactory
from .position_resolver import PositionResolver

logger = logging.getLogger(__name__)


class IDatasetQuery(ABC):
    """Interface for dataset querying and searching operations."""

    @abstractmethod
    def get_start_position_pictograph(
        self, position_key: str, grid_mode: str = "diamond"
    ) -> BeatData | None:
        """Get the actual pictograph data for a start position as BeatData with embedded pictograph."""

    @abstractmethod
    def get_start_position_pictograph_data(
        self, position_key: str, grid_mode: str = "diamond"
    ) -> PictographData | None:
        """Get pictograph data for a start position (proper domain model)."""

    @abstractmethod
    def find_pictograph_by_criteria(
        self, letter: str, start_pos: str, end_pos: str, grid_mode: str = "diamond"
    ) -> BeatData | None:
        """Find a pictograph by specific criteria."""

    @abstractmethod
    def find_pictographs_by_letter(
        self, letter: str, grid_mode: str = "diamond"
    ) -> list[BeatData]:
        """Find all pictographs with a specific letter."""

    @abstractmethod
    def find_pictographs_by_position_range(
        self, start_positions: list[str], grid_mode: str = "diamond"
    ) -> list[BeatData]:
        """Find pictographs within a range of start positions."""

    @abstractmethod
    def get_available_letters(self, grid_mode: str = "diamond") -> list[str]:
        """Get all available letters in the dataset."""

    @abstractmethod
    def get_available_positions(self, grid_mode: str = "diamond") -> dict:
        """Get all available positions in the dataset."""


class DatasetQuery(IDatasetQuery):
    """
    Handles querying and searching operations on pictograph datasets.

    Responsible for:
    - Finding pictographs by various criteria
    - Retrieving start position entries
    - Filtering dataset entries
    - Converting query results to domain objects
    """

    def __init__(self, data_service: IDataManager):
        """Initialize the dataset query service."""
        self.data_service = data_service
        self.pictograph_factory = PictographFactory()
        self.position_resolver = PositionResolver()

    def get_start_position_pictograph(
        self, position_key: str, grid_mode: str = "diamond"
    ) -> BeatData | None:
        """
        Get the actual pictograph data for a start position as BeatData with embedded pictograph.

        Args:
            position_key: Position key like "alpha1_alpha1", "beta5_beta5"
            grid_mode: "diamond" or "box"

        Returns:
            BeatData object with embedded pictograph data, or None if not found
        """
        try:
            # Validate position key format
            parsed = self.position_resolver.parse_position_key(position_key)
            if not parsed:
                return None

            start_pos, end_pos = parsed

            # Get the appropriate dataset
            dataset = self.data_service.get_dataset_by_mode(grid_mode)
            if dataset is None or dataset.empty:
                return None

            # Find matching entry where start_pos == end_pos (start position entries)
            matching_entries = dataset[
                (dataset["start_pos"] == start_pos) & (dataset["end_pos"] == end_pos)
            ]

            if matching_entries.empty:
                return None

            # Take the first matching entry and convert to BeatData with embedded pictograph
            entry = matching_entries.iloc[0]
            pictograph_data = self.pictograph_factory.create_pictograph_data_from_entry(
                entry, grid_mode
            )

            # Use BeatFactory to create start position beat with embedded pictograph
            from shared.application.services.sequence.beat_factory import BeatFactory

            beat_data = BeatFactory.create_start_position_beat_data(pictograph_data)
            return beat_data

        except Exception as e:
            # Only log actual unexpected errors, not validation failures
            if "split" not in str(e) and "NoneType" not in str(e):
                logger.error(f"Error getting start position {position_key}: {e}")
            return None

    def get_start_position_pictograph_data(
        self, position_key: str, grid_mode: str = "diamond"
    ) -> PictographData | None:
        """
        Get pictograph data for a start position (proper domain model).

        Args:
            position_key: Position key like "alpha1_alpha1", "beta5_beta5"
            grid_mode: "diamond" or "box"

        Returns:
            PictographData object with motion data, or None if not found
        """
        try:
            # Validate position key format
            parsed = self.position_resolver.parse_position_key(position_key)
            if not parsed:
                return None

            start_pos, end_pos = parsed

            # Get the appropriate dataset
            dataset = self.data_service.get_dataset_by_mode(grid_mode)
            if dataset is None or dataset.empty:
                return None

            # Find matching entries
            matching_entries = dataset[
                (dataset["start_pos"] == start_pos) & (dataset["end_pos"] == end_pos)
            ]

            if matching_entries.empty:
                return None

            # Take the first matching entry and convert to PictographData
            entry = matching_entries.iloc[0]
            return self.pictograph_factory.create_pictograph_data_from_entry(
                entry, grid_mode
            )

        except Exception as e:
            logger.error(f"Error getting pictograph data for {position_key}: {e}")
            return None

    def find_pictograph_by_criteria(
        self, letter: str, start_pos: str, end_pos: str, grid_mode: str = "diamond"
    ) -> BeatData | None:
        """
        Find a pictograph by specific criteria.

        Args:
            letter: Letter to search for
            start_pos: Start position
            end_pos: End position
            grid_mode: "diamond" or "box"

        Returns:
            BeatData object if found, None otherwise
        """
        try:
            # Get the appropriate dataset
            dataset = self.data_service.get_dataset_by_mode(grid_mode)
            if dataset is None or dataset.empty:
                return None

            # Find matching entries
            matching_entries = dataset[
                (dataset["letter"] == letter)
                & (dataset["start_pos"] == start_pos)
                & (dataset["end_pos"] == end_pos)
            ]

            if matching_entries.empty:
                return None

            # Take the first matching entry and convert
            entry = matching_entries.iloc[0]
            pictograph_data = self.pictograph_factory.create_pictograph_data_from_entry(
                entry, grid_mode
            )
            return self.pictograph_factory.convert_pictograph_to_beat_data(
                pictograph_data
            )

        except Exception as e:
            logger.error(f"Error finding pictograph by criteria: {e}")
            return None

    def find_pictographs_by_letter(
        self, letter: str, grid_mode: str = "diamond"
    ) -> list[BeatData]:
        """
        Find all pictographs with a specific letter.

        Args:
            letter: Letter to search for
            grid_mode: "diamond" or "box"

        Returns:
            List of BeatData objects matching the letter
        """
        try:
            # Get the appropriate dataset
            dataset = self.data_service.get_dataset_by_mode(grid_mode)
            if dataset is None or dataset.empty:
                return []

            # Find matching entries
            matching_entries = dataset[dataset["letter"] == letter]

            if matching_entries.empty:
                return []

            # Convert all matching entries
            results = []
            for _, entry in matching_entries.iterrows():
                try:
                    pictograph_data = (
                        self.pictograph_factory.create_pictograph_data_from_entry(
                            entry, grid_mode
                        )
                    )
                    beat_data = self.pictograph_factory.convert_pictograph_to_beat_data(
                        pictograph_data
                    )
                    results.append(beat_data)
                except Exception as e:
                    logger.warning(f"Error converting entry for letter {letter}: {e}")
                    continue

            return results

        except Exception as e:
            logger.error(f"Error finding pictographs by letter {letter}: {e}")
            return []

    def find_pictographs_by_position_range(
        self, start_positions: list[str], grid_mode: str = "diamond"
    ) -> list[BeatData]:
        """
        Find pictographs within a range of start positions.

        Args:
            start_positions: List of start positions to search
            grid_mode: "diamond" or "box"

        Returns:
            List of BeatData objects matching the position range
        """
        try:
            # Get the appropriate dataset
            dataset = self.data_service.get_dataset_by_mode(grid_mode)
            if dataset is None or dataset.empty:
                return []

            # Find matching entries
            matching_entries = dataset[dataset["start_pos"].isin(start_positions)]

            if matching_entries.empty:
                return []

            # Convert all matching entries
            results = []
            for _, entry in matching_entries.iterrows():
                try:
                    pictograph_data = (
                        self.pictograph_factory.create_pictograph_data_from_entry(
                            entry, grid_mode
                        )
                    )
                    beat_data = self.pictograph_factory.convert_pictograph_to_beat_data(
                        pictograph_data
                    )
                    results.append(beat_data)
                except Exception as e:
                    logger.warning(f"Error converting entry in position range: {e}")
                    continue

            return results

        except Exception as e:
            logger.error(f"Error finding pictographs by position range: {e}")
            return []

    def get_available_letters(self, grid_mode: str = "diamond") -> list[str]:
        """
        Get all available letters in the dataset.

        Args:
            grid_mode: "diamond" or "box"

        Returns:
            List of unique letters available in the dataset
        """
        try:
            # Get the appropriate dataset
            dataset = self.data_service.get_dataset_by_mode(grid_mode)
            if dataset is None or dataset.empty:
                return []

            # Get unique letters and sort them
            letters = dataset["letter"].unique().tolist()
            return sorted(
                [letter for letter in letters if letter and str(letter) != "nan"]
            )

        except Exception as e:
            logger.error(f"Error getting available letters: {e}")
            return []

    def get_available_positions(self, grid_mode: str = "diamond") -> dict:
        """
        Get all available positions in the dataset.

        Args:
            grid_mode: "diamond" or "box"

        Returns:
            Dictionary with start_positions and end_positions lists
        """
        try:
            # Get the appropriate dataset
            dataset = self.data_service.get_dataset_by_mode(grid_mode)
            if dataset is None or dataset.empty:
                return {"start_positions": [], "end_positions": []}

            # Get unique positions
            start_positions = dataset["start_pos"].unique().tolist()
            end_positions = dataset["end_pos"].unique().tolist()

            # Filter out invalid values
            start_positions = [
                pos for pos in start_positions if pos and str(pos) != "nan"
            ]
            end_positions = [pos for pos in end_positions if pos and str(pos) != "nan"]

            return {
                "start_positions": sorted(start_positions),
                "end_positions": sorted(end_positions),
            }

        except Exception as e:
            logger.error(f"Error getting available positions: {e}")
            return {"start_positions": [], "end_positions": []}
