"""
Helper Functions and Utilities for TKA Modern E2E Testing Framework

This module provides utility functions, wait conditions, and helper methods
that support the testing framework and make tests more reliable and maintainable.
"""

import logging
import time
from typing import Any, Callable, Optional

from PyQt6.QtTest import QTest

logger = logging.getLogger(__name__)


class WaitConditions:
    """
    Wait condition utilities for reliable test execution.

    This class provides various wait conditions that can be used to ensure
    components are ready before proceeding with test operations.
    """

    @staticmethod
    def wait_for_condition(
        condition: Callable[[], bool],
        timeout: int = 5000,
        interval: int = 100,
        description: str = "condition",
    ) -> bool:
        """
        Wait for a condition to become true.

        Args:
            condition: Function that returns True when condition is met
            timeout: Maximum time to wait in milliseconds
            interval: Check interval in milliseconds
            description: Description of condition for logging

        Returns:
            bool: True if condition was met, False if timeout
        """
        logger.debug(f"Waiting for {description} (timeout: {timeout}ms)")

        elapsed = 0
        while elapsed < timeout:
            try:
                if condition():
                    logger.debug(f"Condition '{description}' met after {elapsed}ms")
                    return True
            except Exception as e:
                logger.debug(f"Exception while checking condition '{description}': {e}")

            QTest.qWait(interval)
            elapsed += interval

        logger.warning(f"Condition '{description}' not met after {timeout}ms")
        return False

    @staticmethod
    def wait_for_component_loaded(component, timeout: int = 5000) -> bool:
        """
        Wait for a component to be loaded.

        Args:
            component: Component with is_loaded() method
            timeout: Maximum time to wait in milliseconds

        Returns:
            bool: True if component loaded, False if timeout
        """
        return WaitConditions.wait_for_condition(
            lambda: component.is_loaded(),
            timeout=timeout,
            description=f"{component.__class__.__name__} loading",
        )

    @staticmethod
    def wait_for_sequence_length(
        workbench, expected_length: int, timeout: int = 5000
    ) -> bool:
        """
        Wait for sequence to reach expected length.

        Args:
            workbench: SequenceWorkbenchPage instance
            expected_length: Expected sequence length
            timeout: Maximum time to wait in milliseconds

        Returns:
            bool: True if length reached, False if timeout
        """
        return WaitConditions.wait_for_condition(
            lambda: workbench.get_sequence_length() == expected_length,
            timeout=timeout,
            description=f"sequence length = {expected_length}",
        )

    @staticmethod
    def wait_for_options_available(
        option_picker, min_count: int = 1, timeout: int = 5000
    ) -> bool:
        """
        Wait for options to become available.

        Args:
            option_picker: OptionPickerPage instance
            min_count: Minimum number of options required
            timeout: Maximum time to wait in milliseconds

        Returns:
            bool: True if options available, False if timeout
        """
        return WaitConditions.wait_for_condition(
            lambda: len(option_picker.get_available_options()) >= min_count,
            timeout=timeout,
            description=f"at least {min_count} options available",
        )


class TestDataHelpers:
    """
    Helper functions for creating and managing test data.
    """

    @staticmethod
    def get_test_positions() -> list[str]:
        """
        Get standard test positions.

        Returns:
            List[str]: List of test position identifiers
        """
        return ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11", "delta15_delta15"]

    @staticmethod
    def get_test_sequence_lengths() -> list[int]:
        """
        Get standard test sequence lengths.

        Returns:
            List[int]: List of test sequence lengths
        """
        return [1, 2, 3, 5, 8]

    @staticmethod
    def create_test_metadata(test_name: str, **kwargs) -> dict[str, Any]:
        """
        Create test metadata dictionary.

        Args:
            test_name: Name of the test
            **kwargs: Additional metadata fields

        Returns:
            Dict: Test metadata
        """
        metadata = {
            "test_name": test_name,
            "timestamp": time.time(),
            "framework_version": "1.0.0",
        }
        metadata.update(kwargs)
        return metadata


class ComponentHelpers:
    """
    Helper functions for working with UI components.
    """

    @staticmethod
    def ensure_component_ready(
        component, component_name: str, timeout: int = 5000
    ) -> bool:
        """
        Ensure component is ready for interaction.

        Args:
            component: Component to check
            component_name: Name for logging
            timeout: Maximum wait time

        Returns:
            bool: True if component is ready, False otherwise
        """
        logger.debug(f"Ensuring {component_name} is ready")

        # Wait for component to load
        if not WaitConditions.wait_for_component_loaded(component, timeout):
            logger.error(f"{component_name} failed to load")
            return False

        # Additional readiness checks could go here
        logger.debug(f"{component_name} is ready")
        return True

    @staticmethod
    def refresh_component(component, component_name: str) -> bool:
        """
        Refresh component state.

        Args:
            component: Component to refresh
            component_name: Name for logging

        Returns:
            bool: True if refresh successful, False otherwise
        """
        logger.debug(f"Refreshing {component_name}")

        try:
            if hasattr(component, "refresh"):
                component.refresh()
            elif hasattr(component, "clear_cache"):
                component.clear_cache()

            logger.debug(f"{component_name} refreshed successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to refresh {component_name}: {e}")
            return False


class LoggingHelpers:
    """
    Helper functions for test logging and debugging.
    """

    @staticmethod
    def log_test_start(test_name: str, parameters: Optional[dict[str, Any]] = None):
        """
        Log test start with parameters.

        Args:
            test_name: Name of the test
            parameters: Test parameters to log
        """
        logger.info(f"=== STARTING TEST: {test_name} ===")
        if parameters:
            for key, value in parameters.items():
                logger.info(f"  {key}: {value}")

    @staticmethod
    def log_test_end(test_name: str, success: bool, duration: Optional[float] = None):
        """
        Log test completion.

        Args:
            test_name: Name of the test
            success: Whether test succeeded
            duration: Test duration in seconds
        """
        status = "PASSED" if success else "FAILED"
        duration_str = f" ({duration:.2f}s)" if duration else ""
        logger.info(f"=== {status}: {test_name}{duration_str} ===")

    @staticmethod
    def log_workflow_step(step_name: str, details: Optional[str] = None):
        """
        Log workflow step execution.

        Args:
            step_name: Name of the workflow step
            details: Additional details to log
        """
        message = f"Workflow Step: {step_name}"
        if details:
            message += f" - {details}"
        logger.info(message)

    @staticmethod
    def log_component_state(component, component_name: str):
        """
        Log current state of a component.

        Args:
            component: Component to log state for
            component_name: Name of component
        """
        try:
            state_info = []

            if hasattr(component, "is_loaded"):
                state_info.append(f"loaded={component.is_loaded()}")

            if hasattr(component, "get_sequence_length"):
                state_info.append(f"length={component.get_sequence_length()}")

            if hasattr(component, "is_sequence_valid"):
                state_info.append(f"valid={component.is_sequence_valid()}")

            if hasattr(component, "get_available_options"):
                options = component.get_available_options()
                state_info.append(f"options={len(options)}")

            state_str = (
                ", ".join(state_info) if state_info else "no state info available"
            )
            logger.debug(f"{component_name} state: {state_str}")

        except Exception as e:
            logger.debug(f"Error logging {component_name} state: {e}")


class PerformanceHelpers:
    """
    Helper functions for performance monitoring and optimization.
    """

    @staticmethod
    def time_operation(operation: Callable, operation_name: str) -> tuple[Any, float]:
        """
        Time an operation and return result with duration.

        Args:
            operation: Function to time
            operation_name: Name for logging

        Returns:
            tuple: (operation_result, duration_in_seconds)
        """
        logger.debug(f"Timing operation: {operation_name}")
        start_time = time.time()

        try:
            result = operation()
            duration = time.time() - start_time
            logger.debug(f"Operation '{operation_name}' completed in {duration:.3f}s")
            return result, duration

        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Operation '{operation_name}' failed after {duration:.3f}s: {e}"
            )
            raise

    @staticmethod
    def measure_workflow_performance(workflow_builder) -> dict[str, Any]:
        """
        Measure workflow performance metrics.

        Args:
            workflow_builder: WorkflowBuilder instance

        Returns:
            Dict: Performance metrics
        """
        start_time = time.time()

        result = workflow_builder.execute()

        end_time = time.time()
        duration = end_time - start_time

        metrics = {
            "total_duration": duration,
            "successful": result.successful,
            "operations_count": len(result.operation_results),
            "validations_count": len(result.validation_results),
            "avg_operation_time": duration / max(len(result.operation_results), 1),
        }

        logger.info(f"Workflow performance: {metrics}")
        return metrics


class ErrorHandlingHelpers:
    """
    Helper functions for error handling and recovery.
    """

    @staticmethod
    def safe_operation(
        operation: Callable, operation_name: str, default_return: Any = False
    ) -> Any:
        """
        Execute operation safely with error handling.

        Args:
            operation: Function to execute
            operation_name: Name for logging
            default_return: Value to return on error

        Returns:
            Any: Operation result or default_return on error
        """
        try:
            return operation()
        except Exception as e:
            logger.error(f"Safe operation '{operation_name}' failed: {e}")
            return default_return

    @staticmethod
    def retry_operation(
        operation: Callable,
        max_retries: int = 3,
        delay: float = 1.0,
        operation_name: str = "operation",
    ) -> Any:
        """
        Retry operation with exponential backoff.

        Args:
            operation: Function to retry
            max_retries: Maximum number of retries
            delay: Initial delay between retries
            operation_name: Name for logging

        Returns:
            Any: Operation result

        Raises:
            Exception: Last exception if all retries fail
        """
        last_exception = None

        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    logger.debug(
                        f"Retrying {operation_name} (attempt {attempt + 1}/{max_retries + 1})"
                    )

                return operation()

            except Exception as e:
                last_exception = e
                if attempt < max_retries:
                    wait_time = delay * (2**attempt)  # Exponential backoff
                    logger.warning(
                        f"{operation_name} failed (attempt {attempt + 1}), retrying in {wait_time}s: {e}"
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(
                        f"{operation_name} failed after {max_retries + 1} attempts: {e}"
                    )

        raise last_exception
