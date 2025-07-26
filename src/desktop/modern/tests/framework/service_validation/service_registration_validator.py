"""
Service Registration Validator - Service Resolution and Availability
===================================================================

Provides validation of service resolution and availability during runtime,
particularly for pictograph scenes and export operations.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ServiceAccessReport:
    """Report of service access validation."""
    scene_id: str
    can_access_services: bool
    accessible_services: List[str]
    inaccessible_services: List[str]
    container_switching_works: bool = False
    global_container_available: bool = False
    export_container_available: bool = False
    errors: List[str] = None
    warnings: List[str] = None


class ServiceRegistrationValidator:
    """
    Validate service resolution and availability during runtime.
    
    Provides methods to test service access from different contexts,
    particularly focusing on the container switching mechanism used
    during image export operations.
    """
    
    def __init__(self):
        """Initialize the service registration validator."""
        self.critical_services = [
            "IPictographRenderingService",
            "IArrowPositioningOrchestrator", 
            "IGridRenderingService",
            "IPropRenderingService",
        ]
    
    def validate_pictograph_service_access(self, scene_id: str) -> ServiceAccessReport:
        """
        Validate that pictograph scenes can access required services.
        
        Args:
            scene_id: Identifier for the test scene
            
        Returns:
            ServiceAccessReport with access validation results
        """
        errors = []
        warnings = []
        accessible_services = []
        inaccessible_services = []
        
        try:
            logger.info(f"Validating service access for scene: {scene_id}")
            
            # Check global container availability
            global_container_available = self._check_global_container()
            
            # Check export container availability (if in export context)
            export_container_available = self._check_export_container()
            
            # Test service resolution for each critical service
            for service_name in self.critical_services:
                try:
                    can_access = self._test_service_access(service_name)
                    if can_access:
                        accessible_services.append(service_name)
                    else:
                        inaccessible_services.append(service_name)
                        
                except Exception as e:
                    inaccessible_services.append(service_name)
                    errors.append(f"Service access test failed for {service_name}: {e}")
            
            # Test container switching mechanism
            container_switching_works = self._test_container_switching()
            
            # Determine overall access status
            can_access_services = len(inaccessible_services) == 0
            
            if not can_access_services:
                errors.append(f"Cannot access {len(inaccessible_services)} critical services")
            
            if not global_container_available:
                warnings.append("Global container not available")
            
            return ServiceAccessReport(
                scene_id=scene_id,
                can_access_services=can_access_services,
                accessible_services=accessible_services,
                inaccessible_services=inaccessible_services,
                container_switching_works=container_switching_works,
                global_container_available=global_container_available,
                export_container_available=export_container_available,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            logger.error(f"Service access validation failed: {e}")
            return ServiceAccessReport(
                scene_id=scene_id,
                can_access_services=False,
                accessible_services=[],
                inaccessible_services=self.critical_services,
                errors=[f"Validation failed: {e}"]
            )
    
    def validate_export_container_switching(self) -> bool:
        """
        Validate the container switching mechanism used during export.
        
        Returns:
            True if container switching works correctly, False otherwise
        """
        try:
            logger.info("Validating export container switching mechanism")
            
            # Store original container state
            original_container = self._get_current_container()
            
            # Test setting export container as global
            export_container_set = self._test_set_export_container()
            if not export_container_set:
                logger.error("Failed to set export container as global")
                return False
            
            # Test service access with export container
            services_accessible = self._test_services_with_export_container()
            if not services_accessible:
                logger.error("Services not accessible with export container")
                return False
            
            # Test restoring original container
            original_restored = self._test_restore_original_container(original_container)
            if not original_restored:
                logger.warning("Failed to restore original container")
            
            logger.info("Container switching validation completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Container switching validation failed: {e}")
            return False
    
    def _check_global_container(self) -> bool:
        """Check if global container is available."""
        try:
            from desktop.modern.core.dependency_injection.di_container import get_container
            container = get_container()
            return container is not None
        except Exception as e:
            logger.debug(f"Global container check failed: {e}")
            return False
    
    def _check_export_container(self) -> bool:
        """Check if export container is available."""
        try:
            # This would depend on the specific export service implementation
            # For now, we'll check if we can create an export container
            from desktop.modern.core.dependency_injection.di_container import DIContainer
            from desktop.modern.core.dependency_injection.image_export_service_registration import register_image_export_services
            
            test_container = DIContainer()
            register_image_export_services(test_container)
            return True
            
        except Exception as e:
            logger.debug(f"Export container check failed: {e}")
            return False
    
    def _test_service_access(self, service_name: str) -> bool:
        """Test if a specific service can be accessed."""
        try:
            # Get the interface class
            interface_class = self._get_interface_class(service_name)
            if not interface_class:
                return False
            
            # Try to resolve from global container
            from desktop.modern.core.dependency_injection.di_container import get_container
            container = get_container()
            
            if not container:
                return False
            
            service = container.resolve(interface_class)
            return service is not None
            
        except Exception as e:
            logger.debug(f"Service access test failed for {service_name}: {e}")
            return False
    
    def _test_container_switching(self) -> bool:
        """Test the container switching mechanism."""
        try:
            # This is a simplified test - in practice, we would need to
            # simulate the actual export container switching process
            
            original_container = self._get_current_container()
            
            # Create a test export container
            from desktop.modern.core.dependency_injection.di_container import DIContainer, set_container
            from desktop.modern.core.dependency_injection.image_export_service_registration import register_image_export_services
            
            test_export_container = DIContainer()
            register_image_export_services(test_export_container)
            
            # Switch to export container
            set_container(test_export_container, force=True)
            
            # Test service access
            services_work = self._test_service_access("IPictographRenderingService")
            
            # Restore original container
            if original_container:
                set_container(original_container, force=True)
            
            return services_work
            
        except Exception as e:
            logger.debug(f"Container switching test failed: {e}")
            return False
    
    def _get_current_container(self):
        """Get the current global container."""
        try:
            from desktop.modern.core.dependency_injection.di_container import get_container
            return get_container()
        except Exception:
            return None
    
    def _test_set_export_container(self) -> bool:
        """Test setting export container as global."""
        try:
            from desktop.modern.core.dependency_injection.di_container import DIContainer, set_container
            from desktop.modern.core.dependency_injection.image_export_service_registration import register_image_export_services
            
            export_container = DIContainer()
            register_image_export_services(export_container)
            set_container(export_container, force=True)
            
            return True
            
        except Exception as e:
            logger.debug(f"Set export container test failed: {e}")
            return False
    
    def _test_services_with_export_container(self) -> bool:
        """Test that services are accessible with export container."""
        try:
            # Test a few critical services
            test_services = ["IPictographRenderingService", "IArrowPositioningOrchestrator"]
            
            for service_name in test_services:
                if not self._test_service_access(service_name):
                    return False
            
            return True
            
        except Exception as e:
            logger.debug(f"Export container services test failed: {e}")
            return False
    
    def _test_restore_original_container(self, original_container) -> bool:
        """Test restoring the original container."""
        try:
            if original_container:
                from desktop.modern.core.dependency_injection.di_container import set_container
                set_container(original_container, force=True)
                return True
            return False
            
        except Exception as e:
            logger.debug(f"Restore container test failed: {e}")
            return False
    
    def _get_interface_class(self, service_name: str):
        """Get the interface class for a service name."""
        try:
            # Map service names to their modules
            interface_modules = {
                "IPictographRenderingService": "core.interfaces.pictograph_rendering_services",
                "IArrowPositioningOrchestrator": "core.interfaces.arrow_positioning_interfaces",
                "IGridRenderingService": "core.interfaces.pictograph_rendering_services",
                "IPropRenderingService": "core.interfaces.pictograph_rendering_services",
                "IGlyphRenderingService": "core.interfaces.pictograph_rendering_services",
            }
            
            module_name = interface_modules.get(service_name)
            if not module_name:
                return None
            
            # Import the module and get the class
            module = __import__(module_name, fromlist=[service_name])
            return getattr(module, service_name, None)
            
        except Exception as e:
            logger.debug(f"Failed to get interface class for {service_name}: {e}")
            return None
