"""
Modern Animation Service - this replaces the legacy animation_service.py

For the complete modern implementation, see:
- animation_orchestrator.py (main orchestration)
- core/animation/animation_engine.py (core engine)
- adapters/qt_adapters.py (Qt-specific adapters)
"""

# For backward compatibility during migration, import from new location
from .animation_orchestrator import ModernAnimationOrchestrator as AnimationService

__all__ = ['AnimationService']
