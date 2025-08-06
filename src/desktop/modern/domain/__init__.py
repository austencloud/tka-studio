# Modern Domain Module

# Export models for easy importing
from __future__ import annotations


__all__ = (
    [
        # Re-export everything from models
    ]
    + getattr(
        __import__("desktop.modern.domain.models", fromlist=["__all__"]), "__all__", []
    )
)
