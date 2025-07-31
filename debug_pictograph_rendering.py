#!/usr/bin/env python3
"""
Debug script to test pictograph rendering in Learn tab
"""

import sys

sys.path.append("F:/CODE/TKA/src")
sys.path.append("F:/CODE/TKA")


def test_pictograph_rendering():
    try:
        # Import required modules
        from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

        from desktop.modern.domain.models.grid_data import GridData
        from desktop.modern.domain.models.pictograph_data import PictographData
        from desktop.modern.presentation.components.pictograph.views import (
            create_learn_view,
        )

        # Create QApplication
        app = QApplication(sys.argv)

        # Create main window
        window = QMainWindow()
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        window.setCentralWidget(central_widget)

        # Create a simple pictograph data
        pictograph_data = PictographData(
            id="test_pictograph", grid_data=GridData(), letter="A"
        )

        print(f"Created pictograph data: {pictograph_data}")

        # Create learn view
        learn_view = create_learn_view(parent=central_widget, context="question")
        layout.addWidget(learn_view)

        print(f"Created learn view: {learn_view}")
        print(f"Learn view scene: {learn_view._scene}")

        # Try to render the pictograph
        print("Attempting to render pictograph...")
        learn_view.update_from_pictograph_data(pictograph_data)
        print("Pictograph rendering completed")

        # Check if anything was rendered
        scene = learn_view._scene
        items = scene.items()
        print(f"Scene items after rendering: {len(items)} items")
        for i, item in enumerate(items):
            print(f"  Item {i}: {type(item).__name__}")

        # Check rendering service
        rendering_service = scene.rendering_service
        print(f"Rendering service: {rendering_service}")

        # Show window
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
    test_pictograph_rendering()
