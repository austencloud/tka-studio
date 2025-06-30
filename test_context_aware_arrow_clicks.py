"""
Test Context-Aware Arrow Click Behavior

This test verifies that arrow clicks are properly handled based on the parent component context:
- Graph Editor: Arrow clicks should trigger arrow selection
- Other Contexts: Arrow clicks should be ignored and bubble up to pictograph selection

Uses TKAAITestHelper for comprehensive testing of the TKA system.
"""

import sys
import os
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtCore import Qt, QPoint

# Add TKA paths
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
)

from core.application.application_factory import ApplicationFactory
from core.testing.ai_agent_helpers import TKAAITestHelper
from domain.models.core_models import BeatData, MotionData
from presentation.components.pictograph.pictograph_component import PictographComponent
from presentation.components.pictograph.pictograph_scene import PictographScene
from presentation.components.pictograph.graphics_items.arrow_item import ArrowItem


class ContextAwareArrowClickTester:
    """Test suite for context-aware arrow click behavior."""

    def __init__(self):
        self.app = None
        self.container = None
        self.helper = None
        self.test_results = {}

    def setup(self):
        """Setup test environment."""
        print("🔧 Setting up test environment...")

        # Create QApplication if needed
        if not QApplication.instance():
            self.app = QApplication(sys.argv)

        # Create TKA application container
        self.container = ApplicationFactory.create_test_app()

        # Create AI test helper
        self.helper = TKAAITestHelper(use_test_mode=True)

        # Verify TKA system is working
        system_check = self.helper.run_comprehensive_test_suite()
        if not system_check.success:
            raise RuntimeError(f"TKA system not working: {system_check.error}")

        print("✅ Test environment setup complete")

    def create_test_beat_data(self) -> BeatData:
        """Create test beat data with both arrows."""
        # Create motion data for both colors
        blue_motion = MotionData(
            color="blue",
            motion_type="pro",
            prop_rot_dir="cw",
            start_loc="n",
            end_loc="s",
            turns=1,
        )

        red_motion = MotionData(
            color="red",
            motion_type="anti",
            prop_rot_dir="ccw",
            start_loc="e",
            end_loc="w",
            turns=1,
        )

        return BeatData(
            beat_number=1,
            letter="A",
            blue_motion=blue_motion,
            red_motion=red_motion,
            duration=1.0,
        )

    def test_graph_editor_context(self) -> Dict[str, Any]:
        """Test arrow clicks in graph editor context."""
        print("🧪 Testing graph editor context...")

        try:
            # Create a mock graph editor container
            graph_editor_widget = QWidget()
            graph_editor_widget.setObjectName(
                "GraphEditorWidget"
            )  # Ensure "graph" in class name

            # Create pictograph container within graph editor
            pictograph_container = GraphEditorPictographContainer(graph_editor_widget)

            # Set test beat data
            beat_data = self.create_test_beat_data()
            pictograph_container.set_beat(beat_data)

            # Get the pictograph scene
            scene = pictograph_container._pictograph_view._pictograph_scene

            # Verify context detection
            component_type = scene._determine_component_type()
            assert (
                component_type == "graph_editor"
            ), f"Expected 'graph_editor', got '{component_type}'"

            # Find arrow items in the scene
            arrow_items = [
                item for item in scene.items() if isinstance(item, ArrowItem)
            ]

            if not arrow_items:
                return {
                    "success": False,
                    "error": "No arrow items found in graph editor scene",
                    "context": "graph_editor",
                }

            # Test arrow click handling
            arrow_item = arrow_items[0]
            should_handle = arrow_item._should_handle_arrow_click()

            return {
                "success": should_handle,
                "context": component_type,
                "arrow_items_found": len(arrow_items),
                "should_handle_clicks": should_handle,
                "error": (
                    None
                    if should_handle
                    else "Arrow clicks not handled in graph editor"
                ),
            }

        except Exception as e:
            return {"success": False, "error": str(e), "context": "graph_editor"}

    def test_option_picker_context(self) -> Dict[str, Any]:
        """Test arrow clicks in option picker context."""
        print("🧪 Testing option picker context...")

        try:
            # Create a mock option picker widget
            option_picker_widget = QWidget()
            option_picker_widget.setObjectName(
                "OptionPickerWidget"
            )  # Ensure "option" in class name

            # Create clickable pictograph frame within option picker
            beat_data = self.create_test_beat_data()
            clickable_frame = ClickablePictographFrame(option_picker_widget, beat_data)

            # Get the pictograph component and scene
            pictograph_component = clickable_frame.pictograph_component
            if not pictograph_component or not pictograph_component.scene:
                return {
                    "success": False,
                    "error": "Could not access pictograph scene in option picker",
                    "context": "option_picker",
                }

            scene = pictograph_component.scene

            # Verify context detection
            component_type = scene._determine_component_type()
            assert (
                component_type == "option_picker"
            ), f"Expected 'option_picker', got '{component_type}'"

            # Find arrow items in the scene
            arrow_items = [
                item for item in scene.items() if isinstance(item, ArrowItem)
            ]

            if not arrow_items:
                return {
                    "success": False,
                    "error": "No arrow items found in option picker scene",
                    "context": "option_picker",
                }

            # Test arrow click handling
            arrow_item = arrow_items[0]
            should_handle = arrow_item._should_handle_arrow_click()

            return {
                "success": not should_handle,  # Should NOT handle in option picker
                "context": component_type,
                "arrow_items_found": len(arrow_items),
                "should_handle_clicks": should_handle,
                "error": (
                    None
                    if not should_handle
                    else "Arrow clicks incorrectly handled in option picker"
                ),
            }

        except Exception as e:
            return {"success": False, "error": str(e), "context": "option_picker"}

    def test_unknown_context(self) -> Dict[str, Any]:
        """Test arrow clicks in unknown/generic context."""
        print("🧪 Testing unknown context...")

        try:
            # Create a generic widget (no specific context)
            generic_widget = QWidget()
            generic_widget.setObjectName("GenericWidget")

            # Create pictograph component directly
            pictograph_component = PictographComponent(generic_widget)

            # Set test beat data
            beat_data = self.create_test_beat_data()
            pictograph_component.update_from_beat(beat_data)

            # Get the scene
            scene = pictograph_component.scene

            # Verify context detection
            component_type = scene._determine_component_type()
            assert (
                component_type == "unknown"
            ), f"Expected 'unknown', got '{component_type}'"

            # Find arrow items in the scene
            arrow_items = [
                item for item in scene.items() if isinstance(item, ArrowItem)
            ]

            if not arrow_items:
                return {
                    "success": False,
                    "error": "No arrow items found in unknown context scene",
                    "context": "unknown",
                }

            # Test arrow click handling (should fallback to allowing clicks)
            arrow_item = arrow_items[0]
            should_handle = arrow_item._should_handle_arrow_click()

            return {
                "success": should_handle,  # Should handle in unknown context (fallback)
                "context": component_type,
                "arrow_items_found": len(arrow_items),
                "should_handle_clicks": should_handle,
                "error": (
                    None
                    if should_handle
                    else "Arrow clicks not handled in unknown context (fallback failed)"
                ),
            }

        except Exception as e:
            return {"success": False, "error": str(e), "context": "unknown"}

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all context-aware arrow click tests."""
        print("🚀 Starting context-aware arrow click tests...")

        self.setup()

        # Run individual tests
        tests = {
            "graph_editor": self.test_graph_editor_context,
            "option_picker": self.test_option_picker_context,
            "unknown_context": self.test_unknown_context,
        }

        results = {}
        overall_success = True

        for test_name, test_func in tests.items():
            print(f"\n--- Running {test_name} test ---")
            try:
                result = test_func()
                results[test_name] = result

                if result["success"]:
                    print(f"✅ {test_name}: PASSED")
                else:
                    print(
                        f"❌ {test_name}: FAILED - {result.get('error', 'Unknown error')}"
                    )
                    overall_success = False

            except Exception as e:
                print(f"💥 {test_name}: EXCEPTION - {str(e)}")
                results[test_name] = {
                    "success": False,
                    "error": f"Test exception: {str(e)}",
                    "context": test_name,
                }
                overall_success = False

        # Summary
        print(f"\n{'='*50}")
        print(f"CONTEXT-AWARE ARROW CLICK TEST SUMMARY")
        print(f"{'='*50}")

        for test_name, result in results.items():
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"{test_name:20} {status}")
            if not result["success"]:
                print(f"                     Error: {result.get('error', 'Unknown')}")

        print(
            f"\nOverall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}"
        )

        return {
            "overall_success": overall_success,
            "individual_results": results,
            "summary": f"Passed: {sum(1 for r in results.values() if r['success'])}/{len(results)}",
        }


if __name__ == "__main__":
    tester = ContextAwareArrowClickTester()
    results = tester.run_all_tests()

    # Exit with appropriate code
    sys.exit(0 if results["overall_success"] else 1)
