"""
Workflow Builder for TKA Modern E2E Testing Framework

This module provides the WorkflowBuilder class that implements a fluent interface
for creating readable, chainable test workflows that combine multiple operations.
"""

import logging
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


class WorkflowBuilder:
    """
    Fluent interface for building test workflows.

    This class provides a chainable API for creating complex test workflows
    that combine navigation, sequence building, and validation operations
    in a readable, maintainable way.

    Example usage:
        workflow = (WorkflowBuilder(workflow_steps)
                   .navigate_to_position("alpha1_alpha1")
                   .build_sequence(length=3)
                   .validate_length(3)
                   .validate_is_valid()
                   .execute())Very good this time it worked
    """

    def __init__(self, workflow_steps: dict[str, Any]):
        """
        Initialize the workflow builder.

        Args:
            workflow_steps: Dictionary of workflow step objects
        """
        self.workflow_steps = workflow_steps
        self.navigation = workflow_steps["navigation"]
        self.sequence = workflow_steps["sequence"]
        self.validation = workflow_steps["validation"]

        self._operations: list[Callable] = []
        self._validations: list[Callable] = []
        self._metadata: dict[str, Any] = {}

        logger.debug("WorkflowBuilder initialized")

    # Navigation Operations

    def navigate_to_position(self, position: str) -> "WorkflowBuilder":
        """
        Add navigation to specific position to workflow.

        Args:
            position: Position identifier to navigate to

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def operation():
            logger.debug(f"Workflow: Navigating to position '{position}'")
            return self.navigation.select_start_position(position)

        self._operations.append(operation)
        logger.debug(f"Workflow: Added navigation to '{position}'")
        return self

    def navigate_to_first_available(self) -> "WorkflowBuilder":
        """
        Add navigation to first available position to workflow.

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def operation():
            logger.debug("Workflow: Navigating to first available position")
            return self.navigation.select_first_available_position() is not None

        self._operations.append(operation)
        logger.debug("Workflow: Added navigation to first available position")
        return self

    def navigate_to_random(self) -> "WorkflowBuilder":
        """
        Add navigation to random position to workflow.

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def operation():
            logger.debug("Workflow: Navigating to random position")
            return self.navigation.select_random_position() is not None

        self._operations.append(operation)
        logger.debug("Workflow: Added navigation to random position")
        return self

    # Sequence Operations

    def build_sequence(self, length: int) -> "WorkflowBuilder":
        """
        Add sequence building to workflow.

        Args:
            length: Target sequence length

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def operation():
            logger.debug(f"Workflow: Building sequence of length {length}")
            return self.sequence.build_sequence(length)

        self._operations.append(operation)
        logger.debug(f"Workflow: Added sequence building (length {length})")
        return self

    def extend_sequence(self, additional_length: int) -> "WorkflowBuilder":
        """
        Add sequence extension to workflow.

        Args:
            additional_length: Number of elements to add

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def operation():
            logger.debug(f"Workflow: Extending sequence by {additional_length}")
            return self.sequence.extend_sequence(additional_length)

        self._operations.append(operation)
        logger.debug(f"Workflow: Added sequence extension ({additional_length})")
        return self

    def clear_sequence(self) -> "WorkflowBuilder":
        """
        Add sequence clearing to workflow.

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def operation():
            logger.debug("Workflow: Clearing sequence")
            return self.sequence.clear_sequence()

        self._operations.append(operation)
        logger.debug("Workflow: Added sequence clearing")
        return self

    def rebuild_sequence(self, new_length: int) -> "WorkflowBuilder":
        """
        Add sequence rebuilding to workflow.

        Args:
            new_length: Length of new sequence

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def operation():
            logger.debug(f"Workflow: Rebuilding sequence with length {new_length}")
            return self.sequence.rebuild_sequence(new_length)

        self._operations.append(operation)
        logger.debug(f"Workflow: Added sequence rebuilding (length {new_length})")
        return self

    def add_specific_options(self, options: list[str]) -> "WorkflowBuilder":
        """
        Add specific option selection to workflow.

        Args:
            options: List of option identifiers to add

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def operation():
            logger.debug(f"Workflow: Adding specific options: {options}")
            return self.sequence.build_sequence_with_specific_options(options)

        self._operations.append(operation)
        logger.debug(f"Workflow: Added specific options: {options}")
        return self

    # Validation Operations

    def validate_length(self, expected_length: int) -> "WorkflowBuilder":
        """
        Add length validation to workflow.

        Args:
            expected_length: Expected sequence length

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def validation():
            logger.debug(f"Workflow: Validating sequence length = {expected_length}")
            return self.validation.sequence_has_length(expected_length)

        self._validations.append(validation)
        logger.debug(f"Workflow: Added length validation ({expected_length})")
        return self

    def validate_is_valid(self) -> "WorkflowBuilder":
        """
        Add validity validation to workflow.

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def validation():
            logger.debug("Workflow: Validating sequence is valid")
            return self.validation.sequence_is_valid()

        self._validations.append(validation)
        logger.debug("Workflow: Added validity validation")
        return self

    def validate_not_empty(self) -> "WorkflowBuilder":
        """
        Add non-empty validation to workflow.

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def validation():
            logger.debug("Workflow: Validating sequence is not empty")
            return self.validation.sequence_is_not_empty()

        self._validations.append(validation)
        logger.debug("Workflow: Added non-empty validation")
        return self

    def validate_empty(self) -> "WorkflowBuilder":
        """
        Add empty validation to workflow.

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def validation():
            logger.debug("Workflow: Validating sequence is empty")
            return self.validation.sequence_is_empty()

        self._validations.append(validation)
        logger.debug("Workflow: Added empty validation")
        return self

    def validate_length_in_range(
        self, min_length: int, max_length: int
    ) -> "WorkflowBuilder":
        """
        Add length range validation to workflow.

        Args:
            min_length: Minimum acceptable length
            max_length: Maximum acceptable length

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def validation():
            logger.debug(
                f"Workflow: Validating sequence length in range [{min_length}, {max_length}]"
            )
            return self.validation.sequence_length_in_range(min_length, max_length)

        self._validations.append(validation)
        logger.debug(
            f"Workflow: Added length range validation [{min_length}, {max_length}]"
        )
        return self

    # Custom Operations

    def custom_operation(
        self, operation: Callable[[], bool], description: str = "Custom operation"
    ) -> "WorkflowBuilder":
        """
        Add custom operation to workflow.

        Args:
            operation: Function that returns bool indicating success
            description: Description of the operation for logging

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def wrapped_operation():
            logger.debug(f"Workflow: Executing {description}")
            return operation()

        self._operations.append(wrapped_operation)
        logger.debug(f"Workflow: Added custom operation: {description}")
        return self

    def custom_validation(
        self, validation: Callable[[], bool], description: str = "Custom validation"
    ) -> "WorkflowBuilder":
        """
        Add custom validation to workflow.

        Args:
            validation: Function that returns bool indicating validation success
            description: Description of the validation for logging

        Returns:
            WorkflowBuilder: Self for method chaining
        """

        def wrapped_validation():
            logger.debug(f"Workflow: Executing {description}")
            return validation()

        self._validations.append(wrapped_validation)
        logger.debug(f"Workflow: Added custom validation: {description}")
        return self

    # Metadata and Configuration

    def with_metadata(self, key: str, value: Any) -> "WorkflowBuilder":
        """
        Add metadata to workflow.

        Args:
            key: Metadata key
            value: Metadata value

        Returns:
            WorkflowBuilder: Self for method chaining
        """
        self._metadata[key] = value
        logger.debug(f"Workflow: Added metadata: {key} = {value}")
        return self

    # Execution

    def execute(self) -> "WorkflowResult":
        """
        Execute the workflow.

        Returns:
            WorkflowResult: Result of workflow execution
        """
        logger.info(
            f"Executing workflow with {len(self._operations)} operations and {len(self._validations)} validations"
        )

        result = WorkflowResult()

        try:
            # Execute operations
            for i, operation in enumerate(self._operations):
                logger.debug(f"Executing operation {i + 1}/{len(self._operations)}")
                success = operation()
                result.add_operation_result(i, success)

                if not success:
                    logger.error(f"Operation {i + 1} failed")
                    result.set_failed(f"Operation {i + 1} failed")
                    return result

            # Execute validations
            for i, validation in enumerate(self._validations):
                logger.debug(f"Executing validation {i + 1}/{len(self._validations)}")
                success = validation()
                result.add_validation_result(i, success)

                if not success:
                    logger.error(f"Validation {i + 1} failed")
                    result.set_failed(f"Validation {i + 1} failed")
                    return result

            result.set_successful()
            logger.info("Workflow executed successfully")

        except Exception as e:
            logger.error(f"Workflow execution failed with exception: {e}")
            result.set_failed(f"Exception: {e}")

        return result

    # Convenience methods for common patterns

    @classmethod
    def simple_sequence_workflow(
        cls, workflow_steps, position: str, length: int
    ) -> "WorkflowBuilder":
        """
        Create a simple sequence building workflow.

        Args:
            workflow_steps: Workflow step objects
            position: Start position
            length: Sequence length

        Returns:
            WorkflowBuilder: Configured workflow builder
        """
        return (
            cls(workflow_steps)
            .navigate_to_position(position)
            .build_sequence(length)
            .validate_length(length)
            .validate_is_valid()
        )

    @classmethod
    def sequence_management_workflow(
        cls, workflow_steps, position: str, initial_length: int, final_length: int
    ) -> "WorkflowBuilder":
        """
        Create a sequence management workflow (build, clear, rebuild).

        Args:
            workflow_steps: Workflow step objects
            position: Start position
            initial_length: Initial sequence length
            final_length: Final sequence length

        Returns:
            WorkflowBuilder: Configured workflow builder
        """
        return (
            cls(workflow_steps)
            .navigate_to_position(position)
            .build_sequence(initial_length)
            .validate_length(initial_length)
            .clear_sequence()
            .validate_empty()
            .build_sequence(final_length)
            .validate_length(final_length)
        )


class WorkflowResult:
    """
    Result of workflow execution.

    This class encapsulates the results of executing a workflow,
    including success/failure status and detailed operation results.
    """

    def __init__(self):
        """Initialize workflow result."""
        self.successful = False
        self.error_message: Optional[str] = None
        self.operation_results: dict[int, bool] = {}
        self.validation_results: dict[int, bool] = {}

    def add_operation_result(self, index: int, success: bool):
        """Add operation result."""
        self.operation_results[index] = success

    def add_validation_result(self, index: int, success: bool):
        """Add validation result."""
        self.validation_results[index] = success

    def set_successful(self):
        """Mark workflow as successful."""
        self.successful = True
        self.error_message = None

    def set_failed(self, error_message: str):
        """Mark workflow as failed."""
        self.successful = False
        self.error_message = error_message

    def __bool__(self) -> bool:
        """Boolean conversion returns success status."""
        return self.successful

    def __str__(self) -> str:
        """String representation of result."""
        if self.successful:
            return f"WorkflowResult(successful=True, operations={len(self.operation_results)}, validations={len(self.validation_results)})"
        else:
            return f"WorkflowResult(successful=False, error='{self.error_message}')"
