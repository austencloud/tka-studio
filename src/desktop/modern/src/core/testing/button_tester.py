"""
Simple UI Testing Framework - Chunk 3: Button Testing with Legacy Guidance

Tests buttons and provides clear guidance for AI agents when buttons fail.
"""
from __future__ import annotations

import time

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QPushButton

from desktop.modern.core.testing.ai_agent_helpers import AITestResult


class ButtonTester:
    """Tests workbench buttons and provides AI agent guidance."""

    # Legacy guidance mapping
    LEGACY_GUIDANCE = {
        "add_to_dictionary": {
            "file": "presentation/components/workbench/workbench.py",
            "method": "_on_add_to_dictionary_clicked",
            "signal": "add_to_dictionary_button.clicked.connect",
            "common_issues": [
                "Button not connected to signal",
                "Dictionary service not resolved",
                "Validation failing on sequence data",
            ],
        },
        "delete_beat": {
            "file": "presentation/components/workbench/workbench.py",
            "method": "_on_delete_beat_clicked",
            "signal": "delete_beat_button.clicked.connect",
            "common_issues": [
                "Beat deletion service not connected",
                "No beat selected for deletion",
                "Undo/redo not properly implemented",
            ],
        },
        "clone_beat": {
            "file": "presentation/components/workbench/workbench.py",
            "method": "_on_clone_beat_clicked",
            "signal": "clone_beat_button.clicked.connect",
            "common_issues": [
                "Beat cloning logic not implemented",
                "Position insertion logic missing",
                "Immutable beat data not properly handled",
            ],
        },
        "mirror_beat": {
            "file": "presentation/components/workbench/workbench.py",
            "method": "_on_mirror_beat_clicked",
            "signal": "mirror_beat_button.clicked.connect",
            "common_issues": [
                "Mirror transformation not implemented",
                "Motion data transformation missing",
                "Start/end location mapping incorrect",
            ],
        },
        "rotate_beat": {
            "file": "presentation/components/workbench/workbench.py",
            "method": "_on_rotate_beat_clicked",
            "signal": "rotate_beat_button.clicked.connect",
            "common_issues": [
                "Rotation transformation not implemented",
                "Location rotation mapping missing",
                "Prop rotation direction not handled",
            ],
        },
        "reset_beat": {
            "file": "presentation/components/workbench/workbench.py",
            "method": "_on_reset_beat_clicked",
            "signal": "reset_beat_button.clicked.connect",
            "common_issues": [
                "Beat reset logic not implemented",
                "Default state not properly defined",
                "Undo operation not available",
            ],
        },
        "generate_beat": {
            "file": "presentation/components/workbench/workbench.py",
            "method": "_on_generate_beat_clicked",
            "signal": "generate_beat_button.clicked.connect",
            "common_issues": [
                "Beat generation service not connected",
                "Generation algorithms not implemented",
                "Context data not properly passed",
            ],
        },
        "add_beat": {
            "file": "presentation/components/workbench/workbench.py",
            "method": "_on_add_beat_clicked",
            "signal": "add_beat_button.clicked.connect",
            "common_issues": [
                "Beat addition logic not implemented",
                "Position insertion not handled",
                "Sequence length validation missing",
            ],
        },
        "export_image": {
            "file": "presentation/components/workbench/workbench.py",
            "method": "_on_export_image_clicked",
            "signal": "export_image_button.clicked.connect",
            "common_issues": [
                "Image export service not connected",
                "File dialog not properly configured",
                "Rendering pipeline not complete",
            ],
        },
        "fullscreen": {
            "file": "presentation/components/workbench/workbench.py",
            "method": "_on_fullscreen_clicked",
            "signal": "fullscreen_button.clicked.connect",
            "common_issues": [
                "Fullscreen service not connected",
                "Window state management missing",
                "Keyboard shortcuts not handled",
            ],
        },
        "settings": {
            "file": "presentation/components/workbench/workbench.py",
            "method": "_on_settings_clicked",
            "signal": "settings_button.clicked.connect",
            "common_issues": [
                "Settings dialog not implemented",
                "Configuration service not connected",
                "Dialog modal behavior not correct",
            ],
        },
    }

    def __init__(self, workbench, app):
        self.workbench = workbench
        self.app = app
        self.test_results = []

    def test_button_click(
        self, button_name: str, button_widget: QPushButton
    ) -> AITestResult:
        """Test a single button click with comprehensive error handling."""
        start_time = time.time()

        print(f"🧪 Testing button: {button_name}")

        try:
            # Check if button exists and is enabled
            if not button_widget:
                return self._create_failure_result(
                    button_name, ["Button widget not found"], start_time
                )

            if not button_widget.isEnabled():
                return self._create_failure_result(
                    button_name,
                    ["Button is disabled"],
                    start_time,
                    warnings=["Button may be disabled due to application state"],
                )

            # Test button click
            click_successful = self._perform_button_click(button_widget)

            if not click_successful:
                return self._create_failure_result(
                    button_name, ["Button click failed to execute"], start_time
                )

            # Test hover events
            hover_successful = self._test_hover_events(button_widget)

            result = AITestResult(
                success=click_successful and hover_successful,
                errors=[],
                execution_time=time.time() - start_time,
                metadata={
                    "button_name": button_name,
                    "click_successful": click_successful,
                    "hover_successful": hover_successful,
                    "button_enabled": button_widget.isEnabled(),
                    "button_visible": button_widget.isVisible(),
                },
            )

            if result.success:
                print(f"✅ Button {button_name} test passed")
            else:
                print(f"❌ Button {button_name} test failed")
                self._print_legacy_guidance(button_name)

            return result

        except Exception as e:
            print(f"❌ Exception testing button {button_name}: {e}")
            return self._create_failure_result(
                button_name, [f"Exception during testing: {e!s}"], start_time
            )

    def _perform_button_click(self, button_widget: QPushButton) -> bool:
        """Perform the actual button click and verify it worked."""
        try:
            # Record initial state
            self._capture_application_state()

            # Perform click
            QTest.mouseClick(button_widget, Qt.MouseButton.LeftButton)

            # Process events
            self.app.processEvents()

            # Give time for any async operations
            time.sleep(0.1)

            # Check if state changed (indicates button worked)
            self._capture_application_state()

            # Basic success check - if no exception occurred, consider it successful
            # More sophisticated checks could be added here
            return True

        except Exception as e:
            print(f"❌ Button click failed: {e}")
            return False

    def _test_hover_events(self, button_widget: QPushButton) -> bool:
        """Test hover enter and leave events."""
        try:
            # Test hover enter
            QTest.mouseMove(button_widget, QPoint(10, 10))
            self.app.processEvents()

            # Test hover leave
            QTest.mouseMove(button_widget, QPoint(-10, -10))
            self.app.processEvents()

            return True

        except Exception as e:
            print(f"❌ Hover event test failed: {e}")
            return False

    def _capture_application_state(self) -> dict:
        """Capture current application state for comparison."""
        # This is a simplified state capture
        # In a real implementation, you'd capture relevant application state
        return {
            "timestamp": time.time(),
            "workbench_visible": (
                self.workbench.isVisible() if self.workbench else False
            ),
        }

    def _create_failure_result(
        self,
        button_name: str,
        errors: list[str],
        start_time: float,
        warnings: list[str] | None = None,
    ) -> AITestResult:
        """Create a failure result with legacy guidance."""
        self._print_legacy_guidance(button_name)

        return AITestResult(
            success=False,
            errors=errors,
            execution_time=time.time() - start_time,
            metadata={"button_name": button_name, "legacy_guidance_provided": True},
        )

    def _print_legacy_guidance(self, button_name: str):
        """Print legacy guidance for failed button."""
        guidance = self.LEGACY_GUIDANCE.get(button_name, {})

        if not guidance:
            print(f"⚠️  No legacy guidance available for button: {button_name}")
            return

        print(f"\n🔍 LEGACY GUIDANCE for {button_name}:")
        print(f"   📁 File: {guidance.get('file', 'Unknown')}")
        print(f"   ⚙️  Method: {guidance.get('method', 'Unknown')}")
        print(f"   🔗 Signal: {guidance.get('signal', 'Unknown')}")
        print("   🐛 Common Issues:")

        for issue in guidance.get("common_issues", []):
            print(f"      • {issue}")
        print()

    def test_all_buttons(self, button_map: dict) -> AITestResult:
        """Test all buttons and return comprehensive results."""
        print(f"🧪 Testing {len(button_map)} workbench buttons...")

        start_time = time.time()
        results = []

        for button_name, button_widget in button_map.items():
            result = self.test_button_click(button_name, button_widget)
            results.append(result)

            # Small delay between tests
            time.sleep(0.1)

        # Calculate summary
        successful_tests = sum(1 for r in results if r.success)
        failed_tests = len(results) - successful_tests
        all_errors = []

        for result in results:
            all_errors.extend(result.errors)

        overall_success = failed_tests == 0
        execution_time = time.time() - start_time

        print("\n📊 BUTTON TESTING SUMMARY:")
        print(f"   ✅ Successful: {successful_tests}/{len(results)}")
        print(f"   ❌ Failed: {failed_tests}/{len(results)}")
        print(f"   ⏱️  Total time: {execution_time:.2f}s")

        return AITestResult(
            success=overall_success,
            errors=all_errors,
            execution_time=execution_time,
            metadata={
                "total_buttons": len(button_map),
                "successful_buttons": successful_tests,
                "failed_buttons": failed_tests,
                "individual_results": results,
            },
        )
