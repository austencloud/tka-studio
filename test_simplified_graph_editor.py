#!/usr/bin/env python3
"""
Test Simplified Graph Editor Architecture
=========================================

Validates that the simplified graph editor architecture works correctly
after removing over-engineered manager patterns and complex abstractions.
"""

import sys
import os
from pathlib import Path

# Add TKA source path
tka_root = Path(__file__).parent
sys.path.insert(0, str(tka_root / "src" / "desktop" / "modern" / "src"))

def test_basic_imports():
    """Test that all simplified components can be imported."""
    print("Testing imports...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        print("  ✓ PyQt6 import successful")
        
        from presentation.components.graph_editor.graph_editor import GraphEditor
        print("  ✓ GraphEditor import successful")
        
        from presentation.components.graph_editor.managers.state_manager import GraphEditorStateManager
        print("  ✓ StateManager import successful")
        
        from presentation.components.graph_editor.managers.signal_coordinator import GraphEditorSignalCoordinator
        print("  ✓ SignalCoordinator import successful")
        
        from presentation.components.graph_editor.utils.validation import ValidationResult, validate_sequence_data
        print("  ✓ Validation utilities import successful")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False

def test_graph_editor_instantiation():
    """Test that GraphEditor can be instantiated with simplified architecture."""
    print("\nTesting GraphEditor instantiation...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.graph_editor import GraphEditor
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Test basic instantiation
        editor = GraphEditor()
        print("  ✓ GraphEditor instantiated successfully")
        
        # Test component references exist
        assert hasattr(editor, '_pictograph_display'), "Missing _pictograph_display"
        assert hasattr(editor, '_adjustment_panel'), "Missing _adjustment_panel"
        print("  ✓ Component references exist")
        
        # Test core state variables exist
        assert hasattr(editor, '_current_sequence'), "Missing _current_sequence"
        assert hasattr(editor, '_selected_beat_index'), "Missing _selected_beat_index"
        assert hasattr(editor, '_selected_beat_data'), "Missing _selected_beat_data"
        print("  ✓ Core state variables exist")
        
        # Test signals exist
        assert hasattr(editor, 'beat_modified'), "Missing beat_modified signal"
        assert hasattr(editor, 'arrow_selected'), "Missing arrow_selected signal"
        assert hasattr(editor, 'visibility_changed'), "Missing visibility_changed signal"
        print("  ✓ Required signals exist")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Instantiation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_api_methods():
    """Test that basic API methods work correctly."""
    print("\nTesting basic API methods...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.graph_editor import GraphEditor
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        editor = GraphEditor()
        
        # Test set_sequence with None
        result = editor.set_sequence(None)
        assert result == True, "set_sequence(None) should return True"
        print("  ✓ set_sequence(None) works")
        
        # Test set_selected_beat_data
        result = editor.set_selected_beat_data(-1, None)
        assert result == True, "set_selected_beat_data(-1, None) should return True"
        print("  ✓ set_selected_beat_data(-1, None) works")
        
        # Test set_visibility
        result = editor.set_visibility(True)
        assert result == True, "set_visibility(True) should return True"
        print("  ✓ set_visibility(True) works")
        
        # Test getter methods
        sequence = editor.get_current_sequence()
        assert sequence is None, "get_current_sequence() should return None initially"
        print("  ✓ get_current_sequence() works")
        
        beat_data = editor.get_selected_beat_data()
        assert beat_data is None, "get_selected_beat_data() should return None initially"
        print("  ✓ get_selected_beat_data() works")
        
        beat_index = editor.get_selected_beat_index()
        assert beat_index == -1, "get_selected_beat_index() should return -1 initially"
        print("  ✓ get_selected_beat_index() works")
        
        return True
        
    except Exception as e:
        print(f"  ✗ API method test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validation_functionality():
    """Test that validation functionality works."""
    print("\nTesting validation functionality...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.graph_editor import GraphEditor
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        editor = GraphEditor()
        
        # Test validate_current_state
        validation_result = editor.validate_current_state()
        assert hasattr(validation_result, 'is_valid'), "ValidationResult should have is_valid"
        assert hasattr(validation_result, 'errors'), "ValidationResult should have errors"
        assert hasattr(validation_result, 'warnings'), "ValidationResult should have warnings"
        print("  ✓ validate_current_state() returns proper ValidationResult")
        
        # With no data, validation should pass
        assert validation_result.is_valid == True, "Empty state should be valid"
        print("  ✓ Empty state validation passes")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Validation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_state_manager():
    """Test that the simplified state manager works."""
    print("\nTesting simplified StateManager...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QObject
        from presentation.components.graph_editor.graph_editor import GraphEditor
        from presentation.components.graph_editor.managers.state_manager import GraphEditorStateManager
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        editor = GraphEditor()
        state_manager = GraphEditorStateManager(editor)
        
        # Test basic state operations
        state_manager.set_visibility(True)
        assert state_manager.get_visibility() == True, "Visibility should be True"
        print("  ✓ Visibility state management works")
        
        state_manager.set_sequence(None)
        assert state_manager.get_sequence() is None, "Sequence should be None"
        print("  ✓ Sequence state management works")
        
        state_manager.set_selected_beat(None, None)
        assert state_manager.get_selected_beat() is None, "Selected beat should be None"
        assert state_manager.get_selected_beat_index() is None, "Selected beat index should be None"
        print("  ✓ Beat selection state management works")
        
        # Test utility methods
        assert state_manager.has_sequence() == False, "Should not have sequence"
        assert state_manager.is_beat_selected() == False, "Should not have beat selected"
        assert state_manager.get_beat_count() == 0, "Beat count should be 0"
        print("  ✓ Utility methods work")
        
        return True
        
    except Exception as e:
        print(f"  ✗ StateManager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_signal_coordinator():
    """Test that the simplified signal coordinator works."""
    print("\nTesting simplified SignalCoordinator...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.graph_editor import GraphEditor
        from presentation.components.graph_editor.managers.signal_coordinator import GraphEditorSignalCoordinator
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        editor = GraphEditor()
        coordinator = GraphEditorSignalCoordinator(editor)
        
        # Test that signals exist
        assert hasattr(coordinator, 'beat_modified'), "Should have beat_modified signal"
        assert hasattr(coordinator, 'arrow_selected'), "Should have arrow_selected signal"
        assert hasattr(coordinator, 'visibility_changed'), "Should have visibility_changed signal"
        print("  ✓ Required signals exist")
        
        # Test dependency setting (with None values for now)
        coordinator.set_dependencies(None, None, None, None)
        print("  ✓ Dependency setting works")
        
        # Test public emission methods
        coordinator.emit_visibility_changed(True)
        print("  ✓ Signal emission methods work")
        
        return True
        
    except Exception as e:
        print(f"  ✗ SignalCoordinator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests for the simplified graph editor architecture."""
    print("=" * 60)
    print("Testing Simplified Graph Editor Architecture")
    print("=" * 60)
    
    tests = [
        test_basic_imports,
        test_graph_editor_instantiation,
        test_basic_api_methods,
        test_validation_functionality,
        test_state_manager,
        test_signal_coordinator,
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
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("SUCCESS: All tests passed! Simplified architecture is working correctly.")
        return True
    else:
        print("FAILURE: Some tests failed. Architecture needs fixes.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
