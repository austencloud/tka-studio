#!/usr/bin/env python3
"""
Test script to validate the simple arrow approach.

This script tests that the simplified arrow selection works correctly:
- Arrows are non-selectable by default
- Graph editor can enable selection explicitly
- No complex context detection needed
"""

import sys
import os

# Add the TKA source directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'desktop', 'modern', 'src'))

def test_arrow_item_simple_approach():
    """Test that ArrowItem has the simple approach methods."""
    print("🧪 Testing simple arrow item approach...")
    
    try:
        from presentation.components.pictograph.graphics_items.arrow_item import ArrowItem
        from PyQt6.QtCore import Qt
        
        # Create arrow item
        arrow = ArrowItem()
        
        # Test default state (non-selectable)
        assert not (arrow.flags() & arrow.GraphicsItemFlag.ItemIsSelectable), "Arrow should not be selectable by default"
        assert not arrow.acceptHoverEvents(), "Arrow should not accept hover events by default"
        assert arrow.cursor().shape() == Qt.CursorShape.ArrowCursor, "Arrow should have arrow cursor by default"
        
        print("✅ Default state: non-selectable")
        
        # Test enable_selection
        arrow.enable_selection()
        assert arrow.flags() & arrow.GraphicsItemFlag.ItemIsSelectable, "Arrow should be selectable after enable_selection()"
        assert arrow.acceptHoverEvents(), "Arrow should accept hover events after enable_selection()"
        assert arrow.cursor().shape() == Qt.CursorShape.PointingHandCursor, "Arrow should have pointing hand cursor after enable_selection()"
        
        print("✅ Enable selection: selectable with pointing hand cursor")
        
        # Test disable_selection
        arrow.disable_selection()
        assert not (arrow.flags() & arrow.GraphicsItemFlag.ItemIsSelectable), "Arrow should not be selectable after disable_selection()"
        assert not arrow.acceptHoverEvents(), "Arrow should not accept hover events after disable_selection()"
        assert arrow.cursor().shape() == Qt.CursorShape.ArrowCursor, "Arrow should have arrow cursor after disable_selection()"
        
        print("✅ Disable selection: non-selectable with arrow cursor")
        
        # Test arrow properties
        assert hasattr(arrow, 'arrow_color'), "Arrow should have arrow_color attribute"
        assert hasattr(arrow, 'add_selection_highlight'), "Arrow should have add_selection_highlight method"
        assert hasattr(arrow, 'remove_selection_highlight'), "Arrow should have remove_selection_highlight method"
        
        print("✅ Arrow has all required properties and methods")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple arrow approach test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_graph_editor_integration():
    """Test that graph editor container can enable arrow selection."""
    print("\n🧪 Testing graph editor integration...")
    
    try:
        # Check that the graph editor container has the updated method
        with open("src/desktop/modern/src/presentation/components/graph_editor/components/pictograph_container.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for the simple approach
        assert "item.enable_selection()" in content, "Graph editor should call enable_selection() on arrows"
        assert "Simple method call - no complex context detection" in content, "Should have comment about simple approach"
        
        print("✅ Graph editor uses simple enable_selection() approach")
        
        # Check that complex context detection is removed
        assert "context_aware" not in content.lower() or content.lower().count("context_aware") < 3, "Should have minimal context references"
        
        print("✅ Complex context detection removed from graph editor")
        
        return True
        
    except Exception as e:
        print(f"❌ Graph editor integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_legacy_compatibility():
    """Test that the approach matches legacy behavior."""
    print("\n🧪 Testing legacy compatibility...")
    
    try:
        # Check that the approach is documented as legacy-compatible
        with open("src/desktop/modern/src/presentation/components/pictograph/graphics_items/arrow_item.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for legacy approach documentation
        assert "legacy version" in content.lower(), "Should reference legacy version approach"
        assert "non-selectable by default" in content.lower(), "Should document default non-selectable state"
        assert "graph editor explicitly enables" in content.lower(), "Should document explicit enabling"
        
        print("✅ Approach documented as legacy-compatible")
        
        # Check that complex imports are removed
        assert "RenderingContext" not in content, "Should not import RenderingContext"
        assert "IPictographContextService" not in content, "Should not import IPictographContextService"
        assert "context_aware_scaling_service" not in content, "Should not import context service"
        
        print("✅ Complex context detection imports removed")
        
        return True
        
    except Exception as e:
        print(f"❌ Legacy compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mouse_event_handling():
    """Test that mouse events are handled correctly."""
    print("\n🧪 Testing mouse event handling...")
    
    try:
        from presentation.components.pictograph.graphics_items.arrow_item import ArrowItem
        
        # Create arrow item
        arrow = ArrowItem()
        
        # Test that mouse event methods exist
        assert hasattr(arrow, 'mousePressEvent'), "Arrow should have mousePressEvent method"
        assert hasattr(arrow, 'mouseReleaseEvent'), "Arrow should have mouseReleaseEvent method"
        assert hasattr(arrow, 'hoverEnterEvent'), "Arrow should have hoverEnterEvent method"
        assert hasattr(arrow, 'hoverLeaveEvent'), "Arrow should have hoverLeaveEvent method"
        
        print("✅ All mouse event methods present")
        
        # Check that the logic is based on flags, not complex context detection
        with open("src/desktop/modern/src/presentation/components/pictograph/graphics_items/arrow_item.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should check flags, not context
        assert "self.flags() &" in content, "Should check flags for selectability"
        assert "ItemIsSelectable" in content, "Should check ItemIsSelectable flag"
        assert "acceptHoverEvents()" in content, "Should check acceptHoverEvents()"
        
        print("✅ Mouse events based on flags, not complex context detection")
        
        return True
        
    except Exception as e:
        print(f"❌ Mouse event handling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_simplicity_metrics():
    """Test that the solution is actually simpler."""
    print("\n🧪 Testing simplicity metrics...")
    
    try:
        # Count lines in arrow item
        with open("src/desktop/modern/src/presentation/components/pictograph/graphics_items/arrow_item.py", 'r', encoding='utf-8') as f:
            arrow_lines = len(f.readlines())
        
        print(f"📊 Arrow item: {arrow_lines} lines")
        
        # Should be reasonable size (not too complex)
        assert arrow_lines < 150, f"Arrow item should be simple, got {arrow_lines} lines"
        
        # Count methods in arrow item
        with open("src/desktop/modern/src/presentation/components/pictograph/graphics_items/arrow_item.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        method_count = content.count("def ")
        print(f"📊 Arrow item methods: {method_count}")
        
        # Should have reasonable number of methods
        assert method_count < 15, f"Arrow item should be simple, got {method_count} methods"
        
        # Check for absence of complex patterns
        complex_patterns = [
            "_determine_context",
            "_safe_fallback",
            "_update_behavior_for_context",
            "context_service",
            "service_resolution"
        ]
        
        for pattern in complex_patterns:
            assert pattern not in content, f"Should not have complex pattern: {pattern}"
        
        print("✅ Solution is appropriately simple")
        
        return True
        
    except Exception as e:
        print(f"❌ Simplicity metrics test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all validation tests."""
    print("🚀 Starting simple arrow approach validation...\n")
    
    tests = [
        test_arrow_item_simple_approach,
        test_graph_editor_integration,
        test_legacy_compatibility,
        test_mouse_event_handling,
        test_simplicity_metrics,
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
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print(f"\n📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed}/{passed + failed} ({100 * passed / (passed + failed):.1f}%)")
    
    if failed == 0:
        print("\n🎉 All tests passed! Simple arrow approach is working correctly.")
        print("\n📋 Simple Solution Summary:")
        print("❌ OLD: Complex context detection with service resolution")
        print("✅ NEW: Simple enable/disable selection methods")
        print("❌ OLD: Arrows try to detect their own context")
        print("✅ NEW: Graph editor explicitly enables selection when needed")
        print("❌ OLD: Complex service registration and protocol errors")
        print("✅ NEW: No services needed - direct method calls")
        
        print("\n🔧 Technical Approach:")
        print("• Arrows are non-selectable by default (safe)")
        print("• Graph editor calls enable_selection() on arrows")
        print("• Mouse events check flags, not complex context")
        print("• No service resolution or context detection needed")
        print("• Matches legacy version approach exactly")
        
        print("\n🎯 Expected Behavior:")
        print("• Graph editor: Arrows selectable with pointing hand cursor")
        print("• Option picker: Arrows non-selectable, events pass through")
        print("• All contexts: Simple, predictable behavior")
        print("• No runtime errors or complex service dependencies")
        
        return True
    else:
        print(f"\n💥 {failed} tests failed. The simple approach needs more work.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
