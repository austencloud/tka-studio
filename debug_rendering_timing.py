#!/usr/bin/env python3
"""
Debug script to test rendering service timing
"""

import sys
sys.path.append('F:/CODE/TKA/src')
sys.path.append('F:/CODE/TKA')

def test_rendering_timing():
    try:
        # Import required modules
        from PyQt6.QtWidgets import QApplication
        from desktop.modern.main import create_application
        from desktop.modern.core.dependency_injection.di_container import get_container
        from desktop.modern.core.interfaces.pictograph_rendering_services import IPictographRenderingService
        
        # Create QApplication
        app = QApplication(sys.argv)
        
        print("=== TESTING RENDERING SERVICE TIMING ===")
        
        # Step 1: Check container before app creation
        print("\n1. Before application creation:")
        try:
            container = get_container()
            print(f"   Container services: {len(getattr(container, '_services', {}))}")
            service = container.resolve(IPictographRenderingService)
            print(f"   ✅ Rendering service available: {type(service)}")
        except Exception as e:
            print(f"   ❌ Rendering service not available: {e}")
        
        # Step 2: Create application
        print("\n2. Creating application...")
        tka_app = create_application()
        print("   ✅ Application created")
        
        # Step 3: Check container after app creation
        print("\n3. After application creation:")
        try:
            container = get_container()
            print(f"   Container services: {len(getattr(container, '_services', {}))}")
            service = container.resolve(IPictographRenderingService)
            print(f"   ✅ Rendering service available: {type(service)}")
        except Exception as e:
            print(f"   ❌ Rendering service not available: {e}")
        
        # Step 4: Show main window
        print("\n4. Showing main window...")
        tka_app.show()
        app.processEvents()
        print("   ✅ Main window shown")
        
        # Step 5: Check container after window shown
        print("\n5. After window shown:")
        try:
            container = get_container()
            print(f"   Container services: {len(getattr(container, '_services', {}))}")
            service = container.resolve(IPictographRenderingService)
            print(f"   ✅ Rendering service available: {type(service)}")
        except Exception as e:
            print(f"   ❌ Rendering service not available: {e}")
        
        # Step 6: Navigate to Learn tab
        print("\n6. Navigating to Learn tab...")
        learn_tab = tka_app.main_window.tab_widget.learn_tab
        tka_app.main_window.tab_widget.setCurrentWidget(learn_tab)
        app.processEvents()
        print("   ✅ Learn tab activated")
        
        # Step 7: Check container after Learn tab activation
        print("\n7. After Learn tab activation:")
        try:
            container = get_container()
            print(f"   Container services: {len(getattr(container, '_services', {}))}")
            service = container.resolve(IPictographRenderingService)
            print(f"   ✅ Rendering service available: {type(service)}")
        except Exception as e:
            print(f"   ❌ Rendering service not available: {e}")
        
        # Step 8: Try to create a pictograph scene
        print("\n8. Creating pictograph scene...")
        from desktop.modern.presentation.components.pictograph.pictograph_scene import PictographScene
        scene = PictographScene()
        print(f"   Scene created: {scene.scene_id}")
        print(f"   Scene rendering service: {scene.rendering_service}")
        
        if scene.rendering_service:
            print("   ✅ Scene has rendering service!")
        else:
            print("   ❌ Scene has no rendering service")
        
        app.quit()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_rendering_timing()
