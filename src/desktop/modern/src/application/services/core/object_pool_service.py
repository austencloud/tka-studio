"""
Object Pool Service - Business Logic for Object Pool Management

This service contains the pure business logic for object pool management,
extracted from the presentation layer. It has no PyQt6 dependencies and can be used
across different UI frameworks.

RESPONSIBILITIES:
- Generic object pool initialization and management
- Progress tracking for pool creation
- Factory pattern for object creation
- Pool state management and reset

USAGE:
    service = container.resolve(IObjectPoolService)
    service.initialize_pool("pictographs", 36, factory_func, progress_callback)
    obj = service.get_pooled_object("pictographs", 5)
"""

import logging
from typing import Dict, Any, Optional, Callable, List

from core.interfaces.core_services import IObjectPoolService

logger = logging.getLogger(__name__)


class ObjectPoolService(IObjectPoolService):
    """
    Business logic service for object pool management.
    
    This service implements generic object pooling logic that was previously
    embedded in the presentation layer. It provides a clean interface for
    pool management without any UI dependencies.
    """

    def __init__(self):
        """Initialize the object pool service."""
        self._pools: Dict[str, List[Any]] = {}
        self._pool_states: Dict[str, Dict[str, Any]] = {}
        logger.debug("Object pool service initialized")

    def initialize_pool(
        self, 
        pool_name: str,
        max_objects: int, 
        object_factory: Callable[[], Any],
        progress_callback: Optional[Callable] = None
    ) -> None:
        """
        Initialize object pool with progress tracking.
        
        Args:
            pool_name: Name identifier for the pool
            max_objects: Maximum number of objects to create
            object_factory: Factory function to create objects
            progress_callback: Optional progress reporting callback
        """
        try:
            logger.debug(f"Initializing pool '{pool_name}' with {max_objects} objects")
            
            # Check if pool already exists
            if pool_name in self._pools and self._pool_states.get(pool_name, {}).get('initialized', False):
                logger.debug(f"Pool '{pool_name}' already initialized")
                return

            # Initialize pool state
            self._pool_states[pool_name] = {
                'initialized': False,
                'max_objects': max_objects,
                'created_objects': 0,
                'factory': object_factory
            }

            if progress_callback:
                progress_callback(f"Starting {pool_name} pool initialization", 0.0)

            # Create the pool list
            pool_objects = []
            
            # Create objects with progress tracking
            for i in range(max_objects):
                try:
                    # Report progress periodically
                    if i % max(1, max_objects // 10) == 0 and progress_callback:
                        progress = i / max_objects
                        progress_callback(
                            f"Creating {pool_name} object {i+1}/{max_objects}",
                            progress
                        )

                    # Create object using factory
                    obj = object_factory()
                    if obj is not None:
                        pool_objects.append(obj)
                        self._pool_states[pool_name]['created_objects'] += 1
                    else:
                        logger.warning(f"Factory returned None for object {i} in pool '{pool_name}'")

                except Exception as e:
                    logger.error(f"Failed to create object {i} in pool '{pool_name}': {e}")
                    # Continue creating other objects even if one fails
                    continue

            # Store the pool
            self._pools[pool_name] = pool_objects
            self._pool_states[pool_name]['initialized'] = True

            if progress_callback:
                progress_callback(f"{pool_name} pool initialization complete", 1.0)

            logger.info(f"Successfully initialized pool '{pool_name}' with {len(pool_objects)} objects")

        except Exception as e:
            logger.error(f"Error initializing pool '{pool_name}': {e}")
            # Ensure pool exists even if initialization failed
            if pool_name not in self._pools:
                self._pools[pool_name] = []
            if pool_name not in self._pool_states:
                self._pool_states[pool_name] = {'initialized': False, 'max_objects': 0, 'created_objects': 0}

    def get_pooled_object(self, pool_name: str, index: int) -> Optional[Any]:
        """
        Get object from pool by index.
        
        Args:
            pool_name: Name of the pool
            index: Index of the object to retrieve
            
        Returns:
            Object at the specified index, None if not found
        """
        try:
            if pool_name not in self._pools:
                logger.error(f"Pool '{pool_name}' does not exist")
                return None

            pool = self._pools[pool_name]
            
            if index < 0 or index >= len(pool):
                logger.warning(f"Index {index} out of range for pool '{pool_name}' (size: {len(pool)})")
                return None

            obj = pool[index]
            logger.debug(f"Retrieved object at index {index} from pool '{pool_name}'")
            return obj

        except Exception as e:
            logger.error(f"Error getting object from pool '{pool_name}' at index {index}: {e}")
            return None

    def reset_pool(self, pool_name: str) -> None:
        """
        Reset pool state.
        
        Args:
            pool_name: Name of the pool to reset
        """
        try:
            if pool_name in self._pools:
                # Clear the pool objects
                self._pools[pool_name].clear()
                logger.debug(f"Cleared objects from pool '{pool_name}'")

            if pool_name in self._pool_states:
                # Reset pool state
                self._pool_states[pool_name]['initialized'] = False
                self._pool_states[pool_name]['created_objects'] = 0
                logger.debug(f"Reset state for pool '{pool_name}'")

            logger.info(f"Successfully reset pool '{pool_name}'")

        except Exception as e:
            logger.error(f"Error resetting pool '{pool_name}': {e}")

    def get_pool_info(self, pool_name: str) -> Dict[str, Any]:
        """
        Get information about a pool.
        
        Args:
            pool_name: Name of the pool
            
        Returns:
            Dictionary containing pool information
        """
        try:
            if pool_name not in self._pools:
                return {
                    'exists': False,
                    'initialized': False,
                    'size': 0,
                    'max_objects': 0,
                    'created_objects': 0
                }

            pool = self._pools[pool_name]
            state = self._pool_states.get(pool_name, {})

            return {
                'exists': True,
                'initialized': state.get('initialized', False),
                'size': len(pool),
                'max_objects': state.get('max_objects', 0),
                'created_objects': state.get('created_objects', 0)
            }

        except Exception as e:
            logger.error(f"Error getting pool info for '{pool_name}': {e}")
            return {
                'exists': False,
                'initialized': False,
                'size': 0,
                'max_objects': 0,
                'created_objects': 0,
                'error': str(e)
            }

    def list_pools(self) -> List[str]:
        """
        List all available pools.
        
        Returns:
            List of pool names
        """
        try:
            pool_names = list(self._pools.keys())
            logger.debug(f"Available pools: {pool_names}")
            return pool_names

        except Exception as e:
            logger.error(f"Error listing pools: {e}")
            return []

    def cleanup_all_pools(self) -> None:
        """Clean up all pools and their resources."""
        try:
            for pool_name in list(self._pools.keys()):
                self.reset_pool(pool_name)
            
            self._pools.clear()
            self._pool_states.clear()
            
            logger.info("Successfully cleaned up all pools")

        except Exception as e:
            logger.error(f"Error cleaning up pools: {e}")

    def get_pool_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about all pools.
        
        Returns:
            Dictionary containing pool statistics
        """
        try:
            stats = {
                'total_pools': len(self._pools),
                'initialized_pools': 0,
                'total_objects': 0,
                'pools': {}
            }

            for pool_name, pool in self._pools.items():
                pool_info = self.get_pool_info(pool_name)
                stats['pools'][pool_name] = pool_info
                
                if pool_info['initialized']:
                    stats['initialized_pools'] += 1
                
                stats['total_objects'] += pool_info['size']

            logger.debug(f"Pool statistics: {stats}")
            return stats

        except Exception as e:
            logger.error(f"Error getting pool statistics: {e}")
            return {
                'total_pools': 0,
                'initialized_pools': 0,
                'total_objects': 0,
                'pools': {},
                'error': str(e)
            }
