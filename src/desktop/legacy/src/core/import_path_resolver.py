"""
Intelligent Import Path Resolver for TKA Legacy Application

This module provides automatic import path resolution for 'core.*' modules,
finding the correct core directory regardless of the current file's location.
"""

import importlib.util
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class CoreImportResolver:
    """
    Intelligent resolver for core module imports that can find the correct
    core directory regardless of the current file's location.
    """

    _instance = None
    _core_mappings: Dict[str, Path] = {}
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._scan_core_directories()
            self._initialized = True

    def _scan_core_directories(self):
        """Scan for all core directories and their modules."""
        # Start from the current file and search upward
        current_path = Path(__file__).parent
        project_root = self._find_project_root(current_path)

        if project_root:
            self._scan_directory_for_cores(project_root)

    def _find_project_root(self, start_path: Path) -> Optional[Path]:
        """Find the project root by looking for key indicators."""
        current = start_path

        # Look for project indicators
        indicators = [
            "pyproject.toml",
            "requirements.txt",
            "main.py",
            ".git",
            "README.md",
        ]

        while current.parent != current:  # Stop at filesystem root
            for indicator in indicators:
                if (current / indicator).exists():
                    return current
            current = current.parent

        return None

    def _scan_directory_for_cores(self, root: Path):
        """Recursively scan for core directories and map their modules."""
        try:
            for core_dir in root.rglob("core"):
                if core_dir.is_dir() and (core_dir / "__init__.py").exists():
                    self._scan_core_modules(core_dir)
        except Exception as e:
            logger.warning(f"Error scanning core directories: {e}")

    def _scan_core_modules(self, core_dir: Path):
        """Scan a specific core directory for Python modules."""
        try:
            for py_file in core_dir.rglob("*.py"):
                if py_file.name == "__init__.py":
                    continue

                # Create module path relative to core directory
                relative_path = py_file.relative_to(core_dir)
                module_parts = list(relative_path.with_suffix("").parts)
                module_name = ".".join(module_parts)

                # Store full path with core prefix
                full_module_name = f"core.{module_name}"

                # Only store if not already mapped or if this is a more specific match
                if full_module_name not in self._core_mappings:
                    self._core_mappings[full_module_name] = py_file
                    logger.debug(f"Mapped {full_module_name} -> {py_file}")
        except Exception as e:
            logger.warning(f"Error scanning core modules in {core_dir}: {e}")

    def resolve_core_import(
        self, module_name: str, requesting_file: Optional[str] = None
    ) -> Optional[Path]:
        """
        Resolve a core module import to its actual file path.

        Args:
            module_name: The module name (e.g., 'core.glassmorphism_styler')
            requesting_file: The file making the request (for context-aware resolution)

        Returns:
            Path to the actual module file, or None if not found
        """
        if not module_name.startswith("core."):
            return None

        # Try exact match first
        if module_name in self._core_mappings:
            return self._core_mappings[module_name]

        # Try fuzzy matching for partial module names
        module_suffix = module_name[5:]  # Remove 'core.' prefix

        for mapped_name, path in self._core_mappings.items():
            if mapped_name.endswith(module_suffix):
                return path

        # If requesting file is provided, try context-aware resolution
        if requesting_file:
            return self._context_aware_resolve(module_name, requesting_file)

        return None

    def _context_aware_resolve(
        self, module_name: str, requesting_file: str
    ) -> Optional[Path]:
        """
        Attempt to resolve based on the requesting file's location.
        """
        requesting_path = Path(requesting_file).parent
        module_suffix = module_name[5:]  # Remove 'core.' prefix

        # Look for core directories in the same hierarchy
        current = requesting_path
        while current.parent != current:
            potential_core = current / "core"
            if potential_core.exists():
                potential_module = potential_core / f"{module_suffix}.py"
                if potential_module.exists():
                    return potential_module

                # Try nested paths
                for py_file in potential_core.rglob(f"{module_suffix}.py"):
                    return py_file

            current = current.parent

        return None

    def install_import_hook(self):
        """Install the import hook to automatically resolve core imports."""
        if not hasattr(sys, "meta_path"):
            return

        # Remove existing hook if present
        for finder in sys.meta_path[:]:
            if isinstance(finder, CoreImportFinder):
                sys.meta_path.remove(finder)

        # Install new hook
        sys.meta_path.insert(0, CoreImportFinder(self))
        logger.info("Core import hook installed successfully")

    def get_mappings(self) -> Dict[str, Path]:
        """Get all current core module mappings for debugging."""
        return self._core_mappings.copy()


class CoreImportFinder:
    """Meta path finder for core module imports."""

    def __init__(self, resolver: CoreImportResolver):
        self.resolver = resolver

    def find_spec(self, fullname: str, path=None, target=None):
        """Find module spec for core imports."""
        if not fullname.startswith("core."):
            return None

        # Get the file that's trying to import
        frame = sys._getframe(1)
        requesting_file = frame.f_globals.get("__file__")

        module_path = self.resolver.resolve_core_import(fullname, requesting_file)
        if module_path and module_path.exists():
            spec = importlib.util.spec_from_file_location(fullname, str(module_path))
            return spec

        return None


# Global resolver instance
_resolver = CoreImportResolver()


def install_core_import_resolver():
    """Install the core import resolver globally."""
    global _resolver
    _resolver.install_import_hook()
    return _resolver


def get_core_mappings() -> Dict[str, Path]:
    """Get all core module mappings for debugging."""
    global _resolver
    return _resolver.get_mappings()


# Auto-install on import
install_core_import_resolver()
