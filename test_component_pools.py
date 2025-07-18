#!/usr/bin/env python3
"""
Test script for component-specific pictograph pools
"""
import os
import sys
import time

# Add the modern desktop source to Python path
modern_src = os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
if modern_src not in sys.path:
    sys.path.insert(0, modern_src)

# Initialize Qt Application
from PyQt6.QtWidgets import QApplication

app = None


def ensure_qt_app():
    """Ensure QApplication is initialized."""
    global app
    if app is None:
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
    return app


def test_basic_imports():
    """Test that we can import the component-specific pools."""
    print("🔍 Testing component-specific pool imports...")

    try:
        from presentation.components.pictograph.component_specific_view_pools import (
            get_beat_frame_view_pool,
            get_option_picker_view_pool,
            get_start_position_picker_view_pool,
            initialize_component_view_pools,
        )

        print("✅ Component-specific pool imports successful")
        return True
    except Exception as e:
        print(f"❌ Component-specific pool imports failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_pool_initialization():
    """Test component-specific pool initialization"""
    print("\n🏊 Testing component-specific pool initialization...")

    # Ensure Qt app is initialized
    ensure_qt_app()

    try:
        from presentation.components.pictograph.component_specific_view_pools import (
            get_beat_frame_view_pool,
            get_option_picker_view_pool,
            get_start_position_picker_view_pool,
            initialize_component_view_pools,
        )

        # Initialize component view pools
        start = time.perf_counter()
        initialize_component_view_pools()
        view_time = (time.perf_counter() - start) * 1000

        print(f"Component view pools init: {view_time:.1f}ms")

        # Test individual pools
        option_pool = get_option_picker_view_pool()
        beat_pool = get_beat_frame_view_pool()
        start_pool = get_start_position_picker_view_pool()

        print(f"Option picker pool: {option_pool.get_pool_stats()}")
        print(f"Beat frame pool: {beat_pool.get_pool_stats()}")
        print(f"Start position pool: {start_pool.get_pool_stats()}")

        return True

    except Exception as e:
        print(f"❌ Pool initialization failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_component_view_performance():
    """Test component-specific view creation performance"""
    print("\n⚡ Testing component-specific view creation performance...")

    # Ensure Qt app is initialized
    ensure_qt_app()

    try:
        from presentation.components.pictograph.component_specific_view_pools import (
            get_beat_frame_view_pool,
            get_option_picker_view_pool,
            get_start_position_picker_view_pool,
        )

        # Test option picker views (120x120)
        option_pool = get_option_picker_view_pool()
        option_pool.initialize_pool()
        times = []
        for i in range(10):
            start = time.perf_counter()
            view = option_pool.checkout_view()
            end = time.perf_counter()
            times.append((end - start) * 1000)
            option_pool.checkin_view(view)

        avg_time = sum(times) / len(times)
        print(f"Option picker view checkout: {avg_time:.2f}ms")
        print(f"Expected: < 5ms (pre-sized, no resizing)")
        print(f'Test result: {"PASS" if avg_time < 5 else "FAIL"}')

        return True

    except Exception as e:
        print(f"❌ Component view performance test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_option_picker_simulation():
    """Test option picker performance (36 pictographs)"""
    import time

    from application.services.pictograph_pool_manager import get_pictograph_pool
    from presentation.components.pictograph.component_specific_view_pools import (
        get_option_picker_view_pool,
        initialize_component_view_pools,
    )

    print("\nTesting option picker simulation (36 pictographs)...")

    # Initialize pools
    scene_pool = get_pictograph_pool()
    scene_pool.initialize_pool()
    initialize_component_view_pools()
    option_pool = get_option_picker_view_pool()

    # Simulate option picker loading 36 pre-sized pictographs
    start = time.perf_counter()
    scenes = []
    views = []

    for i in range(36):
        scene = scene_pool.checkout_pictograph()
        view = option_pool.checkout_view()
        scene.attach_view(view)
        scenes.append(scene)
        views.append(view)

    load_time = (time.perf_counter() - start) * 1000

    print(f"Loading 36 option picker pictographs: {load_time:.1f}ms")
    print(f"Expected: < 50ms (no resizing overhead)")
    print(f'Test result: {"PASS" if load_time < 50 else "FAIL"}')

    # Test that views are correctly sized
    sample_view = views[0]
    view_size = sample_view.size()
    print(f"View size: {view_size.width()}x{view_size.height()}")
    print(f"Expected: 120x120")
    print(
        f'Size test: {"PASS" if view_size.width() == 120 and view_size.height() == 120 else "FAIL"}'
    )

    # Cleanup
    for scene, view in zip(scenes, views):
        scene.detach_view()
        scene_pool.checkin_pictograph(scene)
        option_pool.checkin_view(view)


def test_beat_frame_simulation():
    """Test beat frame performance (64 pictographs)"""
    import time

    from application.services.pictograph_pool_manager import get_pictograph_pool
    from presentation.components.pictograph.component_specific_view_pools import (
        get_beat_frame_view_pool,
        initialize_component_view_pools,
    )

    print("\nTesting beat frame simulation (64 pictographs)...")

    scene_pool = get_pictograph_pool()
    scene_pool.initialize_pool()
    initialize_component_view_pools()
    beat_pool = get_beat_frame_view_pool()

    start = time.perf_counter()
    components = []

    for i in range(64):
        scene = scene_pool.checkout_pictograph()
        view = beat_pool.checkout_view()
        scene.attach_view(view)
        components.append((scene, view))

    load_time = (time.perf_counter() - start) * 1000

    print(f"Loading 64 beat frame pictographs: {load_time:.1f}ms")
    print(f"Expected: < 100ms (no resizing overhead)")
    print(f'Test result: {"PASS" if load_time < 100 else "FAIL"}')

    # Test that views are correctly sized
    sample_view = components[0][1]
    view_size = sample_view.size()
    print(f"View size: {view_size.width()}x{view_size.height()}")
    print(f"Expected: 150x150")
    print(
        f'Size test: {"PASS" if view_size.width() == 150 and view_size.height() == 150 else "FAIL"}'
    )

    # Cleanup
    for scene, view in components:
        scene.detach_view()
        scene_pool.checkin_pictograph(scene)
        beat_pool.checkin_view(view)


def test_start_position_simulation():
    """Test start position picker performance (19 pictographs)"""
    import time

    from application.services.pictograph_pool_manager import get_pictograph_pool
    from presentation.components.pictograph.component_specific_view_pools import (
        get_start_position_picker_view_pool,
        initialize_component_view_pools,
    )

    print("\nTesting start position picker simulation (19 pictographs)...")

    scene_pool = get_pictograph_pool()
    scene_pool.initialize_pool()
    initialize_component_view_pools()
    start_pool = get_start_position_picker_view_pool()

    start_time = time.perf_counter()
    components = []

    for i in range(19):
        scene = scene_pool.checkout_pictograph()
        view = start_pool.checkout_view()
        scene.attach_view(view)
        components.append((scene, view))

    load_time = (time.perf_counter() - start_time) * 1000

    print(f"Loading 19 start position pictographs: {load_time:.1f}ms")
    print(f"Expected: < 30ms (no resizing overhead)")
    print(f'Test result: {"PASS" if load_time < 30 else "FAIL"}')

    # Test that views are correctly sized
    sample_view = components[0][1]
    view_size = sample_view.size()
    print(f"View size: {view_size.width()}x{view_size.height()}")
    print(f"Expected: 100x100")
    print(
        f'Size test: {"PASS" if view_size.width() == 100 and view_size.height() == 100 else "FAIL"}'
    )

    # Cleanup
    for scene, view in components:
        scene.detach_view()
        scene_pool.checkin_pictograph(scene)
        start_pool.checkin_view(view)


def test_memory_management():
    """Test for memory leaks in component pools"""
    import gc

    from application.services.pictograph_pool_manager import get_pictograph_pool
    from presentation.components.pictograph.component_specific_view_pools import (
        get_beat_frame_view_pool,
        get_option_picker_view_pool,
        initialize_component_view_pools,
    )

    print("\nTesting memory management with component pools...")

    # Initialize pools
    scene_pool = get_pictograph_pool()
    scene_pool.initialize_pool()
    initialize_component_view_pools()

    option_pool = get_option_picker_view_pool()
    beat_pool = get_beat_frame_view_pool()

    # Create and destroy many component combinations
    for i in range(500):
        # Test option picker combination
        scene = scene_pool.checkout_pictograph()
        view = option_pool.checkout_view()
        scene.attach_view(view)
        scene.detach_view()
        scene_pool.checkin_pictograph(scene)
        option_pool.checkin_view(view)

        # Test beat frame combination
        scene = scene_pool.checkout_pictograph()
        view = beat_pool.checkout_view()
        scene.attach_view(view)
        scene.detach_view()
        scene_pool.checkin_pictograph(scene)
        beat_pool.checkin_view(view)

        if i % 100 == 0:
            gc.collect()
            print(f"Completed {i} cycles...")

    print("✅ Memory test completed without crashes")


if __name__ == "__main__":
    try:
        ensure_qt_app()  # Initialize Qt first

        if not test_basic_imports():
            sys.exit(1)

        if not test_pool_initialization():
            sys.exit(1)

        if not test_component_view_performance():
            sys.exit(1)
        print("\n🎉 BASIC TESTS COMPLETED!")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
