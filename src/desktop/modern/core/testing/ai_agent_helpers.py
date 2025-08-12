"""
AI Agent Testing Utilities for TKA

Provides simple interfaces for AI agents to test complex workflows
using the existing sophisticated TKA architecture.
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

# Import your existing architecture
from desktop.modern.core.application.application_factory import ApplicationFactory
from desktop.modern.core.interfaces.core_services import (
    IPictographManager,
    ISequenceManager,
    IValidationService,
)
from desktop.modern.domain.models import (
    BeatData,
    Location,
    MotionData,
    MotionType,
    RotationDirection,
)
from desktop.modern.domain.models.enums import GridMode


logger = logging.getLogger(__name__)


@dataclass
class AITestResult:
    """Simple result format for AI agents."""

    success: bool
    data: Any | None = None
    errors: list[str] = None
    execution_time: float = 0.0
    metadata: dict[str, Any] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.errors is None:
            self.errors = []
        if self.metadata is None:
            self.metadata = {}


class TKAAITestHelper:
    """
    Simplified testing interface for AI agents.

    Abstracts the complexity of your domain models and services
    while providing access to real business logic testing.
    """

    def __init__(self, use_test_mode: bool = True):
        """Initialize with test or production services."""
        if use_test_mode:
            self.container = ApplicationFactory.create_test_app()
        else:
            self.container = ApplicationFactory.create_headless_app()

        self.execution_history: list[tuple] = []

        # Cache frequently used services
        self._sequence_service = None
        self._pictograph_service = None
        self._validation_service = None

    @property
    def sequence_service(self):
        if self._sequence_service is None:
            self._sequence_service = self.container.resolve(ISequenceManager)
        return self._sequence_service

    @property
    def pictograph_service(self):
        if self._pictograph_service is None:
            self._pictograph_service = self.container.resolve(IPictographManager)
        return self._pictograph_service

    @property
    def validation_service(self):
        if self._validation_service is None:
            self._validation_service = self.container.resolve(IValidationService)
        return self._validation_service

    def create_sequence(self, name: str, length: int = 8) -> AITestResult:
        """
        Create a sequence using your existing SequenceManager.

        Returns simple result format for AI agents.
        """
        import time

        start_time = time.time()

        try:
            # Use your existing sophisticated service
            sequence_data = self.sequence_service.create_sequence(name, length)

            # Handle both SequenceData objects and dictionaries (for mock services)
            if hasattr(sequence_data, "to_dict"):
                # Real SequenceData object
                sequence_dict = sequence_data.to_dict()
                is_valid_check = sequence_data.is_valid
                beat_count = len(sequence_data.beats)
                sequence_id = sequence_data.id
                sequence_name = sequence_data.name
            else:
                # Mock service returns dictionary
                sequence_dict = sequence_data
                is_valid_check = True  # Mock always valid
                beat_count = sequence_data.get("length", 0)
                sequence_id = sequence_data.get("id", "unknown")
                sequence_name = sequence_data.get("name", "unknown")

            # Validate using your existing validation
            is_valid = self.validation_service.validate_sequence(sequence_dict)

            if not is_valid:
                errors = self.validation_service.get_validation_errors(sequence_dict)
                return AITestResult(
                    success=False,
                    errors=errors,
                    execution_time=time.time() - start_time,
                )

            result = AITestResult(
                success=True,
                data=sequence_data,
                execution_time=time.time() - start_time,
                metadata={
                    "sequence_id": sequence_id,
                    "sequence_name": sequence_name,
                    "beat_count": beat_count,
                    "is_valid": is_valid_check,
                },
            )

            self.execution_history.append(("create_sequence", result))
            return result

        except Exception as e:
            logger.exception(f"Sequence creation failed: {e}")
            result = AITestResult(
                success=False,
                errors=[f"Sequence creation failed: {e!s}"],
                execution_time=time.time() - start_time,
            )
            self.execution_history.append(("create_sequence", result))
            return result

    def create_beat_with_motions(
        self, beat_number: int, letter: str = "A"
    ) -> AITestResult:
        """
        Create a BeatData with proper MotionData using your domain models.
        """
        import time

        start_time = time.time()

        try:
            # Create using your sophisticated domain models
            blue_motion = MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                turns=0.5,
            )

            red_motion = MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.WEST,
                turns=0.5,
            )

            beat_data = BeatData(
                beat_number=beat_number,
                letter=letter,
                blue_motion=blue_motion,
                red_motion=red_motion,
                duration=1.0,
            )

            # Validate using your existing validation
            is_valid = self.validation_service.validate_beat(beat_data.to_dict())

            result = AITestResult(
                success=is_valid,
                data=beat_data,
                execution_time=time.time() - start_time,
                metadata={
                    "beat_number": beat_data.beat_number,
                    "letter": beat_data.letter,
                    "has_blue_motion": beat_data.blue_motion is not None,
                    "has_red_motion": beat_data.red_motion is not None,
                    "is_valid": beat_data.is_valid(),
                },
            )

            if not is_valid:
                result.errors = self.validation_service.get_validation_errors(
                    beat_data.to_dict()
                )

            self.execution_history.append(("create_beat", result))
            return result

        except Exception as e:
            logger.exception(f"Beat creation failed: {e}")
            result = AITestResult(
                success=False,
                errors=[f"Beat creation failed: {e!s}"],
                execution_time=time.time() - start_time,
            )
            self.execution_history.append(("create_beat", result))
            return result

    def test_existing_command_pattern(self) -> AITestResult:
        """
        Test your existing command pattern with undo/redo.

        Uses your SequenceManager's add_beat_with_undo method.
        """
        import time

        start_time = time.time()

        try:
            # Create a sequence
            sequence_result = self.create_sequence("Command Test", 4)
            if not sequence_result.success:
                return sequence_result

            sequence_data = sequence_result.data

            # Create a beat
            beat_result = self.create_beat_with_motions(1, "A")
            if not beat_result.success:
                return beat_result

            beat_data = beat_result.data

            # Test your existing command pattern
            if hasattr(self.sequence_service, "add_beat_with_undo"):
                # Use your existing command with undo
                updated_sequence = self.sequence_service.add_beat_with_undo(
                    beat_data, 0
                )

                # Test undo functionality
                can_undo = self.sequence_service.can_undo()
                undo_description = self.sequence_service.get_undo_description()

                result = AITestResult(
                    success=True,
                    data=updated_sequence,
                    execution_time=time.time() - start_time,
                    metadata={
                        "command_pattern_available": True,
                        "can_undo": can_undo,
                        "undo_description": undo_description,
                        "updated_sequence_beats": (
                            len(updated_sequence.beats)
                            if hasattr(updated_sequence, "beats")
                            else len(updated_sequence.get("beats", []))
                        ),
                        "sequence_is_valid": (
                            updated_sequence.is_valid
                            if hasattr(updated_sequence, "is_valid")
                            else True
                        ),
                    },
                )
            else:
                # Fallback to regular add_beat
                updated_sequence = self.sequence_service.add_beat(
                    sequence_data, beat_data, 0
                )

                result = AITestResult(
                    success=True,
                    data=updated_sequence,
                    execution_time=time.time() - start_time,
                    metadata={
                        "command_pattern_available": False,
                        "fallback_used": True,
                        "updated_sequence_beats": (
                            len(updated_sequence.beats)
                            if hasattr(updated_sequence, "beats")
                            else len(updated_sequence.get("beats", []))
                        ),
                        "sequence_is_valid": (
                            updated_sequence.is_valid
                            if hasattr(updated_sequence, "is_valid")
                            else True
                        ),
                    },
                )

            self.execution_history.append(("test_command_pattern", result))
            return result

        except Exception as e:
            logger.exception(f"Command pattern test failed: {e}")
            result = AITestResult(
                success=False,
                errors=[f"Command pattern test failed: {e!s}"],
                execution_time=time.time() - start_time,
            )
            self.execution_history.append(("test_command_pattern", result))
            return result

    def create_pictograph(self, grid_mode: str = "diamond") -> AITestResult:
        """
        Create a pictograph using your existing PictographManagementService.
        """
        import time

        start_time = time.time()

        try:
            grid_mode_enum = (
                GridMode.DIAMOND if grid_mode == "diamond" else GridMode.BOX
            )

            # Use your existing sophisticated pictograph service
            pictograph_data = self.pictograph_service.create_pictograph(grid_mode_enum)

            # Handle both PictographData objects and dictionaries (for mock services)
            if hasattr(pictograph_data, "id"):
                # Real PictographData object
                pictograph_id = pictograph_data.id
                grid_mode_value = pictograph_data.grid_data.grid_mode.value
                is_blank = pictograph_data.is_blank
                has_arrows = len(pictograph_data.arrows) > 0
            else:
                # Mock service returns dictionary
                pictograph_id = pictograph_data.get("id", "unknown")
                grid_mode_value = pictograph_data.get("grid_mode", "diamond")
                is_blank = pictograph_data.get("is_blank", False)
                has_arrows = len(pictograph_data.get("arrows", [])) > 0

            result = AITestResult(
                success=True,
                data=pictograph_data,
                execution_time=time.time() - start_time,
                metadata={
                    "pictograph_id": pictograph_id,
                    "grid_mode": grid_mode_value,
                    "is_blank": is_blank,
                    "has_arrows": has_arrows,
                },
            )

            self.execution_history.append(("create_pictograph", result))
            return result

        except Exception as e:
            logger.exception(f"Pictograph creation failed: {e}")
            result = AITestResult(
                success=False,
                errors=[f"Pictograph creation failed: {e!s}"],
                execution_time=time.time() - start_time,
            )
            self.execution_history.append(("create_pictograph", result))
            return result

    def test_pictograph_from_beat(self) -> AITestResult:
        """
        Test your existing create_from_beat functionality.
        """
        import time

        start_time = time.time()

        try:
            # Create a beat with motions
            beat_result = self.create_beat_with_motions(1, "A")
            if not beat_result.success:
                return beat_result

            beat_data = beat_result.data

            # Use your existing create_from_beat method
            pictograph_data = self.pictograph_service.create_from_beat(beat_data)

            # Handle both PictographData objects and dictionaries (for mock services)
            if hasattr(pictograph_data, "id"):
                # Real PictographData object
                pictograph_id = pictograph_data.id
                has_blue_arrow = "blue" in pictograph_data.arrows
                has_red_arrow = "red" in pictograph_data.arrows
                is_blank = pictograph_data.is_blank
            else:
                # Mock service returns dictionary
                pictograph_id = pictograph_data.get("id", "unknown")
                arrows = pictograph_data.get("arrows", [])
                has_blue_arrow = any("blue" in str(arrow) for arrow in arrows)
                has_red_arrow = any("red" in str(arrow) for arrow in arrows)
                is_blank = pictograph_data.get("is_blank", False)

            result = AITestResult(
                success=True,
                data=pictograph_data,
                execution_time=time.time() - start_time,
                metadata={
                    "pictograph_id": pictograph_id,
                    "created_from_beat": beat_data.beat_number,
                    "letter": beat_data.letter,
                    "has_blue_arrow": has_blue_arrow,
                    "has_red_arrow": has_red_arrow,
                    "is_blank": is_blank,
                },
            )

            self.execution_history.append(("pictograph_from_beat", result))
            return result

        except Exception as e:
            logger.exception(f"Pictograph from beat test failed: {e}")
            result = AITestResult(
                success=False,
                errors=[f"Pictograph from beat test failed: {e!s}"],
                execution_time=time.time() - start_time,
            )
            self.execution_history.append(("pictograph_from_beat", result))
            return result

    def test_csv_dataset_integration(self) -> AITestResult:
        """
        Test your existing CSV dataset functionality.
        """
        import time

        start_time = time.time()

        try:
            # Test your existing get_pictographs_by_letter method
            pictographs = self.pictograph_service.get_pictographs_by_letter("A")

            result = AITestResult(
                success=True,
                data=pictographs,
                execution_time=time.time() - start_time,
                metadata={
                    "pictographs_found": len(pictographs),
                    "letter_tested": "A",
                    "csv_integration_working": len(pictographs) > 0,
                },
            )

            self.execution_history.append(("csv_dataset_test", result))
            return result

        except Exception as e:
            logger.exception(f"CSV dataset test failed: {e}")
            result = AITestResult(
                success=False,
                errors=[f"CSV dataset test failed: {e!s}"],
                execution_time=time.time() - start_time,
            )
            self.execution_history.append(("csv_dataset_test", result))
            return result

    def run_comprehensive_test_suite(self) -> AITestResult:
        """
        Run comprehensive test of your existing architecture.

        Perfect for AI agents to validate all systems working.
        """
        import time

        start_time = time.time()

        test_results = {}
        errors = []

        # Test 1: Sequence creation
        seq_result = self.create_sequence("Comprehensive Test", 4)
        test_results["sequence_creation"] = seq_result.success
        if not seq_result.success:
            errors.extend(seq_result.errors)

        # Test 2: Beat creation
        beat_result = self.create_beat_with_motions(1, "A")
        test_results["beat_creation"] = beat_result.success
        if not beat_result.success:
            errors.extend(beat_result.errors)

        # Test 3: Command pattern
        cmd_result = self.test_existing_command_pattern()
        test_results["command_pattern"] = cmd_result.success
        if not cmd_result.success:
            errors.extend(cmd_result.errors)

        # Test 4: Pictograph creation
        picto_result = self.create_pictograph("diamond")
        test_results["pictograph_creation"] = picto_result.success
        if not picto_result.success:
            errors.extend(picto_result.errors)

        # Test 5: Pictograph from beat
        picto_beat_result = self.test_pictograph_from_beat()
        test_results["pictograph_from_beat"] = picto_beat_result.success
        if not picto_beat_result.success:
            errors.extend(picto_beat_result.errors)

        # Test 6: CSV dataset
        csv_result = self.test_csv_dataset_integration()
        test_results["csv_dataset"] = csv_result.success
        if not csv_result.success:
            errors.extend(csv_result.errors)

        # Calculate overall success
        total_tests = len(test_results)
        passed_tests = sum(test_results.values())
        success_rate = passed_tests / total_tests

        overall_success = success_rate >= 0.8  # 80% success threshold

        result = AITestResult(
            success=overall_success,
            data=test_results,
            errors=errors,
            execution_time=time.time() - start_time,
            metadata={
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "success_rate": success_rate,
                "test_breakdown": test_results,
            },
        )

        self.execution_history.append(("comprehensive_test", result))
        return result

    def get_execution_summary(self) -> dict[str, Any]:
        """Get summary of all executed tests."""
        total_commands = len(self.execution_history)
        successful_commands = len([r for _, r in self.execution_history if r.success])
        total_time = sum(r.execution_time for _, r in self.execution_history)

        return {
            "total_commands": total_commands,
            "successful_commands": successful_commands,
            "failed_commands": total_commands - successful_commands,
            "success_rate": (
                successful_commands / total_commands if total_commands > 0 else 0
            ),
            "total_execution_time": total_time,
            "average_execution_time": (
                total_time / total_commands if total_commands > 0 else 0
            ),
            "command_history": [
                {
                    "command": cmd_type,
                    "success": result.success,
                    "execution_time": result.execution_time,
                    "errors": result.errors,
                }
                for cmd_type, result in self.execution_history
            ],
        }


# Simple convenience functions for AI agents
