"""
Centralized path resolution for TKA Desktop Application.

This module provides a robust way to locate project directories without
brittle relative path navigation. It searches upward from any location
to find the correct project structure.
"""

from pathlib import Path
from typing import Optional


class TKAPathResolver:
    """Centralized path resolver for TKA project structure."""
    
    _instance: Optional['TKAPathResolver'] = None
    _desktop_root: Optional[Path] = None
    _project_root: Optional[Path] = None
    
    def __new__(cls) -> 'TKAPathResolver':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize path resolver with automatic discovery."""
        if self._desktop_root is None:
            self._discover_paths()
    
    def _discover_paths(self) -> None:
        """Discover project paths by searching upward from current file."""
        current_path = Path(__file__).resolve()
        
        # Search upward for desktop directory
        for parent in [current_path] + list(current_path.parents):
            if parent.name == "desktop" and (parent / "images").exists():
                self._desktop_root = parent
                break
        
        # Search upward for TKA project root
        current_path = Path(__file__).resolve()
        for parent in [current_path] + list(current_path.parents):
            if parent.name == "TKA":
                self._project_root = parent
                break
        
        # Fallback: if desktop not found, try to find it relative to TKA root
        if self._desktop_root is None and self._project_root is not None:
            desktop_candidate = self._project_root / "src" / "desktop"
            if desktop_candidate.exists() and (desktop_candidate / "images").exists():
                self._desktop_root = desktop_candidate
        
        # Last resort: use current working directory structure
        if self._desktop_root is None:
            cwd = Path.cwd()
            # Try common locations from CWD
            for candidate in [
                cwd / "src" / "desktop",
                cwd / "desktop",
                cwd.parent / "desktop",
            ]:
                if candidate.exists() and (candidate / "images").exists():
                    self._desktop_root = candidate
                    break
    
    @property
    def desktop_root(self) -> Path:
        """Get the desktop root directory."""
        if self._desktop_root is None:
            raise RuntimeError("Could not locate TKA desktop directory")
        return self._desktop_root
    
    @property
    def project_root(self) -> Path:
        """Get the TKA project root directory."""
        if self._project_root is None:
            # Try to derive from desktop root
            if self._desktop_root is not None:
                # Desktop is typically at TKA/src/desktop
                candidate = self._desktop_root.parent.parent
                if candidate.name == "TKA":
                    self._project_root = candidate
            
            if self._project_root is None:
                raise RuntimeError("Could not locate TKA project root")
        return self._project_root
    
    @property
    def images_dir(self) -> Path:
        """Get the images directory path."""
        return self.desktop_root / "images"
    
    @property
    def data_dir(self) -> Path:
        """Get the data directory path."""
        return self.desktop_root / "data"
    
    def get_image_path(self, relative_path: str) -> Path:
        """
        Get absolute path to an image file.
        
        Args:
            relative_path: Path relative to images directory
            
        Returns:
            Absolute path to the image file
        """
        return self.images_dir / relative_path
    
    def get_data_path(self, relative_path: str) -> Path:
        """
        Get absolute path to a data file.
        
        Args:
            relative_path: Path relative to data directory
            
        Returns:
            Absolute path to the data file
        """
        return self.data_dir / relative_path
    
    def validate_paths(self) -> bool:
        """
        Validate that all essential paths exist.
        
        Returns:
            True if all paths are valid, False otherwise
        """
        try:
            essential_paths = [
                self.desktop_root,
                self.images_dir,
                self.data_dir,
            ]
            
            for path in essential_paths:
                if not path.exists():
                    print(f"❌ Essential path missing: {path}")
                    return False
            
            # Check for essential files
            diamond_csv = self.data_dir / "DiamondPictographDataframe.csv"
            if not diamond_csv.exists():
                print(f"❌ Essential file missing: {diamond_csv}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Path validation failed: {e}")
            return False
    
    def get_debug_info(self) -> dict:
        """Get debug information about resolved paths."""
        return {
            "desktop_root": str(self.desktop_root) if self._desktop_root else "Not found",
            "project_root": str(self.project_root) if self._project_root else "Not found", 
            "images_dir": str(self.images_dir),
            "data_dir": str(self.data_dir),
            "images_exists": self.images_dir.exists(),
            "data_exists": self.data_dir.exists(),
            "validation_passed": self.validate_paths(),
        }


# Global instance for easy access
path_resolver = TKAPathResolver()


# Convenience functions for backward compatibility
def get_image_path(relative_path: str) -> str:
    """Get absolute path to an image file as string."""
    path = path_resolver.get_image_path(relative_path)
    if not path.exists():
        print(f"Warning: Asset not found: {path}")
        print("Please ensure required assets are in desktop/images/")
    return str(path)


def get_data_path(relative_path: str) -> str:
    """Get absolute path to a data file as string."""
    return str(path_resolver.get_data_path(relative_path))


def get_desktop_root() -> str:
    """Get desktop root directory as string."""
    return str(path_resolver.desktop_root)


def get_images_dir() -> str:
    """Get images directory as string."""
    return str(path_resolver.images_dir)


def get_data_dir() -> str:
    """Get data directory as string."""
    return str(path_resolver.data_dir)
