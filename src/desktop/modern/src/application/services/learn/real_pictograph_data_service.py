"""
Real Pictograph Data Service for Learn Tab

Adapter that implements IPictographDataService using the existing PictographDataManager.
This bridges the Learn Tab's expected interface with the actual TKA data services.
"""

import logging
from typing import Optional, Any, Dict, List, Tuple

from core.interfaces.data_builder_services import IPictographDataService
from core.interfaces.pictograph_services import IPictographDataManager
from application.services.data.dataset_query import IDatasetQuery
from domain.models.beat_data import BeatData
from domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)


class RealPictographDataService(IPictographDataService):
    """
    Adapter that implements IPictographDataService using existing TKA services.

    This service bridges the Learn Tab's expected interface with the actual
    PictographDataManager and dataset services to provide real pictograph data.
    """

    def __init__(self, container):
        """Initialize adapter with existing TKA services."""
        self.container = container
        self._pictograph_manager: Optional[IPictographDataManager] = None
        self._dataset_query_service: Optional[IDatasetQuery] = None
        self._dataset_cache: Optional[Dict[str, List[BeatData]]] = None
        logger.info(
            "🎯 REAL PICTOGRAPH DATA SERVICE INITIALIZED - Using actual TKA dataset!"
        )

    @property
    def pictograph_manager(self) -> IPictographDataManager:
        """Lazy-loaded pictograph data manager."""
        if self._pictograph_manager is None:
            try:
                self._pictograph_manager = self.container.resolve(
                    IPictographDataManager
                )
                logger.info("Pictograph data manager resolved successfully")
            except Exception as e:
                logger.error(f"Failed to resolve PictographDataManager: {e}")
                raise
        return self._pictograph_manager

    @property
    def dataset_query_service(self) -> IDatasetQuery:
        """Lazy-loaded dataset query service."""
        if self._dataset_query_service is None:
            try:
                self._dataset_query_service = self.container.resolve(IDatasetQuery)
                logger.info("Dataset query service resolved successfully")
            except Exception as e:
                logger.error(f"Failed to resolve DatasetQuery service: {e}")
                raise
        return self._dataset_query_service

    def get_pictograph_data(self, pictograph_id: str) -> Optional[PictographData]:
        """
        Get pictograph data by ID.

        Args:
            pictograph_id: Unique identifier for pictograph

        Returns:
            PictographData object or None if not found
        """
        try:
            # Check cache first
            if pictograph_id in self._pictograph_cache:
                return self._pictograph_cache[pictograph_id]

            # For Learn Tab, pictograph_id format is "letter_index" (e.g., "A_0", "B_1")
            if "_" in pictograph_id:
                letter, index_str = pictograph_id.split("_", 1)
                try:
                    index = int(index_str)
                    beat_data_list = (
                        self.dataset_query_service.find_pictographs_by_letter(letter)
                    )

                    if index < len(beat_data_list):
                        beat_data = beat_data_list[index]
                        if beat_data.has_pictograph:
                            pictograph_data = beat_data.pictograph_data
                            # Cache the result
                            self._pictograph_cache[pictograph_id] = pictograph_data
                            return pictograph_data
                except (ValueError, IndexError):
                    pass

            logger.warning(f"Pictograph not found for ID: {pictograph_id}")
            return None

        except Exception as e:
            logger.error(f"Error getting pictograph data for {pictograph_id}: {e}")
            return None

    def get_pictographs_by_letter(self, letter: str) -> List[Dict[str, Any]]:
        """
        Get pictographs for a specific letter.

        Args:
            letter: Letter to search for

        Returns:
            List of pictograph data dictionaries
        """
        try:
            beat_data_list = self.dataset_query_service.find_pictographs_by_letter(
                letter
            )

            pictographs = []
            for i, beat_data in enumerate(beat_data_list):
                if beat_data.has_pictograph:
                    pictograph_dict = {
                        "id": f"{letter}_{i}",
                        "letter": letter,
                        "type": "real",
                        "data": beat_data.pictograph_data,
                        "beat_data": beat_data,  # Include full beat data for rendering
                    }
                    pictographs.append(pictograph_dict)

            logger.debug(f"Found {len(pictographs)} pictographs for letter {letter}")
            return pictographs

        except Exception as e:
            logger.error(f"Error getting pictographs for letter {letter}: {e}")
            return []

    def get_pictograph_dataset(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get the complete pictograph dataset for question generation.

        Returns:
            Dictionary mapping letters to lists of pictograph data
        """
        try:
            # Use cached dataset if available
            if self._dataset_cache is not None:
                return self._convert_beat_data_to_dict_format(self._dataset_cache)

            # Get all available letters from the dataset
            available_letters = self.dataset_query_service.get_available_letters()
            logger.info(
                f"Loading dataset for {len(available_letters)} letters: {available_letters}"
            )

            # Build dataset dictionary
            dataset = {}
            beat_data_cache = {}

            for letter in available_letters:
                try:
                    beat_data_list = (
                        self.dataset_query_service.find_pictographs_by_letter(letter)
                    )
                    beat_data_cache[letter] = beat_data_list

                    # Convert to dictionary format for compatibility
                    pictographs = []
                    for i, beat_data in enumerate(beat_data_list):
                        if beat_data.has_pictograph:
                            pictograph_data = beat_data.pictograph_data
                            pictograph_dict = {
                                "id": f"{letter}_{i}",
                                "letter": letter,
                                "type": "real",
                                "data": pictograph_data,
                                "beat_data": beat_data,
                            }
                            pictographs.append(pictograph_dict)

                            # Debug: Log pictograph data details
                            if i < 2:  # Log first 2 for each letter
                                logger.info(
                                    f"🎨 {letter}_{i}: PictographData type={type(pictograph_data)}, "
                                    f"has_arrows={hasattr(pictograph_data, 'arrows') and len(pictograph_data.arrows) > 0 if pictograph_data else False}, "
                                    f"has_grid={hasattr(pictograph_data, 'grid_data') if pictograph_data else False}"
                                )
                        else:
                            logger.warning(
                                f"❌ {letter}_{i}: Beat has no pictograph data"
                            )

                    dataset[letter] = pictographs
                    logger.debug(
                        f"Loaded {len(pictographs)} pictographs for letter {letter}"
                    )

                except Exception as e:
                    logger.warning(
                        f"Error loading pictographs for letter {letter}: {e}"
                    )
                    dataset[letter] = []

            # Cache the beat data for future use
            self._dataset_cache = beat_data_cache

            total_pictographs = sum(
                len(pictographs) for pictographs in dataset.values()
            )
            logger.info(
                f"Dataset loaded successfully: {total_pictographs} total pictographs across {len(dataset)} letters"
            )

            return dataset

        except Exception as e:
            logger.error(f"Error loading pictograph dataset: {e}")
            # Return empty dataset as fallback
            return {}

    def _convert_beat_data_to_dict_format(
        self, beat_data_cache: Dict[str, List[BeatData]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Convert cached beat data to dictionary format."""
        dataset = {}
        for letter, beat_data_list in beat_data_cache.items():
            pictographs = []
            for i, beat_data in enumerate(beat_data_list):
                if beat_data.has_pictograph:
                    pictograph_dict = {
                        "id": f"{letter}_{i}",
                        "letter": letter,
                        "type": "real",
                        "data": beat_data.pictograph_data,
                        "beat_data": beat_data,
                    }
                    pictographs.append(pictograph_dict)
            dataset[letter] = pictographs
        return dataset

    def search_pictographs(self, criteria: Dict[str, Any]) -> List[Any]:
        """
        Search pictographs by criteria.

        Args:
            criteria: Search criteria dictionary

        Returns:
            List of matching pictographs
        """
        try:
            # Extract search criteria
            letter = criteria.get("letter")
            start_pos = criteria.get("start_pos")
            end_pos = criteria.get("end_pos")

            if letter and start_pos and end_pos:
                # Search by specific criteria
                beat_data = self.dataset_query_service.find_pictograph_by_criteria(
                    letter, start_pos, end_pos
                )
                return [beat_data] if beat_data else []

            elif letter:
                # Search by letter only
                return self.dataset_query_service.find_pictographs_by_letter(letter)

            else:
                logger.warning(f"Unsupported search criteria: {criteria}")
                return []

        except Exception as e:
            logger.error(f"Error searching pictographs: {e}")
            return []

    def save_pictograph_data(self, pictograph_id: str, data: Any) -> bool:
        """
        Save pictograph data (not implemented for Learn Tab).

        Args:
            pictograph_id: Unique identifier for pictograph
            data: Pictograph data to save

        Returns:
            False - Learn Tab is read-only
        """
        logger.warning("Save operation not supported in Learn Tab (read-only mode)")
        return False

    def delete_pictograph_data(self, pictograph_id: str) -> bool:
        """
        Delete pictograph data (not implemented for Learn Tab).

        Args:
            pictograph_id: Unique identifier for pictograph

        Returns:
            False - Learn Tab is read-only
        """
        logger.warning("Delete operation not supported in Learn Tab (read-only mode)")
        return False

    def list_pictograph_ids(self) -> List[str]:
        """
        List all pictograph IDs.

        Returns:
            List of pictograph identifiers in "letter_index" format
        """
        try:
            pictograph_ids = []
            dataset = self.get_pictograph_dataset()

            for letter, beat_data_list in dataset.items():
                for index, beat_data in enumerate(beat_data_list):
                    if beat_data.has_pictograph:
                        pictograph_ids.append(f"{letter}_{index}")

            return pictograph_ids

        except Exception as e:
            logger.error(f"Error listing pictograph IDs: {e}")
            return []

    def validate_pictograph_data(self, data: Any) -> Tuple[bool, List[str]]:
        """
        Validate pictograph data.

        Args:
            data: Pictograph data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        try:
            if not isinstance(data, PictographData):
                return False, ["Data must be a PictographData instance"]

            errors = []

            # Basic validation
            if not hasattr(data, "grid_data") or data.grid_data is None:
                errors.append("Missing grid_data")

            if not hasattr(data, "arrows"):
                errors.append("Missing arrows")

            return len(errors) == 0, errors

        except Exception as e:
            logger.error(f"Error validating pictograph data: {e}")
            return False, [f"Validation error: {e}"]

    def get_pictograph_metadata(self, pictograph_id: str) -> Optional[Dict[str, Any]]:
        """
        Get pictograph metadata.

        Args:
            pictograph_id: Unique identifier for pictograph

        Returns:
            Metadata dictionary or None if not found
        """
        try:
            pictograph_data = self.get_pictograph_data(pictograph_id)
            if pictograph_data and hasattr(pictograph_data, "metadata"):
                return pictograph_data.metadata
            return None

        except Exception as e:
            logger.error(f"Error getting pictograph metadata: {e}")
            return None

    def update_pictograph_metadata(
        self, pictograph_id: str, metadata: Dict[str, Any]
    ) -> bool:
        """
        Update pictograph metadata (not implemented for Learn Tab).

        Args:
            pictograph_id: Unique identifier for pictograph
            metadata: Metadata to update

        Returns:
            False - Learn Tab is read-only
        """
        logger.warning(
            "Update metadata operation not supported in Learn Tab (read-only mode)"
        )
        return False
