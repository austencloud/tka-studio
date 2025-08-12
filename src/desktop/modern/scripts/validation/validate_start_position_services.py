"""
Validation script for start position services.

This script validates that the services can be properly imported and instantiated.
Run this to verify the basic structure is correct.
"""

from __future__ import annotations

from pathlib import Path
import sys


# Add src to path for imports
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def validate_services():
    """Validate that all start position services can be imported and instantiated."""
    print("🔍 Validating start position services...")

    try:
        # Test interface imports
        print("  📋 Testing interface imports...")
        from desktop.modern.core.interfaces.start_position_services import (
            IStartPositionDataService,
            IStartPositionOrchestrator,
            IStartPositionSelectionService,
            IStartPositionUIService,
        )

        print("    ✅ All interfaces imported successfully")

        # Test service implementation imports
        print("  🔧 Testing service implementation imports...")
        from desktop.modern.application.services.start_position import (
            StartPositionDataService,
            StartPositionOrchestrator,
            StartPositionSelectionService,
            StartPositionUIService,
        )

        print("    ✅ All service implementations imported successfully")

        # Test service instantiation
        print("  🏗️  Testing service instantiation...")

        # Data service
        data_service = StartPositionDataService()
        assert isinstance(data_service, IStartPositionDataService)
        print("    ✅ StartPositionDataService instantiated and implements interface")

        # Selection service
        selection_service = StartPositionSelectionService()
        assert isinstance(selection_service, IStartPositionSelectionService)
        print(
            "    ✅ StartPositionSelectionService instantiated and implements interface"
        )

        # UI service
        ui_service = StartPositionUIService()
        assert isinstance(ui_service, IStartPositionUIService)
        print("    ✅ StartPositionUIService instantiated and implements interface")

        # Orchestrator service (requires dependencies)
        orchestrator = StartPositionOrchestrator(
            data_service, selection_service, ui_service
        )
        assert isinstance(orchestrator, IStartPositionOrchestrator)
        print("    ✅ StartPositionOrchestrator instantiated and implements interface")

        # Test basic functionality
        print("  🧪 Testing basic functionality...")

        # Test validation
        is_valid = selection_service.validate_selection("alpha1_alpha1")
        assert isinstance(is_valid, bool)
        print("    ✅ Selection validation works")

        # Test position extraction
        end_pos = selection_service.extract_end_position_from_key("alpha1_alpha1")
        assert end_pos == "alpha1"
        print("    ✅ Position extraction works")

        # Test UI calculations
        size = ui_service.calculate_option_size(1000, False)
        assert isinstance(size, int)
        assert size > 0
        print("    ✅ UI size calculation works")

        # Test positions for mode
        positions = ui_service.get_positions_for_mode("diamond", False)
        assert isinstance(positions, list)
        assert len(positions) == 3
        print("    ✅ Position retrieval works")

        print("🎉 All validations passed! Services are properly structured.")
        return True

    except Exception as e:
        print(f"❌ Validation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def validate_di_registration():
    """Validate that services can be registered in DI container."""
    print("\n🔍 Validating DI registration...")

    try:
        # Test DI container creation
        from desktop.modern.core.dependency_injection.di_container import DIContainer

        container = DIContainer()
        print("    ✅ DI container created")

        # Test registration function import
        from desktop.modern.core.dependency_injection.config_registration import (
            register_start_position_services,
        )

        print("    ✅ Registration function imported")

        # Test service registration
        register_start_position_services(container)
        print("    ✅ Services registered in container")

        # Test service resolution
        from desktop.modern.core.interfaces.start_position_services import (
            IStartPositionDataService,
            IStartPositionOrchestrator,
            IStartPositionSelectionService,
            IStartPositionUIService,
        )

        data_service = container.resolve(IStartPositionDataService)
        assert data_service is not None
        print("    ✅ Data service resolved from container")

        selection_service = container.resolve(IStartPositionSelectionService)
        assert selection_service is not None
        print("    ✅ Selection service resolved from container")

        ui_service = container.resolve(IStartPositionUIService)
        assert ui_service is not None
        print("    ✅ UI service resolved from container")

        orchestrator = container.resolve(IStartPositionOrchestrator)
        assert orchestrator is not None
        print("    ✅ Orchestrator resolved from container")

        print("🎉 DI registration validation passed! Services can be injected.")
        return True

    except Exception as e:
        print(f"❌ DI registration validation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Starting Start Position Services Validation")
    print("=" * 60)

    # Run validations
    services_valid = validate_services()
    di_valid = validate_di_registration()

    print("\n" + "=" * 60)
    if services_valid and di_valid:
        print("✅ ALL VALIDATIONS PASSED! Start position services are ready.")
        sys.exit(0)
    else:
        print("❌ SOME VALIDATIONS FAILED! Check the errors above.")
        sys.exit(1)
