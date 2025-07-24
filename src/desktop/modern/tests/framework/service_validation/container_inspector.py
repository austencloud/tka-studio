"""
Container Inspector - Service Registration Verification
======================================================

Provides comprehensive inspection of DI container state and service registration
to detect missing services that cause export failures.
"""

import logging
from typing import Dict, List, Optional, Any, Type, Set
from dataclasses import dataclass
import inspect

logger = logging.getLogger(__name__)


@dataclass
class ServiceInfo:
    """Information about a registered service."""
    interface_name: str
    implementation_class: Optional[str] = None
    is_registered: bool = False
    is_resolvable: bool = False
    dependencies: List[str] = None
    error_message: Optional[str] = None


@dataclass
class ServiceRegistrationReport:
    """Report of service registration status."""
    all_required_services_present: bool
    total_services_checked: int
    registered_services: int
    resolvable_services: int
    missing_services: List[str]
    failed_resolutions: List[str]
    service_details: Dict[str, ServiceInfo]
    container_type: str
    errors: List[str] = None
    warnings: List[str] = None


class ContainerInspector:
    """
    Verify service registration completeness in DI containers.
    
    Provides methods to inspect container state, validate service registration,
    and detect missing services that could cause export failures.
    """
    
    def __init__(self):
        """Initialize the container inspector."""
        # Define required services for image export
        self.required_export_services = [
            "IImageExportService",
            "IImageRenderer", 
            "IImageLayoutCalculator",
            "ISequenceMetadataExtractor",
            "IPictographRenderingService",
            "IArrowPositioningOrchestrator",
            "IGridRenderingService",
            "IPropRenderingService",
        ]
        
        # Define optional services that enhance functionality
        self.optional_export_services = [
            "IGlyphRenderingService",
            "IAnimationOrchestrator",
            "IPositioningService",
        ]
    
    def verify_export_services_registered(self, container) -> ServiceRegistrationReport:
        """
        Verify that all required export services are registered.
        
        Args:
            container: DI container to inspect
            
        Returns:
            ServiceRegistrationReport with detailed registration status
        """
        errors = []
        warnings = []
        service_details = {}
        missing_services = []
        failed_resolutions = []
        
        try:
            container_type = type(container).__name__
            logger.info(f"Inspecting container: {container_type}")
            
            # Check all required services
            all_services = self.required_export_services + self.optional_export_services
            
            for service_name in all_services:
                service_info = self._inspect_service(container, service_name)
                service_details[service_name] = service_info
                
                if service_name in self.required_export_services:
                    if not service_info.is_registered:
                        missing_services.append(service_name)
                    elif not service_info.is_resolvable:
                        failed_resolutions.append(service_name)
                else:
                    # Optional service
                    if not service_info.is_registered:
                        warnings.append(f"Optional service not registered: {service_name}")
            
            # Calculate statistics
            total_checked = len(all_services)
            registered_count = sum(1 for info in service_details.values() if info.is_registered)
            resolvable_count = sum(1 for info in service_details.values() if info.is_resolvable)
            
            # Check if all required services are present
            all_required_present = len(missing_services) == 0 and len(failed_resolutions) == 0
            
            # Additional container-specific checks
            self._perform_container_specific_checks(container, errors, warnings)
            
            return ServiceRegistrationReport(
                all_required_services_present=all_required_present,
                total_services_checked=total_checked,
                registered_services=registered_count,
                resolvable_services=resolvable_count,
                missing_services=missing_services,
                failed_resolutions=failed_resolutions,
                service_details=service_details,
                container_type=container_type,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            logger.error(f"Service registration verification failed: {e}")
            return ServiceRegistrationReport(
                all_required_services_present=False,
                total_services_checked=0,
                registered_services=0,
                resolvable_services=0,
                missing_services=self.required_export_services,
                failed_resolutions=[],
                service_details={},
                container_type="unknown",
                errors=[f"Verification failed: {e}"]
            )
    
    def validate_pictograph_service_access(self, scene_id: str = "test_scene") -> 'ServiceAccessReport':
        """
        Validate that pictograph scenes can access required services.
        
        Args:
            scene_id: Identifier for the test scene
            
        Returns:
            ServiceAccessReport with access validation results
        """
        try:
            from .service_registration_validator import ServiceRegistrationValidator
            validator = ServiceRegistrationValidator()
            return validator.validate_pictograph_service_access(scene_id)
            
        except Exception as e:
            logger.error(f"Pictograph service access validation failed: {e}")
            # Return a basic failure report
            from .service_registration_validator import ServiceAccessReport
            return ServiceAccessReport(
                scene_id=scene_id,
                can_access_services=False,
                accessible_services=[],
                inaccessible_services=self.required_export_services,
                errors=[f"Access validation failed: {e}"]
            )
    
    def check_positioning_services_available(self) -> bool:
        """
        Check if positioning services are available for arrow rendering.
        
        Returns:
            True if positioning services are available, False otherwise
        """
        try:
            # Try to get the global container
            from core.dependency_injection.di_container import get_container
            container = get_container()
            
            if not container:
                logger.error("No global container available")
                return False
            
            # Check for arrow positioning service
            arrow_service_info = self._inspect_service(container, "IArrowPositioningOrchestrator")
            if not arrow_service_info.is_resolvable:
                logger.error("IArrowPositioningOrchestrator not available")
                return False
            
            # Check for positioning service
            positioning_service_info = self._inspect_service(container, "IPositioningService")
            if not positioning_service_info.is_resolvable:
                logger.warning("IPositioningService not available (may be optional)")
            
            return True
            
        except Exception as e:
            logger.error(f"Positioning services check failed: {e}")
            return False
    
    def _inspect_service(self, container, service_name: str) -> ServiceInfo:
        """Inspect a specific service in the container."""
        service_info = ServiceInfo(
            interface_name=service_name,
            dependencies=[]
        )
        
        try:
            # Try to get the interface class
            interface_class = self._get_interface_class(service_name)
            
            if not interface_class:
                service_info.error_message = f"Interface class not found: {service_name}"
                return service_info
            
            # Check if service is registered
            service_info.is_registered = self._is_service_registered(container, interface_class)
            
            if service_info.is_registered:
                # Try to resolve the service
                try:
                    resolved_service = container.resolve(interface_class)
                    service_info.is_resolvable = resolved_service is not None
                    
                    if resolved_service:
                        service_info.implementation_class = type(resolved_service).__name__
                        service_info.dependencies = self._get_service_dependencies(resolved_service)
                    
                except Exception as e:
                    service_info.is_resolvable = False
                    service_info.error_message = f"Resolution failed: {e}"
            
        except Exception as e:
            service_info.error_message = f"Inspection failed: {e}"
        
        return service_info
    
    def _get_interface_class(self, service_name: str) -> Optional[Type]:
        """Get the interface class for a service name."""
        try:
            # Map service names to their modules
            interface_modules = {
                "IImageExportService": "core.interfaces.image_export_services",
                "IImageRenderer": "core.interfaces.image_export_services", 
                "IImageLayoutCalculator": "core.interfaces.image_export_services",
                "ISequenceMetadataExtractor": "core.interfaces.image_export_services",
                "IPictographRenderingService": "core.interfaces.pictograph_rendering_services",
                "IArrowPositioningOrchestrator": "core.interfaces.arrow_positioning_interfaces",
                "IGridRenderingService": "core.interfaces.pictograph_rendering_services",
                "IPropRenderingService": "core.interfaces.pictograph_rendering_services",
                "IGlyphRenderingService": "core.interfaces.pictograph_rendering_services",
                "IAnimationOrchestrator": "core.interfaces.animation_core_interfaces",
                "IPositioningService": "core.interfaces.positioning_interfaces",
            }
            
            module_name = interface_modules.get(service_name)
            if not module_name:
                logger.warning(f"Unknown service interface: {service_name}")
                return None
            
            # Import the module and get the class
            module = __import__(module_name, fromlist=[service_name])
            return getattr(module, service_name, None)
            
        except Exception as e:
            logger.error(f"Failed to get interface class for {service_name}: {e}")
            return None
    
    def _is_service_registered(self, container, interface_class: Type) -> bool:
        """Check if a service is registered in the container."""
        try:
            # Different containers may have different methods to check registration
            if hasattr(container, 'is_registered'):
                return container.is_registered(interface_class)
            elif hasattr(container, '_services') and interface_class in container._services:
                return True
            elif hasattr(container, '_registrations') and interface_class in container._registrations:
                return True
            else:
                # Try to resolve and see if it works
                try:
                    service = container.resolve(interface_class)
                    return service is not None
                except:
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to check service registration: {e}")
            return False
    
    def _get_service_dependencies(self, service_instance) -> List[str]:
        """Get the dependencies of a service instance."""
        dependencies = []
        
        try:
            # Check constructor parameters
            init_signature = inspect.signature(service_instance.__class__.__init__)
            for param_name, param in init_signature.parameters.items():
                if param_name != 'self' and param.annotation != inspect.Parameter.empty:
                    dependencies.append(str(param.annotation))
            
        except Exception as e:
            logger.debug(f"Failed to get dependencies for {type(service_instance).__name__}: {e}")
        
        return dependencies
    
    def _perform_container_specific_checks(self, container, errors: List[str], warnings: List[str]) -> None:
        """Perform additional checks specific to the container type."""
        try:
            container_type = type(container).__name__
            
            # Check for common container issues
            if hasattr(container, '_services'):
                service_count = len(container._services)
                if service_count == 0:
                    errors.append("Container has no registered services")
                elif service_count < 5:
                    warnings.append(f"Container has only {service_count} services (may be incomplete)")
            
            # Check for circular dependencies (basic check)
            if hasattr(container, '_registrations'):
                # This would require more sophisticated analysis
                pass
            
        except Exception as e:
            logger.debug(f"Container-specific checks failed: {e}")
