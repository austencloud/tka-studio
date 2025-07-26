"""
Asset utilities for pictograph rendering.
Delegates to centralized asset path service.
"""

from desktop.modern.application.services.backgrounds.shared.asset_paths import AssetPathResolver

# Global instance for backward compatibility
_asset_resolver = AssetPathResolver()


def get_image_path(filename: str) -> str:
    """Get the path to an image file from the root assets directory."""
    return _asset_resolver.get_image_path(filename)


def get_cached_image(filename: str):
    """Get cached image from asset resolver"""
    return _asset_resolver.get_cached_image(filename)
