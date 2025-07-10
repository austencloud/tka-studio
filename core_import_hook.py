"""
Core Import Hook - Automatic resolution of 'core.*' imports

This hook automatically resolves imports like `from core.glassmorphism_styler import GlassmorphismStyler`
to the correct core directory based on the calling file's location.

Usage:
    Just import this module at the start of your application:
    import core_import_hook

    Then use normal imports:
    from core.glassmorphism_styler import GlassmorphismStyler
"""

import sys
import os
import importlib.util
from pathlib import Path
from importlib.abc import MetaPathFinder, Loader
from types import ModuleType
import inspect


class CorePackageLoader(Loader):
    """Loader that creates a virtual core package."""

    def __init__(self, fullname, core_path):
        self.fullname = fullname
        self.core_path = core_path

    def create_module(self, spec):
        """Create a virtual core package module."""
        return None  # Use default creation

    def exec_module(self, module):
        """Execute the virtual core package."""
        # Set up the package
        module.__path__ = [str(self.core_path)]
        module.__file__ = str(self.core_path / "__init__.py")
        module.__package__ = "core"


class CoreImportLoader(Loader):
    """Loader that handles core.* imports by finding the correct core directory."""

    def __init__(self, fullname, core_path):
        self.fullname = fullname
        self.core_path = core_path

    def create_module(self, spec):
        """Create module - return None to use default creation."""
        return None

    def exec_module(self, module):
        """Execute module by loading from the correct core directory."""
        # Get the actual module name (after 'core.')
        module_name = self.fullname.split(".", 1)[1]
        module_path = self.core_path / f"{module_name}.py"

        if not module_path.exists():
            raise ImportError(
                f"No module named '{self.fullname}' (searched in {self.core_path})"
            )

        # Load the module from the correct path
        spec = importlib.util.spec_from_file_location(self.fullname, module_path)
        if spec is None:
            raise ImportError(
                f"Could not load spec for '{self.fullname}' from {module_path}"
            )

        # Create and execute the module
        temp_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(temp_module)

        # Copy all attributes to our module
        for attr_name in dir(temp_module):
            if not attr_name.startswith("_"):
                setattr(module, attr_name, getattr(temp_module, attr_name))


class CoreImportFinder(MetaPathFinder):
    """Meta path finder that locates core.* imports."""

    def find_spec(self, fullname, path, target=None):
        """Find spec for core.* imports."""
        if not (fullname == "core" or fullname.startswith("core.")):
            return None

        # Find the calling file to determine which core directory to use
        calling_file = self._find_calling_file()

        if not calling_file:
            return None

        # Find the appropriate core directory
        core_path = self._find_core_directory(calling_file)

        if not core_path:
            return None

        # Handle 'core' package itself
        if fullname == "core":
            # Create a virtual core package
            loader = CorePackageLoader(fullname, core_path)
            spec = importlib.util.spec_from_loader(fullname, loader)
            return spec

        # Handle 'core.module' imports
        module_name = fullname.split(".", 1)[1]
        module_path = core_path / f"{module_name}.py"

        if not module_path.exists():
            return None

        # Create a spec for this module
        loader = CoreImportLoader(fullname, core_path)
        spec = importlib.util.spec_from_loader(fullname, loader)
        return spec

    def _find_calling_file(self):
        """Find the file that's trying to import core.*"""
        frame = inspect.currentframe()
        try:
            # Walk up the stack to find the file doing the import
            while frame:
                frame = frame.f_back
                if frame is None:
                    break

                filename = frame.f_code.co_filename
                if filename and not filename.startswith("<"):
                    # Skip frames from the import system itself
                    if (
                        "importlib" not in filename
                        and "core_import_hook" not in filename
                        and "_bootstrap" not in filename
                        and "test_core_import_regression" not in filename
                    ):
                        return Path(filename)
        finally:
            del frame

        # If we can't find a specific calling file, use the project root as context
        return Path(__file__).parent / "dummy_context.py"

    def _find_core_directory(self, calling_file):
        """Find the appropriate core directory based on the calling file."""
        calling_dir = calling_file.parent

        # Search upward from the calling file for core directories
        current_dir = calling_dir
        while current_dir and current_dir != current_dir.parent:
            core_dir = current_dir / "core"
            if core_dir.exists() and core_dir.is_dir():
                return core_dir
            current_dir = current_dir.parent

        # If no core directory found in the path, search in common locations
        # Priority order: settings_dialog/core (has glassmorphism_styler), then others
        project_root = Path(__file__).parent
        common_core_locations = [
            project_root
            / "src"
            / "desktop"
            / "legacy"
            / "src"
            / "main_window"
            / "main_widget"
            / "settings_dialog"
            / "core",
            project_root / "src" / "desktop" / "legacy" / "src" / "core",
            project_root / "src" / "desktop" / "modern" / "src" / "core",
            project_root / "launcher" / "core",
        ]

        for core_path in common_core_locations:
            if core_path.exists() and core_path.is_dir():
                return core_path

        return None


# Install the hook automatically when this module is imported
def install_core_import_hook():
    """Install the core import hook."""
    # Only install if not already installed
    for finder in sys.meta_path:
        if isinstance(finder, CoreImportFinder):
            return  # Already installed

    # Insert at the beginning so it takes precedence
    sys.meta_path.insert(0, CoreImportFinder())
    # Removed verbose logging message


# Auto-install when module is imported
install_core_import_hook()
