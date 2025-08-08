from __future__ import annotations

import os

from PyQt6.QtGui import QPixmap


class AssetPathResolver:
    """Centralized asset path resolution for all background animations"""

    def __init__(self):
        self._cached_images: dict[str, QPixmap] = {}
        self._asset_root = self._find_asset_root()

    def get_image_path(self, filename: str) -> str:
        """Get the path to an image file from the root assets directory"""
        assets_path = os.path.join(self._asset_root, filename)
        normalized_path = os.path.normpath(assets_path)

        if not os.path.exists(normalized_path):
            print(f"Warning: Asset not found: {normalized_path}")
            print("Please ensure required assets are in root/images/")

        return normalized_path

    def get_cached_image(self, filename: str) -> QPixmap:
        """Get cached image or load if not cached"""
        if filename in self._cached_images:
            return self._cached_images[filename]

        full_path = self.get_image_path(filename)
        if os.path.exists(full_path):
            pixmap = QPixmap(full_path)
            self._cached_images[filename] = pixmap
            return pixmap

        return QPixmap()  # Return empty pixmap if not found

    def _find_asset_root(self) -> str:
        """Find the root images directory"""
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Try to find images directory by going up the directory tree
        for _ in range(10):  # Go up directories to find images
            images_path = os.path.join(current_dir, "images")
            if os.path.exists(images_path):
                return images_path
            current_dir = os.path.dirname(current_dir)

        # If not found, try common locations
        common_paths = [
            os.path.join(os.path.dirname(current_dir), "desktop", "images"),
            os.path.join(os.path.dirname(current_dir), "..", "desktop", "images"),
            os.path.join(os.path.dirname(current_dir), "..", "..", "desktop", "images"),
            os.path.join(
                os.path.dirname(current_dir), "..", "..", "..", "desktop", "images"
            ),
        ]

        for path in common_paths:
            normalized_path = os.path.normpath(path)
            if os.path.exists(normalized_path):
                return normalized_path

        return ""
