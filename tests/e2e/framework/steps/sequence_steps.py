"""
Sequence Steps for TKA Modern E2E Testing Framework

This module provides the SequenceSteps class that encapsulates
sequence building operations and workflows, making tests more
readable and maintainable.
"""

import logging
from typing import Any, Optional

from PyQt6.QtTest import QTest

logger = logging.getLogger(__name__)


class SequenceSteps:
    """
    Reusable sequence building operations for TKA E2E tests.

    This class provides high-level sequence manipulation methods that combine
    multiple page object interactions into meaningful workflow steps.
    """

    def __init__(self, sequence_workbench, option_picker):
        """
        Initialize sequence steps.

        Args:
            sequence_workbench: SequenceWorkbenchPage instance
            option_picker: OptionPickerPage instance
        """
        self.workbench = sequence_workbench
        self.option_picker = option_picker

        logger.debug("SequenceSteps initialized")

    def build_sequence(self, length: int) -> bool:
        """
        Build a sequence of specified length by selecting available options.

        Args:
            length: Target sequence length

        Returns:
            bool: True if sequence built successfully, False otherwise
        """
        logger.info(f"Building sequence of length {length}")

        # Ensure components are ready
        if not self._ensure_components_ready():
            return False

        # Get initial sequence length
        initial_length = self.workbench.get_sequence_length()
        logger.debug(f"Initial sequence length: {initial_length}")

        # Build sequence step by step
        for i in range(length):
            step_number = i + 1
            logger.debug(f"Building sequence step {step_number}/{length}")

            if not self._add_next_option():
                logger.error(f"Failed to add option at step {step_number}")
                return False

            # Wait for UI to update
            QTest.qWait(500)

            # Verify length increased
            current_length = self.workbench.get_sequence_length()
            expected_length = initial_length + step_number

            if current_length != expected_length:
                logger.warning(
                    f"Unexpected sequence length at step {step_number}: "
                    f"expected {expected_length}, got {current_length}"
                )

        # Final verification
        final_length = self.workbench.get_sequence_length()
        target_length = initial_length + length

        if final_length == target_length:
            logger.info(f"Successfully built sequence: final length {final_length}")
            return True
        else:
            logger.error(
                f"Sequence building failed: expected {target_length}, got {final_length}"
            )
            return False

    def add_single_option(self, option_identifier: Optional[str] = None) -> bool:
        """
        Add a single option to the sequence.

        Args:
            option_identifier: Specific option to add, or None for first available

        Returns:
            bool: True if option added successfully, False otherwise
        """
        logger.info(f"Adding single option: {option_identifier or 'first available'}")

        if option_identifier:
            return self.option_picker.select_option(option_identifier)
        else:
            return self._add_next_option()

    def clear_sequence(self) -> bool:
        """
        Clear the current sequence.

        Returns:
            bool: True if sequence cleared successfully, False otherwise
        """
        logger.info("Clearing sequence")

        if not self.workbench.clear_sequence():
            logger.error("Failed to clear sequence")
            return False

        # Verify sequence was cleared
        QTest.qWait(500)  # Wait for clearing to complete
        length = self.workbench.get_sequence_length()

        if length == 0:
            logger.info("Sequence cleared successfully")
            return True
        else:
            logger.error(f"Sequence not fully cleared: length is {length}")
            return False

    def rebuild_sequence(self, new_length: int) -> bool:
        """
        Clear current sequence and build a new one.

        Args:
            new_length: Length of new sequence to build

        Returns:
            bool: True if rebuild successful, False otherwise
        """
        logger.info(f"Rebuilding sequence with length {new_length}")

        # Clear existing sequence
        if not self.clear_sequence():
            logger.error("Failed to clear sequence for rebuild")
            return False

        # Build new sequence
        if not self.build_sequence(new_length):
            logger.error("Failed to build new sequence")
            return False

        logger.info(f"Successfully rebuilt sequence with length {new_length}")
        return True

    def extend_sequence(self, additional_length: int) -> bool:
        """
        Extend current sequence by adding more options.

        Args:
            additional_length: Number of options to add

        Returns:
            bool: True if extension successful, False otherwise
        """
        logger.info(f"Extending sequence by {additional_length} options")

        initial_length = self.workbench.get_sequence_length()

        if not self.build_sequence(additional_length):
            logger.error("Failed to extend sequence")
            return False

        final_length = self.workbench.get_sequence_length()
        expected_length = initial_length + additional_length

        if final_length == expected_length:
            logger.info(
                f"Successfully extended sequence: {initial_length} -> {final_length}"
            )
            return True
        else:
            logger.error(
                f"Extension failed: expected {expected_length}, got {final_length}"
            )
            return False

    def build_sequence_with_specific_options(
        self, option_identifiers: list[str]
    ) -> bool:
        """
        Build sequence using specific options in order.

        Args:
            option_identifiers: List of option identifiers to select in order

        Returns:
            bool: True if sequence built successfully, False otherwise
        """
        logger.info(f"Building sequence with specific options: {option_identifiers}")

        initial_length = self.workbench.get_sequence_length()

        for i, option_id in enumerate(option_identifiers):
            step_number = i + 1
            logger.debug(
                f"Adding specific option {step_number}/{len(option_identifiers)}: {option_id}"
            )

            if not self.option_picker.select_option(option_id):
                logger.error(
                    f"Failed to select option '{option_id}' at step {step_number}"
                )
                return False

            QTest.qWait(500)  # Wait for processing

        # Verify final length
        final_length = self.workbench.get_sequence_length()
        expected_length = initial_length + len(option_identifiers)

        if final_length == expected_length:
            logger.info("Successfully built sequence with specific options")
            return True
        else:
            logger.error(
                f"Specific sequence building failed: expected {expected_length}, got {final_length}"
            )
            return False

    def get_sequence_info(self) -> dict[str, Any]:
        """
        Get comprehensive information about the current sequence.

        Returns:
            Dict: Sequence information including length, validity, data
        """
        logger.debug("Getting sequence information")

        info = {
            "length": self.workbench.get_sequence_length(),
            "is_valid": self.workbench.is_sequence_valid(),
            "data": self.workbench.get_sequence_data(),
            "available_options": self.option_picker.get_available_options(),
            "option_count": self.option_picker.get_option_count(),
        }

        logger.debug(
            f"Sequence info: length={info['length']}, valid={info['is_valid']}, "
            f"options_available={info['option_count']}"
        )

        return info

    def _add_next_option(self) -> bool:
        """
        Add the next available option to the sequence.

        Returns:
            bool: True if option added successfully, False otherwise
        """
        # Get available options
        options = self.option_picker.get_available_options()
        if not options:
            logger.error("No options available to add")
            return False

        # Select the first available option
        first_option = options[0]
        logger.debug(f"Selecting first available option: {first_option}")

        return self.option_picker.select_option(first_option)

    def _ensure_components_ready(self) -> bool:
        """
        Ensure all required components are ready for sequence building.

        Returns:
            bool: True if components are ready, False otherwise
        """
        # Check workbench
        if not self.workbench.wait_for_load():
            logger.error("Sequence workbench not ready")
            return False

        # Check option picker
        if not self.option_picker.wait_for_load():
            logger.error("Option picker not ready")
            return False

        # Check if options are available
        if not self.option_picker.has_options_available():
            logger.error("No options available for sequence building")
            return False

        logger.debug("All sequence building components are ready")
        return True
