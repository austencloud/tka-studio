"""
CAP (Continuous Action Pattern) Definitions Module

Contains definitions and executors for CAP patterns used in TKA sequences.

Modules:
- halved_caps: Half-turn CAP patterns
- quartered_caps: Quarter-turn CAP patterns  
- cap_executors/: CAP execution logic and rotation mappings
"""

try:
    from .halved_CAPs import halved_CAPs
    from .quartered_CAPs import quartered_CAPs
    
except ImportError:
    pass

__all__ = [
    "halved_CAPs",
    "quartered_CAPs",
    "cap_executors"
]
