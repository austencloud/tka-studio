"""
Global singleton for the GlobalVisibilityService to ensure all components use the same instance.
"""

from typing import Optional

from application.services.pictograph.global_visibility_service import (
    PictographVisibilityManager,
)

# Global singleton instance
_global_visibility_service_instance: Optional[PictographVisibilityManager] = None


def get_global_visibility_service() -> PictographVisibilityManager:
    """
    Get the global singleton instance of GlobalVisibilityService.

    This ensures that all components (VisibilityTab, PictographScene, etc.)
    use the same service instance for proper communication.

    Returns:
        The singleton GlobalVisibilityService instance
    """
    global _global_visibility_service_instance

    if _global_visibility_service_instance is None:
        _global_visibility_service_instance = PictographVisibilityManager()

    return _global_visibility_service_instance


def reset_global_visibility_service() -> None:
    """
    Reset the global singleton instance (mainly for testing).
    """
    global _global_visibility_service_instance
    _global_visibility_service_instance = None
