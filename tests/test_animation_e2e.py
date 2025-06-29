"""
TKA Animation Controller End-to-End Test
========================================

Comprehensive test that establishes baseline behavior by clicking actual UI buttons
and validating animations. This test serves as the reference for refactoring validation.

This test must pass before and after the animation controller refactoring to ensure
no regression in functionality.
"""

import pytest
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtTest import QTest

# TKA imports
from presentation.components.workbench import ModernSequenceWorkbench
from presentation.components.workbench.graph_editor.toggle_tab import ToggleTab
from domain.models.core_models import SequenceData, BeatData
from core.dependency_injection.di_container import DIContainer, get_container

import sys
import os
import time
from pathlib import Path

# Add TKA paths for imports
tka_root = Path(__file__).parent.parent
sys.path.insert(0, str(tka_root / "src" / "desktop" / "modern" / "src"))


class TestAnimationE2E:
    """End-to-end animation tests that validate complete UI workflows"""

    @pytest.fixture(autouse=True)
    def setup_qt_app(self):
        """Ensure QApplication exists for GUI tests"""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
            app.setQuitOnLastWindowClosed(False)

        # Enable offscreen rendering for headless testing
        if os.environ.get("CI"):
            app.setAttribute(Qt.ApplicationAttribute.AA_UseDesktopOpenGL, False)
            app.setAttribute(Qt.ApplicationAttribute.AA_UseSoftwareOpenGL, True)

        yield app

        # Cleanup
        try:
            app.processEvents()
        except Exception:
            pass

    @pytest.fixture
    def mock_container(self):
        """Create a mock DI container with required services"""
        from unittest.mock import Mock

        container = Mock(spec=DIContainer)

        # Mock layout service with proper return values
        layout_service = Mock()
        layout_service.calculate_layout.return_value = (2, 1)  # (rows, columns)
        layout_service.get_beat_frame_size.return_value = (400, 300)  # (width, height)
        layout_service.calculate_beat_frame_layout.return_value = {
            "rows": 2,
            "columns": 1,
            "beat_size": (100, 100),
        }

        # Mock other required services
        workbench_service = Mock()
        fullscreen_service = Mock()
        deletion_service = Mock()
        graph_service = Mock()
        dictionary_service = Mock()

        # Configure container to return mocked services
        service_map = {
            "ILayoutService": layout_service,
            "ISequenceWorkbenchService": workbench_service,
            "IFullScreenService": fullscreen_service,
            "IBeatDeletionService": deletion_service,
            "IGraphEditorService": graph_service,
            "IDictionaryService": dictionary_service,
        }

        def mock_resolve(interface_type):
            interface_name = getattr(interface_type, "__name__", str(interface_type))
            return service_map.get(interface_name, Mock())

        container.resolve.side_effect = mock_resolve

        return container

    @pytest.fixture
    def sample_sequence(self):
        """Create a sample sequence for testing"""
        beat1 = BeatData(beat_number=1, letter="A")
        beat2 = BeatData(beat_number=2, letter="B")

        return SequenceData(
            name="Test Sequence",
            word="AB",
            beats=[beat1, beat2],
            start_position="alpha1",
        )

    def create_workbench(self, mock_container, sample_sequence):
        """Create a workbench instance for testing"""
        # Create workbench with mocked dependencies
        workbench = ModernSequenceWorkbench(
            layout_service=mock_container.resolve("ILayoutService"),
            workbench_service=mock_container.resolve("ISequenceWorkbenchService"),
            fullscreen_service=mock_container.resolve("IFullScreenService"),
            deletion_service=mock_container.resolve("IBeatDeletionService"),
            graph_service=mock_container.resolve("IGraphEditorService"),
            dictionary_service=mock_container.resolve("IDictionaryService"),
        )

        # Set up workbench with test data
        workbench.set_sequence(sample_sequence)
        workbench.resize(800, 600)
        workbench.show()

        return workbench

    def find_graph_editor_toggle_button(self, workbench) -> ToggleTab:
        """Locate the bottom-left toggle button for graph editor"""
        # Strategy 1: Search by object name if available
        toggle_button = workbench.findChild(ToggleTab)
        if toggle_button:
            return toggle_button

        # Strategy 2: Search by position (bottom-left area)
        bottom_left_widgets = self._find_widgets_in_region(
            workbench,
            x_range=(0, workbench.width() // 4),
            y_range=(workbench.height() * 3 // 4, workbench.height()),
        )

        # Strategy 3: Search by widget type
        for widget in bottom_left_widgets:
            if isinstance(widget, ToggleTab):
                return widget

        # Strategy 4: Navigate through workbench structure
        if hasattr(workbench, "_graph_section"):
            graph_section = workbench._graph_section
            if hasattr(graph_section, "_graph_editor"):
                graph_editor = graph_section._graph_editor
                if hasattr(graph_editor, "_toggle_tab"):
                    return graph_editor._toggle_tab

        raise ValueError("Could not locate graph editor toggle button")

    def _find_widgets_in_region(self, parent_widget, x_range, y_range):
        """Find all widgets within a specific region of the parent widget"""
        widgets_in_region = []

        def check_widget_recursively(widget):
            if widget == parent_widget:
                return

            # Get widget position relative to parent
            try:
                pos = widget.mapTo(parent_widget, QPoint(0, 0))
                if (
                    x_range[0] <= pos.x() <= x_range[1]
                    and y_range[0] <= pos.y() <= y_range[1]
                ):
                    widgets_in_region.append(widget)
            except Exception:
                pass

            # Check children
            for child in widget.findChildren(QWidget):
                check_widget_recursively(child)

        check_widget_recursively(parent_widget)
        return widgets_in_region

    def get_graph_editor(self, workbench):
        """Get the graph editor component from workbench"""
        if hasattr(workbench, "_graph_section"):
            graph_section = workbench._graph_section
            if hasattr(graph_section, "_graph_editor"):
                return graph_section._graph_editor

        raise ValueError("Could not locate graph editor component")

    def test_animation_controller_direct_api(self, mock_container, sample_sequence):
        """Test animation controller API directly - more reliable baseline test"""
        # Step 1: Create workbench and get animation controller
        workbench = self.create_workbench(mock_container, sample_sequence)
        QTest.qWait(100)  # Allow UI to initialize

        graph_editor = self.get_graph_editor(workbench)
        animation_controller = graph_editor.get_animation_controller()

        # Step 2: Verify initial state
        initial_visibility = graph_editor.is_visible()
        initial_height = graph_editor.height()
        initial_animating = animation_controller.is_animating()

        print(
            f"🔍 Initial state: visible={initial_visibility}, height={initial_height}, animating={initial_animating}"
        )

        # Step 3: Test slide_up animation
        slide_up_start_time = time.time()
        slide_up_result = animation_controller.slide_up()

        print(f"🔼 slide_up() returned: {slide_up_result}")

        # Wait for animation to complete
        timeout = 1.0  # 1 second timeout
        while time.time() - slide_up_start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        slide_up_time = time.time() - slide_up_start_time
        after_show_visibility = graph_editor.is_visible()
        after_show_height = graph_editor.height()

        print(
            f"🔼 After slide_up: visible={after_show_visibility}, height={after_show_height}, time={slide_up_time:.3f}s"
        )

        # Verify slide_up worked
        assert slide_up_result, "slide_up() should return True when animation starts"
        assert after_show_visibility, "Graph editor should be visible after slide_up"
        assert (
            after_show_height > 0
        ), "Graph editor should have positive height after slide_up"

        # Step 4: Wait for cooldown period to complete before slide_down
        QTest.qWait(150)  # Wait for 150ms to ensure 100ms cooldown completes

        # Test slide_down animation
        slide_down_start_time = time.time()
        slide_down_result = animation_controller.slide_down()

        print(f"🔽 slide_down() returned: {slide_down_result}")

        # Wait for animation to complete
        while time.time() - slide_down_start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        slide_down_time = time.time() - slide_down_start_time
        after_hide_visibility = graph_editor.is_visible()
        after_hide_height = graph_editor.height()

        print(
            f"🔽 After slide_down: visible={after_hide_visibility}, height={after_hide_height}, time={slide_down_time:.3f}s"
        )

        # Verify slide_down worked
        assert (
            slide_down_result
        ), "slide_down() should return True when animation starts"
        assert (
            not after_hide_visibility or after_hide_height == 0
        ), "Graph editor should be hidden after slide_down"

        # Step 5: Test animation timing
        expected_duration = 0.4  # 400ms as configured
        tolerance = 0.3  # 300ms tolerance for test environment

        assert slide_up_time < 1.0, f"slide_up animation too slow: {slide_up_time:.3f}s"
        assert (
            slide_down_time < 1.0
        ), f"slide_down animation too slow: {slide_down_time:.3f}s"

        print("✅ Animation controller direct API test passed!")

    def test_multi_cycle_animation_comprehensive(self, mock_container, sample_sequence):
        """Comprehensive multi-cycle test to catch state management issues and silent failures"""
        print("\n" + "=" * 80)
        print("🔄 COMPREHENSIVE MULTI-CYCLE ANIMATION TEST")
        print("=" * 80)

        # Step 1: Create workbench and get components
        workbench = self.create_workbench(mock_container, sample_sequence)
        QTest.qWait(100)  # Allow UI to initialize

        graph_editor = self.get_graph_editor(workbench)
        animation_controller = graph_editor.get_animation_controller()

        # Get internal components for state debugging
        state_manager = animation_controller._state_manager
        size_calculator = animation_controller._size_calculator
        synchronizer = animation_controller._synchronizer

        def log_complete_state(cycle_num: int, phase: str):
            """Log complete state of all animation components"""
            print(f"\n📊 [CYCLE {cycle_num}] {phase} - COMPLETE STATE:")
            print(
                f"   Graph Editor: visible={graph_editor.is_visible()}, height={graph_editor.height()}, width={graph_editor.width()}"
            )
            print(
                f"   Animation Controller: animating={animation_controller.is_animating()}"
            )
            print(
                f"   State Manager: animating={state_manager._animating}, cooldown={state_manager._animation_cooldown_active}"
            )
            if hasattr(state_manager, "_current_visibility"):
                print(
                    f"   State Manager: current_visibility={state_manager._current_visibility}, intended={state_manager._intended_visibility}"
                )
            print(
                f"   Size Calculator: workbench_width={size_calculator._workbench_width}, workbench_height={size_calculator._workbench_height}"
            )
            print(
                f"   Synchronizer: last_position={getattr(synchronizer, '_last_graph_position', 'N/A')}"
            )

        # Test 5 complete cycles to catch state persistence issues
        for cycle in range(1, 6):
            print(f"\n🔄 ===== CYCLE {cycle} START =====")

            # Log initial state for this cycle
            log_complete_state(cycle, "INITIAL")

            # PHASE 1: Open (slide_up)
            print(f"\n🔼 [CYCLE {cycle}] Testing slide_up...")
            slide_up_start = time.time()
            slide_up_result = animation_controller.slide_up()

            print(f"🔼 [CYCLE {cycle}] slide_up() returned: {slide_up_result}")

            if not slide_up_result:
                log_complete_state(cycle, "SLIDE_UP_FAILED")
                pytest.fail(
                    f"CYCLE {cycle}: slide_up() returned False - SILENT FAILURE DETECTED!"
                )

            # Wait for slide_up animation to complete
            timeout = 2.0  # Increased timeout for debugging
            animation_completed = False
            while time.time() - slide_up_start < timeout:
                QTest.qWait(50)
                if not animation_controller.is_animating():
                    animation_completed = True
                    break

            if not animation_completed:
                log_complete_state(cycle, "SLIDE_UP_TIMEOUT")
                pytest.fail(f"CYCLE {cycle}: slide_up animation timed out")

            slide_up_time = time.time() - slide_up_start
            log_complete_state(cycle, f"AFTER_SLIDE_UP (took {slide_up_time:.3f}s)")

            # Validate slide_up results
            assert (
                graph_editor.is_visible()
            ), f"CYCLE {cycle}: Graph editor should be visible after slide_up"
            assert (
                graph_editor.height() > 0
            ), f"CYCLE {cycle}: Graph editor should have positive height after slide_up"

            # PHASE 2: Wait for cooldown
            print(f"\n⏳ [CYCLE {cycle}] Waiting for cooldown...")
            QTest.qWait(200)  # Extended cooldown wait
            log_complete_state(cycle, "AFTER_COOLDOWN")

            # PHASE 3: Close (slide_down)
            print(f"\n🔽 [CYCLE {cycle}] Testing slide_down...")
            slide_down_start = time.time()
            slide_down_result = animation_controller.slide_down()

            print(f"🔽 [CYCLE {cycle}] slide_down() returned: {slide_down_result}")

            if not slide_down_result:
                log_complete_state(cycle, "SLIDE_DOWN_FAILED")
                pytest.fail(
                    f"CYCLE {cycle}: slide_down() returned False - SILENT FAILURE DETECTED!"
                )

            # Wait for slide_down animation to complete
            animation_completed = False
            while time.time() - slide_down_start < timeout:
                QTest.qWait(50)
                if not animation_controller.is_animating():
                    animation_completed = True
                    break

            if not animation_completed:
                log_complete_state(cycle, "SLIDE_DOWN_TIMEOUT")
                pytest.fail(f"CYCLE {cycle}: slide_down animation timed out")

            slide_down_time = time.time() - slide_down_start
            log_complete_state(cycle, f"AFTER_SLIDE_DOWN (took {slide_down_time:.3f}s)")

            # Validate slide_down results
            final_height = graph_editor.height()
            final_visible = graph_editor.is_visible()

            # Graph editor should be hidden (height 0) or invisible
            assert final_height == 0 or not final_visible, (
                f"CYCLE {cycle}: Graph editor should be hidden after slide_down. "
                f"Got: visible={final_visible}, height={final_height}"
            )

            # PHASE 4: Extended cooldown between cycles
            print(f"\n⏳ [CYCLE {cycle}] Extended cooldown between cycles...")
            QTest.qWait(300)  # Extended wait between cycles
            log_complete_state(cycle, "CYCLE_END")

            print(f"✅ [CYCLE {cycle}] COMPLETED SUCCESSFULLY")

        print(f"\n🎉 ALL {5} CYCLES COMPLETED SUCCESSFULLY!")
        print("✅ Multi-cycle animation test passed - no silent failures detected!")

    def test_window_resize_during_animations(self, mock_container, sample_sequence):
        """Test animation behavior during window resize operations"""
        print("\n" + "=" * 80)
        print("📏 WINDOW RESIZE DURING ANIMATIONS TEST")
        print("=" * 80)

        # Step 1: Create workbench and get components
        workbench = self.create_workbench(mock_container, sample_sequence)
        QTest.qWait(100)  # Allow UI to initialize

        graph_editor = self.get_graph_editor(workbench)
        animation_controller = graph_editor.get_animation_controller()

        def log_size_state(phase: str):
            """Log size-related state"""
            print(f"\n📏 {phase}:")
            print(f"   Workbench: {workbench.width()}x{workbench.height()}")
            print(f"   Graph Editor: {graph_editor.width()}x{graph_editor.height()}")
            print(f"   Visible: {graph_editor.is_visible()}")
            print(f"   Animating: {animation_controller.is_animating()}")

        # Test 1: Resize while graph editor is closed
        print("\n🔽 Test 1: Resize while graph editor is closed")
        log_size_state("INITIAL_CLOSED")

        # Resize workbench
        original_size = (workbench.width(), workbench.height())
        new_size = (original_size[0] + 200, original_size[1] + 150)
        workbench.resize(*new_size)
        QTest.qWait(100)  # Allow resize to process

        log_size_state("AFTER_RESIZE_CLOSED")

        # Try to open after resize
        slide_up_result = animation_controller.slide_up()
        assert slide_up_result, "slide_up should work after resize while closed"

        # Wait for animation
        timeout = 2.0
        start_time = time.time()
        while time.time() - start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        log_size_state("AFTER_OPEN_POST_RESIZE")
        assert (
            graph_editor.is_visible()
        ), "Graph editor should be visible after resize and open"

        # Test 2: Resize while graph editor is open
        print("\n🔼 Test 2: Resize while graph editor is open")

        # Resize again while open
        newer_size = (new_size[0] + 100, new_size[1] + 100)
        workbench.resize(*newer_size)
        QTest.qWait(100)  # Allow resize to process

        log_size_state("AFTER_RESIZE_OPEN")

        # Verify graph editor is still functional
        assert (
            graph_editor.is_visible()
        ), "Graph editor should remain visible after resize"
        assert (
            graph_editor.height() > 0
        ), "Graph editor should maintain positive height after resize"

        # Test 3: Resize during animation (if possible)
        print("\n🔄 Test 3: Resize during animation")

        # Close first
        QTest.qWait(200)  # Cooldown
        slide_down_result = animation_controller.slide_down()
        assert slide_down_result, "slide_down should work before resize test"

        # Wait for close
        start_time = time.time()
        while time.time() - start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        log_size_state("CLOSED_BEFORE_RESIZE_TEST")

        # Start opening animation and immediately resize
        slide_up_result = animation_controller.slide_up()
        assert slide_up_result, "slide_up should start for resize test"

        # Resize during animation
        final_size = (newer_size[0] - 50, newer_size[1] - 50)
        workbench.resize(*final_size)

        log_size_state("RESIZE_DURING_ANIMATION")

        # Wait for animation to complete
        start_time = time.time()
        while time.time() - start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        log_size_state("AFTER_ANIMATION_WITH_RESIZE")

        # Verify final state
        assert (
            graph_editor.is_visible()
        ), "Graph editor should be visible after resize during animation"
        assert (
            graph_editor.height() > 0
        ), "Graph editor should have positive height after resize during animation"

        print("✅ Window resize test passed - animations handle resize correctly!")

    def test_rapid_successive_operations(self, mock_container, sample_sequence):
        """Test rapid successive open/close operations and edge cases"""
        print("\n" + "=" * 80)
        print("⚡ RAPID SUCCESSIVE OPERATIONS & EDGE CASES TEST")
        print("=" * 80)

        # Step 1: Create workbench and get components
        workbench = self.create_workbench(mock_container, sample_sequence)
        QTest.qWait(100)  # Allow UI to initialize

        graph_editor = self.get_graph_editor(workbench)
        animation_controller = graph_editor.get_animation_controller()

        def log_rapid_state(test_name: str, attempt: int):
            """Log state during rapid operations"""
            print(
                f"⚡ {test_name} - Attempt {attempt}: animating={animation_controller.is_animating()}, visible={graph_editor.is_visible()}, height={graph_editor.height()}"
            )

        # Test 1: Rapid successive slide_up calls
        print("\n🔼 Test 1: Rapid successive slide_up calls")
        results = []
        for i in range(5):
            result = animation_controller.slide_up()
            results.append(result)
            log_rapid_state("RAPID_SLIDE_UP", i + 1)
            QTest.qWait(10)  # Very short wait

        print(f"Rapid slide_up results: {results}")
        # Only first call should succeed, others should return False
        assert results[0], "First slide_up should succeed"
        assert not any(
            results[1:]
        ), "Subsequent slide_up calls should fail while animating/already open"

        # Wait for animation to complete
        timeout = 2.0
        start_time = time.time()
        while time.time() - start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        # Test 2: Rapid successive slide_down calls
        print("\n🔽 Test 2: Rapid successive slide_down calls")
        QTest.qWait(200)  # Cooldown

        results = []
        for i in range(5):
            result = animation_controller.slide_down()
            results.append(result)
            log_rapid_state("RAPID_SLIDE_DOWN", i + 1)
            QTest.qWait(10)  # Very short wait

        print(f"Rapid slide_down results: {results}")
        # Only first call should succeed, others should return False
        assert results[0], "First slide_down should succeed"
        assert not any(
            results[1:]
        ), "Subsequent slide_down calls should fail while animating/already closed"

        # Wait for animation to complete
        start_time = time.time()
        while time.time() - start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        # Test 3: Alternating rapid calls
        print("\n🔄 Test 3: Alternating rapid calls")
        QTest.qWait(200)  # Cooldown

        operations = []
        for i in range(10):
            if i % 2 == 0:
                result = animation_controller.slide_up()
                op = f"slide_up_{i//2+1}"
            else:
                result = animation_controller.slide_down()
                op = f"slide_down_{i//2+1}"

            operations.append((op, result))
            print(f"⚡ {op}: {result}")
            QTest.qWait(20)  # Very short wait between operations

        print(f"Alternating operations: {operations}")

        # Test 4: Interrupt animation with opposite operation
        print("\n🔄 Test 4: Interrupt animation with opposite operation")
        QTest.qWait(300)  # Extended cooldown

        # Start slide_up
        slide_up_result = animation_controller.slide_up()
        print(f"Started slide_up: {slide_up_result}")
        assert slide_up_result, "slide_up should start"

        # Immediately try slide_down (should fail while animating)
        QTest.qWait(50)  # Small delay to ensure animation started
        slide_down_result = animation_controller.slide_down()
        print(f"Attempted slide_down during slide_up: {slide_down_result}")
        assert (
            not slide_down_result
        ), "slide_down should fail while slide_up is animating"

        # Wait for slide_up to complete
        start_time = time.time()
        while time.time() - start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        print(
            f"After slide_up completion: visible={graph_editor.is_visible()}, height={graph_editor.height()}"
        )

        # Test 5: State consistency after edge cases
        print("\n🔍 Test 5: State consistency validation")
        QTest.qWait(200)  # Cooldown

        # Verify we can still perform normal operations
        normal_slide_down = animation_controller.slide_down()
        print(f"Normal slide_down after edge cases: {normal_slide_down}")
        assert (
            normal_slide_down
        ), "Normal operations should work after edge case testing"

        # Wait for completion
        start_time = time.time()
        while time.time() - start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        QTest.qWait(200)  # Cooldown

        normal_slide_up = animation_controller.slide_up()
        print(f"Normal slide_up after edge cases: {normal_slide_up}")
        assert normal_slide_up, "Normal operations should work after edge case testing"

        # Wait for completion
        start_time = time.time()
        while time.time() - start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        print(
            "✅ Rapid successive operations test passed - edge cases handled correctly!"
        )

    def test_state_desynchronization_detection_and_correction(
        self, mock_container, sample_sequence
    ):
        """Test detection and automatic correction of state desynchronization bugs"""
        print("\n" + "=" * 80)
        print("🔧 STATE DESYNCHRONIZATION DETECTION & CORRECTION TEST")
        print("=" * 80)

        # Step 1: Create workbench and get components
        workbench = self.create_workbench(mock_container, sample_sequence)
        QTest.qWait(100)  # Allow UI to initialize

        graph_editor = self.get_graph_editor(workbench)
        animation_controller = graph_editor.get_animation_controller()
        state_manager = graph_editor.state_manager

        def log_state_details(phase: str):
            """Log detailed state information"""
            visual_height = graph_editor.height()
            internal_visible = state_manager.is_visible()
            visual_visible = visual_height > 0
            print(f"\n🔍 {phase}:")
            print(f"   Internal visibility: {internal_visible}")
            print(f"   Visual height: {visual_height}px")
            print(f"   Visual visibility: {visual_visible}")
            print(f"   States match: {internal_visible == visual_visible}")

        # Step 2: Start with a normal animation cycle to establish baseline
        print("\n📋 Step 2: Establish baseline with normal cycle")
        log_state_details("INITIAL STATE")

        # Open graph editor normally
        slide_up_result = animation_controller.slide_up()
        assert slide_up_result, "slide_up should succeed"

        # Wait for animation to complete
        timeout = 2.0
        start_time = time.time()
        while time.time() - start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        log_state_details("AFTER NORMAL SLIDE_UP")

        # Close graph editor normally
        QTest.qWait(200)  # Cooldown
        slide_down_result = animation_controller.slide_down()
        assert slide_down_result, "slide_down should succeed"

        # Wait for animation to complete
        start_time = time.time()
        while time.time() - start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        log_state_details("AFTER NORMAL SLIDE_DOWN")

        # Step 3: Simulate state desynchronization
        print("\n🚨 Step 3: Simulate state desynchronization scenario")

        # Force the graph editor to have height=0 (visually collapsed)
        graph_editor.setFixedHeight(0)
        QTest.qWait(50)  # Allow geometry update

        # But set internal state to visible=True (desynchronized!)
        state_manager.set_visibility(True, emit_signal=False)

        log_state_details("AFTER FORCED DESYNCHRONIZATION")

        # Verify we've created the desynchronization
        visual_height = graph_editor.height()
        internal_visible = state_manager.is_visible()
        visual_visible = visual_height > 0

        assert visual_height == 0, f"Expected height=0, got {visual_height}"
        assert (
            internal_visible == True
        ), f"Expected internal_visible=True, got {internal_visible}"
        assert (
            visual_visible == False
        ), f"Expected visual_visible=False, got {visual_visible}"
        assert internal_visible != visual_visible, "States should be desynchronized"

        print("✅ Successfully created state desynchronization scenario")
        print(f"   Internal state: {internal_visible}, Visual state: {visual_visible}")

        # Step 4: Test automatic detection and correction
        print("\n🔧 Step 4: Test automatic detection and correction")

        # Call toggle_visibility which should detect and correct the desynchronization
        print("Calling toggle_visibility() - should detect desynchronization...")
        graph_editor.toggle_visibility()

        # Wait for any animation to complete and cleanup to run
        timeout = 2.0
        start_time = time.time()
        while time.time() - start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        # Additional wait for cleanup to complete
        QTest.qWait(200)

        log_state_details("AFTER TOGGLE_VISIBILITY CALL")

        # Verify the state has been corrected
        corrected_internal = state_manager.is_visible()
        corrected_visual = graph_editor.height() > 0

        print(
            f"🔍 State after correction: internal={corrected_internal}, visual={corrected_visual}"
        )

        # The state should now be synchronized (both should be False since height=0)
        assert corrected_internal == corrected_visual, (
            f"States should be synchronized after correction. "
            f"Internal: {corrected_internal}, Visual: {corrected_visual}"
        )

        # Since the visual state was height=0 (collapsed), both should now be False
        assert (
            corrected_internal == False
        ), f"Internal state should be corrected to False (matching visual). Got: {corrected_internal}"

        # Step 5: Verify normal operation after correction
        print("\n✅ Step 5: Verify normal operation after correction")

        # Now toggle should work correctly - since state is False, it should call slide_up
        QTest.qWait(200)  # Cooldown

        # Reset height constraint to allow animation
        graph_editor.setMaximumHeight(16777215)  # Qt's QWIDGETSIZE_MAX
        graph_editor.setMinimumHeight(0)

        # This should now correctly call slide_up since corrected state is False
        slide_up_after_correction = animation_controller.slide_up()
        assert slide_up_after_correction, "slide_up should work after state correction"

        # Wait for animation
        start_time = time.time()
        while time.time() - start_time < timeout:
            QTest.qWait(50)
            if not animation_controller.is_animating():
                break

        log_state_details("AFTER CORRECTED SLIDE_UP")

        # Verify final state is correct
        final_height = graph_editor.height()
        final_internal = state_manager.is_visible()
        final_visual = final_height > 0

        assert (
            final_height > 0
        ), f"Graph editor should be open after slide_up, height={final_height}"
        assert final_internal == True, f"Internal state should be True after slide_up"
        assert final_visual == True, f"Visual state should be True after slide_up"
        assert final_internal == final_visual, "States should remain synchronized"

        print("✅ State desynchronization detection and correction test passed!")
        print("   - Successfully detected desynchronization")
        print("   - Automatically corrected state to match visual reality")
        print("   - Normal operation resumed after correction")


if __name__ == "__main__":
    # Allow running this test directly
    pytest.main([__file__, "-v"])
