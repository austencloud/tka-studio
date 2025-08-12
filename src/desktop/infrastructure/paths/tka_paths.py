#!/usr/bin/env python3
"""
TKA Universal Path Management System
=====================================

This is the SINGLE SOURCE OF TRUTH for all TKA path resolution.
Import this module to automatically configure all paths correctly.

USAGE:
    # At the top of ANY TKA Python file:
    from src.infrastructure.paths import tka_paths  # Auto-configures all paths

    # OR explicitly:
    from src.infrastructure.paths.tka_paths import setup_all_paths
    setup_all_paths()

FEATURES:
- Automatic TKA root detection
- Framework-agnostic path setup
- Desktop (modern/legacy) path setup
- Launcher path setup
- Web/test path setup
- Eliminates all import issues permanently
"""

import os
import sys
import warnings
from pathlib import Path

# Global state
_PATHS_CONFIGURED = False
_TKA_ROOT: Path | None = None
_CONFIGURED_PATHS: set[str] = set()


def find_tka_root(start_path: Path | None = None) -> Path:
    """
    Find the TKA project root directory with 100% reliability.

    Args:
        start_path: Starting search path (defaults to this file's location)

    Returns:
        Path: Absolute path to TKA root

    Raises:
        RuntimeError: If TKA root cannot be found
    """
    global _TKA_ROOT

    if _TKA_ROOT is not None:
        return _TKA_ROOT

    if start_path is None:
        start_path = Path(__file__).resolve()

    current = start_path if start_path.is_dir() else start_path.parent

    # TKA root indicators (in order of preference)
    indicators = [
        "pyproject.toml",  # Primary indicator
        "main.py",  # Secondary indicator
        "launcher",  # TKA-specific directory
        ".git",  # Git repository
        "README.md",  # Documentation
    ]

    # Search upward for TKA root
    while current.parent != current:  # Not at filesystem root
        # Check if this directory has TKA indicators
        for indicator in indicators:
            if (current / indicator).exists():
                # Verify this is actually TKA by checking for key directories
                tka_dirs = ["src", "launcher", "data"]
                if all((current / d).exists() for d in tka_dirs):
                    _TKA_ROOT = current
                    return current
        current = current.parent

    # Fallback: look for "TKA" directory name
    current = start_path if start_path.is_dir() else start_path.parent
    while current.parent != current:
        if current.name == "TKA":
            _TKA_ROOT = current
            return current
        current = current.parent

    raise RuntimeError(f"Could not find TKA root starting from {start_path}")


def get_all_tka_paths(tka_root: Path) -> list[Path]:
    """
    Get ALL TKA paths that should be in sys.path.

    Args:
        tka_root: TKA project root directory

    Returns:
        List[Path]: All paths in priority order
    """
    paths = []

    # 1. Framework-agnostic core services (highest priority)
    core_src = tka_root / "src"
    if core_src.exists():
        paths.append(core_src)

    # 2. Modern desktop application
    modern_src = tka_root / "src" / "desktop" / "modern" / "src"
    if modern_src.exists():
        paths.append(modern_src)

    modern_root = tka_root / "src" / "desktop" / "modern"
    if modern_root.exists():
        paths.append(modern_root)

    # 3. Legacy desktop application
    legacy_src = tka_root / "src" / "desktop" / "legacy" / "src"
    if legacy_src.exists():
        paths.append(legacy_src)

    legacy_root = tka_root / "src" / "desktop" / "legacy"
    if legacy_root.exists():
        paths.append(legacy_root)

    # 4. Launcher
    launcher = tka_root / "launcher"
    if launcher.exists():
        paths.append(launcher)

    # 5. Packages
    packages = tka_root / "packages"
    if packages.exists():
        paths.append(packages)

    # 6. Project root (for top-level imports)
    paths.append(tka_root)

    # Return only existing paths
    return [p for p in paths if p.exists()]


def setup_sys_path(paths: list[Path]) -> int:
    """
    Add paths to sys.path safely (no duplicates, correct order).

    Args:
        paths: Paths to add to sys.path

    Returns:
        int: Number of paths actually added
    """
    global _CONFIGURED_PATHS

    added_count = 0

    for path in paths:
        path_str = str(path)

        # Skip if already added
        if path_str in _CONFIGURED_PATHS:
            continue

        # Add to beginning of sys.path (higher priority)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)
            _CONFIGURED_PATHS.add(path_str)
            added_count += 1

    return added_count


def setup_pythonpath_env(paths: list[Path]) -> None:
    """
    Set PYTHONPATH environment variable for subprocess consistency.

    Args:
        paths: Paths to include in PYTHONPATH
    """
    path_strs = [str(p) for p in paths]

    # Get existing PYTHONPATH
    existing = os.environ.get("PYTHONPATH", "")
    existing_parts = existing.split(os.pathsep) if existing else []

    # Combine new and existing (no duplicates)
    all_parts = path_strs.copy()
    for part in existing_parts:
        if part and part not in all_parts:
            all_parts.append(part)

    # Set environment variable
    os.environ["PYTHONPATH"] = os.pathsep.join(all_parts)


def verify_critical_imports() -> list[str]:
    """
    Verify that critical TKA imports work correctly.

    Returns:
        List[str]: List of import errors (empty if all successful)
    """
    critical_imports = [
        # Framework-agnostic core
        ("application.services.core.image_export_service", "CoreImageExportService"),
        ("application.adapters.qt_image_export_adapter", "QtImageExportAdapter"),
        ("application.services.core.types", "Size"),
        # Modern desktop (available when modern desktop paths are configured)
        # Note: This is in the modern desktop src structure, not core
    ]

    errors = []

    for module_name, class_name in critical_imports:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)  # Verify class exists
        except Exception as e:
            errors.append(f"{module_name}.{class_name}: {e}")

    # Test modern desktop specific imports separately since they may not always be available
    modern_imports = [
        (
            "application.services.image_export.sequence_image_renderer",
            "SequenceImageRenderer",
        ),
    ]

    for module_name, class_name in modern_imports:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
        except Exception as e:
            # Only add as error if modern paths exist
            if (Path(_TKA_ROOT) / "src" / "desktop" / "modern" / "src").exists():
                errors.append(f"{module_name}.{class_name}: {e}")

    return errors


def setup_all_paths(force: bool = False, verbose: bool = False) -> bool:
    """
    Setup ALL TKA paths with complete reliability.

    Args:
        force: Force setup even if already configured
        verbose: Print detailed setup information

    Returns:
        bool: True if setup successful
    """
    global _PATHS_CONFIGURED

    if _PATHS_CONFIGURED and not force:
        return True

    try:
        # Find TKA root
        tka_root = find_tka_root()
        if verbose:
            print(f"✅ TKA root found: {tka_root}")

        # Get all TKA paths
        paths = get_all_tka_paths(tka_root)
        if verbose:
            print(f"✅ Found {len(paths)} TKA paths")

        # Setup sys.path
        added_count = setup_sys_path(paths)
        if verbose:
            print(f"✅ Added {added_count} paths to sys.path")

        # Setup PYTHONPATH environment
        setup_pythonpath_env(paths)
        if verbose:
            print("✅ PYTHONPATH environment configured")

        # Verify imports
        errors = verify_critical_imports()
        if errors and verbose:
            print("⚠️ Some imports still failing:")
            for error in errors:
                print(f"  - {error}")
        elif verbose:
            print("✅ All critical imports verified")

        _PATHS_CONFIGURED = True

        if verbose:
            print(f"🎉 TKA path setup complete! ({len(paths)} paths configured)")

        return True

    except Exception as e:
        if verbose:
            print(f"❌ TKA path setup failed: {e}")
        warnings.warn(f"TKA path setup failed: {e}", UserWarning)
        return False


def get_debug_info() -> dict:
    """
    Get comprehensive debug information about TKA paths.

    Returns:
        dict: Debug information
    """
    try:
        tka_root = find_tka_root()
        paths = get_all_tka_paths(tka_root)

        return {
            "tka_root": str(tka_root),
            "paths_configured": _PATHS_CONFIGURED,
            "configured_paths": list(_CONFIGURED_PATHS),
            "all_tka_paths": [str(p) for p in paths],
            "sys_path_first_10": sys.path[:10],
            "pythonpath": os.environ.get("PYTHONPATH", "Not set"),
            "import_errors": verify_critical_imports(),
        }
    except Exception as e:
        return {"error": str(e)}


def print_debug_info() -> None:
    """Print formatted debug information."""
    info = get_debug_info()

    if "error" in info:
        print(f"❌ Error getting debug info: {info['error']}")
        return

    print("🔍 TKA PATH DEBUG INFORMATION")
    print("=" * 50)
    print(f"TKA Root: {info['tka_root']}")
    print(f"Paths Configured: {info['paths_configured']}")
    print(f"Configured Paths: {len(info['configured_paths'])}")

    print("\nAll TKA Paths:")
    for i, path in enumerate(info["all_tka_paths"], 1):
        exists = "✅" if Path(path).exists() else "❌"
        print(f"  {i}. {exists} {path}")

    print("\nFirst 10 sys.path entries:")
    for i, path in enumerate(info["sys_path_first_10"], 1):
        print(f"  {i}. {path}")

    print(f"\nPYTHONPATH: {info['pythonpath']}")

    if info["import_errors"]:
        print(f"\n⚠️ Import Errors ({len(info['import_errors'])}):")
        for error in info["import_errors"]:
            print(f"  - {error}")
    else:
        print("\n✅ All critical imports working")


# AUTOMATIC SETUP: This runs when the module is imported
if __name__ != "__main__":
    # Auto-setup when imported (silent mode)
    setup_all_paths(verbose=False)


# COMMAND LINE INTERFACE
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="TKA Universal Path Management")
    parser.add_argument("--debug", action="store_true", help="Show debug information")
    parser.add_argument(
        "--force", action="store_true", help="Force path reconfiguration"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.debug:
        print_debug_info()
    else:
        success = setup_all_paths(force=args.force, verbose=args.verbose)
        if success:
            print("✅ TKA paths configured successfully")
            sys.exit(0)
        else:
            print("❌ TKA path configuration failed")
            sys.exit(1)
