#!/usr/bin/env python3
"""
Comprehensive test to verify manual scaling is working correctly.
Tests actual scene sizes vs container sizes and identifies scaling issues.
"""

import os
import sys

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def comprehensive_scaling_test():
    """Comprehensive test of pictograph scaling in start position components."""

    print("🧪 COMPREHENSIVE SCALING TEST")
    print("=" * 60)

    # Create QApplication
    app = QApplication(sys.argv)

    # Initialize core services and DI container
    print("🔧 Initializing core services...")
    from desktop.modern.core.service_locator import initialize_services

    initialize_services()

    print("🔧 Creating production application container...")
    from desktop.modern.core.application.application_factory import ApplicationFactory

    container = ApplicationFactory.create_production_app()

    # Create a test window that simulates the main application
    window = QMainWindow()
    window.setWindowTitle("Comprehensive Scaling Test")
    window.resize(1200, 800)  # Realistic main window size

    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    window.setCentralWidget(central_widget)

    # Test components
    test_components = []

    def create_start_position_view():
        """Create and test StartPositionView."""
        print("\n📍 TESTING START POSITION VIEW")
        print("-" * 40)

        from desktop.modern.presentation.components.sequence_workbench.sequence_beat_frame.start_position_view import (
            StartPositionView,
        )

        start_pos_view = StartPositionView()
        start_pos_view.setFixedSize(150, 150)  # Typical size in beat frame
        layout.addWidget(start_pos_view)

        test_components.append(
            {
                "name": "StartPositionView",
                "widget": start_pos_view,
                "expected_size": 150,
                "type": "basic",
            }
        )

        return start_pos_view

    def create_start_position_options():
        """Create and test StartPositionOption components."""
        print("\n📍 TESTING START POSITION OPTIONS")
        print("-" * 40)

        try:
            from desktop.modern.presentation.components.start_position_picker.start_position_option import (
                StartPositionOption,
            )

            # Get required services from DI container
            pool_manager = container.pictograph_pool_manager
            data_service = container.start_position_data_service

            # Create multiple options to test different sizes
            option_sizes = [120, 100, 80]  # Different container sizes
            options = []

            for i, size in enumerate(option_sizes):
                position_key = f"alpha{i+1}_alpha{i+1}"
                option = StartPositionOption(
                    position_key=position_key,
                    pool_manager=pool_manager,
                    data_service=data_service,
                )
                option.setFixedSize(size, size)
                layout.addWidget(option)

                test_components.append(
                    {
                        "name": f"StartPositionOption_{size}px",
                        "widget": option,
                        "expected_size": size,
                        "type": "advanced" if size < 150 else "basic",
                    }
                )
                options.append(option)

            print(f"   ✅ Created {len(options)} StartPositionOption components")
            return options

        except Exception as e:
            print(f"   ❌ Failed to create StartPositionOption components: {e}")
            return []

    def measure_scaling(component_info):
        """Measure actual scaling vs expected for a component."""
        widget = component_info["widget"]
        name = component_info["name"]
        expected_size = component_info["expected_size"]
        scaling_type = component_info["type"]

        print(f"\n🔍 MEASURING: {name}")

        # Find the pictograph component
        pictograph_component = None
        if hasattr(widget, "_pictograph_component") and widget._pictograph_component:
            pictograph_component = widget._pictograph_component
        elif hasattr(widget, "pictograph_widget") and widget.pictograph_widget:
            pictograph_component = widget.pictograph_widget

        if not pictograph_component:
            print(f"   ❌ No pictograph component found")
            return False

        # Get the graphics view
        graphics_view = None
        if hasattr(pictograph_component, "_view"):
            graphics_view = pictograph_component._view
        elif hasattr(pictograph_component, "view"):
            graphics_view = pictograph_component.view

        if not graphics_view:
            print(f"   ❌ No graphics view found")
            return False

        # Get scene
        scene = graphics_view.scene()
        if not scene:
            print(f"   ❌ No scene found")
            return False

        # Measure sizes
        widget_size = widget.size()
        view_size = graphics_view.size()
        scene_rect = scene.sceneRect()
        transform = graphics_view.transform()

        print(f"   📏 Widget size: {widget_size.width()}x{widget_size.height()}")
        print(f"   📏 View size: {view_size.width()}x{view_size.height()}")
        print(f"   📏 Scene rect: {scene_rect.width():.1f}x{scene_rect.height():.1f}")
        print(f"   📏 Transform scale: {transform.m11():.3f}x{transform.m22():.3f}")

        # Calculate expected scale based on legacy formula
        main_window_width = window.width()
        if scaling_type == "advanced":
            target_size = main_window_width // 12
        else:
            target_size = main_window_width // 10

        border_width = max(1, int(target_size * 0.015))
        target_size = target_size - (2 * border_width)

        expected_scale = (
            target_size / max(scene_rect.width(), scene_rect.height())
            if scene_rect.width() > 0
            else 0
        )
        actual_scale = transform.m11()

        print(f"   🎯 Expected target size: {target_size}px ({scaling_type} mode)")
        print(f"   🎯 Expected scale: {expected_scale:.3f}")
        print(f"   🎯 Actual scale: {actual_scale:.3f}")

        # Check if scaling is correct (within 10% tolerance)
        scale_diff = abs(expected_scale - actual_scale)
        scale_tolerance = expected_scale * 0.1
        is_correct = scale_diff <= scale_tolerance

        if is_correct:
            print(f"   ✅ Scaling is correct (diff: {scale_diff:.3f})")
        else:
            print(
                f"   ❌ Scaling is incorrect (diff: {scale_diff:.3f}, tolerance: {scale_tolerance:.3f})"
            )

        # Check if scene fits properly in view
        scaled_scene_width = scene_rect.width() * actual_scale
        scaled_scene_height = scene_rect.height() * actual_scale
        view_width = view_size.width()
        view_height = view_size.height()

        fits_width = scaled_scene_width <= view_width
        fits_height = scaled_scene_height <= view_height

        print(f"   📦 Scaled scene: {scaled_scene_width:.1f}x{scaled_scene_height:.1f}")
        print(f"   📦 Fits in view: width={fits_width}, height={fits_height}")

        return is_correct and fits_width and fits_height

    def load_test_data():
        """Load test pictograph data into components."""
        print("\n🔧 LOADING TEST DATA")
        print("-" * 40)

        try:
            # Create minimal test beat data
            from domain.enums.grid_mode import GridMode
            from desktop.modern.domain.models.beat_data import BeatData
            from desktop.modern.domain.models.grid_data import GridData
            from desktop.modern.domain.models.pictograph_data import PictographData

            grid_data = GridData(
                grid_mode=GridMode.DIAMOND,
                center_x=0.0,
                center_y=0.0,
                radius=100.0,
                grid_points={},
            )

            pictograph_data = PictographData(
                grid_data=grid_data,
                arrows={},
                props={},
                motions={},
                letter="α",
                start_position="alpha1_alpha1",
                end_position="alpha1",
                glyph_data=None,
                is_blank=False,
                is_mirrored=False,
                metadata={"source": "test"},
            )

            beat_data = BeatData(
                beat_number=1,
                duration=1.0,
                blue_reversal=False,
                red_reversal=False,
                is_blank=False,
                pictograph_data=pictograph_data,
                metadata={"source": "test"},
            )

            # Load data into start position view
            for component_info in test_components:
                if "StartPositionView" in component_info["name"]:
                    widget = component_info["widget"]
                    if hasattr(widget, "set_beat_data"):
                        widget.set_beat_data(beat_data)
                        print(f"   ✅ Loaded data into {component_info['name']}")

            print("   ✅ Test data loaded successfully")
            return True

        except Exception as e:
            print(f"   ❌ Failed to load test data: {e}")
            return False

    def run_scaling_tests():
        """Run scaling tests on all components."""
        print("\n🧪 RUNNING SCALING TESTS")
        print("=" * 60)

        results = []

        for component_info in test_components:
            # Force a resize to trigger scaling
            widget = component_info["widget"]
            current_size = widget.size()

            # Trigger resize event
            resize_event = QResizeEvent(current_size, current_size)
            widget.resizeEvent(resize_event)

            # Measure scaling
            is_correct = measure_scaling(component_info)
            results.append({"name": component_info["name"], "correct": is_correct})

        return results

    def print_summary(results):
        """Print test summary."""
        print("\n📊 TEST SUMMARY")
        print("=" * 60)

        passed = sum(1 for r in results if r["correct"])
        total = len(results)

        for result in results:
            status = "✅ PASS" if result["correct"] else "❌ FAIL"
            print(f"   {status}: {result['name']}")

        print(f"\n🎯 OVERALL: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 ALL TESTS PASSED!")
        else:
            print("⚠️  SOME TESTS FAILED - Manual scaling needs fixes")

    # Create test components
    start_pos_view = create_start_position_view()
    start_pos_options = create_start_position_options()

    # Show window
    window.show()

    def run_tests():
        """Run the actual tests after window is shown."""
        print("\n🚀 STARTING TESTS...")

        # Load test data
        data_loaded = load_test_data()

        # Wait a bit for rendering
        QTimer.singleShot(500, lambda: [run_and_summarize()])

    def run_and_summarize():
        """Run tests and print summary."""
        results = run_scaling_tests()
        print_summary(results)

        # Exit after tests
        QTimer.singleShot(2000, app.quit)

    # Start tests after window is shown
    QTimer.singleShot(1000, run_tests)

    print("🚀 Starting comprehensive scaling test...")
    print("📝 This will test actual scene sizes vs container sizes...")

    # Run the application
    app.exec()

    print("\n✅ Comprehensive scaling test completed")


if __name__ == "__main__":
    comprehensive_scaling_test()
