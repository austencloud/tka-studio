"""Core Services."""

from __future__ import annotations

# Import from modern core services - these modules are now in the modern directory
__all__ = []

# Core services (no Qt dependencies)
try:
    from desktop.modern.application.services.core.pictograph_renderer import (
        CorePictographRenderer,
    )
    __all__.append("CorePictographRenderer")
except ImportError:
    pass

try:
    from desktop.modern.application.services.core.image_export_service import (
        CoreImageExportService,
    )
    __all__.append("CoreImageExportService")
except ImportError:
    pass

try:
    from desktop.modern.application.services.core.thumbnail_service import (
        CoreThumbnailService,
    )
    __all__.append("CoreThumbnailService")
except ImportError:
    pass

# Qt adapters (may fail if PyQt6 not available)
try:
    from desktop.modern.application.adapters.qt_image_export_adapter import (
        QtImageExportAdapter,
    )
    __all__.append("QtImageExportAdapter")
except ImportError:
    # PyQt6 not available - that's okay for testing environments
    pass
