"""
TKA Monorepo Project Root Configuration
======================================

This module establishes the canonical project root for the TKA monorepo
and sets up Python paths consistently across all execution contexts.

The TKA monorepo structure:
- TKA/ (root)
  - src/desktop/modern/src/ (modern desktop application)
  - src/desktop/legacy/src/ (legacy desktop application)
  - launcher/ (application launcher)
  - packages/ (shared packages)

Import this at the top of any script that needs reliable imports:
    from project_root import ensure_project_setup
    ensure_project_setup()
"""

import os
import sys
from pathlib import Path
from typing import List

# Global flag to prevent duplicate setup
_SETUP_COMPLETED = False


def get_project_root() -> Path:
    """
    Get the absolute path to the TKA monorepo root directory.
    This works regardless of where any script is executed from.

    Returns:
        Path: Absolute path to TKA/ directory (monorepo root)
    """
    return Path(__file__).parent.absolute()


def get_modern_src_root() -> Path:
    """
    Get the absolute path to the modern desktop src directory.

    Returns:
        Path: Absolute path to TKA/src/desktop/modern/src/ directory
    """
    return get_project_root() / "src" / "desktop" / "modern" / "src"


def get_modern_root() -> Path:
    """
    Get the absolute path to the modern desktop directory.

    Returns:
        Path: Absolute path to TKA/src/desktop/modern/ directory
    """
    return get_project_root() / "src" / "desktop" / "modern"


def get_legacy_src_root() -> Path:
    """
    Get the absolute path to the legacy desktop src directory.

    Returns:
        Path: Absolute path to TKA/src/desktop/legacy/src/ directory
    """
    return get_project_root() / "src" / "desktop" / "legacy" / "src"


def get_launcher_root() -> Path:
    """
    Get the absolute path to the launcher directory.

    Returns:
        Path: Absolute path to TKA/launcher/ directory
    """
    return get_project_root() / "launcher"


def get_packages_root() -> Path:
    """
    Get the absolute path to the packages directory.

    Returns:
        Path: Absolute path to TKA/packages/ directory
    """
    return get_project_root() / "packages"


def get_import_paths() -> List[Path]:
    """
    Get all required Python import paths for the TKA monorepo.

    Returns:
        List[Path]: All paths that should be in sys.path
    """
    project_root = get_project_root()

    return [
        # Most specific paths first for proper module resolution
        get_modern_src_root(),  # Primary modern source code
        get_modern_root(),  # Modern directory (for tests)
        get_modern_root() / "tests",  # Modern tests
        get_legacy_src_root(),  # Legacy source code
        project_root / "src" / "desktop" / "legacy",  # Legacy root (for tests)
        project_root / "src" / "desktop",  # Desktop root
        get_launcher_root(),  # Launcher
        get_packages_root(),  # Shared packages
        project_root / "src",  # Src root
        project_root,  # TKA Monorepo root
    ]


def setup_python_paths(force: bool = False) -> bool:
    """
    Setup Python import paths consistently for the entire TKA monorepo.

    Args:
        force: If True, setup even if already completed

    Returns:
        bool: True if setup was successful
    """
    global _SETUP_COMPLETED

    if _SETUP_COMPLETED and not force:
        return True

    try:
        import_paths = get_import_paths()

        # Add paths to sys.path in correct order (most specific first)
        for path in import_paths:
            path_str = str(path)
            if path_str not in sys.path:
                sys.path.insert(0, path_str)

        # Set PYTHONPATH environment variable for subprocess consistency
        pythonpath_parts = [str(p) for p in import_paths]
        existing_pythonpath = os.environ.get("PYTHONPATH", "")

        if existing_pythonpath:
            # Avoid duplicates
            existing_parts = existing_pythonpath.split(os.pathsep)
            pythonpath_parts.extend(
                [p for p in existing_parts if p not in pythonpath_parts]
            )

        os.environ["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

        _SETUP_COMPLETED = True
        return True

    except Exception as e:
        print(f"ERROR: Failed to setup TKA monorepo paths: {e}")
        return False


def ensure_project_setup() -> bool:
    """
    Ensures TKA monorepo is properly set up. Call this from any entry point.
    This is the main function that should be imported and called.

    Returns:
        bool: True if setup successful
    """
    return setup_python_paths()


def validate_imports() -> bool:
    """
    Validate that key imports work correctly from the TKA monorepo structure.

    Returns:
        bool: True if all key imports work
    """
    test_imports = [
        # Core modern imports
        "domain.models.core_models",
        "domain.models.pictograph_models",
        "core.events",
        "core.dependency_injection.di_container",
    ]

    successful = 0
    for import_name in test_imports:
        try:
            __import__(import_name)
            print(f"✅ {import_name}")
            successful += 1
        except ImportError as e:
            print(f"❌ {import_name}: {e}")

    print(f"\n📊 {successful}/{len(test_imports)} imports successful")
    return successful == len(test_imports)


def print_debug_info():
    """Print debugging information about paths and imports."""
    print("=== TKA MONOREPO IMPORT DEBUG INFO ===")
    print(f"TKA Monorepo Root: {get_project_root()}")
    print(f"Modern Src Root: {get_modern_src_root()}")
    print(f"Modern Root: {get_modern_root()}")
    print(f"Legacy Src Root: {get_legacy_src_root()}")
    print(f"Launcher Root: {get_launcher_root()}")
    print(f"Packages Root: {get_packages_root()}")
    print(f"Current Working Directory: {Path.cwd()}")
    print(f"Setup Completed: {_SETUP_COMPLETED}")

    print("\nImport Paths:")
    for i, path in enumerate(get_import_paths()):
        exists = "✅" if path.exists() else "❌"
        print(f"  {i+1}. {exists} {path}")

    print(f"\nPython sys.path (first 15 entries):")
    for i, path in enumerate(sys.path[:15]):
        print(f"  {i+1}. {path}")

    print(f"\nPYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")


# BULLETPROOF AUTO-SETUP: This runs automatically when ANY Python file imports this module
if __name__ != "__main__":
    try:
        ensure_project_setup()
    except Exception as e:
        # Fail silently to avoid breaking imports, but log the issue
        import warnings

        warnings.warn(f"TKA Monorepo auto-setup failed: {e}", UserWarning)

# Export key constants and functions
PROJECT_ROOT = get_project_root()
MODERN_SRC = get_modern_src_root()
MODERN_DIR = get_modern_root()
LEGACY_SRC = get_legacy_src_root()
LAUNCHER_ROOT = get_launcher_root()
PACKAGES_ROOT = get_packages_root()

__all__ = [
    "ensure_project_setup",  # Main function - import and call this
    "get_project_root",
    "get_modern_src_root",
    "get_modern_root",
    "get_legacy_src_root",
    "get_launcher_root",
    "get_packages_root",
    "setup_python_paths",
    "validate_imports",
    "print_debug_info",
    "PROJECT_ROOT",
    "MODERN_SRC",
    "MODERN_DIR",
    "LEGACY_SRC",
    "LAUNCHER_ROOT",
    "PACKAGES_ROOT",
]

# If run directly, provide debugging info
if __name__ == "__main__":
    print("TKA Monorepo Project Root Setup")
    ensure_project_setup()
    print_debug_info()
    print("\nValidating imports...")
    validate_imports()
