"""
Image asset utilities for pictograph rendering.

Handles path management and asset loading for SVG files.
"""

from desktop.modern.infrastructure.path_resolver import get_image_path


# Re-export the centralized path resolver function
__all__ = ["get_image_path"]
