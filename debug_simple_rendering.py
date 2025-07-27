#!/usr/bin/env python3
"""
Simple debug script to test pictograph scene rendering
"""

import sys
sys.path.append('F:/CODE/TKA/src')
sys.path.append('F:/CODE/TKA')

def test_scene_rendering():
    try:
        # Import required modules
        from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView
        from desktop.modern.presentation.components.pictograph.pictograph_scene import PictographScene
        from desktop.modern.domain.models.pictograph_data import PictographData
        from desktop.modern.domain.models.grid_data import GridData
        
        # Create QApplication
        app = QApplication(sys.argv)
        
        # Create scene directly
        scene = PictographScene()
        print(f"Created scene: {scene}")
        print(f"Scene ID: {scene.scene_id}")
        
        # Create a simple pictograph data
        pictograph_data = PictographData(
            id="test_pictograph",
            grid_data=GridData(),
            letter="A"
        )
        
        print(f"Created pictograph data: {pictograph_data}")
        
        # Check rendering service
        rendering_service = scene.rendering_service
        print(f"Rendering service: {rendering_service}")
        
        if rendering_service is None:
            print("❌ Rendering service is None - this is the problem!")
        else:
            print("✅ Rendering service is available")
        
        # Try to render the pictograph
        print("Attempting to render pictograph...")
        scene.render_pictograph(pictograph_data)
        print("Pictograph rendering completed")
        
        # Check if anything was rendered
        items = scene.items()
        print(f"Scene items after rendering: {len(items)} items")
        for i, item in enumerate(items):
            print(f"  Item {i}: {type(item).__name__}")
        
        # Create view to display
        view = QGraphicsView(scene)
        window = QMainWindow()
        window.setCentralWidget(view)
        window.resize(800, 600)
        window.show()
        
        print("Window shown. Check if pictograph is visible.")
        
        # Run for a short time to see if anything renders
        import time
        app.processEvents()
        time.sleep(2)
        app.processEvents()
        
        app.quit()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scene_rendering()
