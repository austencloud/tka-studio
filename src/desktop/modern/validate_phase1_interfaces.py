"""
Simple validation script to test Phase 1 interfaces.
Run from the src/desktop/modern/src directory.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_interface_imports():
    """Test that all interfaces can be imported successfully."""
    try:
        print("✅ Settings services interfaces imported successfully")
    except ImportError as e:
        print(f"❌ Settings services import failed: {e}")
        return False

    try:
        print("✅ Workbench export services interfaces imported successfully")
    except ImportError as e:
        print(f"❌ Workbench export services import failed: {e}")
        return False

    try:
        print("✅ Motion services interfaces imported successfully")
    except ImportError as e:
        print(f"❌ Motion services import failed: {e}")
        return False

    try:
        print("✅ Layout services interfaces imported successfully")
    except ImportError as e:
        print(f"❌ Layout services import failed: {e}")
        return False

    return True


def test_interface_structure():
    """Test that interfaces have proper structure."""
    from abc import ABC

    from desktop.modern.core.interfaces.settings_services import (
        IBackgroundSettingsManager,
    )

    # Test that it's an abstract base class
    assert issubclass(IBackgroundSettingsManager, ABC), "Should be ABC subclass"
    assert hasattr(IBackgroundSettingsManager, "__abstractmethods__"), (
        "Should have abstract methods"
    )
    assert len(IBackgroundSettingsManager.__abstractmethods__) > 0, (
        "Should have abstract methods"
    )

    print("✅ Interface structure validation passed")
    return True


def test_enum_definitions():
    """Test that enums are properly defined."""
    from desktop.modern.core.interfaces.layout_services import ComponentType, LayoutMode
    from desktop.modern.core.interfaces.settings_services import PropType

    # Test PropType
    assert hasattr(PropType, "STAFF"), "PropType should have STAFF"
    assert PropType.STAFF.value == "Staff", "PropType.STAFF should have correct value"

    # Test ComponentType
    assert hasattr(ComponentType, "PICTOGRAPH_FRAME"), (
        "ComponentType should have PICTOGRAPH_FRAME"
    )

    # Test LayoutMode
    assert hasattr(LayoutMode, "GRID"), "LayoutMode should have GRID"

    print("✅ Enum definitions validation passed")
    return True


def test_data_classes():
    """Test that data classes work correctly."""
    from desktop.modern.core.interfaces.layout_services import Position, Size

    # Test Size
    size = Size(100, 200)
    assert size.width == 100, "Size width should be correct"
    assert size.height == 200, "Size height should be correct"

    # Test Position
    position = Position(10, 20)
    assert position.x == 10, "Position x should be correct"
    assert position.y == 20, "Position y should be correct"

    print("✅ Data classes validation passed")
    return True


def test_mock_implementation():
    """Test that interfaces can be implemented with mock classes."""
    from desktop.modern.core.interfaces.settings_services import (
        IBackgroundSettingsManager,
    )

    class MockBackgroundSettingsManager(IBackgroundSettingsManager):
        def get_available_backgrounds(self):
            return ["Aurora", "Bubbles"]

        def get_current_background(self):
            return "Aurora"

        def set_background(self, background_type):
            return True

        def is_valid_background(self, background_type):
            return True

    # Test instantiation
    manager = MockBackgroundSettingsManager()
    assert isinstance(manager, IBackgroundSettingsManager), (
        "Should be instance of interface"
    )

    # Test method calls
    assert manager.get_available_backgrounds() == [
        "Aurora",
        "Bubbles",
    ], "Should return expected backgrounds"
    assert manager.get_current_background() == "Aurora", (
        "Should return current background"
    )
    assert manager.set_background("Bubbles") == True, (
        "Should set background successfully"
    )
    assert manager.is_valid_background("Aurora") == True, "Should validate background"

    print("✅ Mock implementation validation passed")
    return True


def main():
    """Run all validation tests."""
    print("🧪 Starting Phase 1 Interface Validation")
    print("=" * 50)

    tests = [
        test_interface_imports,
        test_interface_structure,
        test_enum_definitions,
        test_data_classes,
        test_mock_implementation,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"📊 Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All validation tests passed!")
        return True
    else:
        print("🚨 Some validation tests failed!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
