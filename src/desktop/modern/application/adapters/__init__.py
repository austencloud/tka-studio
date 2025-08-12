"""Application Adapters."""

from __future__ import annotations

# Import from modern adapters - these modules are now in the modern directory
__all__ = []

try:
    from desktop.modern.application.adapters.qt_image_export_adapter import (
        QtImageExportAdapter,
    )
    __all__.append("QtImageExportAdapter")

except ImportError:
    # PyQt6 not available - that's okay for testing environments
    pass

try:
    from desktop.modern.application.adapters.qt_pictograph_adapter import (
        QtPictographAdapter,
    )
    __all__.append("QtPictographAdapter")

except ImportError:
    # PyQt6 not available - that's okay for testing environments
    pass
