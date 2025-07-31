#!/usr/bin/env python3
"""
Debug script to test Learn tab pictograph rendering specifically
"""

import sys

sys.path.append("F:/CODE/TKA/src")
sys.path.append("F:/CODE/TKA")


def test_learn_rendering():
    try:
        # Import required modules
        from PyQt6.QtWidgets import QApplication

        from desktop.modern.domain.models.grid_data import GridData
        from desktop.modern.domain.models.pictograph_data import PictographData
        from desktop.modern.main import create_application

        # Import directly to avoid circular import
        from desktop.modern.presentation.components.pictograph.views.base_pictograph_view import (
            BasePictographView,
        )

        # Create QApplication
        app = QApplication(sys.argv)

        print("=== TESTING LEARN TAB PICTOGRAPH RENDERING ===")

        # Step 1: Create application (this should register services)
        print("\n1. Creating application...")
        tka_app = create_application()
        print("   ✅ Application created")

        # Step 2: Create a learn view (using base view to avoid circular import)
        print("\n2. Creating learn view...")
        learn_view = BasePictographView(parent=None)
        print(f"   ✅ Learn view created: {learn_view}")
        print(f"   Scene: {learn_view._scene}")
        print(f"   Scene ID: {learn_view._scene.scene_id}")

        # Step 3: Check rendering service before rendering
        print("\n3. Checking rendering service before rendering...")
        rendering_service = learn_view._scene.rendering_service
        print(f"   Rendering service: {rendering_service}")

        # Step 4: Create pictograph data
        print("\n4. Creating pictograph data...")
        pictograph_data = PictographData(
            id="test_learn_pictograph", grid_data=GridData(), letter="A"
        )
        print(f"   ✅ Pictograph data created: {pictograph_data.id}")

        # Step 5: Try to render the pictograph
        print("\n5. Attempting to render pictograph...")
        learn_view.update_from_pictograph_data(pictograph_data)
        print("   ✅ Rendering call completed")

        # Step 6: Check rendering service after rendering
        print("\n6. Checking rendering service after rendering...")
        rendering_service = learn_view._scene.rendering_service
        print(f"   Rendering service: {rendering_service}")

        # Step 7: Check scene items
        print("\n7. Checking scene items...")
        scene = learn_view._scene
        items = scene.items()
        print(f"   Scene items: {len(items)} items")
        for i, item in enumerate(items):
            print(f"     Item {i}: {type(item).__name__}")

        # Step 8: Check if scene has any graphics items
        print("\n8. Checking graphics items...")
        from PyQt6.QtWidgets import QGraphicsItem

        graphics_items = [item for item in items if isinstance(item, QGraphicsItem)]
        print(f"   Graphics items: {len(graphics_items)}")

        # Step 9: Force a manual retry
        print("\n9. Forcing manual retry...")
        scene._shared_rendering_service = None  # Reset
        rendering_service = scene.rendering_service  # This should retry
        print(f"   Rendering service after retry: {rendering_service}")

        if rendering_service:
            print("   ✅ Rendering service is now available!")
            # Try rendering again
            print("   Attempting to render again...")
            scene.render_pictograph(pictograph_data)
            items = scene.items()
            print(f"   Scene items after retry: {len(items)} items")
        else:
            print("   ❌ Rendering service still not available")

        app.quit()

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_learn_rendering()
