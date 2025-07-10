#!/usr/bin/env python3
"""
STARTUP AFTER CLEAR TEST: Debug the startup behavior after clear sequence
MANDATORY: Test the exact scenario user is experiencing

This test validates:
1. Clear sequence operation
2. Restart simulation (fresh app startup)
3. Monitor what picker is shown during startup
4. Identify if something switches from start position picker to option picker
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


class StartupAfterClearTester:
    """Test startup behavior after clear sequence"""

    def __init__(self):
        self.app = None
        self.persistence_service = None
        self.startup_log = []

    def setup_test_environment(self) -> bool:
        """Setup the test environment"""
        print("🚀 [STARTUP_TEST] Setting up startup after clear test...")

        try:
            # Create QApplication
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()

            self.persistence_service = SequencePersister()

            print("✅ [STARTUP_TEST] Test environment setup complete")
            return True

        except Exception as e:
            print(f"❌ [STARTUP_TEST] Setup failed: {e}")
            return False

    def create_and_clear_sequence(self) -> bool:
        """Create a sequence, then clear it to simulate user workflow"""
        print("📝 [STARTUP_TEST] Creating and clearing sequence...")

        try:
            # Step 1: Create sequence with content
            test_sequence = [
                {
                    "word": "startup_test",
                    "author": "startup_debug",
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
            print(f"✅ [STARTUP_TEST] Created sequence with {len(test_sequence)} items")

            # Step 2: Clear the sequence
            self.persistence_service.clear_current_sequence()
            cleared = self.persistence_service.load_current_sequence()
            print(f"✅ [STARTUP_TEST] Cleared sequence, now has {len(cleared)} items")

            return True

        except Exception as e:
            print(f"❌ [STARTUP_TEST] Error creating/clearing sequence: {e}")
            return False

    def simulate_fresh_startup(self) -> bool:
        """Simulate a fresh app startup and monitor picker transitions"""
        print("🔄 [STARTUP_TEST] Simulating fresh app startup...")

        try:
            from presentation.tabs.construct.construct_tab_widget import (
                ConstructTabWidget,
            )

            # Create fresh container (simulating app restart)
            container = ApplicationFactory.create_production_app()

            # Create construct tab (this triggers startup sequence loading)
            construct_tab = ConstructTabWidget(container)

            # Get layout manager for monitoring
            layout_manager = (
                construct_tab.layout_manager
                if hasattr(construct_tab, "layout_manager")
                else None
            )

            # Show UI
            construct_tab.show()
            construct_tab.resize(1200, 800)

            # Monitor startup transitions
            self.log_startup_state("STARTUP_INITIAL", layout_manager)

            # Wait for startup to complete with monitoring
            intervals = [100, 250, 500, 1000, 2000, 3000, 5000]
            for interval in intervals:
                QTest.qWait(interval)
                self.log_startup_state(f"STARTUP_+{interval}ms", layout_manager)

            print("✅ [STARTUP_TEST] Fresh startup simulation complete")
            return True

        except Exception as e:
            print(f"❌ [STARTUP_TEST] Error during startup simulation: {e}")
            import traceback

            traceback.print_exc()
            return False

    def log_startup_state(self, event: str, layout_manager):
        """Log the startup state"""
        picker_state = self.get_picker_state(layout_manager)
        timestamp = time.time()

        log_entry = {
            "timestamp": timestamp,
            "event": event,
            "picker_state": picker_state,
        }

        self.startup_log.append(log_entry)
        print(f"🔍 [STARTUP] {event}: {picker_state}")

    def get_picker_state(self, layout_manager) -> str:
        """Get the current picker state"""
        if not layout_manager or not hasattr(layout_manager, "picker_stack"):
            return "no_picker_stack"

        picker_stack = layout_manager.picker_stack
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

    def analyze_startup_behavior(self):
        """Analyze the startup behavior"""
        print("\n📊 [ANALYSIS] Startup After Clear Analysis")
        print("=" * 60)

        if not self.startup_log:
            print("❌ No startup log data")
            return

        # Print detailed log
        for i, entry in enumerate(self.startup_log):
            event = entry["event"]
            picker_state = entry["picker_state"]
            print(f"{i+1:2d}. {event:20s} → {picker_state}")

        # Analyze patterns
        print("\n🔍 [ANALYSIS] Startup Pattern Analysis:")

        # Check initial startup state
        if self.startup_log:
            initial_state = self.startup_log[0]["picker_state"]
            if "index_0" in initial_state:
                print("✅ Startup initially shows start position picker (index 0)")
            elif "index_1" in initial_state:
                print("❌ Startup initially shows option picker (index 1) - PROBLEM!")
            else:
                print(f"❓ Initial startup state unclear: {initial_state}")

        # Check for state changes during startup
        states = [entry["picker_state"] for entry in self.startup_log]
        unique_states = list(dict.fromkeys(states))  # Preserve order, remove duplicates

        if len(unique_states) == 1:
            print(f"✅ Startup state remained consistent: {unique_states[0]}")
        else:
            print(f"⚠️ Startup state changed {len(unique_states)} times:")
            for i, state in enumerate(unique_states):
                print(f"   {i+1}. {state}")

            # Find when it changed
            for i in range(1, len(self.startup_log)):
                if (
                    self.startup_log[i]["picker_state"]
                    != self.startup_log[i - 1]["picker_state"]
                ):
                    prev_event = self.startup_log[i - 1]["event"]
                    curr_event = self.startup_log[i]["event"]
                    prev_state = self.startup_log[i - 1]["picker_state"]
                    curr_state = self.startup_log[i]["picker_state"]
                    print(f"🔄 State changed between {prev_event} and {curr_event}")
                    print(f"   From: {prev_state}")
                    print(f"   To:   {curr_state}")

        # Check final state
        if self.startup_log:
            final_state = self.startup_log[-1]["picker_state"]
            if "index_0" in final_state:
                print(
                    "✅ Final startup state: start position picker (index 0) - CORRECT"
                )
            elif "index_1" in final_state:
                print(
                    "❌ Final startup state: option picker (index 1) - THIS IS THE PROBLEM!"
                )
            else:
                print(f"❓ Final startup state unclear: {final_state}")

    def run_startup_test(self) -> bool:
        """Run the complete startup test"""
        print("🚀 STARTUP AFTER CLEAR TEST")
        print("=" * 50)

        test_steps = [
            ("Setup Test Environment", self.setup_test_environment),
            ("Create and Clear Sequence", self.create_and_clear_sequence),
            ("Simulate Fresh Startup", self.simulate_fresh_startup),
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
        self.analyze_startup_behavior()

        return True


def main():
    """Main test execution"""
    tester = StartupAfterClearTester()
    success = tester.run_startup_test()

    if success:
        print("\n🎉 STARTUP TEST COMPLETED")
        print("✅ Check analysis above for startup issues")
        return 0
    else:
        print("\n❌ STARTUP TEST FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
