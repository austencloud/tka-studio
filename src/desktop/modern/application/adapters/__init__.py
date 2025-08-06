"""Application Adapters."""

# Import shared src modules to make them available in the modern src namespace
from __future__ import annotations


try:
    # Import from shared src - these modules exist in the TKA/src directory
    from pathlib import Path
    import sys

    # Find and add shared src to path if not already there
    current_file = Path(__file__).resolve()
    # Navigate up: __init__.py -> adapters -> application -> src -> desktop -> modern -> src -> desktop -> TKA
    tka_root = current_file.parents[7]
    shared_src = tka_root / "src"

    if shared_src.exists() and str(shared_src) not in sys.path:
        sys.path.append(str(shared_src))

    # Now import the shared modules
    from shared.application.adapters.qt_image_export_adapter import QtImageExportAdapter

    # Make them available in this namespace
    __all__ = ["QtImageExportAdapter"]

except ImportError:
    # If shared modules aren't available, that's okay - they're optional
    pass
