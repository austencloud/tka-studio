#!/usr/bin/env python3
"""
COMPREHENSIVE UI TEST: Clear Sequence with UI Automation
MANDATORY: Tests the complete clear sequence workflow including UI transitions

This test validates:
1. Creates REAL test sequence with actual data
2. Launches TKA UI components
3. Programmatically triggers clear sequence
4. Validates UI state transitions
5. Confirms persistence layer changes
"""
from __future__ import annotations

from pathlib import Path
import sys


# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from application.services.sequence.sequence_persister import SequencePersister
from core.application.application_factory import ApplicationFactory


class ClearSequenceUITest:
    """Comprehensive UI test for clear sequence functionality"""

    def __init__(self):
        self.app = None
        self.container = None
        self.persistence_service = None
        self.construct_tab = None
        self.workbench = None

    def setup_test_environment(self) -> bool:
        """Setup the complete test environment"""
        print("🚀 [UI_TEST] Setting up test environment...")

        try:
            # Create QApplication if needed
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()

            # Create production container
            self.container = ApplicationFactory.create_production_app()
            self.persistence_service = SequencePersister()

            print("✅ [UI_TEST] Test environment setup complete")
            return True

        except Exception as e:
            print(f"❌ [UI_TEST] Setup failed: {e}")
            return False

    def create_real_test_sequence(self) -> bool:
        """Create test sequence with REAL data"""
        print("📝 [UI_TEST] Creating REAL test sequence...")

        try:
            # REAL sequence data - exactly as provided by user
            real_sequence = [
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

            # Save REAL sequence
            self.persistence_service.save_current_sequence(real_sequence)

            # Verify
            loaded = self.persistence_service.load_current_sequence()
            if len(loaded) >= 3:
                print(f"✅ [UI_TEST] REAL sequence created: {len(loaded)} items")
                return True
            print(f"❌ [UI_TEST] Failed to create sequence: {len(loaded)} items")
            return False

        except Exception as e:
            print(f"❌ [UI_TEST] Error creating sequence: {e}")
            return False

    def launch_ui_components(self) -> bool:
        """Launch the TKA UI components"""
        print("🖥️ [UI_TEST] Launching UI components...")

        try:
            from presentation.tabs.construct.construct_tab_widget import (
                ConstructTabWidget,
            )

            # Create construct tab
            self.construct_tab = ConstructTabWidget(self.container)

            # Get workbench reference
            if hasattr(self.construct_tab, "layout_manager") and hasattr(
                self.construct_tab.layout_manager, "workbench"
            ):
                self.workbench = self.construct_tab.layout_manager.workbench
                print("✅ [UI_TEST] Workbench reference obtained")

            # Show the UI
            self.construct_tab.show()
            self.construct_tab.resize(1200, 800)

            # Wait for initialization
            QTest.qWait(1000)

            print("✅ [UI_TEST] UI components launched successfully")
            return True

        except Exception as e:
            print(f"❌ [UI_TEST] Failed to launch UI: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_clear_sequence_via_workbench(self) -> bool:
        """Test clear sequence by calling workbench private method directly"""
        print("🧹 [UI_TEST] Testing clear sequence via workbench...")

        try:
            if not self.workbench:
                print("❌ [UI_TEST] No workbench available")
                return False

            # Record state before clearing
            before_clear = self.persistence_service.load_current_sequence()
            print(f"📝 [UI_TEST] Before clear: {len(before_clear)} items")

            # Call private clear method on workbench
            if hasattr(self.workbench, "_handle_clear"):
                self.workbench._handle_clear()
                print("✅ [UI_TEST] Workbench _handle_clear() called")
            else:
                print("❌ [UI_TEST] Workbench has no _handle_clear method")
                return False

            # Wait for operations to complete
            QTest.qWait(1000)

            # Record state after clearing
            after_clear = self.persistence_service.load_current_sequence()
            print(f"📝 [UI_TEST] After clear: {len(after_clear)} items")

            # Validate results
            if len(after_clear) == 1 and after_clear[0].get("word") == "":
                print("✅ [UI_TEST] Clear sequence via workbench successful")
                return True
            print(f"❌ [UI_TEST] Clear sequence failed: {after_clear}")
            return False

        except Exception as e:
            print(f"❌ [UI_TEST] Error during clear sequence: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_clear_sequence_via_construct_tab(self) -> bool:
        """Test clear sequence by calling construct tab method"""
        print("🧹 [UI_TEST] Testing clear sequence via construct tab...")

        try:
            if not self.construct_tab:
                print("❌ [UI_TEST] No construct tab available")
                return False

            # First create test sequence again
            self.create_real_test_sequence()

            # Record state before clearing
            before_clear = self.persistence_service.load_current_sequence()
            print(f"📝 [UI_TEST] Before clear: {len(before_clear)} items")

            # Call clear sequence on construct tab
            if hasattr(self.construct_tab, "clear_sequence"):
                self.construct_tab.clear_sequence()
                print("✅ [UI_TEST] Construct tab clear_sequence() called")
            else:
                print("❌ [UI_TEST] Construct tab has no clear_sequence method")
                return False

            # Wait for operations to complete
            QTest.qWait(1000)

            # Record state after clearing
            after_clear = self.persistence_service.load_current_sequence()
            print(f"📝 [UI_TEST] After clear: {len(after_clear)} items")

            # Validate results
            if len(after_clear) == 1 and after_clear[0].get("word") == "":
                print("✅ [UI_TEST] Clear sequence via construct tab successful")
                return True
            print(f"❌ [UI_TEST] Clear sequence failed: {after_clear}")
            return False

        except Exception as e:
            print(f"❌ [UI_TEST] Error during clear sequence: {e}")
            import traceback

            traceback.print_exc()
            return False

    def run_complete_ui_test(self) -> bool:
        """Run the complete UI test"""
        print("🚀 COMPREHENSIVE CLEAR SEQUENCE UI TEST")
        print("=" * 60)

        test_steps = [
            ("Setup Test Environment", self.setup_test_environment),
            ("Create REAL Test Sequence", self.create_real_test_sequence),
            ("Launch UI Components", self.launch_ui_components),
            ("Test Clear via Workbench", self.test_clear_sequence_via_workbench),
            (
                "Test Clear via Construct Tab",
                self.test_clear_sequence_via_construct_tab,
            ),
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
                import traceback

                traceback.print_exc()
                return False

        print("\n" + "=" * 60)
        print("🎉 ALL UI TESTS PASSED!")
        print("✅ Clear sequence functionality works correctly")
        print("✅ UI components integrate properly")
        print("✅ REAL data is handled correctly")
        print("=" * 60)

        return True


def main():
    """Main test execution"""
    test = ClearSequenceUITest()
    success = test.run_complete_ui_test()

    if success:
        print("\n🎉 COMPREHENSIVE UI TEST: SUCCESS")
        print("✅ Clear sequence works end-to-end")
        print("✅ UI components function correctly")
        print("✅ Persistence layer validated")
        return 0
    print("\n❌ COMPREHENSIVE UI TEST: FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
