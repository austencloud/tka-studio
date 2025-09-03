#!/usr/bin/env python3
"""
Debug script to test Save Image functionality step by step.
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


def test_save_image_step_by_step():
    """Test save image functionality step by step."""
    print("🔍 Debug: Testing Save Image Step by Step")
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

        # Step 3: Create export service
        print("\n🔧 Step 3: Creating export service...")
        from desktop.modern.application.services.workbench.workbench_export_service import (
            WorkbenchExportService,
        )

        export_service = WorkbenchExportService()
        print("✅ Export service created")

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

        # Test with a specific file path to avoid file dialog
        test_file_path = str(project_root / "test_export.png")
        print(f"📁 Test file path: {test_file_path}")

        # Call export service directly first
        print("\n🔧 Step 5a: Testing export service directly...")
        success, message = export_service.export_sequence_image(
            sequence, test_file_path
        )
        print(f"📊 Direct export result: success={success}, message='{message}'")

        if success:
            print("✅ Direct export succeeded!")
        else:
            print(f"❌ Direct export failed: {message}")
            return False

        # Now test through coordinator
        print("\n🔧 Step 5b: Testing through coordinator...")
        result = coordinator.save_image()
        print(
            f"📊 Coordinator result: success={result.success}, message='{result.message}'"
        )

        if result.success:
            print("✅ Coordinator export succeeded!")
            return True
        else:
            print(f"❌ Coordinator export failed: {result.message}")
            if result.error_details:
                print(f"🔍 Error details: {result.error_details}")
            return False

    except Exception as e:
        print(f"💥 Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_save_image_step_by_step()
    print(f"\n{'🎉 SUCCESS' if success else '💥 FAILED'}")
    sys.exit(0 if success else 1)
