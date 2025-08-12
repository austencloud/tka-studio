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
from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import sys
from typing import Any


# Add the modern src directory to Python path
modern_src = Path(__file__).parent.parent.parent / "src"
if str(modern_src) not in sys.path:
    sys.path.insert(0, str(modern_src))


# Import TKA application components
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QMainWindow

from core.application.application_factory import ApplicationFactory


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

        # Scaling diagnosis tracking
        self.scaling_log = []
        self.enable_scaling_diagnosis = True

    def log_scaling_event(
        self, view_type: str, event: str, view_widget, additional_info: str = ""
    ):
        """Log detailed scaling information for diagnosis"""
        if not self.enable_scaling_diagnosis:
            return

        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        # Extract scaling information
        scale_info = self._extract_scaling_info(view_widget)
        overlay_info = self._extract_overlay_info(view_widget)
        transform_info = self._extract_transform_info(view_widget)

        # Format log entry
        log_entry = (
            f"[{timestamp}] [{view_type}] [{event}] "
            f"Scale: {scale_info['scale_factor']:.3f}, "
            f"Overlay: {overlay_info['mode']}, "
            f"Border: {overlay_info['border_color']}, "
            f"Transform: {transform_info['matrix_str']}"
        )

        if additional_info:
            log_entry += f" | {additional_info}"

        # Store and print
        self.scaling_log.append(
            {
                "timestamp": timestamp,
                "view_type": view_type,
                "event": event,
                "scale_info": scale_info,
                "overlay_info": overlay_info,
                "transform_info": transform_info,
                "additional_info": additional_info,
                "log_entry": log_entry,
            }
        )

        print(log_entry)

    def _extract_scaling_info(self, view_widget) -> dict[str, Any]:
        """Extract scaling information from view widget"""
        try:
            if (
                hasattr(view_widget, "_selection_overlay")
                and view_widget._selection_overlay
            ):
                overlay = view_widget._selection_overlay
                expected_scale = (
                    overlay.SCALE_COMPENSATION
                    if (overlay._is_selection_mode or overlay._is_hover_mode)
                    else 1.0
                )
                return {
                    "scale_factor": expected_scale,
                    "compensation_factor": overlay.SCALE_COMPENSATION,
                    "is_scaled": overlay._is_selection_mode or overlay._is_hover_mode,
                }
            return {
                "scale_factor": 1.0,
                "compensation_factor": "N/A",
                "is_scaled": False,
            }
        except Exception as e:
            return {
                "scale_factor": "ERROR",
                "compensation_factor": "ERROR",
                "is_scaled": "ERROR",
                "error": str(e),
            }

    def _extract_overlay_info(self, view_widget) -> dict[str, Any]:
        """Extract overlay state information"""
        try:
            if (
                hasattr(view_widget, "_selection_overlay")
                and view_widget._selection_overlay
            ):
                overlay = view_widget._selection_overlay

                # Determine mode
                if overlay._is_selection_mode:
                    mode = "SELECTION"
                elif overlay._is_hover_mode:
                    mode = "HOVER"
                else:
                    mode = "NORMAL"

                # Determine border color
                if overlay._current_border_color:
                    if overlay._current_border_color == overlay.SELECTION_COLOR:
                        border_color = "GOLD"
                    elif overlay._current_border_color == overlay.HOVER_COLOR:
                        border_color = "BLUE"
                    else:
                        border_color = f"CUSTOM({overlay._current_border_color.name()})"
                else:
                    border_color = "NONE"

                return {
                    "mode": mode,
                    "border_color": border_color,
                    "is_visible": overlay.isVisible(),
                    "selection_mode": overlay._is_selection_mode,
                    "hover_mode": overlay._is_hover_mode,
                }
            return {
                "mode": "NO_OVERLAY",
                "border_color": "NONE",
                "is_visible": False,
                "selection_mode": False,
                "hover_mode": False,
            }
        except Exception as e:
            return {
                "mode": "ERROR",
                "border_color": "ERROR",
                "is_visible": "ERROR",
                "error": str(e),
            }

    def _extract_transform_info(self, view_widget) -> dict[str, Any]:
        """Extract transform matrix information"""
        try:
            if (
                hasattr(view_widget, "_pictograph_component")
                and view_widget._pictograph_component
            ):
                transform = view_widget._pictograph_component.transform()

                # Extract matrix values
                m11, m12, m13 = transform.m11(), transform.m12(), transform.m13()
                m21, m22, m23 = transform.m21(), transform.m22(), transform.m23()
                m31, m32, m33 = transform.m31(), transform.m32(), transform.m33()

                # Check if it's identity
                is_identity = transform.isIdentity()

                # Calculate effective scale (assuming uniform scaling)
                scale_x = (m11**2 + m21**2) ** 0.5
                scale_y = (m12**2 + m22**2) ** 0.5

                return {
                    "matrix_str": f"[{m11:.3f},{m12:.3f},{m21:.3f},{m22:.3f}]",
                    "is_identity": is_identity,
                    "scale_x": scale_x,
                    "scale_y": scale_y,
                    "effective_scale": (scale_x + scale_y) / 2,
                    "full_matrix": [m11, m12, m13, m21, m22, m23, m31, m32, m33],
                }
            return {
                "matrix_str": "NO_COMPONENT",
                "is_identity": "N/A",
                "scale_x": "N/A",
                "scale_y": "N/A",
                "effective_scale": "N/A",
            }
        except Exception as e:
            return {"matrix_str": "ERROR", "is_identity": "ERROR", "error": str(e)}

    def diagnose_beat_frame_scaling(self):
        """Diagnose scaling issues in the beat frame"""
        print("\n🔍 [SCALING_DIAGNOSIS] Analyzing beat frame scaling...")

        try:
            if not self.workbench:
                print("❌ [SCALING_DIAGNOSIS] No workbench available")
                return

            # Navigate to beat frame
            beat_frame = None
            if hasattr(self.workbench, "_beat_frame_section"):
                beat_frame_section = self.workbench._beat_frame_section
                if hasattr(beat_frame_section, "_beat_frame"):
                    beat_frame = beat_frame_section._beat_frame

            if not beat_frame:
                print("❌ [SCALING_DIAGNOSIS] Could not access beat frame")
                return

            # Get sequence data - try multiple approaches
            sequence_data = None
            if hasattr(beat_frame, "_sequence_data"):
                sequence_data = beat_frame._sequence_data
            elif hasattr(beat_frame, "sequence_data"):
                sequence_data = beat_frame.sequence_data
            elif hasattr(beat_frame, "_sequence"):
                sequence_data = beat_frame._sequence

            if not sequence_data:
                print("❌ [SCALING_DIAGNOSIS] No sequence data in beat frame")
                print("🔍 [SCALING_DIAGNOSIS] Available beat frame attributes:")
                attrs = [attr for attr in dir(beat_frame) if not attr.startswith("__")]
                for attr in attrs[:10]:  # Show first 10 attributes
                    print(f"   - {attr}")
                print("   ... (truncated)")

                # Try to proceed with beat views anyway
                print("🔍 [SCALING_DIAGNOSIS] Proceeding with beat view analysis...")
            else:
                print(
                    f"✅ [SCALING_DIAGNOSIS] Found sequence with {len(sequence_data.beats)} beats"
                )

            # Analyze start position view
            if hasattr(beat_frame, "_start_position_view"):
                start_view = beat_frame._start_position_view
                self.log_scaling_event(
                    "START_POSITION",
                    "INITIAL_STATE",
                    start_view,
                    "Analyzing initial state",
                )

                # Test hover and selection on start position
                print("🔍 [SCALING_DIAGNOSIS] Testing start position scaling...")
                start_view.set_highlighted(True)
                self.log_scaling_event(
                    "START_POSITION", "HOVER_APPLIED", start_view, "Hover state applied"
                )

                start_view.set_selected(True)
                self.log_scaling_event(
                    "START_POSITION",
                    "SELECTION_APPLIED",
                    start_view,
                    "Selection state applied",
                )

                start_view.set_selected(False)
                start_view.set_highlighted(False)
                self.log_scaling_event(
                    "START_POSITION",
                    "RESET_TO_NORMAL",
                    start_view,
                    "Reset to normal state",
                )

            # Analyze beat views - try multiple approaches
            beat_views = []
            if hasattr(beat_frame, "_beat_views"):
                beat_views = beat_frame._beat_views
            elif hasattr(beat_frame, "beat_views"):
                beat_views = beat_frame.beat_views
            elif hasattr(beat_frame, "_views"):
                beat_views = beat_frame._views

            if beat_views:
                print(f"✅ [SCALING_DIAGNOSIS] Found {len(beat_views)} beat views")

                # Test only visible beat views
                visible_beat_views = [bv for bv in beat_views if bv.isVisible()]
                print(
                    f"✅ [SCALING_DIAGNOSIS] Found {len(visible_beat_views)} visible beat views"
                )

                for i, beat_view in enumerate(
                    visible_beat_views[:3]
                ):  # Test first 3 visible beat views
                    print(f"🔍 [SCALING_DIAGNOSIS] Testing beat view {i+1} scaling...")

                    self.log_scaling_event(
                        f"BEAT_{i+1}",
                        "INITIAL_STATE",
                        beat_view,
                        "Analyzing initial state",
                    )

                    # Test hover
                    beat_view.set_highlighted(True)
                    self.log_scaling_event(
                        f"BEAT_{i+1}", "HOVER_APPLIED", beat_view, "Hover state applied"
                    )

                    # Test selection
                    beat_view.set_selected(True)
                    self.log_scaling_event(
                        f"BEAT_{i+1}",
                        "SELECTION_APPLIED",
                        beat_view,
                        "Selection state applied",
                    )

                    # Test hover while selected
                    beat_view.set_highlighted(True)
                    self.log_scaling_event(
                        f"BEAT_{i+1}",
                        "HOVER_WHILE_SELECTED",
                        beat_view,
                        "Hover while selected",
                    )

                    # Reset
                    beat_view.set_selected(False)
                    beat_view.set_highlighted(False)
                    self.log_scaling_event(
                        f"BEAT_{i+1}",
                        "RESET_TO_NORMAL",
                        beat_view,
                        "Reset to normal state",
                    )
            else:
                print("❌ [SCALING_DIAGNOSIS] No beat views found")
                print("🔍 [SCALING_DIAGNOSIS] Available beat frame attributes:")
                attrs = [attr for attr in dir(beat_frame) if "view" in attr.lower()]
                for attr in attrs:
                    print(f"   - {attr}")

            # Print scaling analysis summary
            self._print_scaling_analysis_summary()

        except Exception as e:
            print(f"❌ [SCALING_DIAGNOSIS] Error during scaling diagnosis: {e}")
            import traceback

            traceback.print_exc()

    def _print_scaling_analysis_summary(self):
        """Print summary of scaling analysis"""
        print("\n📊 [SCALING_DIAGNOSIS] SCALING ANALYSIS SUMMARY")
        print("=" * 60)

        # Group logs by view type
        view_types = {}
        for log_entry in self.scaling_log:
            view_type = log_entry["view_type"]
            if view_type not in view_types:
                view_types[view_type] = []
            view_types[view_type].append(log_entry)

        # Analyze each view type
        for view_type, logs in view_types.items():
            print(f"\n🔍 {view_type} Analysis:")

            # Check for scaling consistency
            initial_transforms = [
                log for log in logs if log["event"] == "INITIAL_STATE"
            ]
            hover_transforms = [log for log in logs if log["event"] == "HOVER_APPLIED"]
            selection_transforms = [
                log for log in logs if log["event"] == "SELECTION_APPLIED"
            ]

            if initial_transforms:
                initial_scale = initial_transforms[0]["transform_info"][
                    "effective_scale"
                ]
                print(f"   Initial Scale: {initial_scale}")

            if hover_transforms:
                hover_scale = hover_transforms[0]["transform_info"]["effective_scale"]
                print(f"   Hover Scale: {hover_scale}")

                if initial_transforms:
                    expected_hover = (
                        initial_scale * 0.98
                        if isinstance(initial_scale, (int, float))
                        else "N/A"
                    )
                    print(f"   Expected Hover Scale: {expected_hover}")

            if selection_transforms:
                selection_scale = selection_transforms[0]["transform_info"][
                    "effective_scale"
                ]
                print(f"   Selection Scale: {selection_scale}")

                if initial_transforms:
                    expected_selection = (
                        initial_scale * 0.98
                        if isinstance(initial_scale, (int, float))
                        else "N/A"
                    )
                    print(f"   Expected Selection Scale: {expected_selection}")

        print("\n🎯 [SCALING_DIAGNOSIS] Key Issues to Look For:")
        print("   • Initial scales should be consistent across similar views")
        print("   • Hover/Selection scales should be initial_scale * 0.98")
        print("   • Transforms should reset properly to initial state")
        print("   • No stacking of scaling effects")
        print("=" * 60)

    def test_hover_effects_comprehensive(self) -> bool:
        """Test hover effects across all TKA components to catch crashes"""
        print("\n🔍 [HOVER_TEST] Starting comprehensive hover effects testing...")

        try:
            # Test 1: Option Picker Hover Effects
            if not self._test_option_picker_hover_effects():
                return False

            # Test 2: Start Position Picker Hover Effects
            if not self._test_start_position_picker_hover_effects():
                return False

            # Test 3: Beat Frame Hover Effects
            if not self._test_beat_frame_hover_effects():
                return False

            print("✅ [HOVER_TEST] All hover effects testing completed successfully")
            return True

        except Exception as e:
            print(f"❌ [HOVER_TEST] Critical error during hover testing: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _test_option_picker_hover_effects(self) -> bool:
        """Test hover effects on option picker frames"""
        print("🔍 [HOVER_TEST] Testing option picker hover effects...")

        try:
            if not self.option_picker:
                print("❌ [HOVER_TEST] No option picker available")
                return False

            # Get option picker frames
            frames = self._get_option_picker_frames()
            if not frames:
                print("❌ [HOVER_TEST] No option picker frames found")
                return False

            print(f"✅ [HOVER_TEST] Found {len(frames)} option picker frames")

            # Test hover on first few frames
            for i, frame in enumerate(frames[:3]):
                print(f"🔍 [HOVER_TEST] Testing hover on option picker frame {i+1}...")

                try:
                    # Test programmatic hover
                    if hasattr(frame, "set_highlighted"):
                        frame.set_highlighted(True)
                        print(f"✅ [HOVER_TEST] Frame {i+1} hover applied successfully")

                        # Reset hover
                        frame.set_highlighted(False)
                        print(f"✅ [HOVER_TEST] Frame {i+1} hover reset successfully")
                    else:
                        print(
                            f"⚠️ [HOVER_TEST] Frame {i+1} missing set_highlighted method"
                        )

                    # Test selection overlay existence
                    if hasattr(frame, "_selection_overlay"):
                        if frame._selection_overlay:
                            print(f"✅ [HOVER_TEST] Frame {i+1} has selection overlay")
                        else:
                            print(
                                f"⚠️ [HOVER_TEST] Frame {i+1} selection overlay is None"
                            )
                    else:
                        print(
                            f"⚠️ [HOVER_TEST] Frame {i+1} missing _selection_overlay attribute"
                        )

                except Exception as e:
                    print(f"❌ [HOVER_TEST] Error testing frame {i+1}: {e}")
                    import traceback

                    traceback.print_exc()
                    return False

            print("✅ [HOVER_TEST] Option picker hover effects test completed")
            return True

        except Exception as e:
            print(f"❌ [HOVER_TEST] Error in option picker hover test: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _test_start_position_picker_hover_effects(self) -> bool:
        """Test hover effects on start position picker"""
        print("🔍 [HOVER_TEST] Testing start position picker hover effects...")

        try:
            # For now, we'll skip start position picker testing since it's not in the current workflow
            # but we can add it later when we have access to it
            print(
                "⚠️ [HOVER_TEST] Start position picker testing skipped (not in current workflow)"
            )
            return True

        except Exception as e:
            print(f"❌ [HOVER_TEST] Error in start position picker hover test: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _test_beat_frame_hover_effects(self) -> bool:
        """Test hover effects on beat frame views"""
        print("🔍 [HOVER_TEST] Testing beat frame hover effects...")

        try:
            if not self.workbench:
                print("❌ [HOVER_TEST] No workbench available")
                return False

            # Get beat frame
            beat_frame = self._get_beat_frame()
            if not beat_frame:
                print("❌ [HOVER_TEST] No beat frame available")
                return False

            # Test start position view hover
            if hasattr(beat_frame, "_start_position_view"):
                start_view = beat_frame._start_position_view
                if start_view and start_view.isVisible():
                    print("🔍 [HOVER_TEST] Testing start position view hover...")
                    try:
                        start_view.set_highlighted(True)
                        print(
                            "✅ [HOVER_TEST] Start position hover applied successfully"
                        )
                        start_view.set_highlighted(False)
                        print("✅ [HOVER_TEST] Start position hover reset successfully")
                    except Exception as e:
                        print(f"❌ [HOVER_TEST] Start position hover error: {e}")
                        return False

            # Test beat views hover
            if hasattr(beat_frame, "_beat_views"):
                beat_views = beat_frame._beat_views
                visible_beat_views = [bv for bv in beat_views if bv.isVisible()]

                print(
                    f"✅ [HOVER_TEST] Found {len(visible_beat_views)} visible beat views"
                )

                for i, beat_view in enumerate(visible_beat_views[:3]):
                    print(f"🔍 [HOVER_TEST] Testing beat view {i+1} hover...")
                    try:
                        beat_view.set_highlighted(True)
                        print(
                            f"✅ [HOVER_TEST] Beat view {i+1} hover applied successfully"
                        )
                        beat_view.set_highlighted(False)
                        print(
                            f"✅ [HOVER_TEST] Beat view {i+1} hover reset successfully"
                        )
                    except Exception as e:
                        print(f"❌ [HOVER_TEST] Beat view {i+1} hover error: {e}")
                        return False

            print("✅ [HOVER_TEST] Beat frame hover effects test completed")
            return True

        except Exception as e:
            print(f"❌ [HOVER_TEST] Error in beat frame hover test: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _get_option_picker_frames(self):
        """Get all clickable pictograph frames from option picker"""
        try:
            if not self.option_picker:
                return []

            # Get the widget
            if hasattr(self.option_picker, "widget") and self.option_picker.widget:
                container = self.option_picker.widget
            else:
                container = self.option_picker

            # Find all ClickablePictographFrame widgets
            from presentation.components.option_picker.components.frames.clickable_pictograph_frame import (
                ClickablePictographFrame,
            )

            frames = []
            for child in container.findChildren(ClickablePictographFrame):
                if child.isVisible():
                    frames.append(child)

            return frames

        except Exception as e:
            print(f"❌ [HOVER_TEST] Error getting option picker frames: {e}")
            return []

    def _get_beat_frame(self):
        """Get the beat frame from workbench"""
        try:
            if not self.workbench:
                return None

            # Navigate to beat frame
            beat_frame = None
            if hasattr(self.workbench, "_beat_frame_section"):
                beat_frame_section = self.workbench._beat_frame_section
                if hasattr(beat_frame_section, "_beat_frame"):
                    beat_frame = beat_frame_section._beat_frame

            return beat_frame

        except Exception as e:
            print(f"❌ [HOVER_TEST] Error getting beat frame: {e}")
            return None

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
            with open(self.current_sequence_file, encoding="utf-8") as f:
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
                print(
                    "❌ [PRODUCTION] Start position picker options not accessible"
                )
                return False
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
                    print(
                        f"❌ [PRODUCTION] Beat frame beat count mismatch: expected {expected_beat_count}, got {actual_beat_count}"
                    )
                    return False
                print("❌ [PRODUCTION] Beat frame sequence not accessible")
                return False
            print(
                "❌ [PRODUCTION] Beat frame not accessible - checking attribute structure..."
            )
            # Debug: Show what attributes are actually available
            if hasattr(self.workbench, "_beat_frame_section"):
                print("🔍 [PRODUCTION] Workbench has _beat_frame_section")
                beat_frame_section = self.workbench._beat_frame_section
                if hasattr(beat_frame_section, "_beat_frame"):
                    print("🔍 [PRODUCTION] Beat frame section has _beat_frame")
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
                from domain.models import SequenceData

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

            print("📄 [PRODUCTION] Final sequence file contents:")
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

            # Step 7: Test hover effects across all components
            print("🔍 [PRODUCTION] Testing hover effects across all components...")
            if not self.test_hover_effects_comprehensive():
                print("❌ [PRODUCTION] Hover effects testing failed")
                return False

            # Step 8: Diagnose scaling system with real pictograph data
            print(
                "🔍 [PRODUCTION] Running scaling diagnosis with real pictograph data..."
            )
            self.diagnose_beat_frame_scaling()

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
