#!/usr/bin/env python3
"""
COMPLETE USER WORKFLOW TEST: The exact sequence user described
MANDATORY: Test the exact workflow that reveals the picker transition bug

This test validates:
1. Start up the program
2. Select start position in start position picker
3. Select option in option picker
4. Click Clear Sequence button
5. Verify it correctly resets to start position picker
"""

import sys
import time
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core.application.application_factory import ApplicationFactory
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QPushButton

from application.services.sequence.sequence_persister import SequencePersister


class CompleteUserWorkflowTester:
    """Test the complete user workflow that reveals the bug"""

    def __init__(self):
        self.app = None
        self.container = None
        self.persistence_service = None
        self.construct_tab = None
        self.layout_manager = None
        self.workbench = None
        self.workflow_log = []

    def setup_fresh_environment(self) -> bool:
        """Setup a completely fresh environment"""
        print("🚀 [WORKFLOW] Setting up fresh environment...")

        try:
            # Create QApplication
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()

            # Clear any existing sequence to start fresh
            self.persistence_service = SequencePersister()
            self.persistence_service.clear_current_sequence()

            print("✅ [WORKFLOW] Fresh environment setup complete")
            return True

        except Exception as e:
            print(f"❌ [WORKFLOW] Setup failed: {e}")
            return False

    def startup_program(self) -> bool:
        """Step 1: Start up the program"""
        print("🔄 [WORKFLOW] Step 1: Starting up the program...")

        try:
            from presentation.tabs.construct.construct_tab_widget import (
                ConstructTabWidget,
            )

            # Create fresh container and construct tab
            self.container = ApplicationFactory.create_production_app()
            self.construct_tab = ConstructTabWidget(self.container)

            # Get references
            if hasattr(self.construct_tab, "layout_manager"):
                self.layout_manager = self.construct_tab.layout_manager
                if hasattr(self.layout_manager, "workbench"):
                    self.workbench = self.layout_manager.workbench

            # Show UI
            self.construct_tab.show()
            self.construct_tab.resize(1200, 800)

            # Wait for startup to complete
            QTest.qWait(3000)

            # Log initial state
            self.log_workflow_state("PROGRAM_STARTUP")

            print("✅ [WORKFLOW] Step 1: Program started up")
            return True

        except Exception as e:
            print(f"❌ [WORKFLOW] Step 1 failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def select_start_position(self) -> bool:
        """Step 2: Select start position in start position picker"""
        print("🎯 [WORKFLOW] Step 2: Selecting start position...")

        try:
            # Log state before selecting start position
            self.log_workflow_state("BEFORE_START_POSITION_SELECT")

            # Find start position picker and select alpha1
            if self.layout_manager and hasattr(
                self.layout_manager, "start_position_picker"
            ):
                start_pos_picker = self.layout_manager.start_position_picker

                # Try to find alpha1 option and click it
                if hasattr(start_pos_picker, "position_options"):
                    # Look for alpha1_alpha1 position option
                    alpha1_option = None
                    for option in start_pos_picker.position_options:
                        if (
                            hasattr(option, "position_key")
                            and option.position_key == "alpha1_alpha1"
                        ):
                            alpha1_option = option
                            break

                    if alpha1_option:
                        print("🖱️ [WORKFLOW] Clicking alpha1_alpha1 start position...")
                        QTest.mouseClick(alpha1_option, Qt.MouseButton.LeftButton)
                        QTest.qWait(1000)  # Wait for processing

                        self.log_workflow_state("AFTER_START_POSITION_SELECT")
                        print("✅ [WORKFLOW] Step 2: Start position selected")

                        # CRITICAL: Verify data integrity between selection and display
                        self.verify_start_position_data_integrity()

                        return True
                    else:
                        print("❌ [WORKFLOW] Could not find alpha1_alpha1 option")
                        available_keys = [
                            opt.position_key
                            for opt in start_pos_picker.position_options
                            if hasattr(opt, "position_key")
                        ]
                        print(
                            f"🔍 [WORKFLOW] Available position keys: {available_keys}"
                        )
                        return False
                else:
                    print("❌ [WORKFLOW] Start position picker has no position_options")
                    return False
            else:
                print("❌ [WORKFLOW] Could not find start position picker")
                return False

        except Exception as e:
            print(f"❌ [WORKFLOW] Step 2 failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def select_option_in_picker(self) -> bool:
        """Step 3: Select option in option picker"""
        print("⚙️ [WORKFLOW] Step 3: Selecting option in option picker...")

        try:
            # Log state before selecting option
            self.log_workflow_state("BEFORE_OPTION_SELECT")

            # Wait a moment for transition to option picker
            QTest.qWait(1000)

            # Find option picker and select an option
            if self.layout_manager and hasattr(self.layout_manager, "option_picker"):
                option_picker = self.layout_manager.option_picker

                # Try to access the orchestrator and pool manager
                if hasattr(option_picker, "orchestrator"):
                    orchestrator = option_picker.orchestrator

                    # Check if orchestrator has pool manager
                    if (
                        hasattr(orchestrator, "pool_manager")
                        and orchestrator.pool_manager
                    ):
                        pool_manager = orchestrator.pool_manager

                        # Get the first available pictograph frame from the pool
                        if hasattr(pool_manager, "get_pictograph_from_pool"):
                            first_frame = pool_manager.get_pictograph_from_pool(0)

                            if first_frame and hasattr(first_frame, "clicked"):
                                print(f"🖱️ [WORKFLOW] Clicking first option frame")
                                QTest.mouseClick(first_frame, Qt.MouseButton.LeftButton)
                                QTest.qWait(1000)  # Wait for processing

                                self.log_workflow_state("AFTER_OPTION_SELECT")
                                print("✅ [WORKFLOW] Step 3: Option selected")
                                return True
                            else:
                                print("❌ [WORKFLOW] No clickable frame found in pool")
                                return False
                        else:
                            print(
                                "❌ [WORKFLOW] Pool manager has no get_pictograph_from_pool method"
                            )
                            return False
                    else:
                        print("❌ [WORKFLOW] Orchestrator has no pool_manager")
                        return False
                else:
                    print("❌ [WORKFLOW] Option picker has no orchestrator")
                    return False
            else:
                print("❌ [WORKFLOW] Could not find option picker")
                return False

        except Exception as e:
            print(f"❌ [WORKFLOW] Step 3 failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def click_clear_sequence_button(self) -> bool:
        """Step 4: Click Clear Sequence button"""
        print("🧹 [WORKFLOW] Step 4: Clicking Clear Sequence button...")

        try:
            # Log state before clearing
            self.log_workflow_state("BEFORE_CLEAR_BUTTON")

            # Find and click clear sequence button
            clear_button = self.find_clear_sequence_button()
            if clear_button:
                print("🖱️ [WORKFLOW] Clicking Clear Sequence button...")
                QTest.mouseClick(clear_button, Qt.MouseButton.LeftButton)

                # Monitor transitions after clear
                intervals = [100, 250, 500, 1000, 2000]
                for interval in intervals:
                    QTest.qWait(interval)
                    self.log_workflow_state(f"AFTER_CLEAR_+{interval}ms")

                print("✅ [WORKFLOW] Step 4: Clear Sequence button clicked")
                return True
            else:
                print("❌ [WORKFLOW] Could not find Clear Sequence button")
                return False

        except Exception as e:
            print(f"❌ [WORKFLOW] Step 4 failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def find_clear_sequence_button(self) -> QPushButton:
        """Find the clear sequence button"""
        # Search through all widgets for clear sequence button
        for widget in self.app.allWidgets():
            if isinstance(widget, QPushButton):
                # Check tooltip
                if hasattr(widget, "toolTip") and "clear" in widget.toolTip().lower():
                    return widget
                # Check text
                if hasattr(widget, "text") and "clear" in widget.text().lower():
                    return widget
                # Check object name
                if (
                    hasattr(widget, "objectName")
                    and "clear" in widget.objectName().lower()
                ):
                    return widget
        return None

    def verify_start_position_data_integrity(self):
        """Verify that the selected start position data matches what's displayed."""
        try:
            print("🔍 [DATA_INTEGRITY] Verifying start position data integrity...")

            # Get the start position view from the beat frame
            if (
                self.layout_manager
                and hasattr(self.layout_manager, "beat_frame_section")
                and self.layout_manager.beat_frame_section
                and hasattr(self.layout_manager.beat_frame_section, "beat_frame")
                and self.layout_manager.beat_frame_section.beat_frame
                and hasattr(
                    self.layout_manager.beat_frame_section.beat_frame,
                    "start_position_view",
                )
            ):

                start_position_view = (
                    self.layout_manager.beat_frame_section.beat_frame.start_position_view
                )

                # Get the beat data that was set in the view
                beat_data = start_position_view.get_beat_data()

                if beat_data:
                    print(f"📊 [DATA_INTEGRITY] StartPositionView BeatData:")
                    print(f"   Letter: {beat_data.letter}")
                    print(f"   Beat Number: {beat_data.beat_number}")
                    print(f"   Duration: {beat_data.duration}")
                    if beat_data.pictograph_data.glyph_data:
                        print(
                            f"   Start Position: {beat_data.pictograph_data.glyph_data.start_position}"
                        )
                        print(
                            f"   End Position: {beat_data.pictograph_data.glyph_data.end_position}"
                        )
                    print(
                        f"   Is Start Position: {beat_data.metadata.get('is_start_position', False)}"
                    )

                    # Verify expected values
                    expected_letter = "α"
                    expected_start_pos = "alpha1_alpha1"
                    expected_beat_number = 0
                    expected_is_start = True

                    letter_match = beat_data.letter == expected_letter
                    beat_num_match = beat_data.beat_number == expected_beat_number
                    is_start_match = (
                        beat_data.metadata.get("is_start_position", False)
                        == expected_is_start
                    )

                    if beat_data.pictograph_data.glyph_data:
                        start_pos_match = (
                            beat_data.pictograph_data.glyph_data.start_position
                            == expected_start_pos
                        )
                    else:
                        start_pos_match = False
                        print("❌ [DATA_INTEGRITY] No glyph_data found in BeatData")

                    print(f"🔍 [DATA_INTEGRITY] Verification results:")
                    print(
                        f"   Letter match: {letter_match} (expected: {expected_letter}, actual: {beat_data.letter})"
                    )
                    print(
                        f"   Beat number match: {beat_num_match} (expected: {expected_beat_number}, actual: {beat_data.beat_number})"
                    )
                    print(
                        f"   Start position match: {start_pos_match} (expected: {expected_start_pos}, actual: {beat_data.pictograph_data.glyph_data.start_position if beat_data.pictograph_data.glyph_data else 'None'})"
                    )
                    print(
                        f"   Is start position match: {is_start_match} (expected: {expected_is_start}, actual: {beat_data.metadata.get('is_start_position', False)})"
                    )

                    # NEW: Also check separate PictographData if available
                    pictograph_data = start_position_view.get_pictograph_data()
                    if pictograph_data:
                        print(f"🎯 [DATA_INTEGRITY] Separate PictographData found!")
                        print(f"   Letter: {pictograph_data.letter}")
                        print(f"   Start Position: {pictograph_data.start_position}")
                        print(f"   End Position: {pictograph_data.end_position}")

                        pictograph_letter_match = (
                            pictograph_data.letter == expected_letter
                        )
                        pictograph_start_pos_match = (
                            pictograph_data.start_position == expected_start_pos
                        )

                        print(
                            f"🔍 [DATA_INTEGRITY] PictographData verification results:"
                        )
                        print(
                            f"   Letter match: {pictograph_letter_match} (expected: {expected_letter}, actual: {pictograph_data.letter})"
                        )
                        print(
                            f"   Start position match: {pictograph_start_pos_match} (expected: {expected_start_pos}, actual: {pictograph_data.start_position})"
                        )

                        if pictograph_letter_match and pictograph_start_pos_match:
                            print(
                                "✅ [DATA_INTEGRITY] Separate PictographData is correct!"
                            )
                        else:
                            print(
                                "❌ [DATA_INTEGRITY] Separate PictographData has issues!"
                            )
                    else:
                        print(
                            "⚠️ [DATA_INTEGRITY] No separate PictographData found - using legacy conversion mode"
                        )

                    if (
                        letter_match
                        and beat_num_match
                        and start_pos_match
                        and is_start_match
                    ):
                        print(
                            "✅ [DATA_INTEGRITY] All BeatData matches - StartPositionView should display correct data!"
                        )
                    else:
                        print(
                            "❌ [DATA_INTEGRITY] BeatData mismatch detected - StartPositionView may not be displaying the correct pictograph!"
                        )

                else:
                    print("❌ [DATA_INTEGRITY] No beat data found in StartPositionView")
            else:
                print("❌ [DATA_INTEGRITY] Could not access StartPositionView")

        except Exception as e:
            print(f"❌ [DATA_INTEGRITY] Error verifying data integrity: {e}")
            import traceback

            traceback.print_exc()

    def log_workflow_state(self, event: str):
        """Log the current workflow state"""
        picker_state = self.get_picker_state()
        sequence_state = self.get_sequence_state()
        timestamp = time.time()

        log_entry = {
            "timestamp": timestamp,
            "event": event,
            "picker_state": picker_state,
            "sequence_state": sequence_state,
        }

        self.workflow_log.append(log_entry)
        print(f"🔍 [STATE] {event}: picker={picker_state}, sequence={sequence_state}")

    def get_picker_state(self) -> str:
        """Get the current picker state"""
        if not self.layout_manager or not hasattr(self.layout_manager, "picker_stack"):
            return "no_picker_stack"

        picker_stack = self.layout_manager.picker_stack
        if not picker_stack:
            return "no_picker_stack_widget"

        current_index = picker_stack.currentIndex()
        widget_count = picker_stack.count()

        # Determine picker type
        if current_index == 0:
            return f"START_POSITION_PICKER(index_0_of_{widget_count})"
        elif current_index == 1:
            return f"OPTION_PICKER(index_1_of_{widget_count})"
        else:
            return f"UNKNOWN_PICKER(index_{current_index}_of_{widget_count})"

    def get_sequence_state(self) -> str:
        """Get the current sequence state"""
        try:
            sequence = self.persistence_service.load_current_sequence()
            return f"{len(sequence)}_items"
        except:
            return "unknown"

    def analyze_workflow_results(self):
        """Analyze the complete workflow results"""
        print("\n📊 [ANALYSIS] Complete User Workflow Analysis")
        print("=" * 70)

        if not self.workflow_log:
            print("❌ No workflow log data")
            return

        # Print detailed log
        for i, entry in enumerate(self.workflow_log):
            event = entry["event"]
            picker_state = entry["picker_state"]
            sequence_state = entry["sequence_state"]
            print(
                f"{i+1:2d}. {event:25s} → picker: {picker_state:30s} sequence: {sequence_state}"
            )

        # Critical analysis
        print("\n🔍 [ANALYSIS] Critical Workflow Analysis:")

        # Check if we start with start position picker
        startup_entry = next(
            (e for e in self.workflow_log if "STARTUP" in e["event"]), None
        )
        if startup_entry:
            if "START_POSITION_PICKER" in startup_entry["picker_state"]:
                print("✅ Program starts with start position picker")
            else:
                print(
                    f"❌ Program starts with wrong picker: {startup_entry['picker_state']}"
                )

        # Check transition to option picker after start position
        after_start_pos = next(
            (
                e
                for e in self.workflow_log
                if "AFTER_START_POSITION_SELECT" in e["event"]
            ),
            None,
        )
        if after_start_pos:
            if "OPTION_PICKER" in after_start_pos["picker_state"]:
                print(
                    "✅ Correctly transitions to option picker after start position selection"
                )
            else:
                print(
                    f"❌ Wrong picker after start position: {after_start_pos['picker_state']}"
                )

        # Check final state after clear
        final_entries = [e for e in self.workflow_log if "AFTER_CLEAR" in e["event"]]
        if final_entries:
            final_entry = final_entries[-1]  # Last entry
            if "START_POSITION_PICKER" in final_entry["picker_state"]:
                print("✅ CORRECT: Final state shows start position picker after clear")
            elif "OPTION_PICKER" in final_entry["picker_state"]:
                print(
                    "❌ BUG FOUND: Final state shows option picker after clear - THIS IS THE PROBLEM!"
                )
            else:
                print(f"❓ Unclear final state: {final_entry['picker_state']}")

        # Check for unwanted transitions
        picker_states = [entry["picker_state"] for entry in self.workflow_log]
        transitions = []
        for i in range(1, len(picker_states)):
            if picker_states[i] != picker_states[i - 1]:
                transitions.append(
                    (
                        self.workflow_log[i - 1]["event"],
                        self.workflow_log[i]["event"],
                        picker_states[i - 1],
                        picker_states[i],
                    )
                )

        if transitions:
            print(f"\n🔄 Found {len(transitions)} picker transitions:")
            for from_event, to_event, from_state, to_state in transitions:
                print(f"   {from_event} → {to_event}")
                print(f"   {from_state} → {to_state}")

    def run_complete_workflow_test(self) -> bool:
        """Run the complete user workflow test"""
        print("🚀 COMPLETE USER WORKFLOW TEST")
        print("=" * 50)
        print("Testing the exact sequence that reveals the bug:")
        print("1. Start up program")
        print("2. Select start position")
        print("3. Select option")
        print("4. Click Clear Sequence")
        print("5. Verify correct picker state")
        print("=" * 50)

        test_steps = [
            ("Setup Fresh Environment", self.setup_fresh_environment),
            ("Step 1: Startup Program", self.startup_program),
            ("Step 2: Select Start Position", self.select_start_position),
            ("Step 3: Select Option", self.select_option_in_picker),
            ("Step 4: Click Clear Sequence", self.click_clear_sequence_button),
        ]

        for step_name, step_func in test_steps:
            print(f"\n🧪 {step_name}")
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
                return False

        # Analyze results
        self.analyze_workflow_results()

        return True


def main():
    """Main test execution"""
    tester = CompleteUserWorkflowTester()
    success = tester.run_complete_workflow_test()

    if success:
        print("\n🎉 COMPLETE WORKFLOW TEST COMPLETED")
        print("✅ Check analysis above for the exact bug location")
        return 0
    else:
        print("\n❌ COMPLETE WORKFLOW TEST FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
