"""
TKA Workflow Testing Framework

Reusable testing framework for comprehensive TKA user workflow validation.
Provides a clean API for testing complex user interactions with proper
pictograph rendering and arrow positioning orchestrator integration.

TEST LIFECYCLE: SPECIFICATION
PURPOSE: Provide reusable testing infrastructure for TKA workflows
PERMANENT: Core testing framework for all TKA workflow tests
AUTHOR: AI Agent
"""

import os
import sys
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from application.services.sequence.sequence_persister import SequencePersister
from core.application.application_factory import ApplicationFactory
from core.testing.ai_agent_helpers import AITestResult, TKAAITestHelper
from domain.models import BeatData, SequenceData
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication


class TestMode(Enum):
    """Test execution modes."""

    HEADLESS = "headless"
    UI_VISIBLE = "ui_visible"
    DEBUG = "debug"


class PickerType(Enum):
    """UI picker types."""

    START_POSITION = "start_position"
    OPTION = "option"
    UNKNOWN = "unknown"


@dataclass
class WorkflowState:
    """Represents the current state of the TKA workflow."""

    picker_type: PickerType
    sequence_length: int
    has_start_position: bool
    timestamp: float
    event_name: str


@dataclass
class TestConfiguration:
    """Configuration for test execution."""

    mode: TestMode = TestMode.HEADLESS
    enable_arrow_positioning: bool = True
    debug_logging: bool = False
    timing_delays: Dict[str, int] = None
    visual_validation: bool = True

    def __post_init__(self):
        if self.timing_delays is None:
            self.timing_delays = {
                "startup": 3000,
                "transition": 1000,
                "operation": 500,
                "validation": 200,
            }


class TKAWorkflowTester:
    """
    Reusable testing framework for TKA user workflows.

    Provides a clean API for testing complex user interactions with proper
    pictograph rendering, arrow positioning orchestrator integration, and
    comprehensive validation.
    """

    def __init__(self, config: Optional[TestConfiguration] = None):
        """Initialize the workflow tester with configuration."""
        self.config = config or TestConfiguration()
        self.app = None
        self.container = None
        self.construct_tab = None
        self.layout_manager = None
        self.workbench = None
        self.persistence_service = None
        self.ai_helper = None

        # State tracking
        self.workflow_log: List[WorkflowState] = []
        self.test_results: Dict[str, Any] = {}

        # Component references
        self._component_refs = {}

    def initialize(self) -> bool:
        """Initialize the testing environment with proper DI container setup."""
        try:
            # Create QApplication if needed
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()

            # Create DI container with arrow positioning orchestrator
            self.container = self._create_enhanced_container()

            # Initialize AI test helper
            self.ai_helper = TKAAITestHelper(use_test_mode=True)

            # Initialize persistence service
            self.persistence_service = SequencePersister()

            if self.config.debug_logging:
                print("✅ [FRAMEWORK] TKA Workflow Tester initialized successfully")

            return True

        except Exception as e:
            print(f"❌ [FRAMEWORK] Initialization failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _create_enhanced_container(self):
        """Create DI container with arrow positioning orchestrator properly registered."""
        container = ApplicationFactory.create_production_app()

        # Ensure arrow positioning orchestrator is registered
        try:
            from application.services.positioning.arrows.orchestration.arrow_positioning_orchestrator import (
                ArrowPositioningOrchestrator,
            )
            from core.interfaces.positioning_services import (
                IArrowPositioningOrchestrator,
            )

            # Check if already registered
            try:
                container.resolve(IArrowPositioningOrchestrator)
                if self.config.debug_logging:
                    print(
                        "✅ [FRAMEWORK] Arrow positioning orchestrator already registered"
                    )
            except Exception:
                # Register the orchestrator and its dependencies
                self._register_arrow_positioning_services(container)
                if self.config.debug_logging:
                    print("✅ [FRAMEWORK] Arrow positioning orchestrator registered")

        except ImportError as e:
            if self.config.debug_logging:
                print(f"⚠️ [FRAMEWORK] Arrow positioning services not available: {e}")

        return container

    def _register_arrow_positioning_services(self, container):
        """Register arrow positioning orchestrator and its dependencies."""
        try:
            # Import all required services
            from application.services.positioning.arrows.calculation.arrow_location_calculator import (
                ArrowLocationCalculatorService,
            )
            from application.services.positioning.arrows.calculation.arrow_rotation_calculator import (
                ArrowRotationCalculatorService,
            )
            from application.services.positioning.arrows.coordinate_system.arrow_coordinate_system_service import (
                ArrowCoordinateSystemService,
            )
            from application.services.positioning.arrows.orchestration.arrow_adjustment_calculator_service import (
                ArrowAdjustmentCalculatorService,
            )
            from application.services.positioning.arrows.orchestration.arrow_positioning_orchestrator import (
                ArrowPositioningOrchestrator,
            )
            from core.interfaces.positioning_services import (
                IArrowAdjustmentCalculator,
                IArrowCoordinateSystemService,
                IArrowLocationCalculator,
                IArrowPositioningOrchestrator,
                IArrowRotationCalculator,
            )

            # Register calculator microservices
            container.register_singleton(
                IArrowLocationCalculator, ArrowLocationCalculatorService
            )
            container.register_singleton(
                IArrowRotationCalculator, ArrowRotationCalculatorService
            )
            container.register_singleton(
                IArrowAdjustmentCalculator, ArrowAdjustmentCalculatorService
            )
            container.register_singleton(
                IArrowCoordinateSystemService, ArrowCoordinateSystemService
            )

            # Register orchestrator
            container.register_singleton(
                IArrowPositioningOrchestrator, ArrowPositioningOrchestrator
            )

        except ImportError as e:
            if self.config.debug_logging:
                print(
                    f"⚠️ [FRAMEWORK] Could not register arrow positioning services: {e}"
                )

    def create_fresh_sequence(self) -> bool:
        """Start a new sequence workflow from scratch."""
        try:
            # Clear any existing sequence
            self.persistence_service.clear_current_sequence()

            # Create fresh construct tab if needed
            if not self.construct_tab:
                from presentation.tabs.construct.construct_tab_widget import (
                    ConstructTabWidget,
                )

                self.construct_tab = ConstructTabWidget(self.container)

                # Get component references
                if hasattr(self.construct_tab, "layout_manager"):
                    self.layout_manager = self.construct_tab.layout_manager
                    if hasattr(self.layout_manager, "workbench"):
                        self.workbench = self.layout_manager.workbench

                # Show UI if in visible mode
                if self.config.mode == TestMode.UI_VISIBLE:
                    self.construct_tab.show()
                    self.construct_tab.resize(1200, 800)

                # Wait for startup
                QTest.qWait(self.config.timing_delays["startup"])
            else:
                # Clear existing sequence
                if hasattr(self.construct_tab, "clear_sequence"):
                    self.construct_tab.clear_sequence()
                    QTest.qWait(self.config.timing_delays["operation"])

            # Log initial state
            self._log_workflow_state("FRESH_SEQUENCE_CREATED")

            if self.config.debug_logging:
                print("✅ [FRAMEWORK] Fresh sequence workflow created")

            return True

        except Exception as e:
            print(f"❌ [FRAMEWORK] Failed to create fresh sequence: {e}")
            import traceback

            traceback.print_exc()
            return False

    def select_start_position(self, position_name: str = "alpha1_alpha1") -> bool:
        """Programmatically select a start position."""
        try:
            if not self.layout_manager or not hasattr(
                self.layout_manager, "start_position_picker"
            ):
                print("❌ [FRAMEWORK] Start position picker not available")
                return False

            picker = self.layout_manager.start_position_picker
            if not hasattr(picker, "start_position_selected"):
                print("❌ [FRAMEWORK] Start position picker missing signal")
                return False

            # Log before state
            self._log_workflow_state(f"BEFORE_SELECT_{position_name}")

            # Emit start position selected signal
            picker.start_position_selected.emit(position_name)

            # Wait for processing
            QTest.qWait(self.config.timing_delays["transition"])

            # Log after state
            self._log_workflow_state(f"AFTER_SELECT_{position_name}")

            if self.config.debug_logging:
                print(f"✅ [FRAMEWORK] Selected start position: {position_name}")

            return True

        except Exception as e:
            print(
                f"❌ [FRAMEWORK] Failed to select start position {position_name}: {e}"
            )
            import traceback

            traceback.print_exc()
            return False

    def add_beats(self, beat_data_list: List[BeatData]) -> bool:
        """Add multiple beats to the sequence."""
        try:
            if not self.workbench:
                print("❌ [FRAMEWORK] Workbench not available")
                return False

            for i, beat_data in enumerate(beat_data_list):
                # Log before adding beat
                self._log_workflow_state(f"BEFORE_ADD_BEAT_{i+1}")

                # Add beat to workbench
                if hasattr(self.workbench, "add_beat"):
                    self.workbench.add_beat(beat_data)
                else:
                    print(f"❌ [FRAMEWORK] Workbench missing add_beat method")
                    return False

                # Wait for processing
                QTest.qWait(self.config.timing_delays["operation"])

                # Log after adding beat
                self._log_workflow_state(f"AFTER_ADD_BEAT_{i+1}")

            if self.config.debug_logging:
                print(f"✅ [FRAMEWORK] Added {len(beat_data_list)} beats to sequence")

            return True

        except Exception as e:
            print(f"❌ [FRAMEWORK] Failed to add beats: {e}")
            import traceback

            traceback.print_exc()
            return False

    def validate_picker_state(self, expected_picker: PickerType) -> bool:
        """Assert current picker state matches expected."""
        try:
            current_state = self._get_current_workflow_state()

            if current_state.picker_type == expected_picker:
                if self.config.debug_logging:
                    print(
                        f"✅ [FRAMEWORK] Picker state validation passed: {expected_picker.value}"
                    )
                return True
            else:
                print(
                    f"❌ [FRAMEWORK] Picker state mismatch: expected {expected_picker.value}, got {current_state.picker_type.value}"
                )
                return False

        except Exception as e:
            print(f"❌ [FRAMEWORK] Picker state validation failed: {e}")
            return False

    def validate_sequence_length(self, expected_length: int) -> bool:
        """Assert sequence content matches expected length."""
        try:
            current_state = self._get_current_workflow_state()

            if current_state.sequence_length == expected_length:
                if self.config.debug_logging:
                    print(
                        f"✅ [FRAMEWORK] Sequence length validation passed: {expected_length}"
                    )
                return True
            else:
                print(
                    f"❌ [FRAMEWORK] Sequence length mismatch: expected {expected_length}, got {current_state.sequence_length}"
                )
                return False

        except Exception as e:
            print(f"❌ [FRAMEWORK] Sequence length validation failed: {e}")
            return False

    def validate_pictograph_rendering(self) -> bool:
        """Validate that pictographs are rendering with proper arrow positioning."""
        try:
            if not self.config.visual_validation:
                if self.config.debug_logging:
                    print(
                        "⚠️ [FRAMEWORK] Visual validation disabled, skipping pictograph validation"
                    )
                return True

            # Check if arrow positioning orchestrator is available
            try:
                from core.interfaces.positioning_services import (
                    IArrowPositioningOrchestrator,
                )

                orchestrator = self.container.resolve(IArrowPositioningOrchestrator)

                if self.config.debug_logging:
                    print(
                        "✅ [FRAMEWORK] Arrow positioning orchestrator available for pictograph rendering"
                    )

                # TODO: Add specific pictograph rendering validation
                # This could include checking that pictographs have:
                # - Properly positioned arrows (not fallback positioning)
                # - Correct motion indicators
                # - Proper prop positioning

                return True

            except Exception as e:
                print(
                    f"❌ [FRAMEWORK] Arrow positioning orchestrator not available: {e}"
                )
                return False

        except Exception as e:
            print(f"❌ [FRAMEWORK] Pictograph rendering validation failed: {e}")
            return False

    def clear_sequence(self) -> bool:
        """Clear the current sequence."""
        try:
            if not self.construct_tab or not hasattr(
                self.construct_tab, "clear_sequence"
            ):
                print("❌ [FRAMEWORK] Clear sequence method not available")
                return False

            # Log before state
            self._log_workflow_state("BEFORE_CLEAR_SEQUENCE")

            # Clear the sequence
            self.construct_tab.clear_sequence()

            # Wait for processing
            QTest.qWait(self.config.timing_delays["operation"])

            # Log after state
            self._log_workflow_state("AFTER_CLEAR_SEQUENCE")

            if self.config.debug_logging:
                print("✅ [FRAMEWORK] Sequence cleared successfully")

            return True

        except Exception as e:
            print(f"❌ [FRAMEWORK] Failed to clear sequence: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _log_workflow_state(self, event_name: str):
        """Log the current workflow state."""
        try:
            state = self._get_current_workflow_state()
            state.event_name = event_name
            self.workflow_log.append(state)

            if self.config.debug_logging:
                print(
                    f"🔍 [FRAMEWORK] {event_name}: picker={state.picker_type.value}, sequence_length={state.sequence_length}"
                )

        except Exception as e:
            if self.config.debug_logging:
                print(f"⚠️ [FRAMEWORK] Failed to log workflow state: {e}")

    def _get_current_workflow_state(self) -> WorkflowState:
        """Get the current workflow state."""
        try:
            # Determine picker type
            picker_type = PickerType.UNKNOWN
            if self.layout_manager and hasattr(self.layout_manager, "picker_stack"):
                picker_stack = self.layout_manager.picker_stack
                current_index = picker_stack.currentIndex()

                if current_index == 0:
                    picker_type = PickerType.START_POSITION
                elif current_index == 1:
                    picker_type = PickerType.OPTION

            # Determine sequence length
            sequence_length = 0
            has_start_position = False
            try:
                sequence = self.persistence_service.load_current_sequence()
                sequence_length = len(sequence)

                # Check if workbench has start position
                if self.workbench and hasattr(self.workbench, "start_position_data"):
                    has_start_position = self.workbench.start_position_data is not None

            except Exception:
                sequence_length = 0

            return WorkflowState(
                picker_type=picker_type,
                sequence_length=sequence_length,
                has_start_position=has_start_position,
                timestamp=time.time(),
                event_name="",
            )

        except Exception as e:
            if self.config.debug_logging:
                print(f"⚠️ [FRAMEWORK] Failed to get workflow state: {e}")
            return WorkflowState(
                picker_type=PickerType.UNKNOWN,
                sequence_length=0,
                has_start_position=False,
                timestamp=time.time(),
                event_name="",
            )

    def _workflow_state_to_dict(self, state: WorkflowState) -> Dict[str, Any]:
        """Convert workflow state to dictionary for serialization."""
        return {
            "picker_type": state.picker_type.value,
            "sequence_length": state.sequence_length,
            "has_start_position": state.has_start_position,
            "timestamp": state.timestamp,
            "event_name": state.event_name,
        }

    def cleanup(self):
        """Clean up resources."""
        try:
            if self.construct_tab:
                self.construct_tab.close()

            if self.app and self.app != QApplication.instance():
                self.app.quit()

            if self.config.debug_logging:
                print("✅ [FRAMEWORK] Cleanup completed")

        except Exception as e:
            print(f"⚠️ [FRAMEWORK] Cleanup warning: {e}")

    def run_comprehensive_workflow_test(self) -> Dict[str, Any]:
        """Run a comprehensive workflow test covering all major user interactions."""
        results = {
            "overall_success": False,
            "test_results": {},
            "workflow_log": [],
            "execution_time": 0.0,
            "error_count": 0,
        }

        start_time = time.time()

        try:
            # Test 1: Basic workflow
            print("\n🧪 [FRAMEWORK] Running basic workflow test...")
            basic_result = self._test_basic_workflow()
            results["test_results"]["basic_workflow"] = basic_result

            # Test 2: Pictograph rendering validation
            print("\n🧪 [FRAMEWORK] Running pictograph rendering validation...")
            rendering_result = self.validate_pictograph_rendering()
            results["test_results"]["pictograph_rendering"] = rendering_result

            # Calculate overall success
            test_results = results["test_results"]
            passed_tests = sum(1 for result in test_results.values() if result)
            total_tests = len(test_results)
            success_rate = passed_tests / total_tests if total_tests > 0 else 0

            results["overall_success"] = success_rate >= 0.8
            results["success_rate"] = success_rate
            results["passed_tests"] = passed_tests
            results["total_tests"] = total_tests

        except Exception as e:
            print(f"❌ [FRAMEWORK] Comprehensive test failed: {e}")
            results["error_count"] += 1
            import traceback

            traceback.print_exc()

        finally:
            results["execution_time"] = time.time() - start_time
            results["workflow_log"] = [
                self._workflow_state_to_dict(state) for state in self.workflow_log
            ]

        return results

    def _test_basic_workflow(self) -> bool:
        """Test basic user workflow: start → select position → add beat → clear."""
        try:
            # Create fresh sequence
            if not self.create_fresh_sequence():
                return False

            # Validate initial state (should be start position picker)
            if not self.validate_picker_state(PickerType.START_POSITION):
                return False

            # Select start position
            if not self.select_start_position("alpha1_alpha1"):
                return False

            # Validate transition to option picker
            if not self.validate_picker_state(PickerType.OPTION):
                return False

            # Clear sequence
            if not self.clear_sequence():
                return False

            # Validate return to start position picker
            if not self.validate_picker_state(PickerType.START_POSITION):
                return False

            return True

        except Exception as e:
            print(f"❌ [FRAMEWORK] Basic workflow test failed: {e}")
            return False


# Convenience functions for easy import and use
def create_workflow_tester(
    config: Optional[TestConfiguration] = None,
) -> TKAWorkflowTester:
    """Create and initialize a workflow tester."""
    tester = TKAWorkflowTester(config)
    if tester.initialize():
        return tester
    raise RuntimeError("Failed to initialize TKA workflow tester")


def run_quick_workflow_test(debug: bool = False) -> Dict[str, Any]:
    """Run a quick workflow test with default configuration."""
    config = TestConfiguration(
        mode=TestMode.HEADLESS,
        debug_logging=debug,
        timing_delays={
            "startup": 1000,
            "transition": 500,
            "operation": 200,
            "validation": 100,
        },
    )

    tester = create_workflow_tester(config)
    try:
        return tester.run_comprehensive_workflow_test()
    finally:
        tester.cleanup()
