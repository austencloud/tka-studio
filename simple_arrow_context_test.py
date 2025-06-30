"""
Simple test for context-aware arrow click behavior.
Tests the core functionality without complex imports.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt

# Add TKA paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src"))

from core.application.application_factory import ApplicationFactory
from core.testing.ai_agent_helpers import TKAAITestHelper
from domain.models.core_models import BeatData, MotionData
from presentation.components.pictograph.pictograph_component import PictographComponent
from presentation.components.pictograph.graphics_items.arrow_item import ArrowItem


def create_test_beat_data() -> BeatData:
    """Create test beat data with both arrows."""
    blue_motion = MotionData(
        color="blue",
        motion_type="pro",
        prop_rot_dir="cw",
        start_loc="n",
        end_loc="s",
        turns=1
    )
    
    red_motion = MotionData(
        color="red", 
        motion_type="anti",
        prop_rot_dir="ccw",
        start_loc="e",
        end_loc="w",
        turns=1
    )
    
    return BeatData(
        beat_number=1,
        letter="A",
        blue_motion=blue_motion,
        red_motion=red_motion,
        duration=1.0
    )


def test_context_detection():
    """Test the context detection mechanism."""
    print("🧪 Testing context detection...")
    
    # Create QApplication if needed
    if not QApplication.instance():
        app = QApplication(sys.argv)
    
    # Create TKA application container
    container = ApplicationFactory.create_test_app()
    
    # Test 1: Graph Editor Context
    print("  Testing graph editor context...")
    graph_editor_widget = QWidget()
    graph_editor_widget.setObjectName("GraphEditorWidget")
    
    pictograph_component = PictographComponent(graph_editor_widget)
    beat_data = create_test_beat_data()
    pictograph_component.update_from_beat(beat_data)
    
    scene = pictograph_component.scene
    component_type = scene._determine_component_type()
    print(f"    Graph editor context detected as: {component_type}")
    assert component_type == "graph_editor", f"Expected 'graph_editor', got '{component_type}'"
    
    # Test 2: Option Picker Context
    print("  Testing option picker context...")
    option_picker_widget = QWidget()
    option_picker_widget.setObjectName("OptionPickerWidget")
    
    pictograph_component2 = PictographComponent(option_picker_widget)
    pictograph_component2.update_from_beat(beat_data)
    
    scene2 = pictograph_component2.scene
    component_type2 = scene2._determine_component_type()
    print(f"    Option picker context detected as: {component_type2}")
    assert component_type2 == "option_picker", f"Expected 'option_picker', got '{component_type2}'"
    
    # Test 3: Unknown Context
    print("  Testing unknown context...")
    generic_widget = QWidget()
    generic_widget.setObjectName("GenericWidget")
    
    pictograph_component3 = PictographComponent(generic_widget)
    pictograph_component3.update_from_beat(beat_data)
    
    scene3 = pictograph_component3.scene
    component_type3 = scene3._determine_component_type()
    print(f"    Unknown context detected as: {component_type3}")
    assert component_type3 == "unknown", f"Expected 'unknown', got '{component_type3}'"
    
    print("✅ Context detection tests passed!")
    return True


def test_arrow_click_behavior():
    """Test arrow click behavior in different contexts."""
    print("🧪 Testing arrow click behavior...")
    
    # Create QApplication if needed
    if not QApplication.instance():
        app = QApplication(sys.argv)
    
    # Create TKA application container
    container = ApplicationFactory.create_test_app()
    beat_data = create_test_beat_data()
    
    # Test 1: Graph Editor - should handle arrow clicks
    print("  Testing arrow clicks in graph editor...")
    graph_editor_widget = QWidget()
    graph_editor_widget.setObjectName("GraphEditorWidget")
    
    pictograph_component = PictographComponent(graph_editor_widget)
    pictograph_component.update_from_beat(beat_data)
    
    scene = pictograph_component.scene
    arrow_items = [item for item in scene.items() if isinstance(item, ArrowItem)]
    
    if arrow_items:
        arrow_item = arrow_items[0]
        should_handle = arrow_item._should_handle_arrow_click()
        print(f"    Graph editor arrow handling: {should_handle}")
        assert should_handle, "Arrow clicks should be handled in graph editor"
    else:
        print("    No arrow items found in graph editor scene")
    
    # Test 2: Option Picker - should NOT handle arrow clicks
    print("  Testing arrow clicks in option picker...")
    option_picker_widget = QWidget()
    option_picker_widget.setObjectName("OptionPickerWidget")
    
    pictograph_component2 = PictographComponent(option_picker_widget)
    pictograph_component2.update_from_beat(beat_data)
    
    scene2 = pictograph_component2.scene
    arrow_items2 = [item for item in scene2.items() if isinstance(item, ArrowItem)]
    
    if arrow_items2:
        arrow_item2 = arrow_items2[0]
        should_handle2 = arrow_item2._should_handle_arrow_click()
        print(f"    Option picker arrow handling: {should_handle2}")
        assert not should_handle2, "Arrow clicks should NOT be handled in option picker"
    else:
        print("    No arrow items found in option picker scene")
    
    # Test 3: Unknown Context - should handle arrow clicks (fallback)
    print("  Testing arrow clicks in unknown context...")
    generic_widget = QWidget()
    generic_widget.setObjectName("GenericWidget")
    
    pictograph_component3 = PictographComponent(generic_widget)
    pictograph_component3.update_from_beat(beat_data)
    
    scene3 = pictograph_component3.scene
    arrow_items3 = [item for item in scene3.items() if isinstance(item, ArrowItem)]
    
    if arrow_items3:
        arrow_item3 = arrow_items3[0]
        should_handle3 = arrow_item3._should_handle_arrow_click()
        print(f"    Unknown context arrow handling: {should_handle3}")
        assert should_handle3, "Arrow clicks should be handled in unknown context (fallback)"
    else:
        print("    No arrow items found in unknown context scene")
    
    print("✅ Arrow click behavior tests passed!")
    return True


def main():
    """Run all tests."""
    print("🚀 Starting context-aware arrow click tests...")
    
    try:
        # Test context detection
        test_context_detection()
        
        # Test arrow click behavior
        test_arrow_click_behavior()
        
        print("\n✅ ALL TESTS PASSED!")
        print("Context-aware arrow click behavior is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
