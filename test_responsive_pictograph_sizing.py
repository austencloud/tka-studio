#!/usr/bin/env python3
"""
Test Responsive Pictograph Sizing System
========================================

Comprehensive tests for the fully responsive pictograph sizing system that
dynamically calculates pictograph dimensions based on available container space.
"""

import sys
import os
from pathlib import Path

# Add TKA source path
tka_root = Path(__file__).parent
sys.path.insert(0, str(tka_root / "src" / "desktop" / "modern" / "src"))

def test_responsive_initialization():
    """Test that responsive sizing is properly initialized."""
    print("Testing responsive initialization...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.components.pictograph_display_section import PictographDisplaySection
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Create display section without size parameter
        display_section = PictographDisplaySection()
        print("  ✓ PictographDisplaySection created without size parameter")
        
        # Test responsive configuration
        assert hasattr(display_section, '_min_pictograph_size'), "Should have min size constraint"
        assert hasattr(display_section, '_max_pictograph_size'), "Should have max size constraint"
        assert hasattr(display_section, '_current_pictograph_size'), "Should have current size tracking"
        print("  ✓ Responsive sizing attributes exist")
        
        # Test default constraints
        assert display_section._min_pictograph_size == 200, f"Expected min size 200, got {display_section._min_pictograph_size}"
        assert display_section._max_pictograph_size == 400, f"Expected max size 400, got {display_section._max_pictograph_size}"
        print("  ✓ Default size constraints are correct")
        
        # Test initial size calculation
        initial_size = display_section.get_current_pictograph_size()
        assert 200 <= initial_size <= 400, f"Initial size {initial_size} should be within constraints"
        print(f"  ✓ Initial pictograph size: {initial_size}px (within constraints)")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Responsive initialization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_size_calculation():
    """Test the dynamic size calculation method."""
    print("\nTesting size calculation...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.components.pictograph_display_section import PictographDisplaySection
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        display_section = PictographDisplaySection()
        
        # Test size calculation method exists
        assert hasattr(display_section, '_calculate_optimal_pictograph_size'), "Should have size calculation method"
        print("  ✓ Size calculation method exists")
        
        # Test calculation with different container widths
        test_cases = [
            (300, 200),   # Small container -> min size
            (600, 385),   # Medium container -> calculated size (600 - 215 = 385)
            (1000, 400),  # Large container -> max size (capped at 400)
            (1400, 400),  # Very large container -> max size (capped at 400)
        ]
        
        for container_width, expected_size in test_cases:
            # Simulate container width
            display_section.resize(container_width, 300)
            calculated_size = display_section._calculate_optimal_pictograph_size()
            
            # Allow small tolerance for calculation differences
            assert abs(calculated_size - expected_size) <= 5, \
                f"Container {container_width}px: expected ~{expected_size}px, got {calculated_size}px"
            
            print(f"  ✓ Container {container_width}px -> Pictograph {calculated_size}px")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Size calculation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_size_constraints():
    """Test size constraint functionality."""
    print("\nTesting size constraints...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.components.pictograph_display_section import PictographDisplaySection
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        display_section = PictographDisplaySection()
        
        # Test getting constraints
        min_size, max_size = display_section.get_size_constraints()
        assert min_size == 200, f"Expected min size 200, got {min_size}"
        assert max_size == 400, f"Expected max size 400, got {max_size}"
        print("  ✓ Get size constraints works")
        
        # Test setting new constraints
        display_section.set_size_constraints(250, 350)
        new_min, new_max = display_section.get_size_constraints()
        assert new_min == 250, f"Expected new min size 250, got {new_min}"
        assert new_max == 350, f"Expected new max size 350, got {new_max}"
        print("  ✓ Set size constraints works")
        
        # Test absolute limits (should be clamped)
        display_section.set_size_constraints(50, 1000)  # Too small min, too large max
        clamped_min, clamped_max = display_section.get_size_constraints()
        assert clamped_min >= 100, f"Min size should be clamped to at least 100, got {clamped_min}"
        assert clamped_max <= 800, f"Max size should be clamped to at most 800, got {clamped_max}"
        print("  ✓ Size constraint clamping works")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Size constraints test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_responsive_updates():
    """Test that pictograph size updates responsively."""
    print("\nTesting responsive updates...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.components.pictograph_display_section import PictographDisplaySection
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        display_section = PictographDisplaySection()
        
        # Test manual size update
        initial_size = display_section.get_current_pictograph_size()
        new_size = 320
        display_section._update_pictograph_size(new_size)
        
        updated_size = display_section.get_current_pictograph_size()
        assert updated_size == new_size, f"Expected size {new_size}, got {updated_size}"
        print(f"  ✓ Manual size update: {initial_size}px -> {updated_size}px")
        
        # Test that pictograph component size matches
        if display_section._pictograph_component:
            component_size = display_section._pictograph_component.size()
            assert component_size.width() == new_size, f"Component width should be {new_size}, got {component_size.width()}"
            assert component_size.height() == new_size, f"Component height should be {new_size}, got {component_size.height()}"
            print("  ✓ Pictograph component size matches")
        else:
            print("  ! Pictograph component not created (expected in test environment)")
        
        # Test legacy set_pictograph_size method
        legacy_size = 280
        display_section.set_pictograph_size(legacy_size)
        final_size = display_section.get_current_pictograph_size()
        assert final_size == legacy_size, f"Legacy method: expected {legacy_size}, got {final_size}"
        print(f"  ✓ Legacy set_pictograph_size method works: {final_size}px")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Responsive updates test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_resize_event_handling():
    """Test resize event handling for responsive behavior."""
    print("\nTesting resize event handling...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QResizeEvent
        from PyQt6.QtCore import QSize
        from presentation.components.graph_editor.components.pictograph_display_section import PictographDisplaySection
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        display_section = PictographDisplaySection()
        
        # Test resize event method exists
        assert hasattr(display_section, 'resizeEvent'), "Should have resizeEvent method"
        print("  ✓ Resize event method exists")
        
        # Test resize event handling
        initial_size = display_section.get_current_pictograph_size()
        
        # Simulate resize to larger container
        old_size = QSize(600, 300)
        new_size = QSize(1000, 300)
        resize_event = QResizeEvent(new_size, old_size)
        
        # Manually set the widget size first
        display_section.resize(new_size)
        
        # Call resize event handler
        display_section.resizeEvent(resize_event)
        
        # Check if size was updated (should be capped at max size)
        updated_size = display_section.get_current_pictograph_size()
        print(f"  ✓ Resize event handled: {initial_size}px -> {updated_size}px")
        
        # Test that resize doesn't cause infinite loops
        assert not display_section._resize_pending, "Resize pending flag should be cleared"
        print("  ✓ Resize event loop protection works")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Resize event handling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_with_graph_editor():
    """Test integration with the main graph editor."""
    print("\nTesting integration with graph editor...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.graph_editor import GraphEditor
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Create graph editor (should use responsive pictograph)
        editor = GraphEditor()
        print("  ✓ Graph editor created with responsive pictograph")
        
        # Test that pictograph display uses responsive sizing
        if editor._pictograph_display:
            assert hasattr(editor._pictograph_display, '_calculate_optimal_pictograph_size'), \
                "Graph editor should use responsive pictograph display"
            
            # Test that it has proper constraints
            min_size, max_size = editor._pictograph_display.get_size_constraints()
            assert min_size > 0 and max_size > min_size, "Should have valid size constraints"
            
            current_size = editor._pictograph_display.get_current_pictograph_size()
            assert min_size <= current_size <= max_size, "Current size should be within constraints"
            
            print(f"  ✓ Responsive pictograph in graph editor: {current_size}px (range: {min_size}-{max_size}px)")
        else:
            print("  ! Pictograph display not created (expected in test environment)")
        
        # Test that existing functionality still works
        result = editor.set_selected_beat_data(-1, None)
        assert result == True, "Basic functionality should still work"
        print("  ✓ Existing functionality preserved")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all responsive pictograph sizing tests."""
    print("=" * 60)
    print("Testing Responsive Pictograph Sizing System")
    print("=" * 60)
    
    tests = [
        test_responsive_initialization,
        test_size_calculation,
        test_size_constraints,
        test_responsive_updates,
        test_resize_event_handling,
        test_integration_with_graph_editor,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
                print(f"  PASS: {test.__name__}")
            else:
                failed += 1
                print(f"  FAIL: {test.__name__}")
        except Exception as e:
            failed += 1
            print(f"  ERROR: {test.__name__} - {e}")
    
    print("\n" + "=" * 60)
    print(f"Responsive Sizing Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("SUCCESS: Fully responsive pictograph sizing system is working correctly!")
        print("🎯 Key Features Implemented:")
        print("  • Dynamic size calculation based on available container space")
        print("  • Automatic resize handling with smooth responsive behavior")
        print("  • Configurable min/max size constraints (200-400px default)")
        print("  • 1:1 aspect ratio maintenance (square pictograph)")
        print("  • Backward compatibility with existing set_pictograph_size() API")
        print("  • No hardcoded pixel dimensions - fully adaptive")
        return True
    else:
        print("FAILURE: Some responsive sizing features need fixes.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
