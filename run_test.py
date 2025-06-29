#!/usr/bin/env python3
"""
Run the graph editor animation test
"""

import sys
import os
from pathlib import Path

# Add TKA paths for imports
tka_root = Path(__file__).parent
sys.path.insert(0, str(tka_root / "src" / "desktop" / "modern" / "src"))
sys.path.insert(0, str(tka_root / "tests"))

from PyQt6.QtWidgets import QApplication
from unittest.mock import Mock

# Import test suite
from graph_editor_animation_test_suite import GraphEditorAnimationTestSuite

# TKA imports
from domain.models.core_models import SequenceData, BeatData


def create_mock_container():
    """Create a mock DI container with required services"""
    container = Mock()

    # Mock layout service with proper return values
    layout_service = Mock()
    layout_service.calculate_layout.return_value = (2, 1)  # (rows, columns)
    layout_service.get_beat_frame_size.return_value = (400, 300)  # (width, height)
    layout_service.calculate_beat_frame_layout.return_value = {
        "rows": 2,
        "columns": 1,
        "beat_size": (100, 100),
    }

    # Mock other required services
    service_map = {
        "ILayoutService": layout_service,
        "ISequenceWorkbenchService": Mock(),
        "IFullScreenService": Mock(),
        "IBeatDeletionService": Mock(),
        "IGraphEditorService": Mock(),
        "IDictionaryService": Mock(),
    }

    def mock_resolve(interface_type):
        interface_name = getattr(interface_type, "__name__", str(interface_type))
        return service_map.get(interface_name, Mock())

    container.resolve.side_effect = mock_resolve
    return container


def create_sample_sequence():
    """Create a sample sequence for testing"""
    beat1 = BeatData(beat_number=1, letter="A")
    beat2 = BeatData(beat_number=2, letter="B")

    return SequenceData(
        name="Test Sequence",
        word="AB",
        beats=[beat1, beat2],
        start_position="alpha1",
    )


def run_animation_test():
    """Run the animation test"""
    print("🧪 Running graph editor animation test...")

    # Setup Qt app
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)

    # Create test dependencies
    mock_container = create_mock_container()
    sample_sequence = create_sample_sequence()

    # Create test instance
    test_suite = GraphEditorAnimationTestSuite()

    try:
        # Run the test
        print("🔼 Running animation controller direct API test...")
        test_suite.test_animation_controller_direct_api(mock_container, sample_sequence)
        print("✅ Animation controller direct API test passed!")

        print("\n🔄 Running multi-cycle animation test...")
        test_suite.test_multi_cycle_animation_comprehensive(
            mock_container, sample_sequence
        )
        print("✅ Multi-cycle animation test passed!")

        print("\n📏 Running window resize test...")
        test_suite.test_window_resize_during_animations(mock_container, sample_sequence)
        print("✅ Window resize test passed!")

        print("\n⚡ Running rapid operations test...")
        test_suite.test_rapid_successive_operations(mock_container, sample_sequence)
        print("✅ Rapid operations test passed!")

        print("\n🔧 Running state desynchronization test...")
        test_suite.test_state_desynchronization_detection_and_correction(
            mock_container, sample_sequence
        )
        print("✅ State desynchronization test passed!")

        print("\n🎉 ALL TESTS PASSED! Animation system is working correctly!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = run_animation_test()
    sys.exit(0 if success else 1)
