"""
TKA Graph Editor Animation Package
=================================

Clean, focused animation components for the graph editor.

This package contains the refactored animation system that replaces the monolithic
animation controller with focused, single-responsibility classes:

- AnimationSizeCalculator: Size calculations and workbench tracking
- AnimationStateManager: Race-condition-free state management
- AnimationSynchronizer: Toggle tab synchronization
- GraphEditorAnimationController: Clean PyQt6 animation coordination

Each class has a single responsibility and can be tested independently.
"""

from .animation_size_calculator import AnimationSizeCalculator
from .animation_state_manager import AnimationStateManager
from .animation_synchronizer import AnimationSynchronizer

__all__ = ["AnimationSizeCalculator", "AnimationStateManager", "AnimationSynchronizer"]
