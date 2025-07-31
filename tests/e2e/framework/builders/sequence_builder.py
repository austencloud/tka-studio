"""
Sequence Builder for TKA Modern E2E Testing Framework

This module provides the SequenceBuilder class that uses the Builder pattern
to create flexible, readable test data for sequence building tests.

The Builder pattern allows for fluent, chainable test data creation:
    sequence_spec = (SequenceBuilder()
                    .with_start_position("alpha1_alpha1")
                    .with_length(3)
                    .with_validation_rules({"min_length": 1, "max_length": 5})
                    .build())
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class SequenceBuilder:
    """
    Builder for creating sequence test specifications.

    This class uses the Builder pattern to create flexible, readable
    test data for sequence building operations.

    Example:
        # Basic sequence
        sequence = SequenceBuilder().with_length(3).build()

        # Complex sequence with validation
        sequence = (SequenceBuilder()
                   .with_start_position("alpha1_alpha1")
                   .with_length(5)
                   .with_specific_options(["option_1", "option_2"])
                   .with_validation_rules({"valid": True, "min_length": 3})
                   .with_metadata({"test_type": "performance"})
                   .build())
    """

    def __init__(self):
        """Initialize the builder with default values."""
        self.reset()
        logger.debug("SequenceBuilder initialized")

    def reset(self):
        """Reset the builder to default state."""
        self._start_position = "alpha1_alpha1"  # Default position
        self._length = 1
        self._specific_options = []
        self._validation_rules = {}
        self._metadata = {}
        self._operation_type = "build"  # build, extend, rebuild, clear
        self._expected_result = "success"  # success, failure
        self._timeout = 30  # seconds

        logger.debug("SequenceBuilder reset to defaults")
        return self

    def with_start_position(self, position: str):
        """
        Set the start position for the sequence.

        Args:
            position: Start position identifier (e.g., "alpha1_alpha1")

        Returns:
            SequenceBuilder: Self for method chaining
        """
        self._start_position = position
        logger.debug(f"SequenceBuilder: start position set to '{position}'")
        return self

    def with_length(self, length: int):
        """
        Set the target sequence length.

        Args:
            length: Target sequence length

        Returns:
            SequenceBuilder: Self for method chaining
        """
        self._length = length
        logger.debug(f"SequenceBuilder: length set to {length}")
        return self

    def with_specific_options(self, options: list[str]):
        """
        Set specific options to use for building the sequence.

        Args:
            options: List of option identifiers to use in order

        Returns:
            SequenceBuilder: Self for method chaining
        """
        self._specific_options = options.copy()
        self._length = len(options)  # Auto-adjust length
        logger.debug(f"SequenceBuilder: specific options set: {options}")
        return self

    def with_validation_rules(self, rules: dict[str, Any]):
        """
        Set validation rules for the sequence.

        Args:
            rules: Dictionary of validation rules
                  e.g., {"valid": True, "min_length": 1, "max_length": 10}

        Returns:
            SequenceBuilder: Self for method chaining
        """
        self._validation_rules.update(rules)
        logger.debug(f"SequenceBuilder: validation rules updated: {rules}")
        return self

    def with_metadata(self, metadata: dict[str, Any]):
        """
        Set metadata for the sequence specification.

        Args:
            metadata: Dictionary of metadata
                     e.g., {"test_type": "performance", "priority": "high"}

        Returns:
            SequenceBuilder: Self for method chaining
        """
        self._metadata.update(metadata)
        logger.debug(f"SequenceBuilder: metadata updated: {metadata}")
        return self

    def with_operation_type(self, operation: str):
        """
        Set the type of operation to perform.

        Args:
            operation: Operation type ("build", "extend", "rebuild", "clear")

        Returns:
            SequenceBuilder: Self for method chaining
        """
        valid_operations = ["build", "extend", "rebuild", "clear"]
        if operation not in valid_operations:
            raise ValueError(
                f"Invalid operation '{operation}'. Must be one of: {valid_operations}"
            )

        self._operation_type = operation
        logger.debug(f"SequenceBuilder: operation type set to '{operation}'")
        return self

    def with_expected_result(self, result: str):
        """
        Set the expected result of the operation.

        Args:
            result: Expected result ("success", "failure")

        Returns:
            SequenceBuilder: Self for method chaining
        """
        valid_results = ["success", "failure"]
        if result not in valid_results:
            raise ValueError(
                f"Invalid result '{result}'. Must be one of: {valid_results}"
            )

        self._expected_result = result
        logger.debug(f"SequenceBuilder: expected result set to '{result}'")
        return self

    def with_timeout(self, timeout: int):
        """
        Set the timeout for the operation.

        Args:
            timeout: Timeout in seconds

        Returns:
            SequenceBuilder: Self for method chaining
        """
        self._timeout = timeout
        logger.debug(f"SequenceBuilder: timeout set to {timeout}s")
        return self

    def for_performance_test(self):
        """
        Configure builder for performance testing.

        Returns:
            SequenceBuilder: Self for method chaining
        """
        return (
            self.with_length(10)
            .with_timeout(5)
            .with_metadata({"test_type": "performance", "priority": "high"})
        )

    def for_stress_test(self):
        """
        Configure builder for stress testing.

        Returns:
            SequenceBuilder: Self for method chaining
        """
        return (
            self.with_length(50)
            .with_timeout(120)
            .with_metadata({"test_type": "stress", "priority": "low"})
        )

    def for_edge_case_test(self):
        """
        Configure builder for edge case testing.

        Returns:
            SequenceBuilder: Self for method chaining
        """
        return (
            self.with_length(1)
            .with_validation_rules({"min_length": 1, "max_length": 1})
            .with_metadata({"test_type": "edge_case", "priority": "medium"})
        )

    def for_error_case_test(self):
        """
        Configure builder for error case testing.

        Returns:
            SequenceBuilder: Self for method chaining
        """
        return self.with_expected_result("failure").with_metadata(
            {"test_type": "error_case", "priority": "high"}
        )

    def build(self) -> dict[str, Any]:
        """
        Build and return the sequence specification.

        Returns:
            Dict: Complete sequence specification
        """
        spec = {
            "start_position": self._start_position,
            "length": self._length,
            "specific_options": self._specific_options,
            "validation_rules": self._validation_rules,
            "metadata": self._metadata,
            "operation_type": self._operation_type,
            "expected_result": self._expected_result,
            "timeout": self._timeout,
        }

        logger.debug(f"SequenceBuilder: built specification: {spec}")
        return spec

    def build_and_reset(self) -> dict[str, Any]:
        """
        Build the specification and reset the builder.

        Returns:
            Dict: Complete sequence specification
        """
        spec = self.build()
        self.reset()
        return spec


class WorkflowBuilder:
    """
    Builder for creating complete workflow specifications.

    This builder creates multi-step workflows that combine navigation,
    sequence building, and validation operations.

    Example:
        workflow = (WorkflowBuilder()
                   .add_navigation_step("alpha1_alpha1")
                   .add_sequence_step(SequenceBuilder().with_length(3).build())
                   .add_validation_step({"length": 3, "valid": True})
                   .build())
    """

    def __init__(self):
        """Initialize the workflow builder."""
        self.reset()
        logger.debug("WorkflowBuilder initialized")

    def reset(self):
        """Reset the builder to default state."""
        self._steps = []
        self._metadata = {}
        self._timeout = 60

        logger.debug("WorkflowBuilder reset to defaults")
        return self

    def add_navigation_step(self, position: str, criteria: Optional[dict] = None):
        """
        Add a navigation step to the workflow.

        Args:
            position: Start position to navigate to
            criteria: Optional criteria for position selection

        Returns:
            WorkflowBuilder: Self for method chaining
        """
        step = {"type": "navigation", "position": position, "criteria": criteria or {}}
        self._steps.append(step)
        logger.debug(f"WorkflowBuilder: added navigation step: {step}")
        return self

    def add_sequence_step(self, sequence_spec: dict[str, Any]):
        """
        Add a sequence building step to the workflow.

        Args:
            sequence_spec: Sequence specification from SequenceBuilder

        Returns:
            WorkflowBuilder: Self for method chaining
        """
        step = {"type": "sequence", "spec": sequence_spec}
        self._steps.append(step)
        logger.debug("WorkflowBuilder: added sequence step")
        return self

    def add_validation_step(self, validation_rules: dict[str, Any]):
        """
        Add a validation step to the workflow.

        Args:
            validation_rules: Validation rules to check

        Returns:
            WorkflowBuilder: Self for method chaining
        """
        step = {"type": "validation", "rules": validation_rules}
        self._steps.append(step)
        logger.debug(f"WorkflowBuilder: added validation step: {validation_rules}")
        return self

    def add_custom_step(self, step_type: str, step_data: dict[str, Any]):
        """
        Add a custom step to the workflow.

        Args:
            step_type: Type of step
            step_data: Step-specific data

        Returns:
            WorkflowBuilder: Self for method chaining
        """
        step = {"type": step_type, "data": step_data}
        self._steps.append(step)
        logger.debug(f"WorkflowBuilder: added custom step: {step_type}")
        return self

    def with_metadata(self, metadata: dict[str, Any]):
        """
        Set metadata for the workflow.

        Args:
            metadata: Workflow metadata

        Returns:
            WorkflowBuilder: Self for method chaining
        """
        self._metadata.update(metadata)
        logger.debug(f"WorkflowBuilder: metadata updated: {metadata}")
        return self

    def with_timeout(self, timeout: int):
        """
        Set the overall workflow timeout.

        Args:
            timeout: Timeout in seconds

        Returns:
            WorkflowBuilder: Self for method chaining
        """
        self._timeout = timeout
        logger.debug(f"WorkflowBuilder: timeout set to {timeout}s")
        return self

    def build(self) -> dict[str, Any]:
        """
        Build and return the workflow specification.

        Returns:
            Dict: Complete workflow specification
        """
        workflow = {
            "steps": self._steps.copy(),
            "metadata": self._metadata.copy(),
            "timeout": self._timeout,
            "step_count": len(self._steps),
        }

        logger.debug(f"WorkflowBuilder: built workflow with {len(self._steps)} steps")
        return workflow

    def build_and_reset(self) -> dict[str, Any]:
        """
        Build the workflow and reset the builder.

        Returns:
            Dict: Complete workflow specification
        """
        workflow = self.build()
        self.reset()
        return workflow


# Convenience functions for common patterns
def simple_sequence(length: int, position: str = "alpha1_alpha1") -> dict[str, Any]:
    """
    Create a simple sequence specification.

    Args:
        length: Sequence length
        position: Start position

    Returns:
        Dict: Sequence specification
    """
    return SequenceBuilder().with_start_position(position).with_length(length).build()


def performance_sequence(length: int = 10) -> dict[str, Any]:
    """
    Create a performance test sequence specification.

    Args:
        length: Sequence length for performance testing

    Returns:
        Dict: Performance sequence specification
    """
    return SequenceBuilder().with_length(length).for_performance_test().build()


def error_test_sequence() -> dict[str, Any]:
    """
    Create an error case test sequence specification.

    Returns:
        Dict: Error test sequence specification
    """
    return SequenceBuilder().for_error_case_test().build()


def complete_workflow(
    position: str = "alpha1_alpha1", length: int = 3
) -> dict[str, Any]:
    """
    Create a complete test workflow specification.

    Args:
        position: Start position
        length: Sequence length

    Returns:
        Dict: Complete workflow specification
    """
    sequence_spec = simple_sequence(length, position)

    return (
        WorkflowBuilder()
        .add_navigation_step(position)
        .add_sequence_step(sequence_spec)
        .add_validation_step({"length": length, "valid": True})
        .build()
    )
