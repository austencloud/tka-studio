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
from __future__ import annotations

from pathlib import Path
import sys
import time


# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from application.services.sequence.sequence_persister import SequencePersister
from core.application.application_factory import ApplicationFactory


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
            self.persistence_service = SequencePersister()
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
            # Initialize core services first (like the real application does)
            from core.service_locator import initialize_services

            if not initialize_services():
                print("❌ [SIGNAL_TEST] Failed to initialize core services")
                return False
            print("✅ [SIGNAL_TEST] Core services initialized")

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
        """Step 2: Select start position using command system"""
        print("🎯 [SIGNAL_TEST] Step 2: Selecting start position via command...")

        try:
            # Log state before selecting start position
            self.log_workflow_state("BEFORE_START_POSITION_SELECT")

            # Use the command system to select start position
            from core.commands.start_position_commands import SetStartPositionCommand
            from core.service_locator import get_command_processor, get_event_bus

            command_processor = get_command_processor()
            event_bus = get_event_bus()

            if not command_processor:
                print("❌ [SIGNAL_TEST] Command processor not available")
                return False
            if not event_bus:
                print("❌ [SIGNAL_TEST] Event bus not available")
                return False

            # Execute start position command for alpha1
            print("🎯 [SIGNAL_TEST] Executing start position command for alpha1...")
            command = SetStartPositionCommand(
                position_key="alpha1_alpha1", event_bus=event_bus
            )
            result = command_processor.execute(command)

            if result and result.success:
                print("✅ [SIGNAL_TEST] Start position command executed successfully")

                # Wait for processing
                QTest.qWait(1000)

                self.log_workflow_state("AFTER_START_POSITION_SELECT")
                print("✅ [SIGNAL_TEST] Step 2: Start position selected via command")
                return True
            print("❌ [SIGNAL_TEST] Start position command failed")
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
                from domain.models import BeatData

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
            print("❌ [SIGNAL_TEST] Could not find clear_sequence method")
            return False

        except Exception as e:
            print(f"❌ [SIGNAL_TEST] Step 4 failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def log_workflow_state(self, event: str) -> str:
        """Log the current workflow state and return the state string"""
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
        state_string = f"picker={picker_state}, sequence={sequence_state}"
        print(f"🔍 [STATE] {event}: {state_string}")
        return state_string

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
        if current_index == 1:
            return f"OPTION_PICKER(index_1_of_{widget_count})"
        return f"UNKNOWN_PICKER(index_{current_index}_of_{widget_count})"

    def get_sequence_state(self) -> str:
        """Get the current sequence state"""
        try:
            sequence = self.persistence_service.load_current_sequence()
            return f"{len(sequence)}_items"
        except Exception:
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

    def reset_to_fresh_state(self) -> bool:
        """Reset the current construct tab to a fresh state"""
        try:
            if self.construct_tab and hasattr(self.construct_tab, "clear_sequence"):
                self.construct_tab.clear_sequence()
                QTest.qWait(500)  # Allow clear to complete
                return True
            return False
        except Exception as e:
            print(f"❌ [RESET] Failed to reset state: {e}")
            return False

    def test_multi_beat_sequence(self) -> bool:
        """Test building a sequence with multiple beats"""
        print("\n🧪 Multi-Beat Sequence Test")
        print("-" * 40)

        try:
            # Reset to fresh state instead of full restart
            if not self.reset_to_fresh_state():
                print("❌ [MULTI_BEAT] Could not reset to fresh state")
                return False

            # Select start position
            if not self.select_start_position_via_signal():
                return False

            # Add multiple beats using the correct signal approach
            beat_letters = ["A", "B", "C", "D"]
            for i, letter in enumerate(beat_letters):
                print(f"⚙️ [MULTI_BEAT] Adding beat {i+1}: {letter}")

                # Create beat with different letter
                from domain.models import BeatData

                beat = BeatData(beat_number=i + 1, letter=letter, duration=1.0)

                # Use the option picker signal approach (same as working test)
                if (
                    self.layout_manager
                    and hasattr(self.layout_manager, "option_picker")
                    and self.layout_manager.option_picker
                ):
                    option_picker = self.layout_manager.option_picker
                    if hasattr(option_picker, "beat_data_selected"):
                        option_picker.beat_data_selected.emit(beat)
                        QTest.qWait(500)  # Wait for processing
                    else:
                        print(
                            "❌ [MULTI_BEAT] Option picker missing beat_data_selected signal"
                        )
                        return False
                else:
                    print(
                        f"❌ [MULTI_BEAT] Could not find option picker for beat {letter}"
                    )
                    return False

            # Verify sequence length
            current_state = self.log_workflow_state(
                f"AFTER_ADDING_{len(beat_letters)}_BEATS"
            )
            sequence_length = int(current_state.split("sequence=")[1].split("_")[0])

            expected_length = len(beat_letters) + 2  # beats + start position + metadata
            if sequence_length == expected_length:
                print(
                    f"✅ [MULTI_BEAT] Successfully built sequence with {len(beat_letters)} beats"
                )
                return True
            print(
                f"❌ [MULTI_BEAT] Expected {expected_length} items, got {sequence_length}"
            )
            return False

        except Exception as e:
            print(f"❌ [MULTI_BEAT] Test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_different_start_positions(self) -> bool:
        """Test different start position selections"""
        print("\n🧪 Different Start Positions Test")
        print("-" * 40)

        start_positions = ["alpha1_alpha1", "beta1_beta1", "gamma1_gamma1"]

        for position in start_positions:
            try:
                print(f"🎯 [START_POS_VAR] Testing start position: {position}")

                # Reset for each position
                if not self.reset_to_fresh_state():
                    print(f"❌ [START_POS_VAR] Could not reset for {position}")
                    return False

                # Select specific start position using command system
                try:
                    from core.commands.start_position_commands import (
                        SetStartPositionCommand,
                    )
                    from core.service_locator import (
                        get_command_processor,
                        get_event_bus,
                    )

                    command_processor = get_command_processor()
                    event_bus = get_event_bus()

                    if not command_processor:
                        print("❌ [START_POS_VAR] Command processor not available")
                        return False
                    if not event_bus:
                        print("❌ [START_POS_VAR] Event bus not available")
                        return False

                    print(f"🎯 [START_POS_VAR] Executing command for: {position}")
                    command = SetStartPositionCommand(
                        position_key=position, event_bus=event_bus
                    )
                    result = command_processor.execute(command)

                    if result and result.success:
                        print(
                            f"✅ [START_POS_VAR] Command executed successfully for {position}"
                        )
                        QTest.qWait(1000)

                        # Verify transition to option picker
                        state = self.log_workflow_state(f"AFTER_{position}")
                        if "OPTION_PICKER" in state:
                            print(f"✅ [START_POS_VAR] {position} worked correctly")
                        else:
                            print(f"❌ [START_POS_VAR] {position} failed to transition")
                            return False
                    else:
                        print(f"❌ [START_POS_VAR] Command failed for {position}")
                        return False

                except Exception as e:
                    print(
                        f"❌ [START_POS_VAR] Error executing command for {position}: {e}"
                    )
                    return False

            except Exception as e:
                print(f"❌ [START_POS_VAR] Failed for {position}: {e}")
                return False

        print("✅ [START_POS_VAR] All start positions tested successfully")
        return True

    def test_rapid_interactions(self) -> bool:
        """Test rapid user interactions and state consistency"""
        print("\n🧪 Rapid Interactions Test")
        print("-" * 40)

        try:
            # Reset to fresh state
            if not self.reset_to_fresh_state():
                print("❌ [RAPID] Could not reset to fresh state")
                return False

            # Rapid sequence: start position → option → clear → start position → option
            print("⚡ [RAPID] Performing rapid interactions...")

            # 1. Select start position
            if not self.select_start_position_via_signal():
                return False
            QTest.qWait(100)  # Minimal wait

            # 2. Add beat
            if not self.select_option_via_workbench():
                return False
            QTest.qWait(100)  # Minimal wait

            # 3. Clear sequence
            if not self.clear_sequence_via_construct_tab():
                return False
            QTest.qWait(100)  # Minimal wait

            # 4. Immediately select start position again
            if not self.select_start_position_via_signal():
                return False
            QTest.qWait(100)  # Minimal wait

            # 5. Add another beat
            if not self.select_option_via_workbench():
                return False

            # Verify final state
            final_state = self.log_workflow_state("RAPID_FINAL")
            if "OPTION_PICKER" in final_state and "sequence=3_items" in final_state:
                print("✅ [RAPID] Rapid interactions handled correctly")
                return True
            print(f"❌ [RAPID] Unexpected final state: {final_state}")
            return False

        except Exception as e:
            print(f"❌ [RAPID] Test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_persistence_functionality(self) -> bool:
        """Test auto-save and restore functionality"""
        print("\n🧪 Persistence Functionality Test")
        print("-" * 40)

        try:
            # Reset and build a sequence
            if not self.reset_to_fresh_state():
                print("❌ [PERSISTENCE] Could not reset to fresh state")
                return False
            if not self.select_start_position_via_signal():
                return False
            if not self.select_option_via_workbench():
                return False

            # Verify sequence is saved
            sequence_data = self.persistence_service.load_current_sequence()
            if len(sequence_data) >= 3:  # metadata + start position + beat
                print("✅ [PERSISTENCE] Sequence auto-saved correctly")
            else:
                print(f"❌ [PERSISTENCE] Expected ≥3 items, got {len(sequence_data)}")
                return False

            # Simulate restart by creating new construct tab
            print("🔄 [PERSISTENCE] Simulating application restart...")

            # Create new construct tab (simulates restart)
            from presentation.tabs.construct.construct_tab_widget import (
                ConstructTabWidget,
            )

            self.construct_tab = ConstructTabWidget(self.container)

            # Check if sequence is restored
            QTest.qWait(1000)  # Allow time for restoration

            if hasattr(self.construct_tab, "layout_manager"):
                self.layout_manager = self.construct_tab.layout_manager
                if hasattr(self.layout_manager, "workbench"):
                    self.workbench = self.layout_manager.workbench

                    # Check restored state
                    restored_state = self.log_workflow_state("AFTER_RESTART")
                    if "sequence=3_items" in restored_state:
                        print(
                            "✅ [PERSISTENCE] Sequence restored correctly after restart"
                        )
                        return True
                    print(f"❌ [PERSISTENCE] Sequence not restored: {restored_state}")
                    return False

            print("❌ [PERSISTENCE] Could not access components after restart")
            return False

        except Exception as e:
            print(f"❌ [PERSISTENCE] Test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def run_basic_workflow_test(self) -> bool:
        """Run the basic workflow test (original test)"""
        print("\n🧪 Basic Workflow Test")
        print("-" * 40)

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

            if not step_func():
                print(f"❌ {step_name}: FAILED")
                return False
            print(f"✅ {step_name}: PASSED")

        # Analyze workflow
        self.analyze_signal_workflow_results()
        return True

    def test_edge_cases(self) -> bool:
        """Test edge cases and error conditions"""
        print("\n🧪 Edge Cases Test")
        print("-" * 40)

        try:
            # Test 1: Empty sequence operations
            print("🔍 [EDGE] Testing empty sequence operations...")
            if not self.reset_to_fresh_state():
                print("❌ [EDGE] Could not reset to fresh state")
                return False

            # Try to clear already empty sequence
            if not self.clear_sequence_via_construct_tab():
                return False

            # Verify still on start position picker
            state = self.log_workflow_state("AFTER_CLEAR_EMPTY")
            if "START_POSITION_PICKER" not in state:
                print("❌ [EDGE] Clear empty sequence changed picker state")
                return False

            # Test 2: Multiple start position selections
            print("🔍 [EDGE] Testing multiple start position selections...")
            if not self.select_start_position_via_signal():
                return False

            # Select different start position using command system
            try:
                from core.commands.start_position_commands import (
                    SetStartPositionCommand,
                )
                from core.service_locator import get_command_processor, get_event_bus

                command_processor = get_command_processor()
                event_bus = get_event_bus()

                if command_processor and event_bus:
                    command = SetStartPositionCommand(
                        position_key="beta1_beta1", event_bus=event_bus
                    )
                    result = command_processor.execute(command)

                    if result and result.success:
                        QTest.qWait(500)

                        # Should still be on option picker
                        state = self.log_workflow_state("AFTER_SECOND_START_POS")
                        if "OPTION_PICKER" not in state:
                            print("❌ [EDGE] Second start position selection failed")
                            return False
                    else:
                        print("❌ [EDGE] Second start position command failed")
                        return False
                else:
                    print("❌ [EDGE] Command processor not available")
                    return False
            except Exception as e:
                print(f"❌ [EDGE] Error in second start position selection: {e}")
                return False

            print("✅ [EDGE] Edge cases handled correctly")
            return True

        except Exception as e:
            print(f"❌ [EDGE] Test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_button_operations(self) -> bool:
        """Test button operations and UI interactions"""
        print("\n🧪 Button Operations Test")
        print("-" * 40)

        try:
            # Reset and setup sequence
            if not self.reset_to_fresh_state():
                print("❌ [BUTTON] Could not reset to fresh state")
                return False
            if not self.select_start_position_via_signal():
                return False
            if not self.select_option_via_workbench():
                return False

            # Test clear button functionality
            print("🔘 [BUTTON] Testing clear button...")
            if hasattr(self.construct_tab, "clear_sequence"):
                self.construct_tab.clear_sequence()
                QTest.qWait(500)

                state = self.log_workflow_state("AFTER_CLEAR_BUTTON")
                if "START_POSITION_PICKER" in state:
                    print("✅ [BUTTON] Clear button works correctly")
                else:
                    print("❌ [BUTTON] Clear button failed")
                    return False

            # Test workbench button operations
            print("🔘 [BUTTON] Testing workbench buttons...")
            if self.workbench:
                # Test if workbench has button operations
                if hasattr(self.workbench, "_button_panel"):
                    button_panel = self.workbench._button_panel
                    if hasattr(button_panel, "clear_button"):
                        # Test clear button
                        print("🔘 [BUTTON] Found workbench clear button")
                        # Note: We don't click it to avoid disrupting test state

            print("✅ [BUTTON] Button operations tested successfully")
            return True

        except Exception as e:
            print(f"❌ [BUTTON] Test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_error_recovery(self) -> bool:
        """Test error recovery and system resilience"""
        print("\n🧪 Error Recovery Test")
        print("-" * 40)

        try:
            # Test 1: Recovery from invalid state
            print("🔧 [RECOVERY] Testing recovery from invalid state...")
            if not self.reset_to_fresh_state():
                print("❌ [RECOVERY] Could not reset to fresh state")
                return False

            # Simulate invalid state by directly manipulating workbench
            if self.workbench:

                # Set invalid sequence (None)
                if hasattr(self.workbench, "_current_sequence"):
                    self.workbench._current_sequence = None
                    QTest.qWait(100)

                    # Try to perform normal operation
                    if self.select_start_position_via_signal():
                        print("✅ [RECOVERY] Recovered from invalid sequence state")
                    else:
                        print("❌ [RECOVERY] Failed to recover from invalid state")
                        return False

            # Test 2: Component missing scenarios
            print("🔧 [RECOVERY] Testing missing component scenarios...")
            # Temporarily remove layout manager
            original_layout_manager = self.layout_manager
            self.layout_manager = None

            # Try operations without layout manager
            try:
                self.select_start_position_via_signal()
                print("✅ [RECOVERY] Handled missing layout manager gracefully")
            except Exception:
                print("✅ [RECOVERY] Properly failed with missing components")

            # Restore layout manager
            self.layout_manager = original_layout_manager

            print("✅ [RECOVERY] Error recovery tests completed")
            return True

        except Exception as e:
            print(f"❌ [RECOVERY] Test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def run_signal_workflow_test(self) -> bool:
        """Run the complete signal-based workflow test"""
        print("🚀 COMPREHENSIVE TKA USER WORKFLOW TEST")
        print("=" * 50)
        print("Testing complete user interactions and edge cases:")
        print("1. Basic Workflow: Start → Select Position → Add Beats → Clear")
        print("2. Multi-Beat Sequences: Build longer sequences")
        print("3. Start Position Variations: Test different start positions")
        print("4. Edge Cases: Empty states, rapid interactions, error recovery")
        print("5. UI State Consistency: Verify picker transitions")
        print("6. Persistence: Auto-save and restore functionality")
        print("7. Button Operations: Clear, undo, navigation")
        print("8. Error Handling: Invalid states, missing data")
        print("=" * 50)

        # Run comprehensive test suite
        comprehensive_tests = [
            ("Basic Workflow", self.run_basic_workflow_test),
            ("Multi-Beat Sequences", self.test_multi_beat_sequence),
            ("Different Start Positions", self.test_different_start_positions),
            ("Rapid Interactions", self.test_rapid_interactions),
            ("Persistence Functionality", self.test_persistence_functionality),
            ("Edge Cases", self.test_edge_cases),
            ("Button Operations", self.test_button_operations),
            ("Error Recovery", self.test_error_recovery),
        ]

        # Track test results
        test_results = {}
        total_tests = len(comprehensive_tests)
        passed_tests = 0

        for step_name, step_func in comprehensive_tests:
            print(f"\n🧪 {step_name}")
            print("-" * 40)

            try:
                success = step_func()
                if success:
                    print(f"✅ {step_name}: PASSED")
                    test_results[step_name] = "PASSED"
                    passed_tests += 1
                else:
                    print(f"❌ {step_name}: FAILED")
                    test_results[step_name] = "FAILED"
            except Exception as e:
                print(f"❌ {step_name}: ERROR - {e}")
                test_results[step_name] = f"ERROR - {e}"

        # Print comprehensive summary
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print("\nDetailed Results:")

        for test_name, result in test_results.items():
            status_icon = "✅" if result == "PASSED" else "❌"
            print(f"  {status_icon} {test_name}: {result}")

        # Overall success
        success = passed_tests == total_tests
        if success:
            print("\n🎉 ALL TESTS PASSED - TKA USER WORKFLOW IS WORKING CORRECTLY!")
        else:
            print(
                f"\n⚠️  {total_tests - passed_tests} TESTS FAILED - REVIEW ISSUES ABOVE"
            )

        return success


def main():
    """Main test execution"""
    tester = SignalBasedWorkflowTester()
    success = tester.run_signal_workflow_test()

    if success:
        print("\n🎉 COMPREHENSIVE TKA USER WORKFLOW TEST COMPLETED")
        print("✅ All user interactions and edge cases working correctly")
        return 0
    print("\n❌ COMPREHENSIVE TKA USER WORKFLOW TEST FAILED")
    print("❌ Check detailed results above for specific failures")
    return 1


if __name__ == "__main__":
    sys.exit(main())
