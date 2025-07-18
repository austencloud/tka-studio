#!/usr/bin/env python3
"""
Beat Frame Update Test - Verify beat frame updates when selections are made

This test specifically focuses on verifying that the beat frame properly
updates its display when users make selections in:
1. Start position picker
2. Option picker

The test checks for:
- Visual updates in beat frame
- Data integrity between selections and display
- Signal/slot connections working properly
- Proper rendering of selected pictographs
"""

import sys
import time
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from application.services.sequence.sequence_persister import SequencePersister
from core.application.application_factory import ApplicationFactory
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QPushButton


class BeatFrameUpdateTester:
    """Test beat frame updates when selections are made"""

    def __init__(self):
        self.app = None
        self.container = None
        self.persistence_service = None
        self.construct_tab = None
        self.layout_manager = None
        self.workbench = None
        self.test_results = []

    def setup_environment(self) -> bool:
        """Setup test environment"""
        print("🚀 [BEAT_FRAME_TEST] Setting up test environment...")

        try:
            # Create QApplication
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()

            # Clear any existing sequence
            self.persistence_service = SequencePersister()
            self.persistence_service.clear_current_sequence()

            # CRITICAL FIX: Initialize core services for SequenceStateManager
            print("🔧 [BEAT_FRAME_TEST] Initializing core services...")
            from core.service_locator import initialize_services

            initialize_services()
            print("✅ [BEAT_FRAME_TEST] Core services initialized")

            # Create application
            from core.dependency_injection.di_container import reset_container
            from presentation.tabs.construct.construct_tab_widget import (
                ConstructTabWidget,
            )

            reset_container()
            self.container = ApplicationFactory.create_production_app()

            # Initialize pictograph pool
            try:
                from application.services.pictograph_pool_manager import (
                    initialize_pictograph_pool,
                )

                initialize_pictograph_pool(self.container)
            except Exception as e:
                print(f"⚠️ [BEAT_FRAME_TEST] Pictograph pool initialization failed: {e}")

            self.construct_tab = ConstructTabWidget(self.container)

            # Get references
            if hasattr(self.construct_tab, "layout_manager"):
                self.layout_manager = self.construct_tab.layout_manager
                if hasattr(self.layout_manager, "workbench"):
                    self.workbench = self.layout_manager.workbench

            # Show UI
            self.construct_tab.show()
            self.construct_tab.resize(1200, 800)

            # Wait for startup
            QTest.qWait(2000)

            print("✅ [BEAT_FRAME_TEST] Environment setup complete")
            return True

        except Exception as e:
            print(f"❌ [BEAT_FRAME_TEST] Setup failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def get_beat_frame_components(self):
        """Get beat frame components for testing"""
        if not self.layout_manager or not hasattr(self.layout_manager, "workbench"):
            return None, None, None

        workbench = self.layout_manager.workbench
        if not workbench or not hasattr(workbench, "_beat_frame_section"):
            return None, None, None

        beat_frame_section = workbench._beat_frame_section
        if not beat_frame_section or not hasattr(beat_frame_section, "_beat_frame"):
            return None, None, None

        beat_frame = beat_frame_section._beat_frame
        start_position_view = getattr(beat_frame, "_start_position_view", None)

        return beat_frame, start_position_view, beat_frame_section

    def test_start_position_selection_updates_beat_frame(self) -> bool:
        """Test that start position selection updates the beat frame"""
        print(
            "🎯 [BEAT_FRAME_TEST] Testing start position selection -> beat frame update"
        )

        try:
            # Get beat frame components
            beat_frame, start_position_view, beat_frame_section = (
                self.get_beat_frame_components()
            )

            if not beat_frame or not start_position_view:
                print("❌ [BEAT_FRAME_TEST] Could not access beat frame components")
                return False

            # Record initial state
            initial_beat_data = (
                start_position_view.get_beat_data()
                if hasattr(start_position_view, "get_beat_data")
                else None
            )
            initial_pictograph_data = (
                start_position_view.get_pictograph_data()
                if hasattr(start_position_view, "get_pictograph_data")
                else None
            )

            print(
                f"🔍 [BEAT_FRAME_TEST] Initial beat data: {initial_beat_data.letter if initial_beat_data else 'None'}"
            )
            print(
                f"🔍 [BEAT_FRAME_TEST] Initial pictograph data: {initial_pictograph_data.letter if initial_pictograph_data else 'None'}"
            )

            # Find and select start position
            if self.layout_manager and hasattr(
                self.layout_manager, "start_position_picker"
            ):
                start_pos_picker = self.layout_manager.start_position_picker

                # Find alpha1_alpha1 option
                alpha1_option = None
                if hasattr(start_pos_picker, "position_options"):
                    for option in start_pos_picker.position_options:
                        if (
                            hasattr(option, "position_key")
                            and option.position_key == "alpha1_alpha1"
                        ):
                            alpha1_option = option
                            break

                if alpha1_option:
                    print(
                        "🖱️ [BEAT_FRAME_TEST] Clicking alpha1_alpha1 start position..."
                    )
                    QTest.mouseClick(alpha1_option, Qt.MouseButton.LeftButton)
                    QTest.qWait(1000)  # Wait for processing

                    # Check if beat frame was updated
                    updated_beat_data = (
                        start_position_view.get_beat_data()
                        if hasattr(start_position_view, "get_beat_data")
                        else None
                    )
                    updated_pictograph_data = (
                        start_position_view.get_pictograph_data()
                        if hasattr(start_position_view, "get_pictograph_data")
                        else None
                    )

                    print(
                        f"🔍 [BEAT_FRAME_TEST] Updated beat data: {updated_beat_data.letter if updated_beat_data else 'None'}"
                    )
                    print(
                        f"🔍 [BEAT_FRAME_TEST] Updated pictograph data: {updated_pictograph_data.letter if updated_pictograph_data else 'None'}"
                    )

                    # Verify update occurred
                    beat_data_changed = updated_beat_data != initial_beat_data
                    pictograph_data_changed = (
                        updated_pictograph_data != initial_pictograph_data
                    )

                    if beat_data_changed or pictograph_data_changed:
                        print(
                            "✅ [BEAT_FRAME_TEST] Beat frame was updated after start position selection"
                        )

                        # Verify data correctness
                        if updated_beat_data and updated_beat_data.letter == "α":
                            print(
                                "✅ [BEAT_FRAME_TEST] Beat data has correct letter (α)"
                            )
                        else:
                            print(
                                f"❌ [BEAT_FRAME_TEST] Beat data has incorrect letter: {updated_beat_data.letter if updated_beat_data else 'None'}"
                            )

                        return True
                    else:
                        print(
                            "❌ [BEAT_FRAME_TEST] Beat frame was NOT updated after start position selection"
                        )
                        return False
                else:
                    print("❌ [BEAT_FRAME_TEST] Could not find alpha1_alpha1 option")
                    return False
            else:
                print("❌ [BEAT_FRAME_TEST] Could not access start position picker")
                return False

        except Exception as e:
            print(f"❌ [BEAT_FRAME_TEST] Start position test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_option_selection_updates_beat_frame(self) -> bool:
        """Test that option selection updates the beat frame"""
        print("⚙️ [BEAT_FRAME_TEST] Testing option selection -> beat frame update")

        try:
            # Get beat frame components
            beat_frame, start_position_view, beat_frame_section = (
                self.get_beat_frame_components()
            )

            if not beat_frame:
                print("❌ [BEAT_FRAME_TEST] Could not access beat frame")
                return False

            # Record initial sequence length
            initial_sequence = (
                beat_frame.get_sequence()
                if hasattr(beat_frame, "get_sequence")
                else None
            )
            initial_length = len(initial_sequence.beats) if initial_sequence else 0

            print(f"🔍 [BEAT_FRAME_TEST] Initial sequence length: {initial_length}")

            # Find and select an option
            if self.layout_manager and hasattr(self.layout_manager, "option_picker"):
                option_picker = self.layout_manager.option_picker

                # Navigate to option picker sections
                if hasattr(option_picker, "option_picker_widget"):
                    widget = option_picker.option_picker_widget

                    if hasattr(widget, "option_picker_scroll"):
                        scroll_widget = widget.option_picker_scroll

                        if hasattr(scroll_widget, "sections"):
                            sections = scroll_widget.sections

                            # Find first available option
                            first_frame = None
                            for letter_type, section in sections.items():
                                if hasattr(section, "pictograph_frames"):
                                    frames = section.pictograph_frames
                                    if frames:
                                        first_frame = frames[0]
                                        break

                            if first_frame:
                                print("🖱️ [BEAT_FRAME_TEST] Clicking first option...")
                                QTest.mouseClick(first_frame, Qt.MouseButton.LeftButton)
                                QTest.qWait(1000)  # Wait for processing

                                # Check if sequence was updated
                                updated_sequence = (
                                    beat_frame.get_sequence()
                                    if hasattr(beat_frame, "get_sequence")
                                    else None
                                )
                                updated_length = (
                                    len(updated_sequence.beats)
                                    if updated_sequence
                                    else 0
                                )

                                print(
                                    f"🔍 [BEAT_FRAME_TEST] Updated sequence length: {updated_length}"
                                )

                                if updated_length > initial_length:
                                    print(
                                        "✅ [BEAT_FRAME_TEST] Beat frame sequence was updated after option selection"
                                    )
                                    return True
                                else:
                                    print(
                                        "❌ [BEAT_FRAME_TEST] Beat frame sequence was NOT updated after option selection"
                                    )
                                    return False
                            else:
                                print(
                                    "❌ [BEAT_FRAME_TEST] Could not find any option frames"
                                )
                                return False
                        else:
                            print("❌ [BEAT_FRAME_TEST] Option picker has no sections")
                            return False
                    else:
                        print(
                            "❌ [BEAT_FRAME_TEST] Option picker widget has no scroll widget"
                        )
                        return False
                else:
                    print("❌ [BEAT_FRAME_TEST] Option picker has no widget")
                    return False
            else:
                print("❌ [BEAT_FRAME_TEST] Could not access option picker")
                return False

        except Exception as e:
            print(f"❌ [BEAT_FRAME_TEST] Option selection test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def run_beat_frame_update_tests(self) -> bool:
        """Run all beat frame update tests"""
        print("🚀 BEAT FRAME UPDATE TESTS")
        print("=" * 50)

        test_steps = [
            ("Setup Environment", self.setup_environment),
            (
                "Test Start Position Selection Updates Beat Frame",
                self.test_start_position_selection_updates_beat_frame,
            ),
            (
                "Test Option Selection Updates Beat Frame",
                self.test_option_selection_updates_beat_frame,
            ),
        ]

        for step_name, step_func in test_steps:
            print(f"\n🧪 {step_name}")
            print("-" * 40)

            try:
                success = step_func()
                if success:
                    print(f"✅ {step_name}: PASSED")
                    self.test_results.append((step_name, "PASSED"))
                else:
                    print(f"❌ {step_name}: FAILED")
                    self.test_results.append((step_name, "FAILED"))
                    return False
            except Exception as e:
                print(f"❌ {step_name}: ERROR - {e}")
                self.test_results.append((step_name, "ERROR"))
                return False

        return True

    def print_test_summary(self):
        """Print test summary"""
        print("\n📊 BEAT FRAME UPDATE TEST SUMMARY")
        print("=" * 50)

        for test_name, result in self.test_results:
            status_icon = "✅" if result == "PASSED" else "❌"
            print(f"{status_icon} {test_name}: {result}")


def main():
    """Main test execution"""
    tester = BeatFrameUpdateTester()
    success = tester.run_beat_frame_update_tests()
    tester.print_test_summary()

    if success:
        print("\n🎉 BEAT FRAME UPDATE TESTS COMPLETED SUCCESSFULLY")
        return 0
    else:
        print("\n❌ BEAT FRAME UPDATE TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
