"""
Custom Assertions for TKA Modern E2E Testing Framework

This module provides TKA-specific assertion helpers that make tests
more readable and provide better error messages for common validations.

These assertions go beyond basic pytest assertions to provide:
- Domain-specific validation logic
- Rich error messages with context
- Debugging helpers for complex state validation
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TKAAssertions:
    """
    Custom assertions for TKA E2E testing.

    This class provides high-level assertions that understand TKA's
    domain concepts and provide meaningful error messages.

    Usage:
        assert_tka = TKAAssertions()
        assert_tka.sequence_has_length(workbench, 3)
        assert_tka.options_available(option_picker, min_count=5)
    """

    def __init__(self):
        """Initialize TKA assertions."""
        logger.debug("TKAAssertions initialized")

    def sequence_has_length(
        self, workbench, expected_length: int, message: Optional[str] = None
    ):
        """
        Assert that sequence has expected length.

        Args:
            workbench: Sequence workbench page object
            expected_length: Expected sequence length
            message: Custom error message

        Raises:
            AssertionError: If length doesn't match
        """
        actual_length = workbench.get_sequence_length()

        if message is None:
            message = (
                f"Sequence length assertion failed: "
                f"expected {expected_length}, got {actual_length}"
            )

        assert actual_length == expected_length, message
        logger.debug(f"✓ Sequence length assertion passed: {actual_length}")

    def sequence_is_valid(self, workbench, message: Optional[str] = None):
        """
        Assert that sequence is in valid state.

        Args:
            workbench: Sequence workbench page object
            message: Custom error message

        Raises:
            AssertionError: If sequence is not valid
        """
        is_valid = workbench.is_sequence_valid()

        if message is None:
            sequence_length = workbench.get_sequence_length()
            message = (
                f"Sequence validity assertion failed: "
                f"sequence with length {sequence_length} is not valid"
            )

        assert is_valid, message
        logger.debug("✓ Sequence validity assertion passed")

    def options_available(
        self, option_picker, min_count: int = 1, message: Optional[str] = None
    ):
        """
        Assert that minimum number of options are available.

        Args:
            option_picker: Option picker page object
            min_count: Minimum expected option count
            message: Custom error message

        Raises:
            AssertionError: If insufficient options available
        """
        actual_count = option_picker.get_option_count()

        if message is None:
            message = (
                f"Options availability assertion failed: "
                f"expected at least {min_count} options, got {actual_count}"
            )

        assert actual_count >= min_count, message
        logger.debug(f"✓ Options availability assertion passed: {actual_count} options")

    def component_loaded(
        self, component, component_name: str, message: Optional[str] = None
    ):
        """
        Assert that component is properly loaded.

        Args:
            component: Component page object
            component_name: Name of component for error messages
            message: Custom error message

        Raises:
            AssertionError: If component is not loaded
        """
        is_loaded = component.is_loaded()

        if message is None:
            message = (
                f"Component loading assertion failed: {component_name} is not loaded"
            )

        assert is_loaded, message
        logger.debug(f"✓ Component loading assertion passed: {component_name}")

    def position_selected(
        self, picker, expected_position: str, message: Optional[str] = None
    ):
        """
        Assert that expected position is currently selected.

        Args:
            picker: Start position picker page object
            expected_position: Position that should be selected
            message: Custom error message

        Raises:
            AssertionError: If position is not selected
        """
        current_position = picker.get_current_position()

        if message is None:
            message = (
                f"Position selection assertion failed: "
                f"expected '{expected_position}', got '{current_position}'"
            )

        assert current_position == expected_position, message
        logger.debug(f"✓ Position selection assertion passed: {expected_position}")

    def sequence_length_in_range(
        self, workbench, min_length: int, max_length: int, message: Optional[str] = None
    ):
        """
        Assert that sequence length is within specified range.

        Args:
            workbench: Sequence workbench page object
            min_length: Minimum acceptable length
            max_length: Maximum acceptable length
            message: Custom error message

        Raises:
            AssertionError: If length is outside range
        """
        actual_length = workbench.get_sequence_length()

        if message is None:
            message = (
                f"Sequence length range assertion failed: "
                f"length {actual_length} not in range [{min_length}, {max_length}]"
            )

        assert min_length <= actual_length <= max_length, message
        logger.debug(
            f"✓ Sequence length range assertion passed: {actual_length} in [{min_length}, {max_length}]"
        )

    def workflow_state_matches(
        self,
        state_dict: Dict[str, Any],
        expected_state: Dict[str, Any],
        message: Optional[str] = None,
    ):
        """
        Assert that workflow state matches expected state.

        Args:
            state_dict: Current workflow state
            expected_state: Expected state values
            message: Custom error message

        Raises:
            AssertionError: If states don't match
        """
        mismatches = []

        for key, expected_value in expected_state.items():
            if key not in state_dict:
                mismatches.append(f"Missing key '{key}'")
            elif state_dict[key] != expected_value:
                mismatches.append(
                    f"Key '{key}': expected {expected_value}, got {state_dict[key]}"
                )

        if mismatches:
            if message is None:
                message = f"Workflow state assertion failed: {'; '.join(mismatches)}"
            assert False, message

        logger.debug("✓ Workflow state assertion passed")

    def no_errors_occurred(self, error_list: List[str], message: Optional[str] = None):
        """
        Assert that no errors occurred during operation.

        Args:
            error_list: List of error messages
            message: Custom error message

        Raises:
            AssertionError: If errors are present
        """
        if message is None:
            if error_list:
                error_summary = "; ".join(error_list[:3])  # Show first 3 errors
                if len(error_list) > 3:
                    error_summary += f" (and {len(error_list) - 3} more)"
                message = f"Error-free assertion failed: {error_summary}"
            else:
                message = "Error-free assertion failed: unexpected errors occurred"

        assert len(error_list) == 0, message
        logger.debug("✓ Error-free assertion passed")

    def operation_completed_successfully(
        self, result: Dict[str, Any], message: Optional[str] = None
    ):
        """
        Assert that an operation completed successfully.

        Args:
            result: Operation result dictionary
            message: Custom error message

        Raises:
            AssertionError: If operation failed
        """
        success = result.get("success", False)
        errors = result.get("errors", [])

        if message is None:
            if not success:
                error_info = f" (errors: {errors})" if errors else ""
                message = f"Operation success assertion failed{error_info}"

        assert success, message

        # Also check for errors
        if errors:
            logger.warning(f"Operation succeeded but had warnings: {errors}")

        logger.debug("✓ Operation success assertion passed")


# Convenience instance for direct import
assert_tka = TKAAssertions()


# Decorator for adding assertion context
def with_assertion_context(context_name: str):
    """
    Decorator to add context to assertion failures.

    Args:
        context_name: Name of the test context

    Returns:
        Decorator function
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except AssertionError as e:
                # Add context to assertion error
                enhanced_message = f"[{context_name}] {str(e)}"
                raise AssertionError(enhanced_message) from e

        return wrapper

    return decorator


# Helper functions for common assertion patterns
def assert_sequence_workflow_success(
    navigation_result: bool,
    sequence_result: bool,
    validation_result: bool,
    context: str = "",
):
    """
    Assert that a complete sequence workflow succeeded.

    Args:
        navigation_result: Result of navigation step
        sequence_result: Result of sequence building step
        validation_result: Result of validation step
        context: Optional context for error messages
    """
    context_prefix = f"[{context}] " if context else ""

    assert navigation_result, f"{context_prefix}Navigation step failed"
    assert sequence_result, f"{context_prefix}Sequence building step failed"
    assert validation_result, f"{context_prefix}Validation step failed"

    logger.debug(
        f"✓ Complete workflow assertion passed{' for ' + context if context else ''}"
    )


def assert_component_ready(component, component_name: str, timeout: int = 5):
    """
    Assert that component is ready within timeout.

    Args:
        component: Component page object
        component_name: Name for error messages
        timeout: Timeout in seconds
    """
    ready = component.wait_for_load(timeout * 1000)  # Convert to milliseconds

    assert ready, (
        f"Component readiness assertion failed: "
        f"{component_name} not ready within {timeout}s"
    )

    logger.debug(f"✓ Component readiness assertion passed: {component_name}")


def assert_state_transition(
    initial_state: Dict, final_state: Dict, expected_changes: Dict, context: str = ""
):
    """
    Assert that state transition occurred as expected.

    Args:
        initial_state: State before operation
        final_state: State after operation
        expected_changes: Expected changes between states
        context: Optional context for error messages
    """
    context_prefix = f"[{context}] " if context else ""

    for key, expected_value in expected_changes.items():
        if key not in final_state:
            assert False, (
                f"{context_prefix}State transition failed: missing key '{key}' in final state"
            )

        if final_state[key] != expected_value:
            initial_value = initial_state.get(key, "missing")
            assert False, (
                f"{context_prefix}State transition failed for '{key}': "
                f"expected {expected_value}, got {final_state[key]} "
                f"(was {initial_value})"
            )

    logger.debug(
        f"✓ State transition assertion passed{' for ' + context if context else ''}"
    )


# Convenience functions for common assertion patterns
def assert_basic_sequence_workflow(
    navigation, sequence, validation, position: str, length: int
):
    """
    Assert a basic sequence building workflow completes successfully.

    This is a convenience function that combines multiple assertions
    for the most common test pattern.
    """
    assertions = TKAAssertions()

    # Assert navigation succeeds
    nav_result = navigation.select_start_position(position)
    assert nav_result, f"Start position selection failed: {position}"

    # Assert sequence building succeeds
    seq_result = sequence.build_sequence(length)
    assert seq_result, f"Sequence building failed: length {length}"

    # Assert final state is correct
    assertions.sequence_has_length(validation.workbench, length)
    assertions.sequence_is_valid(validation.workbench)


def assert_sequence_management_workflow(
    sequence, validation, initial_length: int, final_length: int
):
    """
    Assert a sequence management workflow (clear and rebuild) completes successfully.
    """
    assertions = TKAAssertions()

    # Assert clearing succeeds
    clear_result = sequence.clear_sequence()
    assert clear_result, "Sequence clearing failed"

    # Assert rebuilding succeeds
    rebuild_result = sequence.build_sequence(final_length)
    assert rebuild_result, f"Sequence rebuilding failed: length {final_length}"

    assertions.sequence_has_length(validation.workbench, final_length)
