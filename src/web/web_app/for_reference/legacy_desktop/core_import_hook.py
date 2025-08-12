from __future__ import annotations
"""
Smart Core Import Hook

Automatically resolves 'core.*' imports to the correct core directory
without requiring manual path setup or imports.

This hook intercepts imports starting with 'core.' and intelligently
locates the correct core directory based on the calling file's location.
"""

import importlib.machinery
import importlib.util
import os
import sys
from pathlib import Path


class CoreImportFinder:
    """Custom import finder that resolves 'core.*' imports intelligently."""

    def __init__(self):
        self.core_directories = self._find_all_core_directories()

    def _find_all_core_directories(self) -> list[Path]:
        """Find all 'core' directories in the project."""
        core_dirs = []

        # Start from the desktop directory
        desktop_path = Path(__file__).parent.parent.parent / "desktop"

        # Recursively find all 'core' directories
        for root, dirs, files in os.walk(desktop_path):
            if "core" in dirs:
                core_path = Path(root) / "core"
                if core_path.is_dir():
                    core_dirs.append(core_path)

        return core_dirs

    def find_spec(self, fullname: str, path: list[str] | None, target=None):
        """Find the module spec for core.* imports."""
        if not fullname.startswith("core."):
            return None

        module_name = fullname.split(".", 1)[1]  # Remove 'core.' prefix

        # Try to find the module in any available core directory
        for core_dir in self.core_directories:
            module_path = core_dir / f"{module_name}.py"
            if module_path.exists():
                spec = importlib.util.spec_from_file_location(fullname, module_path)
                return spec

        return None

    def _find_best_core_directory(
        self, calling_path: Path, module_name: str
    ) -> Path | None:
        """Find the best core directory for the given module."""
        candidates = []

        # Check each core directory for the module
        for core_dir in self.core_directories:
            module_path = core_dir / f"{module_name}.py"
            if module_path.exists():
                # Calculate how close this core directory is to the calling file
                try:
                    # Try to find common path
                    common_path = os.path.commonpath([calling_path, core_dir])
                    distance = (
                        len(calling_path.parts)
                        + len(core_dir.parts)
                        - 2 * len(Path(common_path).parts)
                    )
                    candidates.append((distance, core_dir))
                except ValueError:
                    # Paths are on different drives, use absolute distance
                    candidates.append((1000, core_dir))

        if candidates:
            # Return the closest core directory
            candidates.sort(key=lambda x: x[0])
            return candidates[0][1]

        return None


class CoreImportLoader:
    """Custom import loader for core modules."""

    def __init__(self, spec):
        self.spec = spec

    def create_module(self, spec):
        """Create the module."""
        return  # Use default module creation

    def exec_module(self, module):
        """Execute the module."""
        with open(self.spec.origin, encoding="utf-8") as f:
            source = f.read()

        # Compile and execute the module
        code = compile(source, self.spec.origin, "exec")
        exec(code, module.__dict__)


def install_core_import_hook():
    """Install the core import hook into Python's import system."""
    # Remove any existing core import hook
    sys.meta_path = [
        finder for finder in sys.meta_path if not isinstance(finder, CoreImportFinder)
    ]

    # Add our custom finder to the beginning of meta_path
    sys.meta_path.insert(0, CoreImportFinder())


# Auto-install the hook when this module is imported
install_core_import_hook()
