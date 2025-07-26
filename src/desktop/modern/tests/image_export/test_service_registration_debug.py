"""
Debug Service Registration

This test helps debug why the pictograph rendering service isn't being registered properly.
"""

import pytest
from PyQt6.QtWidgets import QApplication

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import register_image_export_services


class TestServiceRegistrationDebug:
    """Debug service registration issues."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test environment."""
        # Ensure QApplication exists
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
        
        yield
    
    def test_pictograph_service_registration(self):
        """Test that pictograph services are properly registered."""
        container = DIContainer()
        
        # Try to register services and see what happens
        try:
            register_image_export_services(container)
            print("✅ Image export services registered successfully")
        except Exception as e:
            print(f"❌ Failed to register image export services: {e}")
            raise
        
        # Check what services are available
        print("\n🔍 Checking registered services...")
        
        # Try to resolve the pictograph rendering service
        try:
            from desktop.modern.core.interfaces.pictograph_rendering_services import IPictographRenderingService
            service = container.resolve(IPictographRenderingService)
            print(f"✅ IPictographRenderingService resolved: {type(service)}")
        except Exception as e:
            print(f"❌ Failed to resolve IPictographRenderingService: {e}")
        
        # Try to resolve other services
        try:
            from desktop.modern.core.interfaces.image_export_services import IImageExportService
            export_service = container.resolve(IImageExportService)
            print(f"✅ IImageExportService resolved: {type(export_service)}")
        except Exception as e:
            print(f"❌ Failed to resolve IImageExportService: {e}")
        
        # Check container state
        print(f"\n📊 Container state:")
        print(f"Container ID: {id(container)}")
        
        # Try to get available services (if the container has such a method)
        if hasattr(container, '_registry') and hasattr(container._registry, '_services'):
            services = container._registry._services
            print(f"Registered services: {list(services.keys())}")
        else:
            print("Cannot inspect container registry")
    
    def test_pictograph_registrar_directly(self):
        """Test the pictograph registrar directly."""
        container = DIContainer()
        
        try:
            from shared.application.services.core.registrars.pictograph_service_registrar import (
                PictographServiceRegistrar
            )
            
            print("✅ PictographServiceRegistrar imported successfully")
            
            # Create and use the registrar
            registrar = PictographServiceRegistrar()
            print(f"✅ PictographServiceRegistrar created: {type(registrar)}")
            
            # Try to register services
            registrar.register_services(container)
            print("✅ Pictograph services registered via registrar")
            
            # Try to resolve the service
            from desktop.modern.core.interfaces.pictograph_rendering_services import IPictographRenderingService
            service = container.resolve(IPictographRenderingService)
            print(f"✅ IPictographRenderingService resolved after direct registration: {type(service)}")
            
        except Exception as e:
            print(f"❌ Error with direct pictograph registrar: {e}")
            import traceback
            traceback.print_exc()
    
    def test_pictograph_service_imports(self):
        """Test that all pictograph service imports work."""
        print("🔍 Testing pictograph service imports...")
        
        try:
            from desktop.modern.core.interfaces.pictograph_rendering_services import IPictographRenderingService
            print("✅ IPictographRenderingService imported")
        except Exception as e:
            print(f"❌ Failed to import IPictographRenderingService: {e}")
        
        try:
            from desktop.modern.application.services.pictograph.pictograph_rendering_service import PictographRenderingService
            print("✅ PictographRenderingService imported")
        except Exception as e:
            print(f"❌ Failed to import PictographRenderingService: {e}")
            import traceback
            traceback.print_exc()
        
        try:
            from shared.application.services.core.registrars.pictograph_service_registrar import PictographServiceRegistrar
            print("✅ PictographServiceRegistrar imported")
        except Exception as e:
            print(f"❌ Failed to import PictographServiceRegistrar: {e}")
            import traceback
            traceback.print_exc()
    
    def test_container_behavior(self):
        """Test container behavior and registration methods."""
        container = DIContainer()
        
        print("🔍 Testing container behavior...")
        print(f"Container type: {type(container)}")
        print(f"Container methods: {[m for m in dir(container) if not m.startswith('_')]}")
        
        # Test basic registration
        try:
            class TestService:
                pass
            
            class ITestService:
                pass
            
            container.register_singleton(ITestService, TestService)
            service = container.resolve(ITestService)
            print(f"✅ Basic registration works: {type(service)}")
            
        except Exception as e:
            print(f"❌ Basic registration failed: {e}")
            import traceback
            traceback.print_exc()
