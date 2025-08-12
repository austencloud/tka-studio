"""
Core package for legacy TKA application.
Provides unified access to core modules from different locations.
"""

# Re-export modules from main core directory
try:
    from .application_context import ApplicationContext
    from .dependency_container import configure_dependencies
except ImportError as e:
    print(f"Warning: Could not import from main core: {e}")

# Import from settings dialog core directory
try:
    import os
    import sys
    from pathlib import Path

    # Get the absolute path to the settings dialog core
    current_dir = Path(__file__).parent
    settings_core_path = (
        current_dir.parent / "main_window" / "main_widget" / "settings_dialog" / "core"
    )

    if settings_core_path.exists():
        # Add to path temporarily
        settings_core_str = str(settings_core_path)
        if settings_core_str not in sys.path:
            sys.path.insert(0, settings_core_str)

        try:
            import glassmorphism_styler

            GlassmorphismStyler = glassmorphism_styler.GlassmorphismStyler
        finally:
            # Remove the temporary path
            if settings_core_str in sys.path:
                sys.path.remove(settings_core_str)
    else:
        print(f"Warning: Settings core path not found: {settings_core_path}")

except Exception as e:
    print(f"Warning: Could not import glassmorphism_styler: {e}")

# Make everything available at package level
__all__ = [
    "ApplicationContext",
    "configure_dependencies",
    "GlassmorphismStyler",
]
