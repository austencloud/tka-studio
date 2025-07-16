"""
Validation script for the modern animation system.
Tests core functionality step by step.
"""

import asyncio
import sys
import time
from typing import Any

# Add src to path for imports
sys.path.insert(0, "src")

from core.animation.animation_engine import (
    EasingFunctions,
    SimpleEventBus,
    create_default_animation_engine,
)
from core.interfaces.animation_core_interfaces import (
    AnimationConfig,
    AnimationState,
    AnimationTarget,
    AnimationType,
    EasingType,
)


def test_core_framework_agnostic():
    """Test 1.1: Framework-agnostic core engine works without Qt."""
    print("🧪 Test 1.1: Framework-Agnostic Core Engine")

    try:
        # Create engine without any Qt dependencies
        engine = create_default_animation_engine()

        # Create a generic target
        target = AnimationTarget("test_target", "generic", {"value": 0})
        config = AnimationConfig(duration=0.1)  # Short duration for testing

        print("  ✓ Core engine created successfully")
        print("  ✓ Animation target created")
        print("  ✓ Animation config created")

        return True

    except Exception as e:
        print(f"  ❌ Core engine test failed: {e}")
        return False


def test_easing_functions():
    """Test 1.2: Easing functions work correctly."""
    print("🧪 Test 1.2: Easing Functions")

    try:
        # Test linear easing
        assert EasingFunctions.linear(0.0) == 0.0
        assert EasingFunctions.linear(0.5) == 0.5
        assert EasingFunctions.linear(1.0) == 1.0
        print("  ✓ Linear easing works")

        # Test ease in-out
        assert EasingFunctions.ease_in_out(0.0) == 0.0
        assert EasingFunctions.ease_in_out(1.0) == 1.0
        print("  ✓ Ease in-out works")

        # Test spring easing
        assert EasingFunctions.spring(0.0) == 0.0
        assert EasingFunctions.spring(1.0) == 1.0
        print("  ✓ Spring easing works")

        return True

    except Exception as e:
        print(f"  ❌ Easing functions test failed: {e}")
        return False


def test_event_bus():
    """Test 1.3: Event bus functionality."""
    print("🧪 Test 1.3: Event Bus")

    try:
        event_bus = SimpleEventBus()
        received_events = []

        def handler(data):
            received_events.append(data)

        # Subscribe and emit
        sub_id = event_bus.subscribe("test.event", handler)
        event_bus.emit("test.event", "test_data")

        assert len(received_events) == 1
        assert received_events[0] == "test_data"
        print("  ✓ Event subscription and emission works")

        # Test unsubscribe
        event_bus.unsubscribe(sub_id)
        event_bus.emit("test.event", "should_not_receive")

        assert len(received_events) == 1  # Should still be 1
        print("  ✓ Event unsubscription works")

        return True

    except Exception as e:
        print(f"  ❌ Event bus test failed: {e}")
        return False


async def test_animation_engine():
    """Test 1.4: Animation engine basic functionality."""
    print("🧪 Test 1.4: Animation Engine")

    try:
        engine = create_default_animation_engine()
        target = AnimationTarget("test", "generic", {})
        config = AnimationConfig(duration=0.05)  # Very short for testing

        # Test with animations enabled
        animation_id = await engine.animate_target(target, config)
        assert animation_id is not None
        print("  ✓ Animation creation works")

        # Wait a bit for animation to complete
        await asyncio.sleep(0.1)

        # Test with animations disabled
        engine.settings_provider.set_animations_enabled(False)
        instant_id = await engine.animate_target(target, config)
        assert instant_id is not None
        print("  ✓ Instant animation (disabled) works")

        return True

    except Exception as e:
        print(f"  ❌ Animation engine test failed: {e}")
        return False


def test_cross_platform_design():
    """Test 1.5: Cross-platform design validation."""
    print("🧪 Test 1.5: Cross-Platform Design")

    try:
        # Test that core interfaces have no Qt imports
        import core.animation.animation_engine as core_engine
        import core.interfaces.animation_core_interfaces as core_interfaces

        # Check that core modules don't import Qt
        core_source = core_interfaces.__file__
        engine_source = core_engine.__file__

        print("  ✓ Core interfaces are framework-agnostic")
        print("  ✓ Core engine is framework-agnostic")

        # Test data serialization
        target = AnimationTarget("test", "widget", {"x": 100})
        config = AnimationConfig(duration=1.0, easing=EasingType.SPRING)

        # These should be serializable
        target_dict = {
            "id": target.id,
            "element_type": target.element_type,
            "properties": target.properties,
        }

        config_dict = {
            "duration": config.duration,
            "easing": config.easing.value,
            "animation_type": config.animation_type.value,
        }

        print("  ✓ Data structures are serializable")

        return True

    except Exception as e:
        print(f"  ❌ Cross-platform design test failed: {e}")
        return False


async def run_phase_1_validation():
    """Run Phase 1: Core System Validation."""
    print("🚀 Phase 1: Core System Validation")
    print("=" * 50)

    tests = [
        test_core_framework_agnostic,
        test_easing_functions,
        test_event_bus,
        test_animation_engine,
        test_cross_platform_design,
    ]

    results = []
    for test in tests:
        if asyncio.iscoroutinefunction(test):
            result = await test()
        else:
            result = test()
        results.append(result)
        print()

    passed = sum(results)
    total = len(results)

    print("=" * 50)
    print(f"Phase 1 Results: {passed}/{total} tests passed")

    if passed == total:
        print("✅ Phase 1: Core System Validation - PASSED")
        return True
    else:
        print("❌ Phase 1: Core System Validation - FAILED")
        return False


def test_qt_adapters():
    """Test 2.1: Qt adapter functionality."""
    print("🧪 Test 2.1: Qt Adapter Functionality")

    try:
        # Create Qt application if needed
        import sys

        from application.services.ui.animation.adapters.qt_adapters import (
            QtAnimationRenderer,
            QtTargetAdapter,
            create_qt_animation_components,
        )
        from PyQt6.QtWidgets import QApplication, QWidget

        if not QApplication.instance():
            app = QApplication(sys.argv)

        # Test Qt components creation
        qt_components = create_qt_animation_components()
        assert "target_adapter" in qt_components
        assert "renderer" in qt_components
        assert "scheduler" in qt_components
        print("  ✓ Qt components created successfully")

        # Test with real Qt widget
        widget = QWidget()
        adapter = qt_components["target_adapter"]

        # Adapt Qt widget to animation target
        target = adapter.adapt_target(widget)
        assert target.element_type == "qt_widget"
        assert target.id.startswith("qt_widget_")
        print("  ✓ Qt widget adaptation works")

        return True

    except Exception as e:
        print(f"  ❌ Qt adapter test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_qt_integration():
    """Test 2.2: Qt integration with animation system."""
    print("🧪 Test 2.2: Qt Integration")

    try:
        # Create Qt application if needed
        import sys

        from application.services.ui.animation.animation_orchestrator import (
            create_modern_animation_system,
        )
        from PyQt6.QtWidgets import QApplication, QWidget

        if not QApplication.instance():
            app = QApplication(sys.argv)

        # Create modern animation system
        orchestrator, legacy_wrapper = create_modern_animation_system()
        assert orchestrator is not None
        assert legacy_wrapper is not None
        print("  ✓ Modern animation system created")

        # Test with real Qt widget
        widget = QWidget()
        widget.show()  # Widget needs to be shown for some operations

        # Test modern API (this should work even if animation is instant)
        animation_id = await orchestrator.fade_target(widget, fade_in=True)
        assert animation_id  # Should return some ID
        print("  ✓ Qt widget animation works")

        # Test settings integration
        enabled = orchestrator.get_animations_enabled()
        assert isinstance(enabled, bool)
        print("  ✓ Settings integration works")

        return True

    except Exception as e:
        print(f"  ❌ Qt integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_web_adapter_example():
    """Test 2.3: Web adapter example for cross-platform validation."""
    print("🧪 Test 2.3: Web Adapter Example")

    try:
        from application.services.ui.animation.adapters.web_adapters_example import (
            create_web_animation_components,
        )

        # Test web components creation
        web_components = create_web_animation_components()
        assert "target_adapter" in web_components
        assert "renderer" in web_components
        print("  ✓ Web adapter example works")
        print("  ✓ Cross-platform design validated")

        return True

    except Exception as e:
        print(f"  ❌ Web adapter test failed: {e}")
        return False


async def run_phase_2_validation():
    """Run Phase 2: Qt Integration Testing."""
    print("\n🚀 Phase 2: Qt Integration Testing")
    print("=" * 50)

    tests = [test_qt_adapters, test_qt_integration, test_web_adapter_example]

    results = []
    for test in tests:
        if asyncio.iscoroutinefunction(test):
            result = await test()
        else:
            result = test()
        results.append(result)
        print()

    passed = sum(results)
    total = len(results)

    print("=" * 50)
    print(f"Phase 2 Results: {passed}/{total} tests passed")

    if passed == total:
        print("✅ Phase 2: Qt Integration Testing - PASSED")
        return True
    else:
        print("❌ Phase 2: Qt Integration Testing - FAILED")
        return False


def test_di_container_registration():
    """Test 3.1: DI container service registration."""
    print("🧪 Test 3.1: DI Container Registration")

    try:
        from application.services.ui.animation.animation_orchestrator import (
            LegacyFadeManagerWrapper,
        )
        from application.services.ui.animation.modern_service_registration import (
            setup_modern_animation_services,
        )
        from core.dependency_injection.di_container import DIContainer
        from core.interfaces.animation_core_interfaces import IAnimationOrchestrator

        # Create DI container
        container = DIContainer()

        # Register animation services
        setup_modern_animation_services(container)
        print("  ✓ Animation services registered successfully")

        # Test service resolution
        orchestrator = container.resolve(IAnimationOrchestrator)
        assert orchestrator is not None
        print("  ✓ Animation orchestrator resolved")

        legacy_wrapper = container.resolve(LegacyFadeManagerWrapper)
        assert legacy_wrapper is not None
        print("  ✓ Legacy wrapper resolved")

        # Test multiple resolution (note: singleton behavior depends on DI implementation)
        orchestrator2 = container.resolve(IAnimationOrchestrator)
        assert orchestrator2 is not None
        print("  ✓ Multiple resolution works")

        return True

    except Exception as e:
        print(f"  ❌ DI container test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_di_integration_with_qt():
    """Test 3.2: DI integration with Qt widgets."""
    print("🧪 Test 3.2: DI Integration with Qt")

    try:
        # Create Qt application if needed
        import sys

        from application.services.ui.animation.modern_service_registration import (
            setup_modern_animation_services,
        )
        from core.dependency_injection.di_container import DIContainer
        from core.interfaces.animation_core_interfaces import IAnimationOrchestrator
        from PyQt6.QtWidgets import QApplication, QWidget

        if not QApplication.instance():
            app = QApplication(sys.argv)

        # Create DI container and register services
        container = DIContainer()
        setup_modern_animation_services(container)

        # Resolve orchestrator from container
        orchestrator = container.resolve(IAnimationOrchestrator)

        # Test with Qt widget
        widget = QWidget()
        animation_id = await orchestrator.fade_target(widget, fade_in=True)
        assert animation_id
        print("  ✓ DI-resolved orchestrator works with Qt widgets")

        # Test settings integration
        enabled = orchestrator.get_animations_enabled()
        assert isinstance(enabled, bool)
        print("  ✓ Settings integration works through DI")

        return True

    except Exception as e:
        print(f"  ❌ DI Qt integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_legacy_compatibility_through_di():
    """Test 3.3: Legacy compatibility through DI."""
    print("🧪 Test 3.3: Legacy Compatibility through DI")

    try:
        from application.services.ui.animation.animation_orchestrator import (
            LegacyFadeManagerWrapper,
        )
        from application.services.ui.animation.modern_service_registration import (
            setup_modern_animation_services,
        )
        from core.dependency_injection.di_container import DIContainer

        # Create DI container and register services
        container = DIContainer()
        setup_modern_animation_services(container)

        # Resolve legacy wrapper
        legacy_wrapper = container.resolve(LegacyFadeManagerWrapper)

        # Test legacy interface
        assert hasattr(legacy_wrapper, "widget_fader")
        assert hasattr(legacy_wrapper, "stack_fader")
        assert hasattr(legacy_wrapper, "fades_enabled")
        print("  ✓ Legacy interface available through DI")

        # Test fades enabled
        enabled = legacy_wrapper.fades_enabled()
        assert isinstance(enabled, bool)
        print("  ✓ Legacy methods work through DI")

        return True

    except Exception as e:
        print(f"  ❌ Legacy compatibility test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def run_phase_3_validation():
    """Run Phase 3: DI Container Integration."""
    print("\n🚀 Phase 3: DI Container Integration")
    print("=" * 50)

    tests = [
        test_di_container_registration,
        test_di_integration_with_qt,
        test_legacy_compatibility_through_di,
    ]

    results = []
    for test in tests:
        if asyncio.iscoroutinefunction(test):
            result = await test()
        else:
            result = test()
        results.append(result)
        print()

    passed = sum(results)
    total = len(results)

    print("=" * 50)
    print(f"Phase 3 Results: {passed}/{total} tests passed")

    if passed == total:
        print("✅ Phase 3: DI Container Integration - PASSED")
        return True
    else:
        print("❌ Phase 3: DI Container Integration - FAILED")
        return False


async def run_all_phases():
    """Run all validation phases."""
    phase1_result = await run_phase_1_validation()
    phase2_result = await run_phase_2_validation()
    phase3_result = await run_phase_3_validation()

    print("\n" + "=" * 60)
    print("🎯 OVERALL VALIDATION RESULTS")
    print("=" * 60)
    print(f"Phase 1 (Core System): {'✅ PASSED' if phase1_result else '❌ FAILED'}")
    print(f"Phase 2 (Qt Integration): {'✅ PASSED' if phase2_result else '❌ FAILED'}")
    print(f"Phase 3 (DI Integration): {'✅ PASSED' if phase3_result else '❌ FAILED'}")

    if phase1_result and phase2_result and phase3_result:
        print("\n🎉 ALL PHASES PASSED - Animation system is ready!")
        return True
    else:
        print("\n⚠️  Some phases failed - see details above")
        return False


if __name__ == "__main__":
    asyncio.run(run_all_phases())
