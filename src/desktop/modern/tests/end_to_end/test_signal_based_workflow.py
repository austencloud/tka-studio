#!/usr/bin/env python3
"""
SIGNAL-BASED WORKFLOW TEST: Test the exact user workflow using TKA signals
MANDATORY: Test the complete workflow using proper TKA signal patterns

This test validates:
1. Start up program (start position picker shown)
2. Select start position (triggers transition to option picker)
3. Select option (adds beat to sequence)
4. Click Clear Sequence (should return to start position picker)
5. Verify final state is start position picker
"""

import sys
import time
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from PyQt6.QtTest import QTest

from core.application.application_factory import ApplicationFactory
from application.services.core.sequence_persistence_service import (
    SequencePersistenceService,
)


class SignalBasedWorkflowTester:
    """Test the complete workflow using TKA signal patterns"""

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
        print("🚀 [SIGNAL_TEST] Setting up fresh environment...")

        try:
            # Create QApplication
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()

            # Clear any existing sequence to start fresh
            self.persistence_service = SequencePersistenceService()
            self.persistence_service.clear_current_sequence()

            print("✅ [SIGNAL_TEST] Fresh environment setup complete")
            return True

        except Exception as e:
            print(f"❌ [SIGNAL_TEST] Setup failed: {e}")
            return False

    def startup_program(self) -> bool:
        """Step 1: Start up the program"""
        print("🔄 [SIGNAL_TEST] Step 1: Starting up the program...")

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

            print("✅ [SIGNAL_TEST] Step 1: Program started up")
            return True

        except Exception as e:
            print(f"❌ [SIGNAL_TEST] Step 1 failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def select_start_position_via_signal(self) -> bool:
        """Step 2: Select start position using signal approach"""
        print("🎯 [SIGNAL_TEST] Step 2: Selecting start position via signal...")

        try:
            # Log state before selecting start position
            self.log_workflow_state("BEFORE_START_POSITION_SELECT")

            # Use the start position picker to emit a signal
            if self.layout_manager and hasattr(
                self.layout_manager, "start_position_picker"
            ):
                start_pos_picker = self.layout_manager.start_position_picker

                # Simulate selecting alpha1 start position by emitting the signal
                print(
                    "🎯 [SIGNAL_TEST] Emitting start position selected signal for alpha1..."
                )
                start_pos_picker.start_position_selected.emit("alpha1_alpha1")

                # Wait for processing
                QTest.qWait(1000)

                self.log_workflow_state("AFTER_START_POSITION_SELECT")
                print("✅ [SIGNAL_TEST] Step 2: Start position selected via signal")
                return True
            else:
                print("❌ [SIGNAL_TEST] Could not find start position picker")
                return False

        except Exception as e:
            print(f"❌ [SIGNAL_TEST] Step 2 failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def select_option_via_workbench(self) -> bool:
        """Step 3: Select option by adding beat to workbench"""
        print("⚙️ [SIGNAL_TEST] Step 3: Selecting option via workbench...")

        try:
            # Log state before selecting option
            self.log_workflow_state("BEFORE_OPTION_SELECT")

            # Wait for transition to option picker
            QTest.qWait(1000)

            # Use option picker to emit beat selection signal
            if (
                self.layout_manager
                and hasattr(self.layout_manager, "option_picker")
                and self.layout_manager.option_picker
            ):
                option_picker = self.layout_manager.option_picker

                # Create a simple beat data to simulate option selection
                from domain.models.core_models import BeatData

                beat = BeatData(beat_number=1, letter="A", duration=1.0)

                print("⚙️ [SIGNAL_TEST] Emitting beat data selected signal...")
                # Check if option picker has the signal we need
                if hasattr(option_picker, "beat_data_selected"):
                    option_picker.beat_data_selected.emit(beat)
                elif hasattr(option_picker, "option_selected"):
                    option_picker.option_selected.emit(beat)
                else:
                    print("⚙️ [SIGNAL_TEST] Using workbench add_beat as fallback...")
                    if self.workbench and hasattr(self.workbench, "add_beat"):
                        self.workbench.add_beat(beat)
                    else:
                        print("❌ [SIGNAL_TEST] No suitable method to add beat")
                        return False

                # Wait for processing
                QTest.qWait(1000)

                self.log_workflow_state("AFTER_OPTION_SELECT")
                print("✅ [SIGNAL_TEST] Step 3: Option selected")
                return True
            else:
                print("❌ [SIGNAL_TEST] Could not find option picker")
                return False

        except Exception as e:
            print(f"❌ [SIGNAL_TEST] Step 3 failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def clear_sequence_via_construct_tab(self) -> bool:
        """Step 4: Clear sequence using construct tab method"""
        print("🧹 [SIGNAL_TEST] Step 4: Clearing sequence via construct tab...")

        try:
            # Log state before clearing
            self.log_workflow_state("BEFORE_CLEAR_SEQUENCE")

            # Use construct tab clear sequence method
            if self.construct_tab and hasattr(self.construct_tab, "clear_sequence"):
                print("🧹 [SIGNAL_TEST] Calling construct tab clear_sequence()...")
                self.construct_tab.clear_sequence()

                # Monitor transitions after clear with detailed timing
                intervals = [100, 250, 500, 1000, 2000, 3000]
                for interval in intervals:
                    QTest.qWait(interval)
                    self.log_workflow_state(f"AFTER_CLEAR_+{interval}ms")

                print("✅ [SIGNAL_TEST] Step 4: Clear sequence completed")
                return True
            else:
                print("❌ [SIGNAL_TEST] Could not find clear_sequence method")
                return False

        except Exception as e:
            print(f"❌ [SIGNAL_TEST] Step 4 failed: {e}")
            import traceback

            traceback.print_exc()
            return False

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

    def analyze_signal_workflow_results(self):
        """Analyze the complete signal-based workflow results"""
        print("\n📊 [ANALYSIS] Signal-Based Workflow Analysis")
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
                f"{i+1:2d}. {event:30s} → picker: {picker_state:35s} sequence: {sequence_state}"
            )

        # Critical analysis
        print("\n🔍 [ANALYSIS] Critical Signal Workflow Analysis:")

        # Check startup state
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

        # Check final state after clear - THIS IS THE KEY TEST
        final_entries = [e for e in self.workflow_log if "AFTER_CLEAR" in e["event"]]
        if final_entries:
            final_entry = final_entries[-1]  # Last entry
            if "START_POSITION_PICKER" in final_entry["picker_state"]:
                print("✅ CORRECT: Final state shows start position picker after clear")
            elif "OPTION_PICKER" in final_entry["picker_state"]:
                print(
                    "❌ BUG CONFIRMED: Final state shows option picker after clear - THIS IS THE PROBLEM!"
                )
            else:
                print(f"❓ Unclear final state: {final_entry['picker_state']}")

        # Check for unwanted transitions during clear
        clear_entries = [e for e in self.workflow_log if "AFTER_CLEAR" in e["event"]]
        if len(clear_entries) > 1:
            print(
                f"\n🔄 Clear sequence transition analysis ({len(clear_entries)} snapshots):"
            )
            for entry in clear_entries:
                event = entry["event"]
                picker_state = entry["picker_state"]
                print(f"   {event}: {picker_state}")

            # Check if there are any unwanted transitions
            picker_states = [entry["picker_state"] for entry in clear_entries]
            unique_states = list(dict.fromkeys(picker_states))

            if len(unique_states) == 1:
                print("✅ Picker state remained consistent during clear")
            else:
                print("❌ Picker state changed during clear - TRANSITION BUG DETECTED!")
                for i, state in enumerate(unique_states):
                    print(f"   State {i+1}: {state}")

    def run_signal_workflow_test(self) -> bool:
        """Run the complete signal-based workflow test"""
        print("🚀 SIGNAL-BASED WORKFLOW TEST")
        print("=" * 50)
        print("Testing the exact user workflow using TKA signals:")
        print("1. Start up program")
        print("2. Select start position (via signal)")
        print("3. Select option (via workbench)")
        print("4. Clear sequence (via construct tab)")
        print("5. Verify picker state transitions")
        print("=" * 50)

        test_steps = [
            ("Setup Fresh Environment", self.setup_fresh_environment),
            ("Step 1: Startup Program", self.startup_program),
            ("Step 2: Select Start Position", self.select_start_position_via_signal),
            ("Step 3: Select Option", self.select_option_via_workbench),
            ("Step 4: Clear Sequence", self.clear_sequence_via_construct_tab),
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
        self.analyze_signal_workflow_results()

        return True


def main():
    """Main test execution"""
    tester = SignalBasedWorkflowTester()
    success = tester.run_signal_workflow_test()

    if success:
        print("\n🎉 SIGNAL-BASED WORKFLOW TEST COMPLETED")
        print("✅ Check analysis above for the exact bug location")
        return 0
    else:
        print("\n❌ SIGNAL-BASED WORKFLOW TEST FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
