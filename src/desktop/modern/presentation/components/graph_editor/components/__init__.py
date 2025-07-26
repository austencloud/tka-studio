"""
Graph Editor Components Package - Refactored Architecture
=========================================================

Professional UI components for the TKA graph editor following clean architecture patterns.

This package contains specialized components that provide:
- Pictograph display section with info panel integration
- Main adjustment panel with context-sensitive switching
- Dual orientation picker for start position controls
- Turn adjustment controls with 1.0/0.5 increments
- Detailed information panel for beat data display

Architecture:
- Component-based design with clear separation of concerns
- Signal-based communication between components
- Dependency injection support for service integration
- Immutable domain model integration
- 350-line maximum per component for maintainability
"""

# Refactored component imports
from .pictograph_display_section import PictographDisplaySection
from .main_adjustment_panel import MainAdjustmentPanel
from .detailed_info_panel import DetailedInfoPanel
from .dual_orientation_picker import DualOrientationPicker
from .turn_adjustment_controls.turn_adjustment_controls import TurnAdjustmentControls

# Legacy component imports (for backward compatibility)
from .adjustment_panel import AdjustmentPanel
from .pictograph_container import GraphEditorPictographContainer
from .orientation_picker import OrientationPickerWidget

__all__ = [
    # Refactored components (primary)
    "PictographDisplaySection",
    "MainAdjustmentPanel",
    "DetailedInfoPanel",
    "DualOrientationPicker",
    "TurnAdjustmentControls",
    # Legacy components (backward compatibility)
    "AdjustmentPanel",
    "GraphEditorPictographContainer",
    "OrientationPickerWidget",
]
