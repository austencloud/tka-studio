"""
TKA Modern Data Module

Organized data structure following clean architecture principles.

Structure:
- core/: Core business data (constants, types, mappings)
- datasets/: CSV datasets and data processing
- layouts/: Layout and positioning configurations
- dictionary/: User-created sequences
- settings/: Application configuration
- runtime/: Generated and temporary data

This module provides a clean, organized alternative to the legacy data/ structure.
Use this for new code and gradually migrate existing references.
"""

# Re-export commonly used items for backward compatibility
try:
    from .core.constants import *
    from .core.types import *
except ImportError:
    # Graceful fallback if files don't exist yet
    pass

__version__ = "1.0.0"
__all__ = [
    "core",
    "datasets", 
    "layouts",
    "dictionary",
    "settings",
    "runtime",
    "domain"
]
