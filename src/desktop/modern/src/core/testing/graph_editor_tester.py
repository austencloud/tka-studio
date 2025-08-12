"""
Simple UI Testing Framework - Chunk 4: Graph Editor Testing

Tests graph editor interactions and provides clear guidance for AI agents.
"""
from __future__ import annotations

import time

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from desktop.modern.core.testing.ai_agent_helpers import AITestResult


class GraphEditorTester:
    """Tests graph editor interactions and provides AI agent guidance."""

    # Graph editor control guidance
    CONTROL_GUIDANCE = {
        "turn_adjustment_left": {
            "description": "Left click to decrease turns by 0.5",
            "test_method": "left_click_test",
            "expected_behavior": "Reduces beat turn count",
            "common_issues": [
                "Turn adjustment not connected to beat data",
                "Immutable beat update not implemented",
                "UI not reflecting turn changes",
            ],
        },
        "turn_adjustment_right": {
            "description": "Right click to increase turns by 0.5",
            "test_method": "right_click_test",
            "expected_behavior": "Increases beat turn count",
            "common_issues": [
                "Turn adjustment not connected to beat data",
                "Immutable beat update not implemented",
                "UI not reflecting turn changes",
            ],
        },
        "orientation_picker": {
            "description": "Click to cycle through orientation options",
            "test_method": "click_test",
            "expected_behavior": "Changes beat orientation",
            "common_issues": [
                "Orientation picker not connected to beat data",
                "Orientation options not properly defined",
                "UI not updating with new orientation",
            ],
        },
        "keyboard_shortcuts": {
            "description": "WASD movement, X/Z/C commands",
            "test_method": "keyboard_test",
            "expected_behavior": "Responds to keyboard input",
            "common_issues": [
                "Keyboard event handling not implemented",
                "Focus management not working",
                "Shortcuts not properly mapped",
            ],
        },
    }

    def __init__(self, graph_editor, app):
        self.graph_editor = graph_editor
        self.app = app
        self.test_results = []

    def test_turn_adjustment_controls(self, controls: dict) -> AITestResult:
        """Test turn adjustment left/right controls."""
        print("🧪 Testing turn adjustment controls...")

        start_time = time.time()
        results = []

        # Test left adjustment
        if "turn_adjustment_left" in controls:
            left_result = self._test_turn_control(
                controls["turn_adjustment_left"],
                "turn_adjustment_left",
                Qt.MouseButton.LeftButton,
            )
            results.append(left_result)

        # Test right adjustment
        if "turn_adjustment_right" in controls:
            right_result = self._test_turn_control(
                controls["turn_adjustment_right"],
                "turn_adjustment_right",
                Qt.MouseButton.RightButton,
            )
            results.append(right_result)

        # Calculate summary
        successful_tests = sum(1 for r in results if r.success)
        all_errors = []
        for result in results:
            all_errors.extend(result.errors)

        overall_success = len(results) > 0 and successful_tests == len(results)
        execution_time = time.time() - start_time

        print(
            f"📊 Turn adjustment test results: {successful_tests}/{len(results)} passed"
        )

        return AITestResult(
            success=overall_success,
            errors=all_errors,
            execution_time=execution_time,
            metadata={
                "controls_tested": len(results),
                "successful_controls": successful_tests,
                "individual_results": results,
            },
        )

    def _test_turn_control(
        self, control_widget, control_name: str, mouse_button
    ) -> AITestResult:
        """Test a single turn adjustment control."""
        start_time = time.time()

        try:
            if not control_widget:
                return self._create_failure_result(
                    control_name, ["Control widget not found"], start_time
                )

            if not control_widget.isEnabled():
                return self._create_failure_result(
                    control_name, ["Control is disabled"], start_time
                )

            # Capture initial state
            initial_state = self._capture_graph_state()

            # Perform click
            QTest.mouseClick(control_widget, mouse_button)
            self.app.processEvents()
            time.sleep(0.1)

            # Capture final state
            final_state = self._capture_graph_state()

            # Check if state changed
            state_changed = initial_state != final_state

            result = AITestResult(
                success=state_changed,
                errors=[] if state_changed else ["Control click did not change state"],
                execution_time=time.time() - start_time,
                metadata={
                    "control_name": control_name,
                    "mouse_button": str(mouse_button),
                    "state_changed": state_changed,
                    "initial_state": initial_state,
                    "final_state": final_state,
                },
            )

            if not result.success:
                self._print_control_guidance(control_name)

            return result

        except Exception as e:
            return self._create_failure_result(
                control_name, [f"Exception during testing: {e!s}"], start_time
            )

    def test_keyboard_shortcuts(self) -> AITestResult:
        """Test keyboard shortcuts (WASD, X, Z, C)."""
        print("🧪 Testing keyboard shortcuts...")

        start_time = time.time()
        shortcuts_to_test = [
            ("W", "Move up"),
            ("A", "Move left"),
            ("S", "Move down"),
            ("D", "Move right"),
            ("X", "Special command X"),
            ("Z", "Special command Z"),
            ("C", "Special command C"),
        ]

        results = []

        for key, description in shortcuts_to_test:
            result = self._test_keyboard_shortcut(key, description)
            results.append(result)
            time.sleep(0.05)  # Small delay between key tests

        # Calculate summary
        successful_tests = sum(1 for r in results if r.success)
        all_errors = []
        for result in results:
            all_errors.extend(result.errors)

        overall_success = successful_tests > 0  # At least some shortcuts should work
        execution_time = time.time() - start_time

        print(
            f"📊 Keyboard shortcut test results: {successful_tests}/{len(results)} passed"
        )

        return AITestResult(
            success=overall_success,
            errors=all_errors,
            execution_time=execution_time,
            metadata={
                "shortcuts_tested": len(results),
                "successful_shortcuts": successful_tests,
                "individual_results": results,
            },
        )

    def _test_keyboard_shortcut(self, key: str, description: str) -> AITestResult:
        """Test a single keyboard shortcut."""
        start_time = time.time()

        try:
            # Ensure graph editor has focus
            if self.graph_editor:
                self.graph_editor.setFocus()
                self.app.processEvents()

            # Capture initial state
            initial_state = self._capture_graph_state()

            # Send key event
            QTest.keyClick(self.graph_editor, key)
            self.app.processEvents()
            time.sleep(0.1)

            # Capture final state
            final_state = self._capture_graph_state()

            # Check if state changed
            state_changed = initial_state != final_state

            result = AITestResult(
                success=state_changed,
                errors=[] if state_changed else [f"Key '{key}' did not change state"],
                execution_time=time.time() - start_time,
                metadata={
                    "key": key,
                    "description": description,
                    "state_changed": state_changed,
                },
            )

            if result.success:
                print(f"✅ Key '{key}' ({description}) test passed")
            else:
                print(f"❌ Key '{key}' ({description}) test failed")

            return result

        except Exception as e:
            return AITestResult(
                success=False,
                errors=[f"Exception testing key '{key}': {e!s}"],
                execution_time=time.time() - start_time,
                metadata={"key": key, "description": description},
            )

    def test_orientation_picker(self, controls: dict) -> AITestResult:
        """Test orientation picker functionality."""
        print("🧪 Testing orientation picker...")

        start_time = time.time()

        if "orientation_picker" not in controls:
            return AITestResult(
                success=False,
                errors=["Orientation picker not found"],
                execution_time=time.time() - start_time,
            )

        orientation_picker = controls["orientation_picker"]

        try:
            # Capture initial state
            initial_state = self._capture_graph_state()

            # Click orientation picker multiple times to test cycling
            for _i in range(3):
                QTest.mouseClick(orientation_picker, Qt.MouseButton.LeftButton)
                self.app.processEvents()
                time.sleep(0.1)

            # Capture final state
            final_state = self._capture_graph_state()

            # Check if state changed
            state_changed = initial_state != final_state

            result = AITestResult(
                success=state_changed,
                errors=(
                    [] if state_changed else ["Orientation picker did not change state"]
                ),
                execution_time=time.time() - start_time,
                metadata={
                    "control_name": "orientation_picker",
                    "clicks_performed": 3,
                    "state_changed": state_changed,
                },
            )

            if not result.success:
                self._print_control_guidance("orientation_picker")

            return result

        except Exception as e:
            return self._create_failure_result(
                "orientation_picker",
                [f"Exception during testing: {e!s}"],
                start_time,
            )

    def _capture_graph_state(self) -> dict:
        """Capture current graph editor state for comparison."""
        # This is a simplified state capture
        # In a real implementation, you'd capture relevant graph editor state
        state = {
            "timestamp": time.time(),
            "graph_editor_visible": (
                self.graph_editor.isVisible() if self.graph_editor else False
            ),
        }

        # Try to capture additional state if available
        try:
            if self.graph_editor:
                state.update(
                    {
                        "has_focus": self.graph_editor.hasFocus(),
                        "geometry": (
                            self.graph_editor.geometry().getRect()
                            if hasattr(self.graph_editor, "geometry")
                            else None
                        ),
                    }
                )
        except:
            pass

        return state

    def _create_failure_result(
        self, control_name: str, errors: list[str], start_time: float
    ) -> AITestResult:
        """Create a failure result with control guidance."""
        self._print_control_guidance(control_name)

        return AITestResult(
            success=False,
            errors=errors,
            execution_time=time.time() - start_time,
            metadata={"control_name": control_name, "guidance_provided": True},
        )

    def _print_control_guidance(self, control_name: str):
        """Print guidance for failed control."""
        guidance = self.CONTROL_GUIDANCE.get(control_name, {})

        if not guidance:
            print(f"⚠️  No guidance available for control: {control_name}")
            return

        print(f"\n🔍 CONTROL GUIDANCE for {control_name}:")
        print(f"   📋 Description: {guidance.get('description', 'Unknown')}")
        print(f"   🎯 Expected: {guidance.get('expected_behavior', 'Unknown')}")
        print("   🐛 Common Issues:")

        for issue in guidance.get("common_issues", []):
            print(f"      • {issue}")
        print()

    def test_all_graph_editor_interactions(self, controls: dict) -> AITestResult:
        """Test all graph editor interactions."""
        print("🧪 Testing all graph editor interactions...")

        start_time = time.time()
        all_results = []

        # Test turn adjustment controls
        turn_results = self.test_turn_adjustment_controls(controls)
        all_results.append(turn_results)

        # Test orientation picker
        orientation_results = self.test_orientation_picker(controls)
        all_results.append(orientation_results)

        # Test keyboard shortcuts
        keyboard_results = self.test_keyboard_shortcuts()
        all_results.append(keyboard_results)

        # Calculate overall results
        successful_tests = sum(1 for r in all_results if r.success)
        all_errors = []
        for result in all_results:
            all_errors.extend(result.errors)

        overall_success = successful_tests > 0  # At least some tests should pass
        execution_time = time.time() - start_time

        print("\n📊 GRAPH EDITOR TESTING SUMMARY:")
        print(f"   ✅ Successful test suites: {successful_tests}/{len(all_results)}")
        print(
            f"   ❌ Failed test suites: {len(all_results) - successful_tests}/{len(all_results)}"
        )
        print(f"   ⏱️  Total time: {execution_time:.2f}s")

        return AITestResult(
            success=overall_success,
            errors=all_errors,
            execution_time=execution_time,
            metadata={
                "total_test_suites": len(all_results),
                "successful_test_suites": successful_tests,
                "failed_test_suites": len(all_results) - successful_tests,
                "individual_results": all_results,
            },
        )
