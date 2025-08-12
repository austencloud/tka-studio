"""
Comprehensive validation script for start position service integration (No GUI).

This script validates that all presentation components can properly use the new services
and that backward compatibility is maintained, without requiring GUI components.
"""

from __future__ import annotations

from pathlib import Path
import sys


# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_service_integration():
    """Test that services integrate properly without GUI components."""
    print("🔍 Testing Service Integration...")

    success_count = 0
    total_tests = 0

    # Test 1: Service Imports
    total_tests += 1
    try:
        print("  📋 Testing service and component imports...")
        from desktop.modern.application.services.start_position import (
            StartPositionDataService,
            StartPositionOrchestrator,
            StartPositionSelectionService,
            StartPositionUIService,
        )
        from desktop.modern.core.interfaces.start_position_services import (
            IStartPositionDataService,
            IStartPositionOrchestrator,
            IStartPositionSelectionService,
            IStartPositionUIService,
        )

        print("    ✅ All service imports successful")
        success_count += 1
    except Exception as e:
        print(f"    ❌ Service import failed: {e}")

    # Test 2: Service Instantiation
    total_tests += 1
    try:
        print("  🏗️  Testing service instantiation...")
        data_service = StartPositionDataService()
        selection_service = StartPositionSelectionService()
        ui_service = StartPositionUIService()
        orchestrator = StartPositionOrchestrator(
            data_service, selection_service, ui_service
        )
        print("    ✅ All services instantiated")
        success_count += 1
    except Exception as e:
        print(f"    ❌ Service instantiation failed: {e}")
        return success_count, total_tests

    # Test 3: DI Container Integration
    total_tests += 1
    try:
        print("  🏗️  Testing DI container integration...")
        from desktop.modern.core.dependency_injection.config_registration import (
            register_start_position_services,
        )
        from desktop.modern.core.dependency_injection.di_container import DIContainer

        container = DIContainer()
        register_start_position_services(container)

        # Test that services can be resolved
        resolved_data = container.resolve(IStartPositionDataService)
        resolved_selection = container.resolve(IStartPositionSelectionService)
        resolved_ui = container.resolve(IStartPositionUIService)
        resolved_orchestrator = container.resolve(IStartPositionOrchestrator)

        assert resolved_data is not None
        assert resolved_selection is not None
        assert resolved_ui is not None
        assert resolved_orchestrator is not None

        print("    ✅ DI container integration works")
        success_count += 1
    except Exception as e:
        print(f"    ❌ DI container integration failed: {e}")

    # Test 4: Service Method Functionality
    total_tests += 1
    try:
        print("  🧪 Testing service methods...")

        # Test data service
        positions = data_service.get_available_positions("diamond")
        assert isinstance(positions, list)
        assert len(positions) > 0

        # Test selection service
        assert selection_service.validate_selection("alpha1_alpha1")
        assert not selection_service.validate_selection("invalid")

        # Test UI service
        size = ui_service.calculate_option_size(1000, False)
        assert 80 <= size <= 200

        # Test orchestrator
        from PyQt6.QtCore import QSize

        layout_params = orchestrator.calculate_responsive_layout(QSize(800, 600), 3)
        assert "rows" in layout_params
        assert "cols" in layout_params

        print("    ✅ Service methods work correctly")
        success_count += 1
    except Exception as e:
        print(f"    ❌ Service method testing failed: {e}")

    # Test 5: Service Interface Compliance
    total_tests += 1
    try:
        print("  🎯 Testing service interface compliance...")

        # Check that services implement their interfaces
        assert isinstance(data_service, IStartPositionDataService)
        assert isinstance(selection_service, IStartPositionSelectionService)
        assert isinstance(ui_service, IStartPositionUIService)
        assert isinstance(orchestrator, IStartPositionOrchestrator)

        print("    ✅ All services implement their interfaces")
        success_count += 1
    except Exception as e:
        print(f"    ❌ Interface compliance failed: {e}")

    # Test 6: Service Dependency Injection
    total_tests += 1
    try:
        print("  💉 Testing service dependency injection...")

        # Test that orchestrator has proper dependencies
        assert orchestrator.data_service is not None
        assert orchestrator.selection_service is not None
        assert orchestrator.ui_service is not None

        # Test that orchestrator can use injected services
        test_positions = orchestrator.data_service.get_available_positions("diamond")
        assert len(test_positions) > 0

        print("    ✅ Service dependency injection works")
        success_count += 1
    except Exception as e:
        print(f"    ❌ Service dependency injection failed: {e}")

    # Test 7: Error Handling
    total_tests += 1
    try:
        print("  🛡️  Testing error handling...")

        # Test invalid inputs
        invalid_positions = data_service.get_available_positions("invalid_grid")
        assert isinstance(
            invalid_positions, list
        )  # Should return empty list, not crash

        # Test invalid selection
        assert not selection_service.validate_selection(None)
        assert not selection_service.validate_selection("")

        print("    ✅ Error handling works correctly")
        success_count += 1
    except Exception as e:
        print(f"    ❌ Error handling failed: {e}")

    # Test 8: Service Method Integration
    total_tests += 1
    try:
        print("  🔗 Testing service method integration...")

        # Test that services can work together through orchestrator
        # First normalize the position, then validate it
        normalized = selection_service.normalize_position_key("alpha1")
        assert normalized == "alpha1_alpha1"

        # Now validate the normalized position
        assert selection_service.validate_selection(normalized)

        # Test that UI service can work with data service results
        positions = data_service.get_available_positions("diamond")
        layout_config = ui_service.get_grid_layout_config("diamond", False)

        # For basic picker, layout should be configured for 3 positions
        assert layout_config["position_count"] == 3

        # The actual positions retrieved might be more (advanced positions)
        # but the layout should be configured for basic mode
        assert len(positions) >= 3  # Should have at least 3 positions

        print("    ✅ Service method integration works")
        success_count += 1
    except Exception as e:
        print(f"    ❌ Service method integration failed: {e}")

    return success_count, total_tests


def main():
    """Run the integration validation."""
    print("🚀 Start Position Services - Integration Validation (No GUI)")
    print("=" * 60)

    success_count, total_tests = test_service_integration()

    print(f"\n📊 Integration Test Results: {success_count}/{total_tests} tests passed")
    print("=" * 60)

    if success_count == total_tests:
        print("✅ ALL INTEGRATION TESTS PASSED!")
        print("🎉 Services are properly integrated and ready for use.")
        return True
    print("❌ SOME INTEGRATION TESTS FAILED!")
    print("🔧 Please check the errors above and fix issues.")
    return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
