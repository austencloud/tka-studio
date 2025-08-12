from __future__ import annotations
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
    # Try relative import first (when imported as a package)
    from ..main_window.main_widget.settings_dialog.core import GlassmorphismStyler
except ImportError:
    try:
        # Try absolute import from project root
        from src.desktop.legacy.src.main_window.main_widget.settings_dialog.core import (
            GlassmorphismStyler,
        )
    except ImportError:
        try:
            # Try direct import (when paths are set up)
            from main_window.main_widget.settings_dialog.core import GlassmorphismStyler
        except ImportError as e:
            print(f"Warning: Could not import from settings dialog core: {e}")
            GlassmorphismStyler = None

# Make everything available at package level
__all__ = [
    "ApplicationContext",
    "configure_dependencies",
    "GlassmorphismStyler",
]
