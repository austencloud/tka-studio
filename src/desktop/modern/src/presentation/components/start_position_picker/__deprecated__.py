"""
DEPRECATED: Enhanced Start Position Picker

This component has been replaced by UnifiedStartPositionPicker.

The Enhanced/Advanced/Basic picker hierarchy has been consolidated into a single,
mode-aware component that's easier to maintain and port to web.

Migration:
- Use UnifiedStartPositionPicker instead
- Set initial_mode parameter for desired behavior:
  - PickerMode.BASIC: 3 positions (old basic behavior)
  - PickerMode.ADVANCED: 16 positions (old advanced behavior)
  - PickerMode.AUTO: responsive switching (recommended)

New unified component provides:
- Same functionality with simpler architecture
- Smooth mode transitions
- Better responsive behavior
- Easier web translation
- Single component to maintain

This file will be removed in a future release.
"""

# Re-export the unified component for backward compatibility
from .start_position_picker import PickerMode
from .start_position_picker import StartPositionPicker
from .start_position_picker import StartPositionPicker as EnhancedStartPositionPicker

# Legacy alias
AdvancedStartPositionPicker = StartPositionPicker

__all__ = ["EnhancedStartPositionPicker", "AdvancedStartPositionPicker", "PickerMode"]
