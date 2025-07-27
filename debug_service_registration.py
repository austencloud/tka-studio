#!/usr/bin/env python3
"""
Debug script to check service registration
"""

import sys
sys.path.append('F:/CODE/TKA/src')
sys.path.append('F:/CODE/TKA')

def test_service_registration():
    try:
        # Import required modules
        from PyQt6.QtWidgets import QApplication
        from desktop.modern.core.application.application_factory import ApplicationFactory, ApplicationMode
        from desktop.modern.core.dependency_injection.di_container import get_container
        
        # Create QApplication
        app = QApplication(sys.argv)
        
        # Create container using the same method as the main application
        print("Creating application container...")
        container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)
        print(f"Container created: {container}")
        
        # Check what services are registered
        print(f"Container services: {len(container._services)} services registered")
        
        # Check for pictograph rendering service specifically
        try:
            from desktop.modern.core.interfaces.pictograph_rendering_services import IPictographRenderingService
            service = container.resolve(IPictographRenderingService)
            print(f"✅ IPictographRenderingService found: {type(service)}")
        except Exception as e:
            print(f"❌ IPictographRenderingService not found: {e}")
        
        # Check for other pictograph services
        try:
            from desktop.modern.application.services.pictograph.pictograph_rendering_service import PictographRenderingService
            service = container.resolve(PictographRenderingService)
            print(f"✅ PictographRenderingService found: {type(service)}")
        except Exception as e:
            print(f"❌ PictographRenderingService not found: {e}")
        
        # List all registered services
        print("\nAll registered services:")
        for i, (interface, impl) in enumerate(container._services.items()):
            print(f"  {i+1}: {interface} -> {impl}")
            if i > 20:  # Limit output
                print(f"  ... and {len(container._services) - i - 1} more services")
                break
        
        # Check if the service registration manager was called
        try:
            from shared.application.services.core.service_registration_manager import ServiceRegistrationManager
            print(f"✅ ServiceRegistrationManager available")
            
            # Try to manually register pictograph services
            from shared.application.services.core.registrars.pictograph_service_registrar import PictographServiceRegistrar
            print(f"✅ PictographServiceRegistrar available")
            
            # Create and register manually
            registrar = PictographServiceRegistrar()
            print("Manually registering pictograph services...")
            registrar.register_services(container)
            print("✅ Manual registration completed")
            
            # Try to resolve again
            service = container.resolve(IPictographRenderingService)
            print(f"✅ IPictographRenderingService found after manual registration: {type(service)}")
            
        except Exception as e:
            print(f"❌ Manual registration failed: {e}")
            import traceback
            traceback.print_exc()
        
        app.quit()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_service_registration()
