#!/usr/bin/env python3
"""
Performance test script for pictograph pools.
"""

import logging
import os
import sys
import time

# Add the modern source directory to Python path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
)

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Initialize Qt Application for testing
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
    """Test that we can import the pool modules."""
    print("🔍 Testing basic imports...")

    try:
        from application.services.pictograph_pool_manager import get_pictograph_pool

        print("✅ Scene pool import successful")
        return True
    except Exception as e:
        print(f"❌ Scene pool import failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_pool_initialization():
    """Test pool initialization performance."""
    print("\n🏊 Testing pool initialization...")

    # Ensure Qt app is initialized
    ensure_qt_app()

    try:
        from application.services.pictograph_pool_manager import get_pictograph_pool
        from presentation.components.pictograph.pictograph_view_pool import (
            get_pictograph_view_pool,
        )

        # Test scene pool initialization
        start = time.perf_counter()
        scene_pool = get_pictograph_pool()
        scene_pool.initialize_pool()
        scene_time = (time.perf_counter() - start) * 1000

        # Test view pool initialization
        start = time.perf_counter()
        view_pool = get_pictograph_view_pool()
        view_pool.initialize_pool()
        view_time = (time.perf_counter() - start) * 1000

        print(f"Scene pool init: {scene_time:.1f}ms")
        print(f"View pool init: {view_time:.1f}ms")
        print(f"Total: {scene_time + view_time:.1f}ms")

        return True

    except Exception as e:
        print(f"❌ Pool initialization failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_scene_creation_performance():
    """Test scene creation performance."""
    print("\n⚡ Testing scene creation performance...")

    # Ensure Qt app is initialized
    ensure_qt_app()

    try:
        from presentation.components.pictograph.pictograph_component import (
            create_pictograph_component,
        )

        times = []
        for i in range(100):
            start = time.perf_counter()
            scene = create_pictograph_component()
            end = time.perf_counter()
            times.append((end - start) * 1000)

        avg_time = sum(times) / len(times)
        print(f"Average scene creation time: {avg_time:.2f}ms")
        print(f"Expected: < 5ms (should be ~1-2ms)")
        print(f"Test result: {'PASS' if avg_time < 5 else 'FAIL'}")

        return avg_time < 5

    except Exception as e:
        print(f"❌ Scene creation test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_option_picker_simulation():
    """Test option picker performance simulation."""
    print("\n🎯 Testing option picker simulation (36 pictographs)...")

    # Ensure Qt app is initialized
    ensure_qt_app()

    try:
        from application.services.pictograph_pool_manager import get_pictograph_pool
        from presentation.components.pictograph.pictograph_view_pool import (
            get_pictograph_view_pool,
        )

        # Get initialized pools
        scene_pool = get_pictograph_pool()
        view_pool = get_pictograph_view_pool()

        # Simulate option picker loading 36 pictographs
        start = time.perf_counter()
        scenes = []
        views = []

        for i in range(36):
            scene = scene_pool.checkout_pictograph()
            view = view_pool.checkout_view()
            if scene and view:
                scene.attach_view(view)
                scenes.append(scene)
                views.append(view)

        load_time = (time.perf_counter() - start) * 1000

        print(f"Loading 36 pictographs: {load_time:.1f}ms")
        print(f"Expected: < 100ms")
        print(f"Test result: {'PASS' if load_time < 100 else 'FAIL'}")

        # Cleanup
        for scene, view in zip(scenes, views):
            if scene and view:
                scene.detach_view()
                scene_pool.checkin_pictograph(scene)
                view_pool.checkin_view(view)

        return load_time < 100

    except Exception as e:
        print(f"❌ Option picker simulation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all performance tests."""
    print("🚀 Starting pictograph pool performance tests...\n")

    results = {}

    # Test 1: Basic imports
    results["imports"] = test_basic_imports()
    if not results["imports"]:
        print("\n❌ Basic imports failed - stopping tests")
        return False

    # Test 2: Pool initialization
    results["pool_init"] = test_pool_initialization()
    if not results["pool_init"]:
        print("\n❌ Pool initialization failed - stopping tests")
        return False

    # Test 3: Scene creation performance
    results["scene_creation"] = test_scene_creation_performance()

    # Test 4: Option picker simulation
    results["option_picker"] = test_option_picker_simulation()

    # Summary
    print("\n" + "=" * 60)
    print("📊 PERFORMANCE TEST SUMMARY")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")

    total_passed = sum(results.values())
    total_tests = len(results)
    print(f"\nOverall: {total_passed}/{total_tests} tests passed")

    if total_passed == total_tests:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed - performance optimization needed")

    return total_passed == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
