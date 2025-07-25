"""
Domain Operations Module

Contains all domain-level operations including CAP transformations.
"""

from .cap_operations import (
    CAPType,
    CAPOperation,
    StrictRotatedCAP,
    StrictMirroredCAP,
    CAPExecutorFactory,
    apply_cap_to_sequence,
)

__all__ = [
    "CAPType",
    "CAPOperation", 
    "StrictRotatedCAP",
    "StrictMirroredCAP",
    "CAPExecutorFactory",
    "apply_cap_to_sequence",
]
