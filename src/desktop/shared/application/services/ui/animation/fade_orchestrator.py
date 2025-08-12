"""
Modern Fade Orchestrator - this replaces the legacy fade_orchestrator.py

For the complete modern implementation, see:
- animation_orchestrator.py (main implementation)
- ModernAnimationOrchestrator class
- LegacyFadeManagerWrapper for migration
"""

# For backward compatibility during migration, import from new location
from .animation_orchestrator import LegacyFadeManagerWrapper
from .animation_orchestrator import ModernAnimationOrchestrator as FadeOrchestrator

__all__ = ["FadeOrchestrator", "LegacyFadeManagerWrapper"]
