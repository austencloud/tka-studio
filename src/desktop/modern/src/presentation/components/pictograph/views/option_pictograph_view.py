"""
Option pictograph view - Direct view for option picker like legacy system.

This provides the same direct scaling approach as the legacy OptionView
without widget wrapper complexity.
"""

from typing import Optional, Callable
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QResizeEvent

from .base_pictograph_view import BasePictographView


class OptionPictographView(BasePictographView):
    """
    Direct pictograph view for option picker.
    
    Replicates the legacy OptionView scaling behavior:
    - Calculates size based on main window width and option picker width
    - Applies border width calculations
    - Scales view directly without widget wrapper
    """

    def __init__(self, parent=None, main_window_size_provider: Optional[Callable[[], QSize]] = None):
        super().__init__(parent)
        
        # Store size provider for legacy-style calculations
        self._main_window_size_provider = main_window_size_provider
        
        # Store option picker reference for width calculations
        self._option_picker_width = 800  # Default, will be updated
        
        # Apply option-specific styling
        self._setup_option_styling()

    def _setup_option_styling(self):
        """Apply option picker specific styling."""
        # Add border like legacy option view
        self.setStyleSheet("""
            OptionPictographView {
                border: 1px solid #ccc;
                background-color: white;
            }
        """)

    def set_option_picker_width(self, width: int):
        """Set the option picker width for size calculations."""
        self._option_picker_width = width
        self._recalculate_size()

    def _apply_view_specific_scaling(self):
        """Apply option picker specific scaling like legacy system."""
        # Calculate size using legacy formula
        size = self._calculate_legacy_option_size()
        
        # Apply the calculated size
        self.setFixedSize(size, size)
        
        # Apply legacy-style view scaling
        self._apply_legacy_view_scaling(size)

    def _calculate_legacy_option_size(self) -> int:
        """Calculate option size using exact legacy formula."""
        try:
            # Get main window width
            if self._main_window_size_provider:
                main_window_size = self._main_window_size_provider()
                main_window_width = main_window_size.width()
            else:
                # Fallback to parent window
                parent_window = self.window()
                main_window_width = parent_window.width() if parent_window else 1000

            # LEGACY FORMULA: max(mw_width // 16, option_picker_width // 8)
            size_option_1 = main_window_width // 16
            size_option_2 = self._option_picker_width // 8
            size = max(size_option_1, size_option_2)

            # Apply border width calculation like legacy
            border_width = max(1, int(size * 0.015))
            spacing = 3  # Grid spacing
            size = size - (2 * border_width) - spacing

            # Ensure minimum size
            size = max(size, 80)
            
            return size

        except Exception:
            # Safe fallback
            return 100

    def _apply_legacy_view_scaling(self, target_size: int):
        """Apply legacy-style view scaling."""
        if not self._scene:
            return
            
        # Get scene dimensions
        scene_rect = self._scene.sceneRect()
        if scene_rect.isEmpty():
            return
            
        # Calculate scale factor like legacy system
        # view_scale = size / pictograph.width()
        view_scale = target_size / scene_rect.width()
        
        # Apply the scaling
        self.resetTransform()
        self.scale(view_scale, view_scale)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize with option picker specific logic."""
        super().resizeEvent(event)
        # Recalculate size when parent changes
        self._recalculate_size()

    def _recalculate_size(self):
        """Recalculate and apply size based on current conditions."""
        if self.isVisible():
            self._apply_view_specific_scaling()

    # === COMPATIBILITY METHODS ===

    def resize_option_view(self):
        """Legacy compatibility method."""
        self._recalculate_size()

    def update_border_widths(self):
        """Legacy compatibility method."""
        # Border styling is handled in CSS
        pass
