#!/usr/bin/env python3
"""
Test script for Full Screen Viewer integration.

This script tests the full screen viewer functionality to ensure
it integrates correctly with the workbench and DI container.
"""
from __future__ import annotations

from pathlib import Path
import sys


# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))


def test_full_screen_service_creation():
    """Test that we can create the full screen service"""
    print("🧪 Testing FullScreenService creation...")

    try:
        from desktop.modern.application.services.ui.full_screen_viewer import (
            FullScreenViewer,
        )
        from desktop.modern.application.services.ui.sequence_state_reader import (
            MockSequenceStateReader,
        )
        from desktop.modern.application.services.ui.thumbnail_generation_service import (
            MockThumbnailGenerationService,
        )
        from desktop.modern.presentation.components.ui.full_screen import (
            FullScreenOverlayFactory,
        )

        # Create dependencies
        thumbnail_generator = MockThumbnailGenerationService()
        sequence_state_reader = MockSequenceStateReader()
        overlay_factory = FullScreenOverlayFactory()

        # Create service
        service = FullScreenViewer(
            thumbnail_generator=thumbnail_generator,
            sequence_state_reader=sequence_state_reader,
            overlay_factory=overlay_factory,
        )

        print("✅ FullScreenService created successfully")
        return service

    except Exception as e:
        print(f"❌ Failed to create FullScreenService: {e}")
        return None


def test_thumbnail_generation():
    """Test thumbnail generation with mock data"""
    print("\n🧪 Testing thumbnail generation...")

    try:
        # Initialize Qt application for GUI operations
        import sys

        from PyQt6.QtWidgets import QApplication

        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        from desktop.modern.domain.models.beat_data import BeatData
        from desktop.modern.domain.models.sequence_data import SequenceData

        # Create a test sequence
        beats = [
            BeatData(beat_number=0, letter="A", metadata={"is_start_position": True}),
            BeatData(beat_number=1, letter="B"),
            BeatData(beat_number=2, letter="C"),
        ]

        sequence = SequenceData(name="Test Sequence", word="ABC", beats=beats)

        # Create service
        service = test_full_screen_service_creation()
        if not service:
            return False

        # Test thumbnail creation
        thumbnail_data = service.create_sequence_thumbnail(sequence)

        if thumbnail_data:
            print(f"✅ Thumbnail generated: {len(thumbnail_data)} bytes")
            return True
        print("❌ No thumbnail data returned")
        return False

    except Exception as e:
        print(f"❌ Thumbnail generation failed: {e}")
        return False


def test_di_container_integration():
    """Test DI container integration"""
    print("\n🧪 Testing DI container integration...")

    try:
        from desktop.modern.core.dependency_injection.di_container import DIContainer
        from desktop.modern.core.interfaces.workbench_services import IFullScreenViewer
        from presentation.factories.workbench_factory import (
            configure_workbench_services,
        )

        # Create container
        container = DIContainer()

        # Configure services (this should register our FullScreenService)
        configure_workbench_services(container)

        # Try to resolve the full screen service
        fullscreen_service = container.resolve(IFullScreenViewer)

        if fullscreen_service:
            print(
                f"✅ FullScreenService resolved from DI container: {type(fullscreen_service).__name__}"
            )
            return True
        print("❌ Could not resolve FullScreenService from DI container")
        return False

    except Exception as e:
        print(f"❌ DI container integration failed: {e}")
        return False


def test_workbench_factory():
    """Test workbench factory integration"""
    print("\n🧪 Testing workbench factory integration...")

    try:
        from desktop.modern.core.dependency_injection.di_container import DIContainer
        from presentation.factories.workbench_factory import create_modern_workbench

        # Create container
        container = DIContainer()

        # Register basic services that workbench needs
        from desktop.modern.application.services.core.service_registration_manager import (
            ServiceRegistrationManager,
        )

        registration_manager = ServiceRegistrationManager()
        registration_manager.register_core_services(container)

        # Create workbench (this should work with our new FullScreenService)
        workbench = create_modern_workbench(container)

        if workbench:
            print(f"✅ Workbench created successfully: {type(workbench).__name__}")
            return True
        print("❌ Could not create workbench")
        return False

    except Exception as e:
        print(f"❌ Workbench factory integration failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 Starting Full Screen Viewer Integration Tests\n")

    tests = [
        test_full_screen_service_creation,
        test_thumbnail_generation,
        test_di_container_integration,
        test_workbench_factory,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Full screen viewer integration is working.")
        return True
    print("⚠️ Some tests failed. Check the output above for details.")
    return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
