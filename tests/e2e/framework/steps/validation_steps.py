"""
Validation Steps for TKA Modern E2E Testing Framework

This module provides the ValidationSteps class that encapsulates
common validation operations and assertions, making tests more
readable and maintainable.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class ValidationSteps:
    """
    Reusable validation operations for TKA E2E tests.

    This class provides high-level validation methods that combine
    multiple checks and assertions into meaningful validation steps.
    """

    def __init__(self, sequence_workbench):
        """
        Initialize validation steps.

        Args:
            sequence_workbench: SequenceWorkbenchPage instance
        """
        self.workbench = sequence_workbench

        logger.debug("ValidationSteps initialized")

    def sequence_has_length(self, expected_length: int) -> bool:
        """
        Validate that sequence has the expected length.

        Args:
            expected_length: Expected sequence length

        Returns:
            bool: True if length matches, False otherwise
        """
        actual_length = self.workbench.get_sequence_length()

        if actual_length == expected_length:
            logger.debug(f"Sequence length validation passed: {actual_length}")
            return True
        else:
            logger.error(
                f"Sequence length validation failed: expected {expected_length}, got {actual_length}"
            )
            return False

    def sequence_is_valid(self) -> bool:
        """
        Validate that the current sequence is in a valid state.

        Returns:
            bool: True if sequence is valid, False otherwise
        """
        is_valid = self.workbench.is_sequence_valid()

        if is_valid:
            logger.debug("Sequence validity validation passed")
        else:
            logger.error("Sequence validity validation failed")

        return is_valid

    def sequence_is_empty(self) -> bool:
        """
        Validate that the sequence is empty.

        Returns:
            bool: True if sequence is empty, False otherwise
        """
        return self.sequence_has_length(0)

    def sequence_is_not_empty(self) -> bool:
        """
        Validate that the sequence is not empty.

        Returns:
            bool: True if sequence has elements, False otherwise
        """
        length = self.workbench.get_sequence_length()

        if length > 0:
            logger.debug(f"Sequence non-empty validation passed: length {length}")
            return True
        else:
            logger.error("Sequence non-empty validation failed: sequence is empty")
            return False

    def sequence_length_in_range(self, min_length: int, max_length: int) -> bool:
        """
        Validate that sequence length is within specified range.

        Args:
            min_length: Minimum acceptable length (inclusive)
            max_length: Maximum acceptable length (inclusive)

        Returns:
            bool: True if length is in range, False otherwise
        """
        actual_length = self.workbench.get_sequence_length()

        if min_length <= actual_length <= max_length:
            logger.debug(
                f"Sequence length range validation passed: {actual_length} in [{min_length}, {max_length}]"
            )
            return True
        else:
            logger.error(
                f"Sequence length range validation failed: {actual_length} not in [{min_length}, {max_length}]"
            )
            return False

    def sequence_length_increased_by(
        self, expected_increase: int, initial_length: int
    ) -> bool:
        """
        Validate that sequence length increased by expected amount.

        Args:
            expected_increase: Expected increase in length
            initial_length: Initial sequence length before operation

        Returns:
            bool: True if increase matches expectation, False otherwise
        """
        current_length = self.workbench.get_sequence_length()
        actual_increase = current_length - initial_length

        if actual_increase == expected_increase:
            logger.debug(
                f"Sequence length increase validation passed: increased by {actual_increase}"
            )
            return True
        else:
            logger.error(
                f"Sequence length increase validation failed: "
                f"expected increase {expected_increase}, actual increase {actual_increase}"
            )
            return False

    def workbench_is_functional(self) -> bool:
        """
        Validate that the workbench is loaded and functional.

        Returns:
            bool: True if workbench is functional, False otherwise
        """
        if not self.workbench.is_loaded():
            logger.error("Workbench functionality validation failed: not loaded")
            return False

        # Try to get sequence length as a basic functionality test
        try:
            length = self.workbench.get_sequence_length()
            logger.debug(
                f"Workbench functionality validation passed: can get length ({length})"
            )
            return True
        except Exception as e:
            logger.error(f"Workbench functionality validation failed: {e}")
            return False

    def validate_sequence_state(self, expected_state: dict[str, Any]) -> bool:
        """
        Validate multiple aspects of sequence state.

        Args:
            expected_state: Dictionary with expected state values
                          e.g., {"length": 3, "valid": True, "empty": False}

        Returns:
            bool: True if all validations pass, False otherwise
        """
        logger.debug(f"Validating sequence state: {expected_state}")

        all_passed = True

        # Check length if specified
        if "length" in expected_state:
            if not self.sequence_has_length(expected_state["length"]):
                all_passed = False

        # Check validity if specified
        if "valid" in expected_state:
            expected_valid = expected_state["valid"]
            actual_valid = self.sequence_is_valid()
            if actual_valid != expected_valid:
                logger.error(
                    f"Sequence validity mismatch: expected {expected_valid}, got {actual_valid}"
                )
                all_passed = False

        # Check empty state if specified
        if "empty" in expected_state:
            expected_empty = expected_state["empty"]
            actual_empty = self.sequence_is_empty()
            if actual_empty != expected_empty:
                logger.error(
                    f"Sequence empty state mismatch: expected {expected_empty}, got {actual_empty}"
                )
                all_passed = False

        # Check length range if specified
        if "min_length" in expected_state and "max_length" in expected_state:
            if not self.sequence_length_in_range(
                expected_state["min_length"], expected_state["max_length"]
            ):
                all_passed = False

        if all_passed:
            logger.debug("All sequence state validations passed")
        else:
            logger.error("Some sequence state validations failed")

        return all_passed

    def assert_sequence_length(
        self, expected_length: int, message: Optional[str] = None
    ):
        """
        Assert sequence length with custom message.

        Args:
            expected_length: Expected sequence length
            message: Custom assertion message

        Raises:
            AssertionError: If length doesn't match expectation
        """
        actual_length = self.workbench.get_sequence_length()

        if message is None:
            message = f"Expected sequence length {expected_length}, got {actual_length}"

        assert actual_length == expected_length, message
        logger.debug(f"Sequence length assertion passed: {actual_length}")

    def assert_sequence_valid(self, message: Optional[str] = None):
        """
        Assert that sequence is valid.

        Args:
            message: Custom assertion message

        Raises:
            AssertionError: If sequence is not valid
        """
        is_valid = self.workbench.is_sequence_valid()

        if message is None:
            message = "Expected sequence to be valid"

        assert is_valid, message
        logger.debug("Sequence validity assertion passed")

    def assert_sequence_not_empty(self, message: Optional[str] = None):
        """
        Assert that sequence is not empty.

        Args:
            message: Custom assertion message

        Raises:
            AssertionError: If sequence is empty
        """
        length = self.workbench.get_sequence_length()

        if message is None:
            message = "Expected sequence to not be empty"

        assert length > 0, message
        logger.debug(f"Sequence non-empty assertion passed: length {length}")

    def get_validation_summary(self) -> dict[str, Any]:
        """
        Get a comprehensive validation summary of current sequence state.

        Returns:
            Dict: Summary of validation results
        """
        logger.debug("Generating validation summary")

        length = self.workbench.get_sequence_length()
        is_valid = self.workbench.is_sequence_valid()

        summary = {
            "length": length,
            "is_valid": is_valid,
            "is_empty": length == 0,
            "is_not_empty": length > 0,
            "workbench_functional": self.workbench_is_functional(),
            "timestamp": self._get_timestamp(),
        }

        logger.debug(f"Validation summary: {summary}")
        return summary

    def _get_timestamp(self) -> str:
        """Get current timestamp for validation records."""
        from datetime import datetime

        return datetime.now().isoformat()
