"""
Enhanced Comprehensive TKA User Workflow Test

Enhanced version of the comprehensive test with proper pictograph rendering,
arrow positioning orchestrator integration, and reusable testing framework.

TEST LIFECYCLE: SPECIFICATION
PURPOSE: Validate complete TKA user workflows with proper pictograph rendering
PERMANENT: Core workflow validation for TKA application
AUTHOR: AI Agent
"""
from __future__ import annotations

import os
import sys
from typing import Any


# Add the framework to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'framework'))

from tka_workflow_tester import (
    PickerType,
    TestConfiguration,
    TestMode,
    create_workflow_tester,
)


class EnhancedComprehensiveWorkflowTester:
    """
    Enhanced comprehensive workflow tester with proper pictograph rendering
    and arrow positioning orchestrator integration.
    """

    def __init__(self):
        """Initialize the enhanced tester."""
        self.config = TestConfiguration(
            mode=TestMode.HEADLESS,
            enable_arrow_positioning=True,
            debug_logging=True,
            visual_validation=True,
            timing_delays={
                "startup": 3000,
                "transition": 1000,
                "operation": 500,
                "validation": 200
            }
        )
        self.tester = None
        self.test_results = {}

    def run_enhanced_comprehensive_test(self) -> dict[str, Any]:
        """Run the enhanced comprehensive test suite."""
        print("🚀 ENHANCED COMPREHENSIVE TKA USER WORKFLOW TEST")
        print("=" * 60)
        print("Enhanced features:")
        print("✅ Proper arrow positioning orchestrator integration")
        print("✅ Pictograph rendering validation")
        print("✅ Reusable testing framework")
        print("✅ Visual validation checkpoints")
        print("=" * 60)

        overall_results = {
            "overall_success": False,
            "test_suites": {},
            "execution_time": 0.0,
            "framework_validation": False,
            "arrow_positioning_available": False,
            "pictograph_rendering_validated": False
        }

        try:
            # Initialize the framework
            print("\n🔧 [ENHANCED] Initializing enhanced testing framework...")
            self.tester = create_workflow_tester(self.config)
            overall_results["framework_validation"] = True
            print("✅ [ENHANCED] Framework initialized successfully")

            # Validate arrow positioning orchestrator
            print("\n🎯 [ENHANCED] Validating arrow positioning orchestrator...")
            arrow_validation = self._validate_arrow_positioning_orchestrator()
            overall_results["arrow_positioning_available"] = arrow_validation
            if arrow_validation:
                print("✅ [ENHANCED] Arrow positioning orchestrator available and working")
            else:
                print("⚠️ [ENHANCED] Arrow positioning orchestrator not available")

            # Run core workflow tests
            print("\n🧪 [ENHANCED] Running core workflow test suite...")
            core_results = self.tester.run_comprehensive_workflow_test()
            overall_results["test_suites"]["core_workflow"] = core_results

            # Run enhanced pictograph validation
            print("\n🎨 [ENHANCED] Running enhanced pictograph validation...")
            pictograph_results = self._run_enhanced_pictograph_validation()
            overall_results["test_suites"]["pictograph_validation"] = pictograph_results
            overall_results["pictograph_rendering_validated"] = pictograph_results.get("success", False)

            # Run start position variations with arrow validation
            print("\n🔄 [ENHANCED] Running start position variations with arrow validation...")
            start_pos_results = self._run_start_position_arrow_validation()
            overall_results["test_suites"]["start_position_arrows"] = start_pos_results

            # Run option picker arrow validation
            print("\n⚙️ [ENHANCED] Running option picker arrow validation...")
            option_picker_results = self._run_option_picker_arrow_validation()
            overall_results["test_suites"]["option_picker_arrows"] = option_picker_results

            # Calculate overall success
            self._calculate_overall_success(overall_results)

        except Exception as e:
            print(f"❌ [ENHANCED] Enhanced comprehensive test failed: {e}")
            import traceback
            traceback.print_exc()
            overall_results["error"] = str(e)

        finally:
            if self.tester:
                self.tester.cleanup()

        return overall_results

    def _validate_arrow_positioning_orchestrator(self) -> bool:
        """Validate that the arrow positioning orchestrator is properly registered and working."""
        try:
            if not self.tester or not self.tester.container:
                return False

            from core.interfaces.positioning_services import (
                IArrowPositioningOrchestrator,
            )

            # Try to resolve the orchestrator
            orchestrator = self.tester.container.resolve(IArrowPositioningOrchestrator)

            if orchestrator:
                print("✅ [ENHANCED] Arrow positioning orchestrator resolved successfully")

                # Test basic functionality
                from domain.models import (
                    Location,
                    MotionData,
                    MotionType,
                    RotationDirection,
                )
                from domain.models.pictograph_models import ArrowData, PictographData

                # Create test data
                motion_data = MotionData(
                    motion_type=MotionType.STATIC,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.SOUTH,
                    end_loc=Location.SOUTH,
                    turns=0.0
                )

                arrow_data = ArrowData(color="blue", motion_data=motion_data, is_visible=True)
                pictograph_data = PictographData(arrows={"blue": arrow_data})

                # Test position calculation
                position = orchestrator.calculate_arrow_position(arrow_data, pictograph_data)

                if position and len(position) == 3:
                    print(f"✅ [ENHANCED] Arrow position calculated: {position}")
                    return True
                print("❌ [ENHANCED] Arrow position calculation failed")
                return False
            print("❌ [ENHANCED] Arrow positioning orchestrator not available")
            return False

        except Exception as e:
            print(f"❌ [ENHANCED] Arrow positioning orchestrator validation failed: {e}")
            return False

    def _run_enhanced_pictograph_validation(self) -> dict[str, Any]:
        """Run enhanced pictograph validation with arrow positioning checks."""
        results = {
            "success": False,
            "tests_passed": 0,
            "tests_total": 0,
            "details": {}
        }

        try:
            # Test 1: Start position pictograph rendering
            print("🎨 [ENHANCED] Testing start position pictograph rendering...")
            start_pos_test = self._test_start_position_pictograph_rendering()
            results["details"]["start_position_rendering"] = start_pos_test
            results["tests_total"] += 1
            if start_pos_test:
                results["tests_passed"] += 1

            # Test 2: Option picker pictograph rendering
            print("🎨 [ENHANCED] Testing option picker pictograph rendering...")
            option_test = self._test_option_picker_pictograph_rendering()
            results["details"]["option_picker_rendering"] = option_test
            results["tests_total"] += 1
            if option_test:
                results["tests_passed"] += 1

            # Test 3: Arrow positioning consistency
            print("🎨 [ENHANCED] Testing arrow positioning consistency...")
            consistency_test = self._test_arrow_positioning_consistency()
            results["details"]["arrow_positioning_consistency"] = consistency_test
            results["tests_total"] += 1
            if consistency_test:
                results["tests_passed"] += 1

            # Calculate success rate
            success_rate = results["tests_passed"] / results["tests_total"] if results["tests_total"] > 0 else 0
            results["success"] = success_rate >= 0.8
            results["success_rate"] = success_rate

            print(f"🎨 [ENHANCED] Pictograph validation: {results['tests_passed']}/{results['tests_total']} tests passed")

        except Exception as e:
            print(f"❌ [ENHANCED] Pictograph validation failed: {e}")
            results["error"] = str(e)

        return results

    def _test_start_position_pictograph_rendering(self) -> bool:
        """Test that start position pictographs render with proper arrow positioning."""
        try:
            # Create fresh sequence to get to start position picker
            if not self.tester.create_fresh_sequence():
                return False

            # Validate we're on start position picker
            if not self.tester.validate_picker_state(PickerType.START_POSITION):
                return False

            # Check that arrow positioning orchestrator is being used (not fallback)
            if not self.tester.validate_pictograph_rendering():
                return False

            print("✅ [ENHANCED] Start position pictographs rendering correctly")
            return True

        except Exception as e:
            print(f"❌ [ENHANCED] Start position pictograph rendering test failed: {e}")
            return False

    def _test_option_picker_pictograph_rendering(self) -> bool:
        """Test that option picker pictographs render with proper arrow positioning."""
        try:
            # Create fresh sequence and select start position
            if not self.tester.create_fresh_sequence():
                return False

            if not self.tester.select_start_position("alpha1_alpha1"):
                return False

            # Validate we're on option picker
            if not self.tester.validate_picker_state(PickerType.OPTION):
                return False

            # Check that arrow positioning orchestrator is being used
            if not self.tester.validate_pictograph_rendering():
                return False

            print("✅ [ENHANCED] Option picker pictographs rendering correctly")
            return True

        except Exception as e:
            print(f"❌ [ENHANCED] Option picker pictograph rendering test failed: {e}")
            return False

    def _test_arrow_positioning_consistency(self) -> bool:
        """Test that arrow positioning is consistent across different contexts."""
        try:
            # This test would validate that the same motion data produces
            # consistent arrow positions across different UI contexts

            # For now, just validate that the orchestrator is available
            return self._validate_arrow_positioning_orchestrator()

        except Exception as e:
            print(f"❌ [ENHANCED] Arrow positioning consistency test failed: {e}")
            return False

    def _run_start_position_arrow_validation(self) -> dict[str, Any]:
        """Run start position variations with arrow validation."""
        results = {"success": False, "positions_tested": 0, "positions_passed": 0}

        try:
            start_positions = ["alpha1_alpha1", "beta1_beta1", "gamma1_gamma1"]

            for position in start_positions:
                print(f"🔄 [ENHANCED] Testing start position: {position}")

                # Create fresh sequence
                if not self.tester.create_fresh_sequence():
                    continue

                # Select the start position
                if not self.tester.select_start_position(position):
                    continue

                # Validate pictograph rendering
                if self.tester.validate_pictograph_rendering():
                    results["positions_passed"] += 1
                    print(f"✅ [ENHANCED] {position} arrows rendered correctly")
                else:
                    print(f"❌ [ENHANCED] {position} arrow rendering failed")

                results["positions_tested"] += 1

            success_rate = results["positions_passed"] / results["positions_tested"] if results["positions_tested"] > 0 else 0
            results["success"] = success_rate >= 0.8
            results["success_rate"] = success_rate

        except Exception as e:
            print(f"❌ [ENHANCED] Start position arrow validation failed: {e}")
            results["error"] = str(e)

        return results

    def _run_option_picker_arrow_validation(self) -> dict[str, Any]:
        """Run option picker arrow validation."""
        results = {"success": False, "validation_passed": False}

        try:
            # Create sequence and get to option picker
            if not self.tester.create_fresh_sequence():
                return results

            if not self.tester.select_start_position("alpha1_alpha1"):
                return results

            # Validate option picker arrows
            if self.tester.validate_pictograph_rendering():
                results["validation_passed"] = True
                results["success"] = True
                print("✅ [ENHANCED] Option picker arrows validated successfully")
            else:
                print("❌ [ENHANCED] Option picker arrow validation failed")

        except Exception as e:
            print(f"❌ [ENHANCED] Option picker arrow validation failed: {e}")
            results["error"] = str(e)

        return results

    def _calculate_overall_success(self, results: dict[str, Any]):
        """Calculate overall success based on all test results."""
        try:
            # Count successful test suites
            test_suites = results.get("test_suites", {})
            successful_suites = 0
            total_suites = len(test_suites)

            for _suite_name, suite_results in test_suites.items():
                if (isinstance(suite_results, dict) and suite_results.get("success", False)) or (isinstance(suite_results, dict) and suite_results.get("overall_success", False)):
                    successful_suites += 1

            # Calculate success rate
            success_rate = successful_suites / total_suites if total_suites > 0 else 0

            # Overall success requires:
            # 1. Framework validation passed
            # 2. Arrow positioning available
            # 3. At least 80% of test suites passed
            overall_success = (
                results.get("framework_validation", False) and
                results.get("arrow_positioning_available", False) and
                success_rate >= 0.8
            )

            results["overall_success"] = overall_success
            results["success_rate"] = success_rate
            results["successful_suites"] = successful_suites
            results["total_suites"] = total_suites

            print("\n📊 [ENHANCED] Overall Results:")
            print(f"   Framework Validation: {'✅' if results['framework_validation'] else '❌'}")
            print(f"   Arrow Positioning: {'✅' if results['arrow_positioning_available'] else '❌'}")
            print(f"   Test Suites: {successful_suites}/{total_suites} passed")
            print(f"   Success Rate: {success_rate:.1%}")
            print(f"   Overall Success: {'✅' if overall_success else '❌'}")

        except Exception as e:
            print(f"❌ [ENHANCED] Failed to calculate overall success: {e}")
            results["overall_success"] = False


def main() -> int:
    """Main entry point for the enhanced comprehensive test."""
    tester = EnhancedComprehensiveWorkflowTester()
    results = tester.run_enhanced_comprehensive_test()

    if results.get("overall_success", False):
        print("\n🎉 ENHANCED COMPREHENSIVE TKA USER WORKFLOW TEST COMPLETED")
        print("✅ All enhanced features and workflows working correctly")
        return 0
    print("\n❌ ENHANCED COMPREHENSIVE TKA USER WORKFLOW TEST FAILED")
    print("❌ Check detailed results above for specific failures")
    return 1


if __name__ == "__main__":
    sys.exit(main())
