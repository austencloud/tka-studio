#!/usr/bin/env python3
"""
Test DI Container Integration for Start Position Services.
"""
import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_di_integration():
    """Test that services integrate properly with DI container."""
    print("🔍 Testing DI Integration...")

    try:
        # Create application container
        from desktop.modern.core.application.application_factory import (
            ApplicationFactory,
            ApplicationMode,
        )

        container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

        # Test service resolution
        from desktop.modern.core.interfaces.start_position_services import (
            IStartPositionDataService,
            IStartPositionOrchestrator,
            IStartPositionSelectionService,
            IStartPositionUIService,
        )

        print("  🔍 Resolving services from DI container...")

        # Resolve all services
        data_service = container.resolve(IStartPositionDataService)
        selection_service = container.resolve(IStartPositionSelectionService)
        ui_service = container.resolve(IStartPositionUIService)
        orchestrator = container.resolve(IStartPositionOrchestrator)

        # Verify all services resolved
        assert data_service is not None, "Data service should resolve"
        assert selection_service is not None, "Selection service should resolve"
        assert ui_service is not None, "UI service should resolve"
        assert orchestrator is not None, "Orchestrator should resolve"

        print("    ✅ All services resolved successfully")

        # Test basic functionality
        print("  🔍 Testing basic functionality...")
        assert selection_service.validate_selection("alpha1_alpha1") == True
        print("    ✅ Selection validation works")

        positions = ui_service.get_positions_for_mode("diamond", False)
        assert len(positions) == 3
        print("    ✅ Position retrieval works")

        print("✅ DI Integration test passed!")
        return True

    except Exception as e:
        print(f"❌ DI Integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_di_integration()
    sys.exit(0 if success else 1)
