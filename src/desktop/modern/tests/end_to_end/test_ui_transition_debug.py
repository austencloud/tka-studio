#!/usr/bin/env python3
"""
UI TRANSITION DEBUG TEST: Clear Sequence Picker State
MANDATORY: Debug the exact UI transition behavior after clear sequence

This test identifies:
1. What picker is shown immediately after clear
2. If something is causing it to switch back to option picker
3. The exact timing and sequence of UI state changes
4. Signal flow that might be interfering with the transition
"""

import sys
import time
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from application.services.sequences.persister import SequencePersister
from core.application.application_factory import ApplicationFactory
from PyQt6.QtCore import QTimer
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication


class UITransitionDebugger:
    """Debug UI transitions during clear sequence operation"""

    def __init__(self):
        self.app = None
        self.container = None
        self.persistence_service = None
        self.construct_tab = None
        self.layout_manager = None
        self.workbench = None
        self.transition_log = []

    def setup_test_environment(self) -> bool:
        """Setup the test environment"""
        print("🚀 [DEBUG] Setting up UI transition debug environment...")

        try:
            # Create QApplication
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()

            # Create production container and services
            self.container = ApplicationFactory.create_production_app()
            self.persistence_service = SequencePersister()

            print("✅ [DEBUG] Test environment setup complete")
            return True

        except Exception as e:
            print(f"❌ [DEBUG] Setup failed: {e}")
            return False

    def create_test_sequence_with_content(self) -> bool:
        """Create a sequence with actual content to test clearing"""
        print("📝 [DEBUG] Creating sequence with content...")

        try:
            # Create sequence with start position and beats
            test_sequence = [
                {
                    "word": "debug_test",
                    "author": "ui_debug",
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

            self.persistence_service.save_current_sequence(test_sequence)

            # Verify
            loaded = self.persistence_service.load_current_sequence()
            if len(loaded) >= 3:
                print(f"✅ [DEBUG] Test sequence created: {len(loaded)} items")
                return True

            print(f"❌ [DEBUG] Failed to create sequence: {len(loaded)} items")
            return False

        except Exception as e:
            print(f"❌ [DEBUG] Error creating sequence: {e}")
            return False

    def launch_ui_and_monitor(self) -> bool:
        """Launch UI components and set up monitoring"""
        print("🖥️ [DEBUG] Launching UI with monitoring...")

        try:
            from presentation.tabs.construct.construct_tab_widget import (
                ConstructTabWidget,
            )

            # Create construct tab
            self.construct_tab = ConstructTabWidget(self.container)

            # Get references
            if hasattr(self.construct_tab, "layout_manager"):
                self.layout_manager = self.construct_tab.layout_manager
                if hasattr(self.layout_manager, "workbench"):
                    self.workbench = self.layout_manager.workbench

            # Show UI
            self.construct_tab.show()
            self.construct_tab.resize(1200, 800)

            # Wait for initialization
            QTest.qWait(2000)

            print("✅ [DEBUG] UI launched and monitoring setup")
            return True

        except Exception as e:
            print(f"❌ [DEBUG] Failed to launch UI: {e}")
            import traceback

            traceback.print_exc()
            return False

    def get_current_picker_state(self) -> str:
        """Get the current picker state with detailed info"""
        if not self.layout_manager or not hasattr(self.layout_manager, "picker_stack"):
            return "no_picker_stack"

        picker_stack = self.layout_manager.picker_stack
        if not picker_stack:
            return "no_picker_stack_widget"

        current_index = picker_stack.currentIndex()
        widget_count = picker_stack.count()

        # Get widget names
        widget_info = []
        for i in range(widget_count):
            widget = picker_stack.widget(i)
            widget_name = type(widget).__name__ if widget else "None"
            is_current = "CURRENT" if i == current_index else ""
            widget_info.append(f"[{i}] {widget_name} {is_current}")

        return f"index_{current_index}_of_{widget_count} ({', '.join(widget_info)})"

    def log_transition_state(self, event: str):
        """Log the current transition state"""
        picker_state = self.get_current_picker_state()
        timestamp = time.time()

        log_entry = {
            "timestamp": timestamp,
            "event": event,
            "picker_state": picker_state,
        }

        self.transition_log.append(log_entry)
        print(f"🔍 [TRANSITION] {event}: {picker_state}")

    def test_clear_sequence_transitions(self) -> bool:
        """Test the clear sequence operation and monitor UI transitions"""
        print(
            "🧹 [DEBUG] Testing clear sequence with detailed transition monitoring..."
        )

        try:
            # Log initial state
            self.log_transition_state("INITIAL_STATE")

            # Record state before clearing
            before_clear = self.persistence_service.load_current_sequence()
            print(f"📝 [DEBUG] Before clear: {len(before_clear)} items")

            # Execute clear sequence
            print("🧹 [DEBUG] Executing clear sequence...")
            self.log_transition_state("BEFORE_CLEAR")

            if hasattr(self.construct_tab, "clear_sequence"):
                self.construct_tab.clear_sequence()
                print("✅ [DEBUG] Clear sequence called")
            else:
                print("❌ [DEBUG] No clear_sequence method")
                return False

            # Monitor transitions at multiple intervals
            intervals = [100, 250, 500, 1000, 2000, 3000]
            for interval in intervals:
                QTest.qWait(interval)
                self.log_transition_state(f"AFTER_CLEAR_+{interval}ms")

            # Record final state
            after_clear = self.persistence_service.load_current_sequence()
            print(f"📝 [DEBUG] After clear: {len(after_clear)} items")

            # Final state check
            self.log_transition_state("FINAL_STATE")

            return True

        except Exception as e:
            print(f"❌ [DEBUG] Error during clear sequence test: {e}")
            import traceback

            traceback.print_exc()
            return False

    def analyze_transition_log(self):
        """Analyze the transition log to identify issues"""
        print("\n📊 [ANALYSIS] Transition Log Analysis")
        print("=" * 60)

        if not self.transition_log:
            print("❌ No transition log data")
            return

        # Print detailed log
        for i, entry in enumerate(self.transition_log):
            event = entry["event"]
            picker_state = entry["picker_state"]
            print(f"{i+1:2d}. {event:20s} → {picker_state}")

        # Analyze patterns
        print("\n🔍 [ANALYSIS] Pattern Analysis:")

        # Check if it starts with start position picker
        initial_state = self.transition_log[0]["picker_state"]
        if "index_0" in initial_state:
            print("✅ Initially shows start position picker (index 0)")
        elif "index_1" in initial_state:
            print(
                "⚠️ Initially shows option picker (index 1) - this might be expected with content"
            )
        else:
            print(f"❓ Initial state unclear: {initial_state}")

        # Check immediate after clear
        after_clear_states = [
            entry for entry in self.transition_log if "AFTER_CLEAR" in entry["event"]
        ]
        if after_clear_states:
            immediate_after = after_clear_states[0]["picker_state"]
            if "index_0" in immediate_after:
                print("✅ Immediately after clear: start position picker (index 0)")
            elif "index_1" in immediate_after:
                print(
                    "❌ Immediately after clear: option picker (index 1) - THIS IS THE PROBLEM!"
                )
            else:
                print(f"❓ Immediate after clear unclear: {immediate_after}")

        # Check for state changes
        states = [entry["picker_state"] for entry in self.transition_log]
        unique_states = list(dict.fromkeys(states))  # Preserve order, remove duplicates

        if len(unique_states) == 1:
            print(f"✅ State remained consistent: {unique_states[0]}")
        else:
            print(f"⚠️ State changed {len(unique_states)} times:")
            for i, state in enumerate(unique_states):
                print(f"   {i+1}. {state}")

        # Check final state
        final_state = self.transition_log[-1]["picker_state"]
        if "index_0" in final_state:
            print("✅ Final state: start position picker (index 0) - CORRECT")
        elif "index_1" in final_state:
            print("❌ Final state: option picker (index 1) - INCORRECT!")
        else:
            print(f"❓ Final state unclear: {final_state}")

    def run_debug_test(self) -> bool:
        """Run the complete debug test"""
        print("🚀 UI TRANSITION DEBUG TEST")
        print("=" * 50)

        test_steps = [
            ("Setup Test Environment", self.setup_test_environment),
            ("Create Test Sequence", self.create_test_sequence_with_content),
            ("Launch UI and Monitor", self.launch_ui_and_monitor),
            ("Test Clear Transitions", self.test_clear_sequence_transitions),
        ]

        for step_name, step_func in test_steps:
            print(f"\n🧪 {step_name}")
            print("-" * 30)

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
        self.analyze_transition_log()

        return True


def main():
    """Main test execution"""
    debugger = UITransitionDebugger()
    success = debugger.run_debug_test()

    if success:
        print("\n🎉 DEBUG TEST COMPLETED")
        print("✅ Check analysis above for transition issues")
        return 0
    else:
        print("\n❌ DEBUG TEST FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
