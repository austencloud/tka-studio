"""
Domain Operations Module

Contains all domain-level operations including CAP transformations.
"""

from __future__ import annotations

from .cap_operations import (
    CAPExecutorFactory,
    CAPOperation,
    CAPType,
    StrictMirroredCAP,
    StrictRotatedCAP,
    apply_cap_to_sequence,
)


__all__ = [
    "CAPExecutorFactory",
    "CAPOperation",
    "CAPType",
    "StrictMirroredCAP",
    "StrictRotatedCAP",
    "apply_cap_to_sequence",
]
