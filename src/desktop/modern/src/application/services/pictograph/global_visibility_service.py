"""
Global Visibility Service for TKA.

Provides efficient global pictograph visibility management using modern
dependency injection and event-driven updates to replace legacy PictographCollector.
"""

from typing import Dict, List, Any, Optional, Callable, Set
import logging
import weakref
from threading import Lock
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class PictographRegistration:
    """Registration information for a pictograph instance."""
    pictograph_id: str
    instance_ref: weakref.ref  # Weak reference to avoid memory leaks
    component_type: str  # Type of component (graph_editor, sequence_viewer, etc.)
    update_method: str  # Method name to call for updates
    metadata: Dict[str, Any]


class GlobalVisibilityService:
    """
    Efficient global pictograph visibility management service.
    
    Replaces legacy PictographCollector with modern event-driven approach
    using dependency injection and weak references for memory safety.
    """

    def __init__(self):
        self._lock = Lock()
        self._registrations: Dict[str, PictographRegistration] = {}
        self._component_types: Set[str] = set()
        self._update_callbacks: List[Callable] = []
        
        # Statistics for monitoring
        self._stats = {
            "total_registrations": 0,
            "active_registrations": 0,
            "update_calls": 0,
            "failed_updates": 0,
        }

    def register_pictograph(
        self, 
        pictograph_id: str, 
        pictograph_instance: Any,
        component_type: str = "unknown",
        update_method: str = "update_visibility",
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Register a pictograph instance for global visibility updates.
        
        Args:
            pictograph_id: Unique identifier for this pictograph
            pictograph_instance: The actual pictograph instance
            component_type: Type of component (graph_editor, sequence_viewer, etc.)
            update_method: Method name to call for visibility updates
            metadata: Additional metadata about the pictograph
            
        Returns:
            True if registration successful, False otherwise
        """
        if metadata is None:
            metadata = {}
            
        try:
            with self._lock:
                # Create weak reference to avoid memory leaks
                instance_ref = weakref.ref(
                    pictograph_instance,
                    lambda ref: self._cleanup_registration(pictograph_id)
                )
                
                # Verify the update method exists
                if not hasattr(pictograph_instance, update_method):
                    logger.warning(
                        f"Instance {pictograph_id} does not have method {update_method}"
                    )
                    return False
                
                registration = PictographRegistration(
                    pictograph_id=pictograph_id,
                    instance_ref=instance_ref,
                    component_type=component_type,
                    update_method=update_method,
                    metadata=metadata
                )
                
                self._registrations[pictograph_id] = registration
                self._component_types.add(component_type)
                self._stats["total_registrations"] += 1
                self._stats["active_registrations"] = len(self._registrations)
                
                logger.debug(
                    f"Registered pictograph {pictograph_id} of type {component_type}"
                )
                return True
                
        except Exception as e:
            logger.error(f"Error registering pictograph {pictograph_id}: {e}")
            return False

    def unregister_pictograph(self, pictograph_id: str) -> bool:
        """
        Unregister a pictograph instance.
        
        Args:
            pictograph_id: ID of pictograph to unregister
            
        Returns:
            True if unregistration successful, False otherwise
        """
        try:
            with self._lock:
                if pictograph_id in self._registrations:
                    del self._registrations[pictograph_id]
                    self._stats["active_registrations"] = len(self._registrations)
                    logger.debug(f"Unregistered pictograph {pictograph_id}")
                    return True
                else:
                    logger.warning(f"Pictograph {pictograph_id} not found for unregistration")
                    return False
                    
        except Exception as e:
            logger.error(f"Error unregistering pictograph {pictograph_id}: {e}")
            return False

    def _cleanup_registration(self, pictograph_id: str) -> None:
        """Clean up registration when weak reference is garbage collected."""
        try:
            with self._lock:
                if pictograph_id in self._registrations:
                    del self._registrations[pictograph_id]
                    self._stats["active_registrations"] = len(self._registrations)
                    logger.debug(f"Auto-cleaned up registration for {pictograph_id}")
        except Exception as e:
            logger.error(f"Error during auto-cleanup of {pictograph_id}: {e}")

    def apply_visibility_change(
        self, 
        element_type: str, 
        element_name: str, 
        visible: bool,
        component_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Apply visibility change to all registered pictographs.
        
        Args:
            element_type: Type of element (glyph, motion, etc.)
            element_name: Name of specific element (TKA, red_motion, etc.)
            visible: Whether element should be visible
            component_types: Optional filter for specific component types
            
        Returns:
            Dictionary with update results and statistics
        """
        results = {
            "success_count": 0,
            "failure_count": 0,
            "skipped_count": 0,
            "failed_instances": [],
            "updated_instances": [],
        }
        
        try:
            with self._lock:
                # Get current registrations (copy to avoid lock issues)
                current_registrations = dict(self._registrations)
            
            for pictograph_id, registration in current_registrations.items():
                try:
                    # Filter by component type if specified
                    if component_types and registration.component_type not in component_types:
                        results["skipped_count"] += 1
                        continue
                    
                    # Get the actual instance from weak reference
                    instance = registration.instance_ref()
                    if instance is None:
                        # Instance was garbage collected
                        self._cleanup_registration(pictograph_id)
                        results["skipped_count"] += 1
                        continue
                    
                    # Call the update method
                    update_method = getattr(instance, registration.update_method)
                    update_method(element_type, element_name, visible)
                    
                    results["success_count"] += 1
                    results["updated_instances"].append(pictograph_id)
                    
                except Exception as e:
                    logger.error(f"Error updating {pictograph_id}: {e}")
                    results["failure_count"] += 1
                    results["failed_instances"].append({
                        "id": pictograph_id,
                        "error": str(e)
                    })
            
            # Update statistics
            self._stats["update_calls"] += 1
            self._stats["failed_updates"] += results["failure_count"]
            
            logger.debug(
                f"Applied visibility change {element_name}={visible}: "
                f"{results['success_count']} success, {results['failure_count']} failed"
            )
            
        except Exception as e:
            logger.error(f"Error in apply_visibility_change: {e}")
            results["failure_count"] += 1
        
        return results

    def get_all_registered_pictographs(self) -> List[Dict[str, Any]]:
        """
        Get information about all registered pictographs.
        
        Returns:
            List of dictionaries with pictograph information
        """
        pictographs = []
        
        try:
            with self._lock:
                for pictograph_id, registration in self._registrations.items():
                    instance = registration.instance_ref()
                    pictographs.append({
                        "id": pictograph_id,
                        "component_type": registration.component_type,
                        "update_method": registration.update_method,
                        "metadata": registration.metadata,
                        "is_alive": instance is not None,
                    })
        except Exception as e:
            logger.error(f"Error getting registered pictographs: {e}")
        
        return pictographs

    def get_component_types(self) -> List[str]:
        """Get list of all registered component types."""
        with self._lock:
            return list(self._component_types)

    def get_statistics(self) -> Dict[str, Any]:
        """Get service statistics."""
        with self._lock:
            return {
                **self._stats,
                "active_registrations": len(self._registrations),
                "component_types": list(self._component_types),
            }

    def register_update_callback(self, callback: Callable) -> None:
        """Register a callback to be notified of global updates."""
        if callback not in self._update_callbacks:
            self._update_callbacks.append(callback)
            logger.debug("Registered global update callback")

    def unregister_update_callback(self, callback: Callable) -> None:
        """Unregister an update callback."""
        if callback in self._update_callbacks:
            self._update_callbacks.remove(callback)
            logger.debug("Unregistered global update callback")

    def _notify_update_callbacks(self, element_type: str, element_name: str, visible: bool) -> None:
        """Notify all registered update callbacks."""
        for callback in self._update_callbacks:
            try:
                callback(element_type, element_name, visible)
            except Exception as e:
                logger.error(f"Error in update callback: {e}")

    def cleanup_dead_references(self) -> int:
        """
        Clean up any dead weak references.
        
        Returns:
            Number of dead references cleaned up
        """
        cleaned_count = 0
        
        try:
            with self._lock:
                dead_ids = []
                for pictograph_id, registration in self._registrations.items():
                    if registration.instance_ref() is None:
                        dead_ids.append(pictograph_id)
                
                for dead_id in dead_ids:
                    del self._registrations[dead_id]
                    cleaned_count += 1
                
                self._stats["active_registrations"] = len(self._registrations)
                
            if cleaned_count > 0:
                logger.debug(f"Cleaned up {cleaned_count} dead references")
                
        except Exception as e:
            logger.error(f"Error cleaning up dead references: {e}")
        
        return cleaned_count

    def reset(self) -> None:
        """Reset the service (mainly for testing)."""
        with self._lock:
            self._registrations.clear()
            self._component_types.clear()
            self._update_callbacks.clear()
            self._stats = {
                "total_registrations": 0,
                "active_registrations": 0,
                "update_calls": 0,
                "failed_updates": 0,
            }
        logger.debug("Reset global visibility service")
