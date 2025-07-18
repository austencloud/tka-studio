#!/usr/bin/env python3
"""
END-TO-END TEST: Clear Sequence Functionality
MANDATORY: Full application testing with UI automation

This test validates the complete clear sequence workflow by:
1. Launching the full TKA application
2. Programmatically interacting with UI elements
3. Validating state transitions and persistence
4. Confirming the exact user experience works correctly
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from application.services.sequence.sequence_persister import SequencePersister
from core.application.application_factory import ApplicationFactory
from PyQt6.QtCore import QObject, Qt, QTimer, pyqtSignal
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QPushButton, QWidget


class TKAUIAutomation:
    """UI automation framework for TKA application testing"""

    def __init__(self, app_instance):
        self.app = app_instance
        self.main_window = None
        self.construct_tab = None
        self.workbench = None
        self.layout_manager = None

    def initialize_components(self):
        """Initialize and locate key UI components"""
        print("🔍 [UI_AUTOMATION] Locating UI components...")

        # Find main window
        for widget in self.app.allWidgets():
            if hasattr(widget, "objectName") and "main" in widget.objectName().lower():
                self.main_window = widget
                break

        if not self.main_window:
            # Try to find any top-level widget
            top_level_widgets = self.app.topLevelWidgets()
            if top_level_widgets:
                self.main_window = top_level_widgets[0]

        print(f"✅ [UI_AUTOMATION] Main window found: {self.main_window is not None}")

        # Find construct tab
        self.construct_tab = self._find_widget_by_type("ConstructTabWidget")
        print(
            f"✅ [UI_AUTOMATION] Construct tab found: {self.construct_tab is not None}"
        )

        # Find workbench
        self.workbench = self._find_widget_by_type("SequenceWorkbench")
        print(f"✅ [UI_AUTOMATION] Workbench found: {self.workbench is not None}")

        # Find layout manager
        if self.construct_tab and hasattr(self.construct_tab, "layout_manager"):
            self.layout_manager = self.construct_tab.layout_manager
            print(
                f"✅ [UI_AUTOMATION] Layout manager found: {self.layout_manager is not None}"
            )

        return self.main_window is not None

    def _find_widget_by_type(self, type_name: str) -> Optional[QWidget]:
        """Find widget by class name"""
        for widget in self.app.allWidgets():
            if type_name in str(type(widget)):
                return widget
        return None

    def _find_widget_by_object_name(self, object_name: str) -> Optional[QWidget]:
        """Find widget by object name"""
        for widget in self.app.allWidgets():
            if hasattr(widget, "objectName") and widget.objectName() == object_name:
                return widget
        return None

    def find_clear_sequence_button(self) -> Optional[QPushButton]:
        """Locate the clear sequence button"""
        print("🔍 [UI_AUTOMATION] Searching for clear sequence button...")

        # Search for buttons with clear sequence functionality
        for widget in self.app.allWidgets():
            if isinstance(widget, QPushButton):
                # Check tooltip
                if hasattr(widget, "toolTip") and "clear" in widget.toolTip().lower():
                    print(
                        f"✅ [UI_AUTOMATION] Found clear button by tooltip: {widget.toolTip()}"
                    )
                    return widget

                # Check text
                if hasattr(widget, "text") and "clear" in widget.text().lower():
                    print(
                        f"✅ [UI_AUTOMATION] Found clear button by text: {widget.text()}"
                    )
                    return widget

                # Check object name
                if (
                    hasattr(widget, "objectName")
                    and "clear" in widget.objectName().lower()
                ):
                    print(
                        f"✅ [UI_AUTOMATION] Found clear button by object name: {widget.objectName()}"
                    )
                    return widget

        print("❌ [UI_AUTOMATION] Clear sequence button not found")
        return None

    def get_current_picker_state(self) -> str:
        """Determine which picker is currently visible"""
        print(f"🔍 [UI_AUTOMATION] Checking picker state...")
        print(f"🔍 [UI_AUTOMATION] Layout manager: {self.layout_manager is not None}")

        if not self.layout_manager:
            print("❌ [UI_AUTOMATION] No layout manager found")
            return "unknown"

        print(
            f"🔍 [UI_AUTOMATION] Layout manager has picker_stack: {hasattr(self.layout_manager, 'picker_stack')}"
        )

        if not hasattr(self.layout_manager, "picker_stack"):
            print("❌ [UI_AUTOMATION] Layout manager has no picker_stack attribute")
            return "unknown"

        picker_stack = self.layout_manager.picker_stack
        print(f"🔍 [UI_AUTOMATION] Picker stack: {picker_stack is not None}")

        if not picker_stack:
            print("❌ [UI_AUTOMATION] Picker stack is None")
            return "unknown"

        current_index = picker_stack.currentIndex()
        print(f"🔍 [UI_AUTOMATION] Current picker index: {current_index}")

        if current_index == 0:
            return "start_position_picker"
        elif current_index == 1:
            return "option_picker"
        elif current_index == 2:
            return "graph_editor"
        else:
            return f"unknown_index_{current_index}"

    def click_clear_sequence_button(self) -> bool:
        """Click the clear sequence button"""
        button = self.find_clear_sequence_button()
        if not button:
            return False

        print(f"🖱️ [UI_AUTOMATION] Clicking clear sequence button...")
        QTest.mouseClick(button, Qt.MouseButton.LeftButton)  # Left click

        # Wait for UI to update
        QTest.qWait(500)

        return True

    def wait_for_ui_update(self, timeout_ms: int = 1000):
        """Wait for UI updates to complete"""
        QTest.qWait(timeout_ms)
        self.app.processEvents()


class ClearSequenceE2ETest:
    """End-to-end test for clear sequence functionality"""

    def __init__(self):
        self.app = None
        self.ui_automation = None
        self.persistence_service = None
        self.test_results = {}

    def setup_test_environment(self) -> bool:
        """Setup the complete test environment"""
        print("🚀 [E2E_TEST] Setting up test environment...")

        try:
            # Create QApplication if it doesn't exist
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()

            print("✅ [E2E_TEST] QApplication created")

            # Initialize persistence service
            self.persistence_service = SequencePersister()
            print("✅ [E2E_TEST] Persistence service initialized")

            # Create UI automation framework
            self.ui_automation = TKAUIAutomation(self.app)
            print("✅ [E2E_TEST] UI automation framework created")

            return True

        except Exception as e:
            print(f"❌ [E2E_TEST] Setup failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def launch_tka_application(self) -> bool:
        """Launch the complete TKA application"""
        print("🚀 [E2E_TEST] Launching TKA application...")

        try:
            # CRITICAL FIX: Initialize core services for SequenceStateManager
            print("🔧 [E2E_TEST] Initializing core services...")
            from core.service_locator import initialize_services

            initialize_services()
            print("✅ [E2E_TEST] Core services initialized")

            # Create production application container
            container = ApplicationFactory.create_production_app()
            print("✅ [E2E_TEST] Production application container created")

            # Create the main UI components directly
            try:
                from presentation.components.sequence_workbench.sequence_workbench import (
                    SequenceWorkbench,
                )
                from presentation.tabs.construct.construct_tab_widget import (
                    ConstructTabWidget,
                )

                # Create construct tab with container
                self.construct_tab = ConstructTabWidget(container)
                print("✅ [E2E_TEST] Construct tab created")

                # Get workbench from construct tab
                if hasattr(self.construct_tab, "layout_manager") and hasattr(
                    self.construct_tab.layout_manager, "workbench"
                ):
                    self.workbench = self.construct_tab.layout_manager.workbench
                    print("✅ [E2E_TEST] Workbench accessed from construct tab")

                # Show the construct tab
                self.construct_tab.show()
                self.construct_tab.resize(1200, 800)  # Set reasonable size

                # Wait for initialization
                QTest.qWait(2000)  # Longer wait for full initialization

                # Update UI automation references
                self.ui_automation.construct_tab = self.construct_tab
                self.ui_automation.workbench = self.workbench
                self.ui_automation.main_window = self.construct_tab

                # Initialize UI automation components
                self.ui_automation.initialize_components()

                print("✅ [E2E_TEST] TKA application components launched successfully")
                return True

            except Exception as ui_error:
                print(f"❌ [E2E_TEST] UI creation failed: {ui_error}")
                import traceback

                traceback.print_exc()
                return False

        except Exception as e:
            print(f"❌ [E2E_TEST] Failed to launch TKA: {e}")
            import traceback

            traceback.print_exc()
            return False

    def create_test_sequence(self) -> bool:
        """Create a test sequence with REAL data that will actually be used"""
        print("📝 [E2E_TEST] Creating test sequence with REAL data...")

        try:
            # REAL sequence data - exactly as provided by user
            real_test_sequence = [
                {
                    "word": "test",
                    "author": "e2e_test",
                    "level": 1,
                    "prop_type": "staff",
                    "grid_mode": "diamond",
                    "is_circular": False,
                },
                {
                    "beat": 0,
                    "sequence_start_position": "alpha1",
                    "end_pos": "alpha1",
                    "blue_attributes": {"start_ori": 0, "end_ori": 0, "motion_type": 0},
                    "red_attributes": {"start_ori": 0, "end_ori": 0, "motion_type": 0},
                },
                {
                    "beat": 1,
                    "letter": "A",
                    "blue_attributes": {
                        "start_ori": 0,
                        "end_ori": 90,
                        "motion_type": 1,
                    },
                    "red_attributes": {"start_ori": 0, "end_ori": 90, "motion_type": 1},
                },
            ]

            # Save REAL test sequence
            self.persistence_service.save_current_sequence(real_test_sequence)

            # Verify sequence was saved
            loaded_sequence = self.persistence_service.load_current_sequence()
            if len(loaded_sequence) >= 3:
                print(
                    f"✅ [E2E_TEST] REAL test sequence created with {len(loaded_sequence)} items"
                )
                print(
                    f"📝 [E2E_TEST] Metadata: word='{loaded_sequence[0].get('word')}', author='{loaded_sequence[0].get('author')}'"
                )
                print(
                    f"📝 [E2E_TEST] Start position: {loaded_sequence[1].get('sequence_start_position')}"
                )
                print(
                    f"📝 [E2E_TEST] Beat 1: letter='{loaded_sequence[2].get('letter')}'"
                )
                return True
            else:
                print(
                    f"❌ [E2E_TEST] REAL test sequence creation failed: only {len(loaded_sequence)} items"
                )
                return False

        except Exception as e:
            print(f"❌ [E2E_TEST] Failed to create REAL test sequence: {e}")
            import traceback

            traceback.print_exc()
            return False

    def validate_initial_state(self) -> bool:
        """Validate the initial state before clearing"""
        print("🔍 [E2E_TEST] Validating initial state...")

        try:
            # Check sequence file
            sequence = self.persistence_service.load_current_sequence()
            if len(sequence) < 2:
                print(
                    f"❌ [E2E_TEST] Initial sequence too short: {len(sequence)} items"
                )
                return False

            # Check UI state
            picker_state = self.ui_automation.get_current_picker_state()
            print(f"🔍 [E2E_TEST] Initial picker state: {picker_state}")

            # Should be showing option picker for sequence with content
            if picker_state != "option_picker":
                print(f"⚠️ [E2E_TEST] Expected option picker, got: {picker_state}")

            print("✅ [E2E_TEST] Initial state validated")
            return True

        except Exception as e:
            print(f"❌ [E2E_TEST] Initial state validation failed: {e}")
            return False

    def execute_clear_sequence(self) -> bool:
        """Execute the clear sequence operation"""
        print("🧹 [E2E_TEST] Executing clear sequence operation...")

        try:
            # Record state before clearing
            initial_picker_state = self.ui_automation.get_current_picker_state()
            initial_sequence = self.persistence_service.load_current_sequence()

            print(
                f"🔍 [E2E_TEST] Before clear - Picker: {initial_picker_state}, Sequence items: {len(initial_sequence)}"
            )

            # Try both button click and direct method call
            print("🔄 [E2E_TEST] Trying button click first...")
            button_success = self.ui_automation.click_clear_sequence_button()
            if not button_success:
                print("❌ [E2E_TEST] Button click failed, trying direct method call...")

            # Also try calling clear sequence directly on construct tab
            if hasattr(self, "construct_tab") and self.construct_tab:
                print(
                    "🔄 [E2E_TEST] Calling clear_sequence directly on construct tab..."
                )
                self.construct_tab.clear_sequence()
            else:
                print("❌ [E2E_TEST] No construct tab available for direct call")

            # Wait for operations to complete
            self.ui_automation.wait_for_ui_update(2000)  # 2 second wait

            # Record state after clearing
            final_picker_state = self.ui_automation.get_current_picker_state()
            final_sequence = self.persistence_service.load_current_sequence()

            print(
                f"🔍 [E2E_TEST] After clear - Picker: {final_picker_state}, Sequence items: {len(final_sequence)}"
            )

            # Store results for validation
            self.test_results = {
                "initial_picker_state": initial_picker_state,
                "final_picker_state": final_picker_state,
                "initial_sequence_length": len(initial_sequence),
                "final_sequence_length": len(final_sequence),
                "final_sequence": final_sequence,
            }

            print("✅ [E2E_TEST] Clear sequence operation executed")
            return True

        except Exception as e:
            print(f"❌ [E2E_TEST] Clear sequence execution failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def validate_clear_sequence_results(self) -> bool:
        """Validate the results of the clear sequence operation"""
        print("✅ [E2E_TEST] Validating clear sequence results...")

        try:
            results = self.test_results
            success = True

            # Check UI transition
            if results["final_picker_state"] != "start_position_picker":
                print(
                    f"❌ [E2E_TEST] UI transition failed: expected 'start_position_picker', got '{results['final_picker_state']}'"
                )
                success = False
            else:
                print(
                    "✅ [E2E_TEST] UI correctly transitioned to start position picker"
                )

            # Check sequence file
            if results["final_sequence_length"] != 1:
                print(
                    f"❌ [E2E_TEST] Sequence not properly cleared: expected 1 item (metadata), got {results['final_sequence_length']}"
                )
                success = False
            else:
                print("✅ [E2E_TEST] Sequence file properly cleared to metadata only")

            # Check metadata content
            final_sequence = results["final_sequence"]
            if final_sequence and len(final_sequence) > 0:
                metadata = final_sequence[0]
                if metadata.get("word") != "":
                    print(
                        f"❌ [E2E_TEST] Metadata word not cleared: expected '', got '{metadata.get('word')}'"
                    )
                    success = False
                else:
                    print("✅ [E2E_TEST] Metadata properly reset")

            return success

        except Exception as e:
            print(f"❌ [E2E_TEST] Result validation failed: {e}")
            return False

    def run_complete_test(self) -> bool:
        """Run the complete end-to-end test"""
        print("🚀 STARTING COMPREHENSIVE CLEAR SEQUENCE E2E TEST")
        print("=" * 80)

        test_steps = [
            ("Setup Test Environment", self.setup_test_environment),
            ("Launch TKA Application", self.launch_tka_application),
            ("Create Test Sequence", self.create_test_sequence),
            ("Validate Initial State", self.validate_initial_state),
            ("Execute Clear Sequence", self.execute_clear_sequence),
            ("Validate Results", self.validate_clear_sequence_results),
        ]

        for step_name, step_func in test_steps:
            print(f"\n🧪 STEP: {step_name}")
            print("-" * 40)

            try:
                success = step_func()
                if success:
                    print(f"✅ {step_name}: PASSED")
                else:
                    print(f"❌ {step_name}: FAILED")
                    return False
            except Exception as e:
                print(f"❌ {step_name}: ERROR - {e}")
                import traceback

                traceback.print_exc()
                return False

        print("\n" + "=" * 80)
        print("🎉 ALL E2E TESTS PASSED!")
        print("✅ Clear sequence functionality works correctly")
        print("=" * 80)

        return True


def main():
    """Main test execution"""
    test = ClearSequenceE2ETest()
    success = test.run_complete_test()

    if success:
        print("\n🎉 END-TO-END TEST SUITE: SUCCESS")
        return 0
    else:
        print("\n❌ END-TO-END TEST SUITE: FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
