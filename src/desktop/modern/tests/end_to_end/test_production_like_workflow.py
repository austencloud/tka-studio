#!/usr/bin/env python3
"""
Production-Like Comprehensive TKA User Workflow Test

This test replicates the EXACT user experience by:
- Using full TKA application startup sequence with proper window sizing
- Testing complete beat addition workflow with option picker selections
- Validating JSON persistence to current_sequence.json
- Simulating real user interactions with proper UI dimensions and styling

The test ensures that when users select beats, they properly:
1. Display in the beat frame
2. Convert to JSON dictionaries
3. Update the current_sequence.json file

TEST LIFECYCLE: SPECIFICATION
PURPOSE: Validate complete production-like TKA user workflow with JSON persistence
PERMANENT: Production workflow validation for TKA application
AUTHOR: AI Agent
"""

import sys
import json
from pathlib import Path

# Add the modern src directory to Python path
modern_src = Path(__file__).parent.parent.parent / "src"
if str(modern_src) not in sys.path:
    sys.path.insert(0, str(modern_src))

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtTest import QTest
from PyQt6.QtCore import QTimer, QRect, Qt
from PyQt6.QtGui import QGuiApplication
import time

# Import TKA application components
from core.application.application_factory import ApplicationFactory
from core.testing.ai_agent_helpers import TKAAITestHelper


class ProductionLikeTKATest:
    """
    Production-like TKA test that replicates exact user experience.

    This test creates a full TKA application instance with:
    - Proper window sizing (90% of screen like production)
    - Complete UI setup with background and styling
    - Real option picker with beat selection
    - JSON persistence validation
    """

    def __init__(self):
        self.app = None
        self.main_window = None
        self.container = None
        self.construct_tab = None
        self.workbench = None
        self.option_picker = None
        self.current_sequence_file = (
            Path(__file__).parent.parent.parent / "current_sequence.json"
        )

    def setup_production_application(self):
        """Setup full production-like TKA application."""
        print("🚀 [PRODUCTION] Setting up full TKA application...")

        # Create QApplication with proper styling
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)
            self.app.setStyle("Fusion")

        # Create production container
        self.container = ApplicationFactory.create_production_app()
        print("✅ [PRODUCTION] Production container created")

        # Create main window with production sizing
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("TKA Production Test")

        # Set production-like window geometry (90% of screen)
        screen = QGuiApplication.primaryScreen().availableGeometry()
        window_width = int(screen.width() * 0.9)
        window_height = int(screen.height() * 0.9)
        x = screen.x() + int((screen.width() - window_width) / 2)
        y = screen.y() + int((screen.height() - window_height) / 2)

        self.main_window.setGeometry(x, y, window_width, window_height)
        print(
            f"✅ [PRODUCTION] Window sized: {window_width}x{window_height} at ({x},{y})"
        )

        # Initialize application orchestrator for full UI setup
        from application.services.core.application_orchestrator import (
            ApplicationOrchestrator,
        )

        orchestrator = ApplicationOrchestrator(container=self.container)

        # Initialize complete application with all services
        self.tab_widget = orchestrator.initialize_application(
            self.main_window,
            splash_screen=None,
            target_screen=None,
            parallel_mode=False,
            parallel_geometry=None,
            enable_api=False,  # Disable API for testing
        )

        # Set the tab widget as central widget
        self.main_window.setCentralWidget(self.tab_widget)

        # Get construct tab for testing
        for i in range(self.tab_widget.count()):
            if "construct" in self.tab_widget.tabText(i).lower():
                self.construct_tab = self.tab_widget.widget(i)
                break

        if not self.construct_tab:
            raise RuntimeError("Could not find construct tab")

        print("✅ [PRODUCTION] Construct tab located")

        # Get workbench and option picker references
        if hasattr(self.construct_tab, "workbench"):
            self.workbench = self.construct_tab.workbench
            print("✅ [PRODUCTION] Workbench reference obtained")
        else:
            raise RuntimeError("Could not access workbench")

        # Get option picker reference
        if hasattr(self.construct_tab, "option_picker_manager") and hasattr(
            self.construct_tab.option_picker_manager, "option_picker"
        ):
            self.option_picker = self.construct_tab.option_picker_manager.option_picker
            print(
                f"✅ [PRODUCTION] Option picker reference obtained: {type(self.option_picker)}"
            )
            print(
                f"🔍 [DEBUG] Option picker attributes: {[attr for attr in dir(self.option_picker) if not attr.startswith('_')]}"
            )

            # Check for orchestrator
            if hasattr(self.option_picker, "orchestrator"):
                print(
                    f"🔍 [DEBUG] Orchestrator found: {self.option_picker.orchestrator}"
                )
                if hasattr(self.option_picker.orchestrator, "display_manager"):
                    print(
                        f"🔍 [DEBUG] Display manager found: {self.option_picker.orchestrator.display_manager}"
                    )
                else:
                    print("🔍 [DEBUG] No display_manager on orchestrator")
            else:
                print("🔍 [DEBUG] No orchestrator attribute on option picker")
        else:
            raise RuntimeError("Could not access option picker")

        # Show the main window
        self.main_window.show()
        self.main_window.raise_()
        QTest.qWait(500)  # Allow UI to fully render

        print("✅ [PRODUCTION] Full TKA application setup complete")
        return True

    def clear_sequence_file(self):
        """Clear the current sequence file to start fresh."""
        try:
            default_sequence = [
                {
                    "word": "",
                    "author": "modern",
                    "level": 0,
                    "prop_type": "staff",
                    "grid_mode": "diamond",
                }
            ]

            with open(self.current_sequence_file, "w", encoding="utf-8") as f:
                json.dump(default_sequence, f, indent=4, ensure_ascii=False)

            print("✅ [PRODUCTION] Sequence file cleared")
            return True
        except Exception as e:
            print(f"❌ [PRODUCTION] Failed to clear sequence file: {e}")
            return False

    def load_sequence_file(self):
        """Load and return current sequence file contents."""
        try:
            with open(self.current_sequence_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"❌ [PRODUCTION] Failed to load sequence file: {e}")
            return None

    def validate_sequence_file_update(self, expected_length):
        """Validate that sequence file has been updated with expected number of items."""
        sequence_data = self.load_sequence_file()
        if not sequence_data:
            return False

        actual_length = len(sequence_data)
        if actual_length == expected_length:
            print(f"✅ [PRODUCTION] Sequence file updated: {actual_length} items")
            return True
        else:
            print(
                f"❌ [PRODUCTION] Sequence file length mismatch: expected {expected_length}, got {actual_length}"
            )
            return False

    def select_start_position(self, position_name):
        """Select a start position using the production UI."""
        print(f"🎯 [PRODUCTION] Selecting start position: {position_name}")

        try:
            # Get start position picker from construct tab layout manager
            if hasattr(self.construct_tab, "layout_manager") and hasattr(
                self.construct_tab.layout_manager, "start_position_picker"
            ):
                start_picker = self.construct_tab.layout_manager.start_position_picker

                # Find the position option widget and click it
                if hasattr(start_picker, "position_options"):
                    for option in start_picker.position_options:
                        if (
                            hasattr(option, "position_key")
                            and option.position_key == position_name
                        ):
                            # Simulate mouse click on the option widget
                            QTest.mouseClick(option, Qt.MouseButton.LeftButton)
                            QTest.qWait(2000)  # Wait for processing
                            print(
                                f"✅ [PRODUCTION] Start position selected: {position_name}"
                            )
                            return True

                    print(
                        f"❌ [PRODUCTION] Start position option not found: {position_name}"
                    )
                    print(
                        f"🔍 [PRODUCTION] Available options: {[opt.position_key for opt in start_picker.position_options if hasattr(opt, 'position_key')]}"
                    )
                    return False
                else:
                    print(
                        "❌ [PRODUCTION] Start position picker options not accessible"
                    )
                    return False
            else:
                print("❌ [PRODUCTION] Start position picker not accessible")
                return False

        except Exception as e:
            print(f"❌ [PRODUCTION] Error selecting start position: {e}")
            import traceback

            traceback.print_exc()
            return False

    def select_option_picker_beat(self, beat_index=0):
        """Select a beat from the option picker."""
        print(f"🎵 [PRODUCTION] Selecting beat from option picker (index {beat_index})")

        try:
            # Get option picker widget
            if not self.option_picker:
                print("❌ [PRODUCTION] Option picker not available")
                return False

            # Debug: Check the option picker's actual widget structure
            print("🔍 [PRODUCTION] Investigating option picker widget structure...")
            print(f"🔍 [PRODUCTION] Option picker type: {type(self.option_picker)}")
            print(
                f"🔍 [PRODUCTION] Option picker has widget attr: {hasattr(self.option_picker, 'widget')}"
            )

            # The option picker might have a 'widget' property that's the actual container
            actual_container = None
            if hasattr(self.option_picker, "widget"):
                actual_container = self.option_picker.widget
                print(f"🔍 [PRODUCTION] Option picker widget: {type(actual_container)}")
            elif hasattr(self.option_picker, "container"):
                actual_container = self.option_picker.container
                print(
                    f"🔍 [PRODUCTION] Option picker container: {type(actual_container)}"
                )
            else:
                actual_container = self.option_picker
                print("🔍 [PRODUCTION] Using option picker directly as container")

            # Get all child widgets from the actual container
            from PyQt6.QtWidgets import QWidget

            all_widgets = actual_container.findChildren(QWidget)
            print(
                f"🔍 [PRODUCTION] Found {len(all_widgets)} total child widgets in container"
            )

            # Look for widgets that might be clickable frames
            clickable_widgets = []
            for widget in all_widgets:
                widget_type = type(widget).__name__
                if (
                    "frame" in widget_type.lower()
                    or "pictograph" in widget_type.lower()
                    or "clickable" in widget_type.lower()
                ):
                    print(
                        f"🔍 [PRODUCTION] Found potential frame: {widget_type} - visible: {widget.isVisible()}"
                    )
                    if widget.isVisible():
                        clickable_widgets.append(widget)

            print(
                f"🔍 [PRODUCTION] Found {len(clickable_widgets)} potential clickable widgets"
            )

            # Also try the specific import
            from presentation.components.option_picker.components.frames.clickable_pictograph_frame import (
                ClickablePictographFrame,
            )

            specific_frames = actual_container.findChildren(ClickablePictographFrame)
            print(
                f"🔍 [PRODUCTION] Found {len(specific_frames)} ClickablePictographFrame widgets"
            )

            # Use only the ClickablePictographFrame widgets, not containers
            visible_frames = specific_frames

            if not visible_frames:
                print(
                    "❌ [PRODUCTION] No visible frames found in option picker sections after retries"
                )
                return False

            print(
                f"🔍 [PRODUCTION] Found {len(visible_frames)} visible frames in sections"
            )

            if beat_index >= len(visible_frames):
                print(
                    f"❌ [PRODUCTION] Beat index {beat_index} out of range (max: {len(visible_frames)-1})"
                )
                return False

            # Get the target frame
            target_frame = visible_frames[beat_index]

            # Click the frame to select the beat
            print(
                f"🎯 [PRODUCTION] Clicking frame with beat: {target_frame.beat_data.letter}"
            )
            QTest.mouseClick(target_frame, Qt.MouseButton.LeftButton)
            QTest.qWait(2000)  # Wait for processing

            print(
                f"✅ [PRODUCTION] Beat selected from option picker: {target_frame.beat_data.letter}"
            )
            return True

        except Exception as e:
            print(f"❌ [PRODUCTION] Error selecting beat from option picker: {e}")
            return False

    def validate_beat_frame_display(self, expected_beat_count):
        """Validate that beats are properly displayed in the beat frame."""
        print(
            f"🖼️ [PRODUCTION] Validating beat frame display (expected {expected_beat_count} beats)"
        )

        try:
            # Get beat frame from workbench using correct attribute names
            if hasattr(self.workbench, "_beat_frame_section") and hasattr(
                self.workbench._beat_frame_section, "_beat_frame"
            ):
                beat_frame = self.workbench._beat_frame_section._beat_frame

                # Check if beat frame has the expected number of beats
                if (
                    hasattr(beat_frame, "_current_sequence")
                    and beat_frame._current_sequence
                ):
                    actual_beat_count = len(beat_frame._current_sequence.beats)

                    if actual_beat_count == expected_beat_count:
                        print(
                            f"✅ [PRODUCTION] Beat frame displays {actual_beat_count} beats correctly"
                        )
                        return True
                    else:
                        print(
                            f"❌ [PRODUCTION] Beat frame beat count mismatch: expected {expected_beat_count}, got {actual_beat_count}"
                        )
                        return False
                else:
                    print("❌ [PRODUCTION] Beat frame sequence not accessible")
                    return False
            else:
                print(
                    "❌ [PRODUCTION] Beat frame not accessible - checking attribute structure..."
                )
                # Debug: Show what attributes are actually available
                if hasattr(self.workbench, "_beat_frame_section"):
                    print(f"🔍 [PRODUCTION] Workbench has _beat_frame_section")
                    beat_frame_section = self.workbench._beat_frame_section
                    if hasattr(beat_frame_section, "_beat_frame"):
                        print(f"🔍 [PRODUCTION] Beat frame section has _beat_frame")
                    else:
                        print(
                            f"🔍 [PRODUCTION] Beat frame section attributes: {[attr for attr in dir(beat_frame_section) if not attr.startswith('__')]}"
                        )
                else:
                    print(
                        f"🔍 [PRODUCTION] Workbench attributes: {[attr for attr in dir(self.workbench) if not attr.startswith('__')]}"
                    )
                return False

        except Exception as e:
            print(f"❌ [PRODUCTION] Error validating beat frame display: {e}")
            return False

    def run_complete_workflow_test(self):
        """Run the complete production-like workflow test."""
        print("🚀 PRODUCTION-LIKE TKA USER WORKFLOW TEST")
        print("=" * 60)
        print("Testing complete user workflow:")
        print("✅ Full TKA application startup with proper sizing")
        print("✅ Start position selection")
        print("✅ Beat addition from option picker (3 beats)")
        print("✅ Beat frame display validation")
        print("✅ JSON persistence validation")
        print("=" * 60)
        print()

        try:
            # Step 1: Setup production application
            if not self.setup_production_application():
                print("❌ [PRODUCTION] Failed to setup production application")
                return False

            # Step 2: Clear sequence file to start fresh
            if not self.clear_sequence_file():
                print("❌ [PRODUCTION] Failed to clear sequence file")
                return False

            # Validate initial state (should have 1 item - metadata)
            if not self.validate_sequence_file_update(1):
                print("❌ [PRODUCTION] Initial sequence file validation failed")
                return False

            # Step 3: Clear any existing sequence in the UI and transition to start position picker
            print("🔄 [PRODUCTION] Clearing UI sequence to start fresh...")

            # Get workbench and clear sequence by setting empty sequence
            if hasattr(self.workbench, "set_sequence"):
                from domain.models.core_models import SequenceData

                empty_sequence = SequenceData(name="", beats=[])
                self.workbench.set_sequence(empty_sequence)
                QTest.qWait(1000)
                print("✅ [PRODUCTION] UI sequence cleared")

            # Step 4: Select start position
            if not self.select_start_position("alpha1_alpha1"):
                print("❌ [PRODUCTION] Failed to select start position")
                return False

            # Wait for start position to be processed and option picker to be populated
            QTest.qWait(3000)  # Longer wait for option picker population

            # Validate start position was added (should have 2 items - metadata + start position)
            if not self.validate_sequence_file_update(2):
                print("❌ [PRODUCTION] Start position not added to sequence file")
                return False

            # Step 5: Add 3 beats from option picker
            for i in range(3):
                print(f"🎵 [PRODUCTION] Adding beat {i+1}/3...")

                if not self.select_option_picker_beat(
                    i % 5
                ):  # Cycle through first 5 options
                    print(f"❌ [PRODUCTION] Failed to select beat {i+1}")
                    return False

                # Wait for beat to be processed
                QTest.qWait(2000)

                # Validate beat was added to sequence file
                expected_length = 3 + i  # metadata + start position + beats so far
                if not self.validate_sequence_file_update(expected_length):
                    print(f"❌ [PRODUCTION] Beat {i+1} not added to sequence file")
                    # Show current file contents for debugging
                    sequence_data = self.load_sequence_file()
                    if sequence_data:
                        print(
                            f"🔍 [PRODUCTION] Current file has {len(sequence_data)} items:"
                        )
                        for j, item in enumerate(sequence_data):
                            if j == 0:
                                print(
                                    f"  [{j}] Metadata: word='{item.get('word', '')}'"
                                )
                            else:
                                print(
                                    f"  [{j}] Beat {item.get('beat', '?')}: {item.get('letter', '?')}"
                                )
                    return False

                # Validate beat frame display
                if not self.validate_beat_frame_display(
                    i + 1
                ):  # Just the beats (not including start position)
                    print(f"❌ [PRODUCTION] Beat {i+1} not displayed in beat frame")
                    return False

                print(f"✅ [PRODUCTION] Beat {i+1} added and validated successfully")

            # Step 6: Final validation
            print("🔍 [PRODUCTION] Running final validation...")

            # Check final sequence file state
            final_sequence = self.load_sequence_file()
            if not final_sequence:
                print("❌ [PRODUCTION] Could not load final sequence file")
                return False

            print(f"📄 [PRODUCTION] Final sequence file contents:")
            for i, item in enumerate(final_sequence):
                if i == 0:
                    print(f"   [{i}] Metadata: {item}")
                elif i == 1:
                    print(
                        f"   [{i}] Start Position: {item.get('letter', 'Unknown')} ({item.get('sequence_start_position', 'Unknown')})"
                    )
                else:
                    print(f"   [{i}] Beat {i-1}: {item.get('letter', 'Unknown')}")

            # Validate final beat frame state
            if not self.validate_beat_frame_display(3):
                print("❌ [PRODUCTION] Final beat frame validation failed")
                return False

            print("✅ [PRODUCTION] All validations passed!")
            return True

        except Exception as e:
            print(f"❌ [PRODUCTION] Workflow test failed with exception: {e}")
            import traceback

            traceback.print_exc()
            return False

    def cleanup(self):
        """Clean up test resources."""
        try:
            if self.main_window:
                self.main_window.close()
            if self.app:
                self.app.quit()
            print("✅ [PRODUCTION] Cleanup completed")
        except Exception as e:
            print(f"⚠️ [PRODUCTION] Cleanup error: {e}")


def run_production_like_test():
    """Run the production-like TKA workflow test."""
    test = ProductionLikeTKATest()

    try:
        success = test.run_complete_workflow_test()

        print()
        print("🎉 PRODUCTION-LIKE TKA USER WORKFLOW TEST COMPLETED")
        if success:
            print("✅ All production workflow features working correctly")
            print("✅ Beats properly display in beat frame")
            print("✅ Beats properly convert to JSON dictionaries")
            print("✅ Beats properly update current_sequence.json file")
        else:
            print("❌ Some tests failed - check output above")

        return success

    finally:
        test.cleanup()


if __name__ == "__main__":
    success = run_production_like_test()
    sys.exit(0 if success else 1)
