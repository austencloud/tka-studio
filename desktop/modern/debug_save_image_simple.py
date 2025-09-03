#!/usr/bin/env python3
"""
Simple debug script to test Save Image functionality without Qt rendering.
"""

from __future__ import annotations

import logging
from pathlib import Path
import sys


# Add src to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Set up logging to see debug messages
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def test_coordinator_without_rendering():
    """Test coordinator logic without actual rendering."""
    print("🔍 Debug: Testing Coordinator Logic Only")
    print("=" * 50)

    try:
        # Step 1: Create a test sequence
        print("\n📊 Step 1: Creating test sequence...")
        from desktop.modern.domain.models.beat_data import BeatData
        from desktop.modern.domain.models.sequence_data import SequenceData

        beat1 = BeatData(beat_number=1, is_blank=False)
        beat2 = BeatData(beat_number=2, is_blank=False)

        sequence = SequenceData(name="Test Sequence", word="TEST", beats=[beat1, beat2])

        print(f"✅ Created sequence: {sequence.name}, length={sequence.length}")

        # Step 2: Create state manager and set sequence
        print("\n🔧 Step 2: Creating state manager...")
        from desktop.modern.application.services.workbench.workbench_state_manager import (
            WorkbenchStateManager,
        )

        state_manager = WorkbenchStateManager()
        result = state_manager.set_sequence(sequence)

        print(f"✅ State manager created, sequence set: {result.changed}")
        print(f"📊 Has sequence: {state_manager.has_sequence()}")

        # Step 3: Create a mock export service that doesn't actually render
        print("\n🔧 Step 3: Creating mock export service...")

        class MockExportService:
            def export_sequence_image(self, sequence, file_path=None):
                print(
                    f"🎭 Mock export called with sequence={sequence.name}, file_path={file_path}"
                )
                return True, "Mock export successful"

        export_service = MockExportService()
        print("✅ Mock export service created")

        # Step 4: Create operation coordinator
        print("\n🔧 Step 4: Creating operation coordinator...")
        from desktop.modern.application.services.workbench.workbench_operation_coordinator import (
            WorkbenchOperationCoordinator,
        )

        coordinator = WorkbenchOperationCoordinator(
            workbench_state_manager=state_manager, export_service=export_service
        )

        print("✅ Operation coordinator created")
        print(f"📊 Has state manager: {coordinator._state_manager is not None}")
        print(f"📊 Has export service: {coordinator._export_service is not None}")

        # Step 5: Test save image operation
        print("\n🖼️ Step 5: Testing save image operation...")

        result = coordinator.save_image()
        print(
            f"📊 Coordinator result: success={result.success}, message='{result.message}'"
        )

        if result.success:
            print("✅ Coordinator logic works!")
            return True
        else:
            print(f"❌ Coordinator logic failed: {result.message}")
            if result.error_details:
                print(f"🔍 Error details: {result.error_details}")
            return False

    except Exception as e:
        print(f"💥 Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_actual_workbench_setup():
    """Test how the workbench is actually set up in the real application."""
    print("\n🔍 Debug: Testing Actual Workbench Setup")
    print("=" * 50)

    try:
        # Check how the workbench service registrar creates the coordinator
        print("\n🔧 Testing service registrar...")
        from desktop.modern.application.services.core.registrars.workbench_service_registrar import (
            WorkbenchServiceRegistrar,
        )
        from desktop.modern.core.dependency_injection.di_container import DIContainer

        container = DIContainer()
        registrar = WorkbenchServiceRegistrar()

        print("📊 Registering workbench services...")
        registrar.register_services(container)

        print("📊 Resolving operation coordinator...")
        coordinator = container.resolve("WorkbenchOperationCoordinator")

        print(f"✅ Coordinator resolved: {coordinator}")
        print(f"📊 Has state manager: {coordinator._state_manager is not None}")
        print(f"📊 Has export service: {coordinator._export_service is not None}")

        if coordinator._export_service:
            print(f"📊 Export service type: {type(coordinator._export_service)}")
        else:
            print("❌ No export service injected!")
            return False

        return True

    except Exception as e:
        print(f"💥 Service registrar test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Running Simple Save Image Debug Tests")

    # Test 1: Coordinator logic with mock
    success1 = test_coordinator_without_rendering()

    # Test 2: Actual workbench setup
    success2 = test_actual_workbench_setup()

    overall_success = success1 and success2
    print(f"\n{'🎉 ALL TESTS PASSED' if overall_success else '💥 SOME TESTS FAILED'}")

    if not overall_success:
        print("\n🔍 Possible issues:")
        if not success1:
            print("❌ Coordinator logic has issues")
        if not success2:
            print("❌ Service registration has issues")

    sys.exit(0 if overall_success else 1)
