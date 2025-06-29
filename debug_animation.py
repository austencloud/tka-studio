#!/usr/bin/env python3
"""
Debug script to test graph editor animation issues
"""

import sys
import os
import time
from pathlib import Path

# Add TKA paths for imports
tka_root = Path(__file__).parent
sys.path.insert(0, str(tka_root / "src" / "desktop" / "modern" / "src"))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from PyQt6.QtTest import QTest
from unittest.mock import Mock

# TKA imports
from presentation.components.workbench import SequenceWorkbench
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


def debug_graph_editor_animation():
    """Debug the graph editor animation issues"""
    print("🔍 Starting graph editor animation debug...")

    # Setup Qt app
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)

    # Create mock dependencies
    mock_container = create_mock_container()
    sample_sequence = create_sample_sequence()

    # Create workbench
    print("📋 Creating workbench...")
    workbench = SequenceWorkbench(
        layout_service=mock_container.resolve("ILayoutService"),
        workbench_service=mock_container.resolve("ISequenceWorkbenchService"),
        fullscreen_service=mock_container.resolve("IFullScreenService"),
        deletion_service=mock_container.resolve("IBeatDeletionService"),
        graph_service=mock_container.resolve("IGraphEditorService"),
        dictionary_service=mock_container.resolve("IDictionaryService"),
    )

    # Set up workbench with test data
    workbench.set_sequence(sample_sequence)
    workbench.resize(800, 600)
    workbench.show()

    QTest.qWait(100)  # Allow UI to initialize

    # Get graph editor
    print("🎯 Getting graph editor...")
    if hasattr(workbench, "_graph_section"):
        graph_section = workbench._graph_section
        if hasattr(graph_section, "_graph_editor"):
            graph_editor = graph_section._graph_editor
            print(f"✅ Found graph editor: {graph_editor}")

            # Check initial state
            print(f"📊 Initial state:")
            print(f"   - Visible: {graph_editor.is_visible()}")
            print(f"   - Height: {graph_editor.height()}")
            print(f"   - Width: {graph_editor.width()}")
            print(f"   - Geometry: {graph_editor.geometry()}")

            # Get animation controller
            animation_controller = graph_editor.get_animation_controller()
            print(f"🎬 Animation controller: {animation_controller}")
            print(f"   - Is animating: {animation_controller.is_animating()}")

            # Check toggle tab
            if hasattr(graph_editor, "_toggle_tab"):
                toggle_tab = graph_editor._toggle_tab
                print(f"🔘 Toggle tab: {toggle_tab}")
                print(f"   - Position: {toggle_tab.pos()}")
                print(f"   - Size: {toggle_tab.size()}")
                print(f"   - Visible: {toggle_tab.isVisible()}")
            else:
                print("❌ No toggle tab found")

            # Test slide_up animation
            print("\n🔼 Testing slide_up animation...")
            slide_up_result = animation_controller.slide_up()
            print(f"   - slide_up() returned: {slide_up_result}")

            # Wait for animation to complete
            print("⏳ Waiting for animation to complete...")
            timeout = 2.0
            start_time = time.time()
            while time.time() - start_time < timeout:
                QTest.qWait(50)
                if not animation_controller.is_animating():
                    break

            animation_time = time.time() - start_time
            print(f"📊 After slide_up (took {animation_time:.3f}s):")
            print(f"   - Visible: {graph_editor.is_visible()}")
            print(f"   - Height: {graph_editor.height()}")
            print(f"   - Geometry: {graph_editor.geometry()}")
            print(f"   - Is animating: {animation_controller.is_animating()}")

            if hasattr(graph_editor, "_toggle_tab"):
                toggle_tab = graph_editor._toggle_tab
                print(f"   - Toggle tab position: {toggle_tab.pos()}")
                print(f"   - Toggle tab visible: {toggle_tab.isVisible()}")

            # Test slide_down animation
            print("\n🔽 Testing slide_down animation...")
            QTest.qWait(200)  # Cooldown
            slide_down_result = animation_controller.slide_down()
            print(f"   - slide_down() returned: {slide_down_result}")

            # Wait for animation to complete
            print("⏳ Waiting for slide_down to complete...")
            start_time = time.time()
            while time.time() - start_time < timeout:
                QTest.qWait(50)
                if not animation_controller.is_animating():
                    break

            animation_time = time.time() - start_time
            print(f"📊 After slide_down (took {animation_time:.3f}s):")
            print(f"   - Visible: {graph_editor.is_visible()}")
            print(f"   - Height: {graph_editor.height()}")
            print(f"   - Geometry: {graph_editor.geometry()}")
            print(f"   - Is animating: {animation_controller.is_animating()}")

            if hasattr(graph_editor, "_toggle_tab"):
                toggle_tab = graph_editor._toggle_tab
                print(f"   - Toggle tab position: {toggle_tab.pos()}")
                print(f"   - Toggle tab visible: {toggle_tab.isVisible()}")

        else:
            print("❌ No graph editor found in graph section")
    else:
        print("❌ No graph section found in workbench")

    print("🔍 Debug completed!")


if __name__ == "__main__":
    debug_graph_editor_animation()
