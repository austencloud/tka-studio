"""
Mock Pictograph Data Service for Learn Tab Testing

Provides a simple implementation of IPictographDataService for testing
the Learn Tab functionality without requiring the full pictograph system.
"""

import logging
from typing import Any, Optional

from desktop.modern.core.interfaces.data_builder_services import IPictographDataService

logger = logging.getLogger(__name__)


class MockPictographDataService(IPictographDataService):
    """
    Mock implementation of IPictographDataService for Learn Tab testing.

    Provides minimal functionality to support question generation
    without requiring the full pictograph data infrastructure.
    """

    def __init__(self):
        """Initialize mock service with test data."""
        self._mock_data: dict[str, Any] = {}
        self._initialize_test_data()
        logger.info("Mock pictograph data service initialized")

    def get_pictograph_data(self, pictograph_id: str) -> Optional[Any]:
        """
        Get pictograph data by ID.

        Args:
            pictograph_id: Unique identifier for pictograph

        Returns:
            Mock pictograph data or None if not found
        """
        return self._mock_data.get(pictograph_id)

    def save_pictograph_data(self, pictograph_id: str, data: Any) -> bool:
        """
        Save pictograph data.

        Args:
            pictograph_id: Unique identifier for pictograph
            data: Pictograph data to save

        Returns:
            True (always succeeds in mock)
        """
        self._mock_data[pictograph_id] = data
        return True

    def delete_pictograph_data(self, pictograph_id: str) -> bool:
        """
        Delete pictograph data.

        Args:
            pictograph_id: Unique identifier for pictograph

        Returns:
            True if deleted successfully
        """
        if pictograph_id in self._mock_data:
            del self._mock_data[pictograph_id]
            return True
        return False

    def list_pictograph_ids(self) -> list[str]:
        """
        List all pictograph IDs.

        Returns:
            List of pictograph identifiers
        """
        return list(self._mock_data.keys())

    def search_pictographs(self, search_criteria: dict[str, Any]) -> list[Any]:
        """
        Search pictographs by criteria.

        Args:
            search_criteria: Search criteria dictionary

        Returns:
            List of matching pictographs
        """
        results = []
        letter = search_criteria.get("letter")

        if letter:
            # Return mock pictographs for the specified letter
            for pictograph_id, data in self._mock_data.items():
                if data.get("letter") == letter:
                    results.append(data)
        else:
            # Return all pictographs if no specific criteria
            results = list(self._mock_data.values())

        return results

    def validate_pictograph_data(self, data: Any) -> tuple[bool, list[str]]:
        """
        Validate pictograph data.

        Args:
            data: Pictograph data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        if not isinstance(data, dict):
            errors.append("Data must be a dictionary")
        else:
            if "id" not in data:
                errors.append("Missing required field: id")
            if "letter" not in data:
                errors.append("Missing required field: letter")

        return len(errors) == 0, errors

    def get_pictograph_metadata(self, pictograph_id: str) -> Optional[dict[str, Any]]:
        """
        Get pictograph metadata.

        Args:
            pictograph_id: Unique identifier for pictograph

        Returns:
            Metadata dictionary or None if not found
        """
        data = self._mock_data.get(pictograph_id)
        if data:
            return data.get("metadata", {})
        return None

    def update_pictograph_metadata(
        self, pictograph_id: str, metadata: dict[str, Any]
    ) -> bool:
        """
        Update pictograph metadata.

        Args:
            pictograph_id: Unique identifier for pictograph
            metadata: Metadata to update

        Returns:
            True if updated successfully
        """
        if pictograph_id in self._mock_data:
            if "metadata" not in self._mock_data[pictograph_id]:
                self._mock_data[pictograph_id]["metadata"] = {}
            self._mock_data[pictograph_id]["metadata"].update(metadata)
            return True
        return False

    def get_all_pictograph_ids(self) -> list[str]:
        """Get all available pictograph IDs for testing."""
        return list(self._mock_data.keys())

    def get_pictographs_by_letter(self, letter: str) -> list[dict[str, Any]]:
        """Get mock pictographs for a specific letter with proper PictographData objects."""
        # Import required classes
        try:
            from data.constants import BLUE_ATTRS, END_POS, RED_ATTRS, START_POS
            from desktop.modern.domain.models.enums import GridMode, GridPosition
            from desktop.modern.domain.models.grid_data import GridData
            from desktop.modern.domain.models.pictograph_data import PictographData
        except ImportError:
            # Fallback if imports not available
            logger.error(
                "Could not import required classes for PictographData creation"
            )
            return self._get_fallback_pictographs(letter)

        pictographs = []
        variant = 0

        # Grid position mapping (integer positions to GridPosition enums)
        position_map = {
            1: GridPosition.ALPHA1,
            2: GridPosition.ALPHA3,
            3: GridPosition.ALPHA5,
            4: GridPosition.ALPHA7,
        }

        # Generate pictographs with different start/end position combinations
        for start_pos_int in range(1, 5):  # 1, 2, 3, 4
            for end_pos_int in range(1, 5):  # 1, 2, 3, 4
                variant += 1

                # Create proper PictographData object
                try:
                    pictograph_data = PictographData(
                        id=f"mock_{letter}_{variant}",
                        letter=letter,
                        start_position=position_map.get(
                            start_pos_int, GridPosition.ALPHA1
                        ),
                        end_position=position_map.get(end_pos_int, GridPosition.ALPHA1),
                        grid_data=GridData(grid_mode=GridMode.DIAMOND),
                        metadata={
                            "created_by": "mock_service",
                            "is_test_data": True,
                            "start_pos_int": start_pos_int,
                            "end_pos_int": end_pos_int,
                        },
                    )

                    # Wrap in expected format with position data for legacy compatibility
                    pictograph = {
                        "id": f"mock_{letter}_{variant}",
                        "letter": letter,
                        "type": "mock",
                        START_POS: start_pos_int,  # For legacy question generation
                        END_POS: end_pos_int,  # For legacy question generation
                        "data": pictograph_data,  # For modern rendering
                        BLUE_ATTRS: {
                            "motion_type": "clockwise"
                            if variant % 2 == 0
                            else "counterclockwise",
                            "start_ori": "in",
                            "prop_rot_dir": "clockwise"
                            if variant % 2 == 0
                            else "counterclockwise",
                            "start_loc": "center",
                            "end_loc": "center",
                            "turns": 1,
                        },
                        RED_ATTRS: {
                            "motion_type": "counterclockwise"
                            if variant % 2 == 0
                            else "clockwise",
                            "start_ori": "in",
                            "prop_rot_dir": "counterclockwise"
                            if variant % 2 == 0
                            else "clockwise",
                            "start_loc": "center",
                            "end_loc": "center",
                            "turns": 0,
                        },
                    }
                    pictographs.append(pictograph)

                except Exception as e:
                    logger.warning(
                        f"Failed to create PictographData for {letter}_{variant}: {e}"
                    )
                    # Continue with other pictographs
                    continue

        logger.info(
            f"Generated {len(pictographs)} mock pictographs with PictographData for letter {letter}"
        )
        return pictographs

    def _get_fallback_pictographs(self, letter: str) -> list[dict[str, Any]]:
        """Fallback method when PictographData creation fails."""
        # Simple fallback without PictographData objects
        pictographs = []
        for i in range(1, 5):
            pictograph = {
                "id": f"fallback_{letter}_{i}",
                "letter": letter,
                "type": "fallback",
                "start_pos": i,
                "end_pos": i,
                "data": None,  # No PictographData available
            }
            pictographs.append(pictograph)
        return pictographs

    def get_pictograph_dataset(self) -> dict[str, list[dict[str, Any]]]:
        """
        Get the complete pictograph dataset for question generation.

        Returns:
            Dictionary mapping letters to lists of pictograph data
        """
        dataset = {}
        test_letters = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
        ]

        for letter in test_letters:
            dataset[letter] = self.get_pictographs_by_letter(letter)

        return dataset

    def _initialize_test_data(self) -> None:
        """Initialize mock test data for common letters with PictographData objects."""
        # Import required classes
        try:
            from data.constants import BLUE_ATTRS, END_POS, RED_ATTRS, START_POS
            from desktop.modern.domain.models.enums import GridMode, GridPosition
            from desktop.modern.domain.models.grid_data import GridData
            from desktop.modern.domain.models.pictograph_data import PictographData
        except ImportError:
            logger.error(
                "Could not import required classes - skipping test data initialization"
            )
            return

        test_letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

        # Grid position mapping
        position_map = {
            1: GridPosition.ALPHA1,
            2: GridPosition.ALPHA3,
            3: GridPosition.ALPHA5,
            4: GridPosition.ALPHA7,
        }

        for letter in test_letters:
            variant = 0
            # Generate combinations of start/end positions like legacy system
            for start_pos in range(1, 5):  # 1, 2, 3, 4
                for end_pos in range(1, 5):  # 1, 2, 3, 4
                    variant += 1
                    pictograph_id = f"mock_{letter}_{variant}"

                    try:
                        # Create proper PictographData object
                        pictograph_data = PictographData(
                            id=pictograph_id,
                            letter=letter,
                            start_position=position_map.get(
                                start_pos, GridPosition.ALPHA1
                            ),
                            end_position=position_map.get(end_pos, GridPosition.ALPHA1),
                            grid_data=GridData(grid_mode=GridMode.DIAMOND),
                            metadata={
                                "created_by": "mock_service",
                                "is_test_data": True,
                                "start_pos_int": start_pos,
                                "end_pos_int": end_pos,
                            },
                        )

                        # Store in expected format
                        self._mock_data[pictograph_id] = {
                            "id": pictograph_id,
                            "letter": letter,
                            "type": "mock",
                            START_POS: start_pos,  # Critical for Lesson3
                            END_POS: end_pos,  # Critical for Lesson3
                            "data": pictograph_data,  # For modern rendering
                            BLUE_ATTRS: {
                                "motion_type": "clockwise"
                                if variant % 2 == 0
                                else "counterclockwise",
                                "start_ori": "in",
                                "prop_rot_dir": "clockwise"
                                if variant % 2 == 0
                                else "counterclockwise",
                                "start_loc": "center",
                                "end_loc": "center",
                                "turns": 1,
                            },
                            RED_ATTRS: {
                                "motion_type": "counterclockwise"
                                if variant % 2 == 0
                                else "clockwise",
                                "start_ori": "in",
                                "prop_rot_dir": "counterclockwise"
                                if variant % 2 == 0
                                else "clockwise",
                                "start_loc": "center",
                                "end_loc": "center",
                                "turns": 0,
                            },
                        }

                    except Exception as e:
                        logger.warning(
                            f"Failed to create test data for {pictograph_id}: {e}"
                        )
                        continue

        logger.info(
            f"Initialized mock test data for {len(test_letters)} letters with PictographData objects"
        )
