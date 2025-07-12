#!/usr/bin/env python3
"""
Test script to investigate Qt event processing patterns.
This script tests what happens with and without the setQuitOnLastWindowClosed pattern.
"""

import sys
import time
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt6.QtCore import QTimer

def test_without_pattern(num_objects=10):
    """Test creating QGraphicsViews without the setQuitOnLastWindowClosed pattern."""
    print(f"\n=== Testing WITHOUT pattern ({num_objects} objects) ===")
    
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    views = []
    start_time = time.time()
    
    for i in range(num_objects):
        print(f"Creating view {i+1}/{num_objects}")
        view = QGraphicsView()
        scene = QGraphicsScene()
        view.setScene(scene)
        
        # Immediately hide (as the real code does)
        view.hide()
        view.setVisible(False)
        
        views.append(view)
        
        # Process events after each creation (normal Qt behavior)
        app.processEvents()
    
    end_time = time.time()
    print(f"Created {num_objects} views in {end_time - start_time:.3f} seconds")
    print(f"Views created: {len(views)}")
    
    # Cleanup
    for view in views:
        view.deleteLater()
    
    return end_time - start_time

def test_with_pattern(num_objects=10):
    """Test creating QGraphicsViews WITH the setQuitOnLastWindowClosed pattern."""
    print(f"\n=== Testing WITH pattern ({num_objects} objects) ===")
    
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    # Apply the pattern
    original_quit_setting = app.quitOnLastWindowClosed()
    app.setQuitOnLastWindowClosed(False)
    
    views = []
    start_time = time.time()
    
    try:
        for i in range(num_objects):
            print(f"Creating view {i+1}/{num_objects}")
            view = QGraphicsView()
            scene = QGraphicsScene()
            view.setScene(scene)
            
            # Immediately hide (as the real code does)
            view.hide()
            view.setVisible(False)
            
            views.append(view)
            
            # DON'T process events during creation (the pattern)
        
        # Process events only once after all objects are created
        app.processEvents()
        
    finally:
        # Restore original setting
        app.setQuitOnLastWindowClosed(original_quit_setting)
    
    end_time = time.time()
    print(f"Created {num_objects} views in {end_time - start_time:.3f} seconds")
    print(f"Views created: {len(views)}")
    
    # Cleanup
    for view in views:
        view.deleteLater()
    
    return end_time - start_time

def main():
    """Run the Qt pattern tests."""
    print("Qt Event Processing Pattern Investigation")
    print("=" * 50)
    
    # Test with different numbers of objects
    test_sizes = [5, 10, 20]
    
    for size in test_sizes:
        print(f"\n{'='*60}")
        print(f"TESTING WITH {size} OBJECTS")
        print(f"{'='*60}")
        
        # Test without pattern
        time_without = test_without_pattern(size)
        
        # Small delay between tests
        time.sleep(0.5)
        
        # Test with pattern
        time_with = test_with_pattern(size)
        
        # Compare results
        print(f"\n--- RESULTS FOR {size} OBJECTS ---")
        print(f"Without pattern: {time_without:.3f} seconds")
        print(f"With pattern:    {time_with:.3f} seconds")
        print(f"Difference:      {time_without - time_with:.3f} seconds")
        print(f"Performance:     {((time_without - time_with) / time_without * 100):.1f}% faster with pattern")
    
    print(f"\n{'='*60}")
    print("INVESTIGATION COMPLETE")
    print(f"{'='*60}")
    print("\nNote: This test focuses on performance differences.")
    print("Visual flashing would be more apparent in a GUI environment.")
    print("The pattern prevents window flashing during bulk object creation.")

if __name__ == "__main__":
    main()
