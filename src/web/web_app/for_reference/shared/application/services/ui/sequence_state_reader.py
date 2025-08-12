"""
Sequence State Reader Service

Service for reading the current sequence state from the workbench UI.
Provides clean abstraction over workbench state access.
"""

import logging
from collections.abc import Callable

from desktop.modern.domain.models.sequence_data import SequenceData

logger = logging.getLogger(__name__)


class SequenceStateReader:
    """
    Service for reading current sequence state from the workbench.

    Provides a clean interface for accessing the current sequence
    being edited in the workbench, abstracting away the details
    of how the workbench stores and manages state.
    """

    def __init__(self, workbench_getter: Callable | None = None):
        """
        Initialize the sequence state reader.

        Args:
            workbench_getter: Function that returns the current workbench instance
        """
        self._workbench_getter = workbench_getter

    def get_current_sequence(self) -> SequenceData | None:
        """
        Get the current sequence from the workbench UI state.

        Returns:
            Current sequence data, or None if no sequence is available
        """
        try:
            # Get the workbench instance
            workbench = self._get_workbench()
            if not workbench:
                logger.warning("No workbench available")
                return None

            # Try to get the sequence from the workbench
            if hasattr(workbench, "get_sequence"):
                sequence = workbench.get_sequence()
                if sequence:
                    logger.debug(f"Retrieved sequence from workbench: {sequence.name}")
                    return sequence
                else:
                    logger.debug("Workbench has no current sequence")
                    return None
            else:
                logger.warning("Workbench does not have get_sequence method")
                return None

        except Exception as e:
            logger.error(f"Failed to get current sequence: {e}")
            return None

    def _get_workbench(self):
        """
        Get the current workbench instance.

        Returns:
            Workbench instance, or None if not available
        """
        if not self._workbench_getter:
            logger.warning("No workbench getter configured")
            return None

        try:
            workbench = self._workbench_getter()
            return workbench
        except Exception as e:
            logger.error(f"Failed to get workbench: {e}")
            return None

    def set_workbench_getter(self, workbench_getter: Callable):
        """
        Set or update the workbench getter function.

        Args:
            workbench_getter: Function that returns the current workbench instance
        """
        self._workbench_getter = workbench_getter
        logger.info("Updated workbench getter")


class MockSequenceStateReader(SequenceStateReader):
    """
    Mock implementation for testing and development.

    Returns a mock sequence for testing purposes.
    """

    def __init__(self):
        """Initialize the mock reader"""
        super().__init__(workbench_getter=None)
        self._mock_sequence = self._create_mock_sequence()

    def get_current_sequence(self) -> SequenceData | None:
        """Return a mock sequence for testing"""
        logger.info("Returning mock sequence for testing")
        return self._mock_sequence

    def _create_mock_sequence(self) -> SequenceData:
        """Create a mock sequence for testing"""
        from desktop.modern.domain.models.beat_data import BeatData

        # Create some mock beats
        beats = [
            BeatData(beat_number=0, metadata={"is_start_position": True}),
            BeatData(
                beat_number=1,
            ),
            BeatData(
                beat_number=2,
            ),
        ]

        return SequenceData(
            name="Mock Sequence",
            word="ABC",
            beats=beats,
            metadata={"created_for": "testing"},
        )
